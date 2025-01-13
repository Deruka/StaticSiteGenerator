from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode, LeafNode
import re

# splitting up nodes if one node has one large text with other formatting like **bold** or *italic*
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    # iterate through all nodes
    for node in old_nodes:
        # if node is already TextType.TEXT, add it to the new nodes and go to the next node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        # if node is not a TextType.TEXT, the node has to be split up and the parts of the specific TextType will get converted
        else:
            wip_node = node.text.split(delimiter)
            # if remainder of the node is 0, it means we are missing the delimiter, we need an odd number of entries in the to working nodes.
            if len(wip_node) % 2 == 0:
                raise Exception(f"Missing closing delimiter: {delimiter}")
            # using a boolean inside the delimiter to swap between the intended text_type and TextType.TEXT
            inside_delimiter = False
            # going through all the parts of the node, starting with the TextType.TEXT, then delimiter, rinse and repeat.
            for part in wip_node:
                if inside_delimiter:
                    new_nodes.append(TextNode(part, text_type))
                else:
                    new_nodes.append(TextNode(part,TextType.TEXT))
                # swap boolean
                inside_delimiter = not inside_delimiter        
    return new_nodes

def extract_markdown_images(text):
    # regex for finding image links in a markdown: ![alt text](URL)
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    # regex for finding url links in a markdown: [url text](URL)
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    # similar to split_nodes_delimiter, just focused on images only
    new_nodes = []
    # iterate through all nodes
    for node in old_nodes:
        # get a tuple with the image text and link
        node_img = extract_markdown_images(node.text)
        # if there is no link, just append the current node and go to the next one
        if len(node_img) == 0:
            new_nodes.append(node)
        else: 
            # Put all the text of the current node in a variable to check for matches
            remaining_text = node.text
            while remaining_text:
                # keep working on matches in case there is more than one image in the markdown
                matches = extract_markdown_images(remaining_text)
                # if no match can be found, break the loop
                if not matches:
                    break
                # workable variables for the found matches to filter the text before and after
                image_alt, image_link = matches[0]
                # split up the remaining text to before and after the image
                parts = remaining_text.split(f"![{image_alt}]({image_link})", 1)
                # if the part before the image is not empty, create a TextNode with all the text in it.
                if parts[0] != "":
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                # create the image TextNode
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                # reduce the remaining_text with the already worked through text and check for a next possible match
                remaining_text = parts[1]
            # if remaining text is not empty and no match was found, create the final TextNode
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    # similar to split_nodes_delimiter, just focused on images only
    new_nodes = []
    # iterate through all nodes
    for node in old_nodes:
        # get a tuple with the url text and link
        node_lnk = extract_markdown_links(node.text)
        # if there is no link, just append the current node and go to the next one
        if len(node_lnk) == 0:
            new_nodes.append(node)
        else:
             # Put all the text of the current node in a variable to check for matches
            remaining_text = node.text
            while remaining_text:
                # keep working on matches in case there is more than one link in the markdown
                matches = extract_markdown_links(remaining_text)
                # if no match can be found, break the loop
                if not matches:
                    break
                # workable variables for the found matches to filter the text before and after
                link_txt, link_url = matches[0]
                # split up the remaining text to before and after the link
                parts = remaining_text.split(f"[{link_txt}]({link_url})", 1)
                 # if the part before the link is not empty, create a TextNode with all the text in it.
                if parts[0] != "":
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))
                # create the link TextNode
                new_nodes.append(TextNode(link_txt, TextType.LINK, link_url))
                # reduce the remaining_text with the already worked through text and check for a next possible match
                remaining_text = parts[1]
            # if remaining text is not empty and no match was found, create the final TextNode
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    # create a textnode with all the input text (further down I could've kept using the same variable and just 
    # alter the variable every time, but I wanted different names for clear readabilty)
    nodes = [TextNode(text, TextType.TEXT)]
    # check the new node for images
    nodes_after_images = split_nodes_image(nodes)
    # check the new node for links
    nodes_after_links = split_nodes_link(nodes_after_images)
    # check the new node for code blocks
    nodes_after_code = split_nodes_delimiter(nodes_after_links, "`", TextType.CODE)
    # check the new node for bold text
    nodes_after_bold = split_nodes_delimiter(nodes_after_code, "**", TextType.BOLD)
    # check the new node for italic text
    final_nodes = split_nodes_delimiter(nodes_after_bold, "*", TextType.ITALIC)
    # return the final node list with all nodes from the original input markdown
    return final_nodes

def markdown_to_blocks(markdown):
    md_blocks = []
    # remove all whitespaces in the markdown and make a clear split for new line parameters 
    # with this regex to create all markdown parts into blocks
    wip_md = re.sub(r'\n\s*\n', '\n\n', markdown)
    # split the blocks to iterate through them after
    wip_blocks = wip_md.split("\n\n")
    for block in wip_blocks:
        # split each block in lines
        lines = block.split("\n")
        # strip the block of any whitespaces
        cleaned_lines = [line.strip() for line in lines]
        # rejoin all the lines 
        cleaned_block = '\n'.join(cleaned_lines)
        # if a cleaned block exist, add it to the final list and return it after iterating through it all
        if cleaned_block:
            md_blocks.append(cleaned_block)
    return md_blocks

def block_to_block_type(markdown):
    # this function checks all block types and returns the type of markdown block
    # regex looks for "#" at the beginning of the line, from 1 to 6 times for headings
    if re.match(r'^#{1,6} ', markdown):
        return "heading"
    # regex looks for the code block "```" at the start and end of a string
    elif re.match(r'^```[\s\S]*```$', markdown, re.DOTALL):
        return "code"
    # regex looks for lines that start with "> " in all lines for quotes
    elif all(line.startswith('> ') for line in markdown.splitlines()):
        return "quote"
    # regex looks for either "*" or "-" in all lines to match for an unordered list
    elif all(re.match(r'^[*-] ', line) for line in markdown.splitlines()):
        return "unordered_list"
    # regex looks for numbered listing in all lines to match for an ordered list
    # also checks if the numbers itself are ordered. In case it does not match, it returns as a paragraph
    elif all(re.match(r'^\d+\. ', line) for line in markdown.splitlines()):
        lines = markdown.splitlines()
        numbers = [int(re.match(r'^(\d+)\. ', line).group(1)) for line in lines]
        if all(numbers[i] == i + 1 for i in range(len(numbers))):
            return "ordered_list"
        else:
            return "paragraph"
    # if neither of the options fit, it returns as a paragraph
    else:
        return "paragraph"
    
def markdown_to_html_node(markdown):
    mdblocks = markdown_to_blocks(markdown) # turn the markdown into separate blocks
    parent_nodes = [] # keep track of all created parent nodes
    for block in mdblocks:
        match block_to_block_type(block):
            case "heading":
                    heading_level = len(re.match(r"^#+", block).group()) # Determine heading level
                    headtag = f"h{heading_level}" # Create tag (e.g., h1, h2, etc.)
                    heading_text = block[heading_level + 1:].strip() # Extract heading text
                    child_nodes = text_to_children(heading_text) # Create child nodes from text
                    hp_node = ParentNode(tag=headtag, children=child_nodes)  # Create <hX> node
                    parent_nodes.append(hp_node) # Add to parent node list

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

def extract_title(markdown):
    # Split markdown into individual lines if necessary
    heading_lines = markdown.splitlines()
    for line in heading_lines:
        if re.match(r'^#\s+.+', line):
            return line.strip("#").strip()
    raise Exception("No h1 header in markdown available")
