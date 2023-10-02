# File worker

# User Guide
- Copy folder, change each file extension and paste folder
```python
import shutil
import fileworker as fw

SOURCE_FOLDER_PATH = "data/test"
TARGET_FOLDER_PATH = "data/test_csv"
FILE_FORMAT = ".csv"

# Class for managing file paths
path_manager = fw.PathManager()

# Get a list of source paths
source_paths = path_manager.get_source_paths(SOURCE_FOLDER_PATH)
print("Source paths:", source_paths)
print("Number of source paths:", len(source_paths))

# Get a list of target paths with the ".csv" extension
target_paths = path_manager.get_target_paths(TARGET_FOLDER_PATH, FILE_FORMAT)
print("Target paths:", target_paths)
print("Number of target paths:", len(target_paths))

# Get a list of missing folder paths
target_missing_folder_paths = path_manager.get_target_folder_paths(skip_existing=True)
print("Target missing folder paths:", target_missing_folder_paths   )

# Create missing folders
path_manager.create_missing_folders()

# Get a list of pairs of source and target files, skipping existing ones
path_pairs = path_manager.get_file_pairs(skip_existing=True)
print("List of source and target file pairs:", path_pairs)

for source_path, target_path in path_pairs:
    print("Copying:", source_path, "->", target_path)
    try:
        shutil.copy(source_path, target_path)
    except shutil.SameFileError:
        print("Source and destination represents the same file.")
    except PermissionError:
        print("Permission denied.")
    except:
        print("Error occurred while copying file.")
```
