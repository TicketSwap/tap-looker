import json

from singer_sdk.typing import (
    IntegerType,
    PropertiesList,
    Property,
    StringType,
    ArrayType,
    ObjectType,
    DateTimeType,
    DateType,
    BooleanType,
    TimeType,
    NumberType,
)

query_schema = PropertiesList(
    Property("query.id", IntegerType),
    Property("query.created_time", DateTimeType),
    Property("query.view", StringType),
    Property("query.count_of_dynamic_fields", IntegerType),
    Property("query.dynamic_fields", StringType),
    Property("query.pivots", StringType),
    Property("query.hash", StringType),
    Property("query.fields", StringType),
    Property("query.filters", StringType),
    Property("query.model", StringType),
    Property("query.link", StringType),
    Property("query.query_timezone", StringType),
    Property("query.slug", StringType),
    Property("query.column_limit", StringType),
    Property("query.row_total", StringType),
    Property("query.sorts", StringType),
    Property("query.total", StringType),
    Property("query.limit", IntegerType),
).to_dict()


history_schema = PropertiesList(
    Property("history.id", IntegerType),
    Property("history.cache", StringType),
    Property("history.cache_key", StringType),
    Property("history.result_source", StringType),
    Property("history.completed_time", DateTimeType),
    Property("history.connection_id", StringType),
    Property("history.connection_name", StringType),
    Property("history.dialect", StringType),
    Property("history.created_time", DateTimeType),
    Property("history.real_dash_id", StringType),
    Property("history.dashboard_session", StringType),
    Property("history.message", StringType),
    Property("history.most_recent_run_at_time", DateTimeType),
    Property("history.most_recent_length", NumberType),
    Property("history.is_single_query", StringType),
    Property("history.is_user_dashboard", StringType),
    Property("history.rebuild_pdts", StringType),
    Property("history.render_key", StringType),
    Property("history.result_format", StringType),
    Property("history.runtime", NumberType),
    Property("history.slug", StringType),
    Property("history.source", StringType),
    Property("history.status", StringType),
    Property("history.query_id", IntegerType),
    Property("history.workspace_id", StringType),
).to_dict()

models_schema = PropertiesList(
    Property(
        "can",
        ObjectType(
            Property("index", BooleanType),
            Property("show", BooleanType),
            Property("update_field_unlimited_db_connections", BooleanType),
            Property("update", BooleanType),
            Property("destroy", BooleanType),
        ),
    ),
    Property("allowed_db_connection_names", ArrayType(StringType)),
    Property(
        "explores",
        ArrayType(
            ObjectType(
                Property("name", StringType),
                Property("label", StringType),
                Property("hidden", BooleanType),
                Property("group_label", StringType),
            ),
        ),
    ),
    Property("has_content", BooleanType),
    Property("label", StringType),
    Property("name", StringType),
    Property("project_name", StringType),
    Property("unlimited_db_connections", BooleanType),
).to_dict()

explore_schema = PropertiesList(
    Property("id", StringType),
    Property("name", StringType),
    Property("label", StringType),
    Property("title", StringType),
    Property("scopes", ArrayType(StringType)),
    Property("can_total", BooleanType),
    Property("can_develop", BooleanType),
    Property("can_see_lookml", BooleanType),
    Property("lookml_link", StringType),
    Property("can_save", BooleanType),
    Property("can_explain", BooleanType),
    Property("can_pivot_in_db", BooleanType),
    Property("can_subtotal", BooleanType),
    Property("has_timezone_support", BooleanType),
    Property("supports_cost_estimate", BooleanType),
    Property("connection_name", StringType),
    Property("null_sort_treatment", StringType),
    Property("files", ArrayType(StringType)),
    Property("source_file", StringType),
    Property("project_name", StringType),
    Property("model_name", StringType),
    Property("view_name", StringType),
    Property("hidden", BooleanType),
    Property("sql_table_name", StringType),
    Property("access_filter_fields", ArrayType(StringType)),
    Property("access_filters", ArrayType(ObjectType())),
    Property(
        "aliases",
        ArrayType(
            ObjectType(
                Property("name", StringType),
                Property("value", StringType),
            ),
        ),
    ),
    Property("always_filter", ArrayType(ObjectType())),
    Property("conditionally_filter", ArrayType(ObjectType())),
    Property("index_fields", ArrayType(StringType)),
    Property("tags", ArrayType(StringType)),
    Property("group_label", StringType),
    Property("always_join", ArrayType(StringType)),
).to_dict()

field_schema = PropertiesList(
    Property("explore_and_name", StringType),
    Property("align", StringType),
    Property("can_filter", BooleanType),
    Property("category", StringType),
    Property("description", StringType),
    Property("field_group_variant", StringType),
    Property("fiscal_month_offset", IntegerType),
    Property("has_allowed_values", BooleanType),
    Property("hidden", BooleanType),
    Property("is_filter", BooleanType),
    Property("is_fiscal", BooleanType),
    Property("is_numeric", BooleanType),
    Property("is_timeframe", BooleanType),
    Property("can_time_filter", BooleanType),
    Property("label", StringType),
    Property("label_short", StringType),
    Property("lookml_link", StringType),
    Property("measure", BooleanType),
    Property("name", StringType),
    Property("strict_value_format", BooleanType),
    Property("parameter", BooleanType),
    Property("primary_key", BooleanType),
    Property("project_name", StringType),
    Property("requires_refresh_on_sort", BooleanType),
    Property("scope", StringType),
    Property("sortable", BooleanType),
    Property("source_file", StringType),
    Property("source_file_path", StringType),
    Property("sql", StringType),
    Property("suggest_dimension", StringType),
    Property("suggest_explore", StringType),
    Property("suggestable", BooleanType),
    Property("tags", ArrayType(StringType)),
    Property("type", StringType),
    Property("user_attribute_filter_types", ArrayType(StringType)),
    Property("view", StringType),
    Property("view_label", StringType),
    Property("dynamic", BooleanType),
    Property("week_start_day", StringType),
    Property("times_used", IntegerType),
    Property("original_view", StringType),
    Property("field_group_label", StringType),
    Property("default_filter_value", StringType),
).to_dict()

schemas = {
    "query": query_schema,
    "history": history_schema,
    "model": models_schema,
    "explore": explore_schema,
    "field": field_schema,
}

for name, schema in schemas.items():
    with open(f"tap_looker/schemas/{name}.json", "w") as f:
        json.dump(schema, f, indent=2)
