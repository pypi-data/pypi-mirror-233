import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from filez4eva.file_mover import FileMover


class DirectoryScanner:

    def __init__(self, source_dir_path_str: str):
        self.source_dir_path = Path(source_dir_path_str).expanduser()

    def loop_directory(self, mover: FileMover):
        for file_path in self.source_dir_path.iterdir():
            if not file_path.name.startswith('.'):
                mover.handle_file(file_path)


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(event.src_path)
            # move_file(event.src_path, self.target_root)
