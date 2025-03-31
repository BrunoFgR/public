import re
import os

from pathlib import Path
from block_markdown import markdown_to_html_node

def generate_page(from_path, template_path, to_path, BASEPATH):
    print(f" * {from_path} {template_path} -> {to_path}")
    from_file = open(from_path, 'r')
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, 'r')
    template_content = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template_content.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)
    template = template.replace('href="/', f'href="{BASEPATH}')
    template = template.replace('src="/', f'src="{BASEPATH}')

    dest_dir_path = os.path.dirname(to_path)
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(to_path, 'w')
    to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, BASEPATH):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, BASEPATH)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, BASEPATH)

def extract_title(markdown):
    title = re.search(r'^#\s+(.+)$', markdown, re.MULTILINE)
    if not title:
        raise ValueError("No title found")
    return title.group(1)
