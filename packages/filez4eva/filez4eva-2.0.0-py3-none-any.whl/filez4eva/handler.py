import sys
import os
from pathlib import Path

from filewiz.file_mover import FileMover
from filewiz.directory_scanner import DirectoryScanner

DEFAULT_ROOT_DIR = "~/Dropbox/accounts/"
DEFAULT_SOURCE_DIR = "~/Desktop/"


def main():
    source_dir_str = sys.argv[1]
    if 'FILEWIZ_TARGET_ROOT' in os.environ:
        root_dir = os.environ['FILEWIZ_TARGET_ROOT']
    else:
        root_dir = DEFAULT_ROOT_DIR
    scanner = DirectoryScanner(source_dir_str)
    mover = FileMover(root_dir)
    scanner.loop_directory(mover)
