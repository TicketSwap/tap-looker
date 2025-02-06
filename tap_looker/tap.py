"""Looker tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk.typing import (
    PropertiesList,
    Property,
    StringType,
    DateTimeType,
    ArrayType,
)  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_looker import streams


class TapLooker(Tap):
    """Looker tap class."""

    name = "tap-looker"

    config_jsonschema = PropertiesList(
        Property(
            "start_date",
            DateTimeType,
            default="2000-01-01T00:00:00Z",
        ),
        Property(
            "base_url",
            StringType,
            required=True,
            title="Base URL",
            description="The base URL for the Looker API service",
        ),
        Property(
            "client_id",
            StringType,
            required=True,
            secret=True,  # Flag config as protected.
            title="Client ID",
            description="The Client ID to authenticate against the API service",
        ),
        Property(
            "client_secret",
            StringType,
            required=True,
            secret=True,  # Flag config as protected.
            title="Client Secret",
            description="The Client Secret to authenticate against the API service",
        ),
        Property("filter_models", ArrayType(StringType)),
        Property("filter_explores", ArrayType(StringType)),
    ).to_dict()

    def discover_streams(self) -> list[streams.LookerStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.QueryStream(self),
            streams.HistoryStream(self),
            streams.ModelStream(self),
            streams.ExploreStream(self),
            streams.FieldStream(self),
        ]


if __name__ == "__main__":
    TapLooker.cli()
