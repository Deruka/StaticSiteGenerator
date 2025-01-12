from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode, LeafNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            wip_node = node.text.split(delimiter)
            if len(wip_node) % 2 == 0:
                raise Exception(f"Missing closing delimiter: {delimiter}")
            inside_delimiter = False
            for part in wip_node:
                if inside_delimiter:
                    new_nodes.append(TextNode(part, text_type))
                else:
                    new_nodes.append(TextNode(part,TextType.TEXT))
                inside_delimiter = not inside_delimiter        
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_img = extract_markdown_images(node.text)
        if len(node_img) == 0:
            new_nodes.append(node)
        else:
            remaining_text = node.text
            while remaining_text:
                matches = extract_markdown_images(remaining_text)
                if not matches:
                    break
                image_alt, image_link = matches[0]
                parts = remaining_text.split(f"![{image_alt}]({image_link})", 1)
                if parts[0] != "":
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                remaining_text = parts[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_lnk = extract_markdown_links(node.text)
        if len(node_lnk) == 0:
            new_nodes.append(node)
        else:
            remaining_text = node.text
            while remaining_text:
                matches = extract_markdown_links(remaining_text)
                if not matches:
                    break
                link_txt, link_url = matches[0]
                parts = remaining_text.split(f"[{link_txt}]({link_url})", 1)
                if parts[0] != "":
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(link_txt, TextType.LINK, link_url))
                remaining_text = parts[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes_after_images = split_nodes_image(nodes)
    nodes_after_links = split_nodes_link(nodes_after_images)
    nodes_after_code = split_nodes_delimiter(nodes_after_links, "`", TextType.CODE)
    nodes_after_bold = split_nodes_delimiter(nodes_after_code, "**", TextType.BOLD)
    final_nodes = split_nodes_delimiter(nodes_after_bold, "*", TextType.ITALIC)
    return final_nodes

def markdown_to_blocks(markdown):
    md_blocks = []
    wip_md = re.sub(r'\n\s*\n', '\n\n', markdown)
    wip_blocks = wip_md.split("\n\n")
    for block in wip_blocks:
        lines = block.split("\n")
        cleaned_lines = [line.strip() for line in lines]
        cleaned_block = '\n'.join(cleaned_lines)
        if cleaned_block:
            md_blocks.append(cleaned_block)
    return md_blocks

def block_to_block_type(markdown):
    if re.match(r'^#{1,6} ', markdown):
        return "heading"
    elif re.match(r'^```[\s\S]*```$', markdown, re.DOTALL):
        return "code"
    elif all(line.startswith('> ') for line in markdown.splitlines()):
        return "quote"
    elif all(re.match(r'^[*-] ', line) for line in markdown.splitlines()):
        return "unordered_list"
    elif all(re.match(r'^\d+\. ', line) for line in markdown.splitlines()):
        lines = markdown.splitlines()
        numbers = [int(re.match(r'^(\d+)\. ', line).group(1)) for line in lines]
        if all(numbers[i] == i + 1 for i in range(len(numbers))):
            return "ordered_list"
        else:
            return "paragraph"
    else:
        return "paragraph"
    
def markdown_to_html_node(markdown):
    mdblocks = markdown_to_blocks(markdown) # turn the markdown into separate blocks
    parent_nodes = [] # keep track of all created parent nodes
    for block in mdblocks:
        match block_to_block_type(block):

            case "heading":
                # Split block into individual lines if necessary
                heading_lines = block.splitlines()

                for line in heading_lines:
                    if line.startswith("#"): # process header lines as intended
                        heading_level = len(re.match(r"^#+", line).group())  # Determine heading level
                        headtag = f"h{heading_level}"  # Create tag (e.g., h1, h2, etc.)
                        heading_text = line[heading_level + 1:]  # Extract heading text
                        child_nodes = text_to_children(heading_text)  # Create child nodes from text
                        hp_node = ParentNode(tag=headtag, children=child_nodes)  # Create <hX> node
                        parent_nodes.append(hp_node)  # Add to parent node list
                    else: # process non-headers as paragraphs
                        child_nodes = text_to_children(line)  # Create child nodes from text
                        hpp_node = ParentNode(tag="p", children=child_nodes)  # Create <p> node
                        parent_nodes.append(hpp_node)  # Add to parent node list

            case "code":
                # Extract the content between the code indicators
                code_text = block.strip("```").strip("\n")
                # Create a LeafNode with the raw content and wrap it in <pre><code>
                child_cp_node = LeafNode(tag="code", value=code_text)
                cp_node = ParentNode(tag="pre", children=[child_cp_node])
                # Append the structured node for code block
                parent_nodes.append(cp_node)

            case "quote":
                quote_text = block[2:]  # Extract text after the "> " prefix
                child_nodes = text_to_children(quote_text)  # Create child nodes
                qp_node = ParentNode(tag="blockquote", children=child_nodes)  # Wrap in <blockquote>
                parent_nodes.append(qp_node)  # Add finished node to parent node list

            case "ordered_list":
                list_items = block.splitlines()  # Split the block into list items
                child_nodes = []  # Collect all <li> items
                
                # Process each list item
                for item in list_items:
                    item_text = item[item.index('.') + 2:]  # Skip item number and space
                    child_nodes.append(ParentNode(tag="li", children=text_to_children(item_text)))  # Wrap in <li>

                olp_node = ParentNode(tag="ol", children=child_nodes)  # Wrap all items in <ol>
                parent_nodes.append(olp_node)  # Add finished node to parent node list

            case "unordered_list":
                list_items = block.splitlines()  # Split the block into list items
                child_nodes = []  # Collect all <li> items

                # Process each list item
                for item in list_items:
                    item_text = item[2:]  # Skip "- " or "* " prefix
                    child_nodes.append(ParentNode(tag="li", children=text_to_children(item_text)))  # Wrap in <li>

                ulp_node = ParentNode(tag="ul", children=child_nodes)  # Wrap all items in <ul>
                parent_nodes.append(ulp_node)  # Add finished node to parent node list

            case "paragraph":
                child_nodes = text_to_children(block)  # Create children from the paragraph text
                pp_node = ParentNode(tag="p", children=child_nodes)  # Wrap in <p>
                parent_nodes.append(pp_node)  # Add finished paragraph node to parent node list

    # Wrap all created parent nodes into a single <div> parent node
    root_node = ParentNode(tag="div", children=parent_nodes)
    return root_node

def text_to_children(text):
    # Convert the text into TextNodes
    text_nodes = text_to_textnodes(text)
    # Convert TextNodes into HTMLNodes
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes