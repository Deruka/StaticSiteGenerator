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