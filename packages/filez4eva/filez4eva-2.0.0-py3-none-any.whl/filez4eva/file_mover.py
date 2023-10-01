from pathlib import Path
import re
import sys
from dataclasses import dataclass
from subprocess import run

from wizlib.rlinput import rlinput

PATTERN = re.compile(r'\d{8}\-([a-zA-Z0-9-]+)\.(\w+)')


class FileMover:

    def __init__(self, target_root):
        if isinstance(target_root, str):
            self.target_root_path = Path(target_root).expanduser()
        elif isinstance(target_root, Path):
            self.target_root_path = target_root.expanduser()
        else:
            raise RuntimeError(f"Invalid target root {target_root}")

    def get_parts(self, sub: str) -> set:
        """Return a set of past filename parts"""
        parts = set()
        for year in self.target_root_path.iterdir():
            if year.name.isdigit():
                subdir = year / sub
                if subdir.is_dir():
                    for file in subdir.iterdir():
                        match = re.match(PATTERN, file.name)
                        if match:
                            parts.add(match.groups()[0])
        return parts

    def handle_file(self, source_file_path: Path):
        print()
        assert source_file_path.is_file()
        confirm1 = rlinput(f"Open {source_file_path}? ", default="yes")
        if confirm1.startswith('y'):
            run(['open', source_file_path])
        confirm2 = rlinput(f"Move {source_file_path}? ", default="yes")
        if confirm2.startswith('y'):
            self.move_file(source_file_path)

    def move_file(self, source_file_path: Path):
        """Ask the user some questions then move the file"""
        extension = source_file_path.suffix
        date = input("Date: ")
        account = input("Account: ")
        parts = self.get_parts(account)
        part = rlinput("Part: ", options=parts)
        year = date[:4]
        dirpath = self.target_root_path / year / account
        if not dirpath.exists():
            confirm = rlinput(f"Create {dirpath}? ", default="yes")
            if confirm.startswith('y'):
                dirpath.mkdir(parents=True)
        targetpath = dirpath / f"{date}-{part}{extension}"
        if targetpath.exists():
            print(f"File exists at {targetpath}")
        else:
            confirm = rlinput(f"Move file to {targetpath}? ", default="yes")
            if confirm.startswith('y'):
                source_file_path.rename(targetpath)
