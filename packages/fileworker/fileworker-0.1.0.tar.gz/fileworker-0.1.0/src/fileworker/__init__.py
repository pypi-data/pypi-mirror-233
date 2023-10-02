import os
from typing import List


class PathManager:
    def __init__(self) -> None:
        self.list_path_from = []
        self.list_path_folder_from = []


    def get_source_paths(self, path_folder, file_formats: List[str]=None):
        """
        Parameters:
            path (str): Path.
            file_format (List[str]): File formats, ex: [".mp4", ".jpg"] or None or []
        """
        self.path_folder_from = path_folder
        for dirname, _, filenames in os.walk(path_folder):
            self.list_path_folder_from.append(dirname)
            for filename in filenames:
                if file_formats is None or file_formats == []:
                    self.list_path_from.append(os.path.join(dirname, filename))
                else:
                    for format in file_formats:
                        if filename.endswith(format):
                            self.list_path_from.append(os.path.join(dirname, filename))
        return self.list_path_from


    # pytest test_pathworker.py -s -k test_path_to
    def get_target_paths(self, path_folder, file_format=""):
        
        if path_folder[-1] == "/":
            path_folder = path_folder[:-1]
        self.list_path_to = [s.replace(self.path_folder_from, path_folder) + file_format for s in self.list_path_from]
        self.list_path_folder_to = [s.replace(self.path_folder_from, path_folder) for s in self.list_path_folder_from]
        return self.list_path_to


    def get_target_folder_paths(self, skip_existing=True):
        list_path_folder_skip_existing = []
        for path in self.list_path_folder_to:
            if not os.path.isdir(path):
                list_path_folder_skip_existing.append(path)

        if skip_existing:
            return list_path_folder_skip_existing
        else:
            return self.list_path_folder_to


    def create_missing_folders(self):
        for path in self.list_path_folder_to:
            if not os.path.isdir(path):
                os.mkdir(path)
                print(f"folder created: {path}")
            else:
                print(f"folder skipped: {path}")


    def get_file_pairs(self, skip_existing=True):
        list_from_to = []
        for path_f, path_t in zip(self.list_path_from, self.list_path_to):
            if skip_existing:
                if os.path.exists(path_t):
                    continue
            list_from_to.append([path_f, path_t])
        return list_from_to

