#!/usr/bin/env python
# import asyncio
import sys
import time
from os import system

from .modules.service.argparser import ArgParser
from .modules.service.auth import Authenticate
from .modules.service.bitbucket import BitBucket

args = ArgParser.parse(args=sys.argv[1:])

if args.pipeline:
    auth = Authenticate()
    bb = BitBucket(auth=auth)
    bb.get_repos()
    if args.pipeline in bb.repositories:
        print(f'Pipeline {args.pipeline} found')
        while True:
            system('cls' if sys.platform == 'win32' else 'clear')
            bb.check(repo=args.pipeline)
            time.sleep(10)
    else:
        print(f'Pipeline {args.pipeline} not found')

elif args.username and args.password:
    auth = Authenticate(username=args.username, password=args.password)
    exit(0)
