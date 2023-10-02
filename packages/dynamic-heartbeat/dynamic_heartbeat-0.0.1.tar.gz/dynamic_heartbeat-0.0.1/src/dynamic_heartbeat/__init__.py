# Example package with a console entry point
from . import time
from . import heartbeat

__all__ = ['time', 'heartbeat']


def main():
    print("Hello World")
