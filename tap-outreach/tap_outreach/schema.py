import os
import json
from singer import metadata
from tap_outreach.streams import STREAMS

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

def load_schemas():
    schemas = {}

    for filename in os.listdir(get_abs_path('schemas')):
        path = get_abs_path('schemas') + '/' + filename
        file_raw = filename.replace('.json', '')
        with open(path) as file:
            schemas[file_raw] = json.load(file)

    return schemas

def get_schemas():
    schemas = {}
    field_metadata = {}

    for stream_name, stream_metadata in STREAMS.items():
        schema_path = get_abs_path('schemas/{}.json'.format(stream_name))
        with open(schema_path) as file:
            schema = json.load(file)
        schemas[stream_name] = schema
        mdata = metadata.get_standard_metadata(
            schema=schema,
            key_properties=stream_metadata.get('key_properties', None),
            valid_replication_keys=stream_metadata.get('replication_keys', None),
            replication_method=stream_metadata.get('replication_method', None)
        )

        for i in mdata:
            i['metadata'].update({'selected':stream_metadata.get('selection_desire', False)})

        field_metadata[stream_name] = mdata

    return schemas, field_metadata
