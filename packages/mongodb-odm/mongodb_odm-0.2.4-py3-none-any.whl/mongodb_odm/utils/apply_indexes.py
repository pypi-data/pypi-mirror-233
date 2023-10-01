import logging
from typing import Any, Dict, List, Optional, Tuple, Type

from bson import SON
from pydantic import BaseModel
from pymongo import ASCENDING, TEXT, IndexModel

from ..connection import db
from ..models import INHERITANCE_FIELD_NAME, Document

logger = logging.getLogger(__name__)


class IndexOperation(BaseModel):
    collection_name: str
    create_indexes: List[Any]
    database_name: Optional[str] = None


def index_for_a_collection(operation: IndexOperation) -> Tuple[int, int]:
    """
    First get all indexes for a collection and match with operation.
    Remove full match object.

    If db_index partially match with operation_index then recreate/update it.

    For new_indexes unmatched with db_indexes create new index.
    For db_indexes unmatched with new_indexes drop indexes.
    """
    try:
        collection = db(operation.database_name)[operation.collection_name]
        indexes = operation.create_indexes
    except Exception:
        raise Exception("Invalid index object")

    db_indexes = []
    for index in collection.list_indexes():
        old_index = index.to_dict()  # type: ignore
        # Skip "_id" index since it's create by mongodb system
        if "_id" in old_index["key"]:
            continue
        old_index.pop("v", None)
        db_indexes.append(old_index)

    new_indexes = []
    new_indexes_store = {}

    for index in indexes:
        new_index: Any = index.document
        # Replace SON object with dict
        if type(new_index["key"]) == SON:
            new_index["key"] = new_index["key"].to_dict()
        else:
            continue
        new_indexes.append(new_index)
        # Store index object for future use
        new_indexes_store[new_index["name"]] = index

    update_indexes: List[Tuple[IndexModel, Dict[str, Any]]] = []

    for i in range(len(db_indexes)):
        partial_match = None
        for j in range(len(new_indexes)):
            if type(new_indexes[j]) is not dict:
                continue
            if db_indexes[i] == new_indexes[j]:
                db_indexes[i], new_indexes[j] = None, None
                partial_match = None
                break
            if db_indexes[i].get("name") == new_indexes[j].get("name"):
                db_value, new_value = db_indexes[i], new_indexes[j]
                if (
                    TEXT in db_value["key"].values()
                    and TEXT in new_value["key"].values()
                ):
                    """
                    based on condition this is a text-based index.
                    Check that if value is changed.
                    If not changed then assign null otherwise not.
                    NOTE:
                    The data check may not be sufficient enough.
                    Add conditions based on the issue.
                    """

                    new_keys = new_value["key"].keys()
                    default_language = new_value.get("default_language", "english")
                    new_weight = new_value.get("weights") or {
                        key: 1 for key in new_keys
                    }

                    if (
                        db_value["weights"].keys() == new_keys
                        and new_weight == db_value["weights"]
                        and db_value["default_language"] == default_language
                    ):
                        """All key match with existing values"""
                        db_indexes[i], new_indexes[j] = None, None
                        partial_match = None

            """
            # TODO: make a list for partial match
            if partial match db_indexes[i] with new_indexes[i]:
                partial_match = j
                # not break here check if any other match exist
            """

        if partial_match is not None:
            update_indexes.append((db_indexes[i], new_indexes[partial_match]))
            db_indexes[i], new_indexes[partial_match] = None, None

    delete_db_indexes = [val for val in db_indexes if val]
    new_indexes = [val for val in new_indexes if val]

    for db_index in delete_db_indexes:
        if db_index is not None:
            collection.drop_index(db_index["name"])
    if len(new_indexes) > 0:
        new_indexes = [
            new_indexes_store[new_index["name"]]
            for new_index in new_indexes
            if new_index
        ]
        try:
            collection.create_indexes(new_indexes)
        except Exception as e:
            logger.error(f'\nProblem arise at "{operation.collection_name}": {e}\n')
            raise e

    ne, de = len(new_indexes), len(delete_db_indexes)
    if ne > 0 or de > 0:
        logger.info(
            f'Applied for "{operation.collection_name}": {de} deleted, {ne} added'
        )
    return ne, de


def get_model_indexes(model: Type[Document]) -> List[IndexModel]:
    if hasattr(model.Config, "indexes"):
        return list(model.Config.indexes)
    return []


def get_all_indexes() -> List[IndexOperation]:
    """
    First imports all child models of Document since it's the abstract parent model.
    Then retrieve all the child modules and will try to get indexes inside the Config class.
    """
    operations: List[IndexOperation] = []
    for model in Document.__subclasses__():
        indexes = get_model_indexes(model)
        if indexes:
            obj = IndexOperation(
                collection_name=model._get_collection_name(),
                create_indexes=indexes,
                database_name=model._database_name(),
            )
            if (
                hasattr(model.Config, "allow_inheritance")
                and model.Config.allow_inheritance is True
            ):
                """If a model has child model"""
                if model.Config.index_inheritance_field is True:
                    """
                    No _cls indexes will apply if index_inheritance_field = False
                    """
                    obj.create_indexes.append(
                        IndexModel([(INHERITANCE_FIELD_NAME, ASCENDING)])
                    )
                for child_model in model.__subclasses__():
                    """Get all indexes that are defined in child model"""
                    obj.create_indexes += get_model_indexes(child_model)
            operations.append(obj)
    return operations


def apply_indexes() -> None:
    """Run "python -m app.main apply-indexes" to apply and indexes."""

    """First get all indexes from all model."""
    operations = get_all_indexes()

    """Then execute each indexes operation for each model."""
    new_index, delete_index = 0, 0
    for operation in operations:
        ne, de = index_for_a_collection(operation)
        new_index += ne
        delete_index += de

    if delete_index:
        logger.info(f"{delete_index}, index deleted.")
    if new_index:
        logger.info(f"{new_index}, index created.")
    if [new_index, delete_index] == [0, 0]:
        logger.info("No change detected.")
