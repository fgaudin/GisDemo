#!/usr/bin/env python3

import requests
import time
import sys


def download(url, loops=2, wait=1):
    """
    Download a file from a URL and save it to a file.
    If the URL is not accessible, retry for a number of times.
    If the download fails, return False.

    :param url: the URL to download the file from
    :param loops: the number of times to retry the download
    :param wait: the number of seconds to wait between retries
    :return: True if the download was successful, False otherwise
    """

    for i in range(loops):
        actual_url = url.format(i=i+1)
        print("Downloading data from ", actual_url)
        response = requests.get(actual_url)
        response.raise_for_status()
        with open("data/data{}.json".format(i+1), "wb") as file:
            file.write(response.content)

        time.sleep(wait)

if __name__ == "__main__":
    params = [sys.argv[1]]

    if len(sys.argv) > 2:
        loops = int(sys.argv[2])
        params.append(loops)
    if len(sys.argv) > 3:
        wait = int(sys.argv[3])
        params.append(wait)

    download(*params)