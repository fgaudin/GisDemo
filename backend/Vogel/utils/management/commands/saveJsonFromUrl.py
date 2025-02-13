#!/usr/bin/env python3

import requests
import time
import sys
import environ
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Downloads observations"

    def download(self, loops=2, wait=1):
        env = environ.Env()
        url = env.str("OBSERVATION_API")

        for i in range(loops):
            actual_url = url.format(i=i + 1)
            print("Downloading data from ", actual_url)
            response = requests.get(actual_url)
            response.raise_for_status()
            with open("data/data{}.json".format(i + 1), "wb") as file:
                file.write(response.content)

            time.sleep(wait)

    def add_arguments(self, parser):
        parser.add_argument("loops", nargs="?", type=int, default=2)
        parser.add_argument("wait", nargs="?", type=int, default=1)

    def handle(self, *args, **options):
        self.download(options["loops"], options["wait"])
