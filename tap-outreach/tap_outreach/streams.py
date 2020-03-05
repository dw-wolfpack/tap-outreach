# streams: API URL endpoints to be called
# properties:
#   <root node>: Plural stream name for the endpoint
#   path: API endpoint relative path, when added to the base URL, creates the full path,
#       default = stream_name
#   key_properties: Primary key fields for identifying an endpoint record.
#   replication_method: INCREMENTAL or FULL_TABLE
#   replication_keys: bookmark_field(s), typically a date-time, used for filtering the results
#        and setting the state
#   bookmark_query_field: From date-time field used for filtering the query
#   bookmark_type: Data type for bookmark, integer or datetime

STREAMS = {
    "emailAddresses": {
        #  PII so not being pulled
        "api_method": "GET",
        "selection_desire": False,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "emailAddresses",
        "replication_method": "INCREMENTAL",
        "replication_keys": "updatedAt",
        "include_connections": False
    },
    "stages": {
        "api_method": "GET",
        "selection_desire": True,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "stages",
        "replication_method": "INCREMENTAL",
        "replication_keys": "updatedAt",
        "include_connections": True
    },
    "users": {
        "api_method": "GET",
        "selection_desire": True,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "users",
        "replication_method": "INCREMENTAL",
        "replication_keys": "updatedAt",
        "include_connections": True
    },
    "roles": {
        "api_method": "GET",
        "selection_desire": True,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "roles",
        "replication_method": "FULL",
        "replication_keys": None,
        "include_connections": False
    },
    "teams": {
        "api_method": "GET",
        "selection_desire": True,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "teams",
        "replication_method": "FULL",
        "replication_keys": None,
        "include_connections": False
    },
    "sequences": {
        "api_method": "GET",
        "selection_desire": True,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "sequences",
        "replication_method": "INCREMENTAL",
        "replication_keys": "updatedAt",
        "include_connections": False
    },
    "sequencestates": {
        "api_method": "GET",
        "selection_desire": True,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "sequenceStates",
        "replication_method": "INCREMENTAL",
        "replication_keys": "updatedAt",
        "include_connections": False
    },
    "sequencesteps": {
        "api_method": "GET",
        "selection_desire": True,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "sequenceSteps",
        "replication_method": "INCREMENTAL",
        "replication_keys": "updatedAt",
        "include_connections": False
    },
    "sequencetemplates": {
        # not needed for our data pull
        "api_method": "GET",
        "selection_desire": False,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "sequenceTemplates",
        "replication_method": "FULL",
        "replication_keys": "updatedAt",
        "include_connections": False
    },
    "mailings": {
        "api_method": "GET",
        "selection_desire": True,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "mailings",
        "replication_method": "INCREMENTAL",
        "replication_keys": "updatedAt",
        "include_connections": True
    },
    "mailboxes": {
        "api_method": "GET",
        "selection_desire": True,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "mailboxes",
        "replication_method": "INCREMENTAL",
        "replication_keys": "updatedAt",
        "include_connections": False
    },
    "prospects": {
        "api_method": "GET",
        "selection_desire": True,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "prospects",
        "replication_method": "INCREMENTAL",
        "replication_keys": "updatedAt",
        "include_connections": True
    },
    "profiles": {
        "api_method": "GET",
        "selection_desire": True,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "profiles",
        "replication_method": "FULL",
        "replication_keys": "updatedAt",
        "include_connections": False
    },
    "calls": {
        "api_method": "GET",
        "selection_desire": True,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "calls",
        "replication_method": "INCREMENTAL",
        "replication_keys": "updatedAt",
        "include_connections": True
    },
    "tasks": {
        "api_method": "GET",
        "selection_desire": True,
        "data_key": "data",
        "bookmark_type": "datetime",
        "key_properties": ["id"],
        "path": "tasks",
        "replication_method": "INCREMENTAL",
        "replication_keys": "updatedAt",
        "include_connections": True
    }

}
