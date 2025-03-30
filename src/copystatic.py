import os
import shutil

def copy_file_recursive(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)

    for filename in os.listdir(src_folder):
        src_path = os.path.join(src_folder, filename)
        dest_path = os.path.join(dest_folder, filename)
        print(f" * {src_path} -> {dest_path}")
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dest_path)
        else:
            copy_file_recursive(src_path, dest_path)
