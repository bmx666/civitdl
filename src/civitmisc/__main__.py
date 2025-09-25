#!/usr/bin/env python3

import traceback

from helpers.core.utils import Styler, disable_style, UnexpectedException, NotImplementedException, InputException, set_verbose, run_verbose, print_verbose, print_exc, sprint
from helpers.core.iohelper import IOHelper
from helpers.cache import CacheHelper
from civitmisc.args.argparser import get_args

import requests
import json
import urllib.parse
import os

# TODO: Make verbose and no_style similar to each other


def main():
    try:
        args = get_args()
        if args['verbose']:
            set_verbose(True)
        else:
            set_verbose(False)

        if args['with_color'] == False:
            disable_style()

        subcommand = args['subcommand']
        print_verbose(args)

        if subcommand == 'cache':
            if args['scan_model']:
                CacheHelper.scan_models(args['scan_model'])
            else:
                raise InputException('Cache option not provided.')
        elif subcommand == 'image':
            if args['gendata']:
                output_dir = args['output']
                os.makedirs(output_dir, exist_ok=True)

                session = requests.Session()
                for image_id in args['gendata']:
                    try:
                        gendata_params = {"json": {"id": int(image_id), "authed": True}}
                        gendata_url = f'https://civitai.com/api/trpc/image.getGenerationData?input={urllib.parse.quote(json.dumps(gendata_params))}'
                        print_verbose(f'Fetching generation data for image {image_id}')

                        response = session.get(gendata_url)
                        if response.status_code == 200:
                            filepath = os.path.join(output_dir, f'{image_id}_gendata.json')
                            IOHelper.write_to_file(filepath, [response.text], encoding='UTF-8')
                            sprint(Styler.stylize(f'Downloaded generation data for image {image_id}', color='success'))
                        else:
                            sprint(Styler.stylize(f'Failed to fetch generation data for image {image_id}: HTTP {response.status_code}', color='error'))
                    except Exception as e:
                        sprint(Styler.stylize(f'Error fetching generation data for image {image_id}: {e}', color='error'))
            else:
                raise InputException('Image option not provided.')
        else:
            raise UnexpectedException(
                'Unknown subcommand not caught by argparse')

    except Exception as e:
        sprint('---------')
        run_verbose(traceback.print_exc)
        print_exc(e)
        sprint('---------')
