import os, shutil
from nodehandle import markdown_to_html_node, extract_title

def main():
    source = 'static'
    destination = 'public'
    copy_directory(source, destination)
    # Generate the page
    generate_page(
        "content/index.md",  # from_path
        "template.html",     # template_path
        "public/index.html"  # dest_path
    )

def copy_directory(source, destination):
    # Delete destination if it exists
    if os.path.exists(destination):
        shutil.rmtree(destination)

    # Make sure destination exists
    if not os.path.exists(destination):
        os.mkdir(destination)
    
    # Get list of everything in source directory
    for item in os.listdir(source):
        # Create full paths
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"file {item} copied from {source} to {destination}")
        else:
            print(f"opening directory {source_path}")
            copy_directory(source_path, dest_path)       

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        markdown = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    get_html = markdown_to_html_node(markdown)
    new_html = get_html.to_html()
    html_title = extract_title(markdown)
    template = template.replace("{{ Title }}",html_title)
    template = template.replace("{{ Content }}", new_html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(template)

main()