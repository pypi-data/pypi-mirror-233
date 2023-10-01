import sys
import os
from pathlib import Path

from filez4eva.file_mover import FileMover
from filez4eva.directory_scanner import DirectoryScanner

DEFAULT_ROOT_DIR = "~/Dropbox/accounts/"
DEFAULT_SOURCE_DIR = "~/Desktop/"


def main():
    source_dir_str = sys.argv[1]
    if 'FILEZ4EVA_TARGET_ROOT' in os.environ:
        root_dir = os.environ['FILEZ4EVA_TARGET_ROOT']
    else:
        root_dir = DEFAULT_ROOT_DIR
    scanner = DirectoryScanner(source_dir_str)
    mover = FileMover(root_dir)
    scanner.loop_directory(mover)
