import singer
from singer import (transform, Transformer, metadata, utils)
from tap_outreach.streams import STREAMS
from tap_outreach.client import OutReachClient


LOGGER = singer.get_logger()

def transform_json(data, stream):
    this_json = data
    new_json = this_json
    index = 0
    data_key = "data"
    denest_keys = "attributes"

    for record in list(this_json.get(data_key, [])):
        #     print(record)
        for denest_key in denest_keys.split(","):
            #         print(record)
            for key, val in record.get(denest_keys).items():
                new_json[data_key][index][key] = val
        new_json[data_key][index].pop(denest_key)
        index += 1

    record = transform(new_json, stream.stream)
    return record

def build_path(path, filter_field, external_connection):
    path = path
    end = '&page[limit]=1000'

    if external_connection and filter_field:
        path = path + '?provideDataConnections=true' + '&filter[{}]='.format(filter_field)+'{}..{}'
    elif external_connection:
        path = path + '?provideDataConnections=true'
    elif filter_field:
        path = path + '?filter[{}]='.format(filter_field)+'{}..{}'


    path = path + end
    return path


def sync_endpoint(path, stream_name, stream, key, config):
    rf_tk = config['refresh_token']
    cl_id = config['client_id']
    cl_sc = config['client_secret']
    config = config

    outreach_client = OutReachClient(rf_tk, cl_id, cl_sc)

    data, limit = OutReachClient.request_loop_prospect(outreach_client, path, config)

    records = transform_json(data, stream)

    schema = stream.schema.to_dict()
    stream_metadata = metadata.to_map(stream.metadata)
    # print(schema)
    # print(records)
    singer.write_schema(stream_name, schema, stream.key_properties)
    replication_key = key
    max_key = ''
    num = 0
    value = dict()
    for i in records.get('data'):
        num += 1
        transformed_record = Transformer().transform(i, schema, stream_metadata)
        if replication_key:
            replication_keys = transformed_record[replication_key]
            if max_key < replication_keys:
                max_key = replication_keys
        singer.write_record(stream_name, transformed_record, time_extracted=utils.now())
    LOGGER.info('Total records processed: %s \n for stream: %s', num, stream_name)
    value["stream_"+stream_name] = num
    value['API_LIMIT_REMAINING'] = limit
    if max_key:
        value['replication_key_max'] = max_key
    singer.write_state(value)


    LOGGER.info('--------------------------------')

def sync_streams(catalog, config):
    LOGGER.info('last/currently syncing stream:')
    selected_streams = []
    selected_schemas = dict()
    config = config

    for stream in catalog.get_selected_streams({}):
        selected_streams.append(stream.stream)
        selected_schemas[stream.stream] = stream
        # print(stream, 'hi hi hi hi')
    LOGGER.info('selected_streams: %s', selected_streams)

    if not selected_streams:
        return

    for stream_name in selected_streams:
        LOGGER.info('START syncing %s', stream_name)
        endpoint_config = STREAMS[stream_name]
        incremental_choice = endpoint_config.get('replication_method', stream_name)
        path = endpoint_config.get('path', stream_name)
        replication_keys = endpoint_config.get('replication_keys', stream_name)
        external_connection = endpoint_config.get('include_connections', stream_name)

        if incremental_choice == 'INCREMENTAL' and external_connection:
            path = build_path(path, replication_keys, external_connection)
        elif external_connection:
            path = build_path(path, False, external_connection)
        elif incremental_choice == 'INCREMENTAL':
            path = build_path(path, replication_keys, False)
        else:
            end = '?page[limit]=1000'
            path = path + end
        # print(path)
        sync_endpoint(path, stream_name, selected_schemas[stream_name], replication_keys, config)
