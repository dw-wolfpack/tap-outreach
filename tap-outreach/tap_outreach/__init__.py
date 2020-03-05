#!/usr/bin/env python3
import os
import json
import sys
import singer
from singer import utils, metadata, Transformer
from tap_outreach.discover import discover
from tap_outreach.sync_streams import sync_streams

REQUIRED_CONFIG_KEYS = ["start_date", "refresh_token", "client_id", "client_secret"]
LOGGER = singer.get_logger()

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

def discover_catalog():
    LOGGER.info('Doing Discover Command')
    catalog = discover()
    return json.dump(catalog.to_dict(), sys.stdout, indent=2)

def get_selected_streams(catalog):
    '''
    Gets selected streams.  Checks schema's 'selected' first (legacy)
    and then checks metadata (current), looking for an empty breadcrumb
    and mdata with a 'selected' entry
    '''
    selected_streams = []
    for stream in catalog.streams:
        stream_metadata = metadata.to_map(stream.metadata)
        # stream metadata will have an empty breadcrumb
        if metadata.get(stream_metadata, (), "selected"):
            selected_streams.append(stream.tap_stream_id)

    return selected_streams

@utils.handle_top_exception(LOGGER)
def main():

    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)
    config = args.config

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover_catalog()

    # # Otherwise run in sync mode
    else:
        if args.catalog:
            LOGGER.info('hello there kenobi')
            catalog = args.catalog
        else:
            catalog = discover()

        # sync_streams(args.config, args.state, catalog)
        sync_streams(catalog, config)

if __name__ == "__main__":
    main()
