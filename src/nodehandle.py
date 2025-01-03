from textnode import TextNode, TextType

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