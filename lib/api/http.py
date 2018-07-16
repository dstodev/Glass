import sys

import urllib3


class HTTPInterface:
    """Provides an interface to the internet."""

    def __init__(self, proxy: str = None):
        if proxy:
            self.http = urllib3.ProxyManager(proxy)
        else:
            self.http = urllib3.PoolManager()

    def __enter__(self):
        pass

    def __exit__(self, e_type, e_value, traceback):
        print("Exception '{}' thrown with value '{}'!\n"
              "Traceback: {}".format(e_type, e_value, traceback), file=sys.stderr)
