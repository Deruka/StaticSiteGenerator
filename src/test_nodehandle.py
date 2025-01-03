import unittest
from textnode import TextNode, TextType
from nodehandle import split_nodes_delimiter

class TestNodehandle(unittest.TestCase):
    def test_singlenode_one_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" word", TextType.TEXT),])

    def test_singlenode_twotime_delimiter(self):
        node = TextNode("This text has **not one** but **two bold** word blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**",TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This text has ", TextType.TEXT),
                                     TextNode("not one", TextType.BOLD),
                                     TextNode(" but ", TextType.TEXT),
                                     TextNode("two bold", TextType.BOLD),
                                     TextNode(" word blocks", TextType.TEXT),])

    def test_multinodes_two_dif_delimiter(self):
        node1 = TextNode("This text has a `code block` in between", TextType.TEXT)
        node2 = TextNode("This text has a **bold block** in between", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1], "`", TextType.CODE)
        new_nodes += split_nodes_delimiter([node2], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This text has a ", TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" in between", TextType.TEXT),
                                     TextNode("This text has a ", TextType.TEXT),
                                     TextNode("bold block", TextType.BOLD),
                                     TextNode(" in between", TextType.TEXT),])

    def test_singlenode_two_dif_delimiter(self):
        node = TextNode("This text has a **bold** and a *italic* word block",TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes,"*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This text has a ", TextType.TEXT),
                                     TextNode("bold", TextType.BOLD),
                                     TextNode(" and a ", TextType.TEXT),
                                     TextNode("italic", TextType.ITALIC),
                                     TextNode(" word block", TextType.TEXT),])

    def test_singlenode_missing_delimiter(self):
        with self.assertRaises(Exception):
            node = TextNode("This is text with a `code block word", TextType.TEXT)
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_singlenode_empty_text_in_delimiter(self):
        node = TextNode("This delimiter `` is empty", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This delimiter ", TextType.TEXT),
                                     TextNode("", TextType.CODE),
                                     TextNode(" is empty", TextType.TEXT),])              

if __name__ == "__main__":
    unittest.main()