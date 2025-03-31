import os
import shutil

from copystatic import copy_file_recursive
from gencontent import generate_page, generate_page_recursive, generate_page_with_template

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_file_recursive(dir_path_static, dir_path_public)
    func = generate_page_with_template(template_path)
    generate_page_recursive(dir_path_content, dir_path_public, func)

main()
