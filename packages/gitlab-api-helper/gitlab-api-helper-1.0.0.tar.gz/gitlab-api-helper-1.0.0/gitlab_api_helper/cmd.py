# -*- encoding: utf-8 -*-
import sys
import json
import argparse
import os.path
from datetime import datetime, timedelta

from gitlab_api_helper import __version__
from gitlab_api_helper import api_helper

def main():
    parser = argparse.ArgumentParser(description='A Simple Tool for Gitlab API Usage')
    parser.add_argument('--apiSetupConfig', type=str, default='.env', help='Read Default Info from config file')
    parser.add_argument('--apiAccessToken', type=str, default=None, help='Using Gitlab API with private_token.')
    parser.add_argument('--api', type=str, default=None, help='Gitlab API URL')
    parser.add_argument('--sinceType', choices=['day', 'week', 'month'], default='day', help="commit date range type")
    parser.add_argument('--sinceNumber', type=int, default='7', help="commit date range value")
    parser.add_argument('--lookup', choices=['project', 'branch', 'commit'], default='project', help="query result")
    parser.add_argument('--lookupProjectID', type=int, default=0, help="Gitlab Project ID")
    parser.add_argument('--lookupBranch', type=str, default=None, help="Branch Name")
    args = parser.parse_args()

    output = {'result': None, 'info': [],  'version': __version__ }

    if os.path.isfile(args.apiSetupConfig):
        output['info'].append(f'use config file: {args.apiSetupConfig}')
        conf = None
        try:
            with open(args.apiSetupConfig, 'r') as f:
                conf = json.load(f)
        except Exception as e:
            output['info'].append(f"load config from file '{args.apiSetupConfig}' error: {e}")

        if not args.api and 'api' in conf:
            if api_helper.urlValidator(conf['api']):
                args.api = conf['api']
            else:
                output['info'].append(f"api from config test failed: '{conf['api']}")

        if not args.apiAccessToken and 'accessToken' in conf:
            args.apiAccessToken = conf['accessToken']   
    else:
        output['info'].append(f'config file not found: {args.apiSetupConfig}')

    if not args.api:
        output['info'].append(f"--api empty")
        print(api_helper.jsonOutput(output))
        parser.print_help()
        sys.exit()

    if args.lookup == 'project':
        output['result'] = api_helper.getProjects(args.api, args.apiAccessToken)
    elif args.lookup == 'branch':
        if args.lookupProjectID < 1:
            output['error'] = 'no project id'
        else:
            output['result'] = api_helper.getBranches(args.api, args.apiAccessToken, args.lookupProjectID)
    elif args.lookup == 'commit':
        if args.lookupBranch is None:
            output['error'] = 'no branch name'
        else:
            sinceISO8601FormatDateValue = datetime.now() + timedelta(days = -7)
            if args.sinceType == 'day':
                sinceISO8601FormatDateValue = (datetime.now() + timedelta(days = -1 * args.sinceNumber ))
            elif args.sinceType == 'week':
                sinceISO8601FormatDateValue = (datetime.now() + timedelta(weeks = -1 * args.sinceNumber ))
            elif args.sinceType == 'month':
                sinceISO8601FormatDateValue = (datetime.now() + timedelta(days = -1 * args.sinceNumber * 30 ))
            sinceISO8601FormatDateValue = sinceISO8601FormatDateValue.isoformat(sep='T',timespec='auto')
            output['info'].append(f'sinceISO8601FormatDateValue: {sinceISO8601FormatDateValue}')

            output['result'] = api_helper.getCommits(args.api, args.apiAccessToken, args.lookupProjectID, args.lookupBranch, sinceISO8601FormatDateValue)

    print(api_helper.jsonOutput(output))
    
if __name__ == '__main__':
    main()
