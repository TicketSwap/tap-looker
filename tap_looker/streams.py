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

    def get_records(self, context: Optional[Context]) -> Iterable[Record]:
        """Return a generator of record-type dictionary objects."""
        for model in self.sdk.all_lookml_models():
            if model.name in self.config.get("filter_models", [model.name]):
                model_dict = self.convert_to_dict(model)
                yield model_dict

    def generate_child_contexts(
        self,
        record: Record,
        context: Context | None,
    ) -> Iterable[Context | None]:
        """Generate child contexts.

        Args:
            record: Individual record in the stream.
            context: Stream partition or context dictionary.

        Yields:
            A child context for each child stream.
        """
        for explore in record.get("explores", []):
            if explore["name"] in self.config.get("filter_explores", [explore["name"]]):
                yield self.get_child_context(
                    record={
                        "model_name": record["name"],
                        "explore_name": explore["name"],
                    },
                    context=context,
                )

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return record


class ExploreStream(LookerStream):
    """Explores defined in Looker."""

    name = "explore"
    parent_stream_type = ModelStream

    def get_records(self, context: Optional[Context]) -> Iterable[Record]:
        """Return a generator of record-type dictionary objects."""
        explore = self.sdk.lookml_model_explore(
            lookml_model_name=context["model_name"],
            explore_name=context["explore_name"],
        )
        explore_dict = self.convert_to_dict(explore)
        for key in ["sets", "fields", "joins", "supported_measure_types"]:
            explore_dict.pop(key, None)
        return [explore_dict]


class FieldStream(LookerStream):
    """Dimensions defined in Looker."""

    name = "field"
    parent_stream_type = ModelStream

    def get_records(self, context: Optional[Context]) -> Iterable[Record]:
        """Return a generator of record-type dictionary objects."""
        explore = self.sdk.lookml_model_explore(
            lookml_model_name=context["model_name"],
            explore_name=context["explore_name"],
        )
        fields = self.convert_to_dict(explore.fields)
        for field_type in fields:
            yield from fields[field_type]
