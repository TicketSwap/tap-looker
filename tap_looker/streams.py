"""Stream type classes for tap-looker."""

from __future__ import annotations
import json

from typing import TYPE_CHECKING

# JSON Schema typing helpers
from tap_looker.client import LookerStream, LookerSystemActivityStream

if TYPE_CHECKING:
    from singer_sdk.typing import Context, Iterable, Optional, Record


class QueryStream(LookerSystemActivityStream):
    """Queries ran from looker."""

    name = "query"


class HistoryStream(LookerSystemActivityStream):
    """Looker run history."""

    name = "history"


class ModelStream(LookerStream):
    """Models defined in Looker."""

    name = "model"
    primary_keys = ["name"]

    def get_records(self, context: Optional[Context]) -> Iterable[Record]:
        """Return a generator of record-type dictionary objects."""
        for model in self.sdk.all_lookml_models():
            if model.name in self.config.get("filter_models", [model.name]):
                model_dict = self.convert_to_dict(model)
                yield model_dict

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        explores = [
            explore["name"]
            for explore in record.get("explores", [])
            if explore["name"] in self.config.get("filter_explores", [explore["name"]])
        ]
        self.logger.info(record)
        return {
            "model_name": record["name"],
            "explores": explores,
        }


class ExploreStream(LookerStream):
    """Explores defined in Looker."""

    name = "explore"
    primary_keys = ["id"]
    parent_stream_type = ModelStream

    def get_records(self, context: Optional[Context]) -> Iterable[Record]:
        """Return a generator of record-type dictionary objects."""
        for explore_name in context["explores"]:
            explore = self.sdk.lookml_model_explore(
                lookml_model_name=context["model_name"],
                explore_name=explore_name,
            )
            explore_dict = self.convert_to_dict(explore)
            for key in ["sets", "fields", "joins", "supported_measure_types"]:
                explore_dict.pop(key, None)
            yield explore_dict


class FieldStream(LookerStream):
    """Dimensions defined in Looker."""

    name = "field"
    primary_keys = ["explore_and_name"]
    parent_stream_type = ModelStream

    def get_records(self, context: Optional[Context]) -> Iterable[Record]:
        """Return a generator of record-type dictionary objects."""
        for explore_name in context["explores"]:
            explore = self.sdk.lookml_model_explore(
                lookml_model_name=context["model_name"],
                explore_name=explore_name,
            )
            fields = self.convert_to_dict(explore.fields)
            for field_type in fields:
                for item in fields[field_type]:
                    item["explore_and_name"] = f"{explore_name}.{item['name']}"
                    yield item
