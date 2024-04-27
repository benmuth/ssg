# from textnode import TextNode
import shutil
import os
from block_markdown import markdown_to_html_node
from htmlnode import ParentNode
from pathlib import Path

def main():
    copy_tree("static", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    paths = os.listdir(dir_path_content)
    for path in paths:
        content_path = os.path.join(dir_path_content, path)
        public_path = os.path.join(dest_dir_path, path)
        if os.path.isfile(content_path):
            path_parts = path.split(".")
            if path_parts[1] == "md":
                public_path = os.path.join(dest_dir_path, path_parts[0] + ".html")
                generate_page(content_path,template_path, public_path)
        else:
            generate_pages_recursive(content_path, template_path, public_path)
    print(paths)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown_content = f.read()

    with open(template_path) as f:
        html_template = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html = html_node.toHTML()
    title = extract_title(markdown_content)


    filled_template = html_template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dir = os.path.dirname(dest_path)
    os.makedirs(dir, exist_ok=True)
    with open(dest_path, mode="w") as f:
        f.write(filled_template)
        

def copy_tree(src, dst_dir):
    print()
    print(f"copying {src} to {dst_dir}")

    if os.path.exists(dst_dir):
        print(f"clearing {dst_dir}")
        shutil.rmtree(dst_dir)

    print(f"making {dst_dir}")
    os.mkdir(dst_dir)

    src_contents = os.listdir(src)

    for entry in src_contents:
        entry_path = os.path.join(src, entry)
        if os.path.isfile(entry_path):
            print(f"copying {entry_path} to {dst_dir}")
            shutil.copy(entry_path, dst_dir)
        else:
            copy_tree(entry_path, os.path.join(dst_dir, entry))

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("no title found")

if __name__ == "__main__":
    main()
