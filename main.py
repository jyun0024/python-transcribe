# お題「文字お越しアプリ」

# pip install flet
import flet

import typing
import subprocess
import os
import time

from flet_app import FletApp
# from subject import Subject
from transcribe import Transcribe

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def main(page: flet.Page):
    flet_app = FletApp(page)


if __name__ == "__main__":
    flet.app(main)
