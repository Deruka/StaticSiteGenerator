from textnode import TextNode, TextType
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
    