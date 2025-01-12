import os, shutil
from nodehandle import markdown_to_html_node, extract_title

def main():
    source = 'static'
    destination = 'public'
    copy_directory(source, destination)
    # Generate the page
    generate_pages_recursive(
        "content",           # The top-level content directory
        "template.html",     # The HTML template
        "public"             # The top-level public directory
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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}")

    # Make sure destination exists
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_path) and source_path.endswith(".md"):
            dest_path = dest_path.replace(".md", ".html")
            
            # Read markdown and template
            with open(source_path, 'r') as file:
                markdown = file.read()
            with open(template_path, 'r') as file:
                template = file.read()

            # Transform markdown to HTML
            html_content = markdown_to_html_node(markdown).to_html()
            title = extract_title(markdown)

            # Replace placeholders in template
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", html_content)

            # Ensure destination directories exist
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            # Write out the final HTML
            with open(dest_path, 'w') as file:
                file.write(template)

        elif os.path.isdir(source_path):
            # Ensure destination directory exists and recurse
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(source_path, template_path, dest_path)

main()