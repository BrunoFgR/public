import re
import os

from block_markdown import markdown_to_html_node

def generate_page(from_path, template_path, to_path):
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

    dest_dir_path = os.path.dirname(to_path)
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(to_path, 'w')
    to_file.write(template)

def generate_page_recursive(from_path, dest_path, func):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    for filename in os.listdir(from_path):
        if os.path.isdir(os.path.join(from_path, filename)):
            generate_page_recursive(os.path.join(from_path, filename), os.path.join(dest_path, filename), func)
        else:
            func(os.path.join(from_path, filename), os.path.join(dest_path, filename.replace('.md', '.html')))

def generate_page_with_template(template_path):
    def inner_func(from_path, to_path):
        generate_page(from_path, template_path, to_path)

    return inner_func

def extract_title(markdown):
    title = re.search(r'^#\s+(.+)$', markdown, re.MULTILINE)
    if not title:
        raise ValueError("No title found")
    return title.group(1)
