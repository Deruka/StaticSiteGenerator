import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("A new moon is rising", TextType.ITALIC)
        node2 = TextNode("A new moon is rising", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = TextNode("I need a hero, Song by Skillet", TextType.TEXT, "https://de.wikipedia.org/wiki/Skillet")
        node2 = TextNode("I need a hero, Song by Skillet", TextType.TEXT, "https://de.wikipedia.org/wiki/Skillet")
        self.assertEqual(node, node2)

    def test_eq4(self):
        node = TextNode("This has a bold text", TextType.BOLD, None)
        node2 = TextNode("This has a bold text", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_TN_to_HTMLN_Leaf_Text(self):
        node = TextNode("This was a text node",TextType.TEXT)
        expected = LeafNode(None, "This was a text node", None)
        result = text_node_to_html_node(node)
        self.assertEqual(result, expected)

    def test_TN_to_HTMLN_Leaf_Bold(self):
        node = TextNode("This is a bold HTML node",TextType.BOLD)
        expected = LeafNode("b", "This is a bold HTML node", None)
        result = text_node_to_html_node(node)
        self.assertEqual(result, expected)

    def test_TN_to_HTMLN_Leaf_Italic(self):
        node = TextNode("This is a italic Leaf node",TextType.ITALIC)
        expected = LeafNode("i", "This is a italic Leaf node",None)
        result = text_node_to_html_node(node)
        self.assertEqual(result, expected)         
    
    def test_TN_to_HTMLN_Leaf_Code(self):
        node = TextNode("This is a code HTML node",TextType.CODE)
        expected = LeafNode("code", "This is a code HTML node", None)
        result = text_node_to_html_node(node)
        self.assertEqual(result, expected)

    def test_TN_to_HTMLN_Leaf_Link(self):      
        node = TextNode("This node has a link",TextType.LINK, "https://www.5ushiroll.com")
        expected = LeafNode("a", "This node has a link", {'href': 'https://www.5ushiroll.com'})
        result = text_node_to_html_node(node)
        self.assertEqual(result, expected)

    def test_TN_to_HTMLN_Leaf_Image(self):
        node = TextNode("This node is an image",TextType.IMAGE, "https://imgur.com/exploration-stream-D5TdiNt")
        expected = LeafNode("img", "", {'src': 'https://imgur.com/exploration-stream-D5TdiNt', 'alt': 'This node is an image'})
        result = text_node_to_html_node(node)
        self.assertEqual(result, expected)

    def test_TN_to_HTMLN_Leaf_Illegal(self):
        with self.assertRaises(Exception):
            node = TextNode("This node is illegal",TextType.DOUGDOUG)
            text_node_to_html_node(node)

    def test_TN_to_HTMLN_Leaf_Text_is_None(self):
        with self.assertRaises(ValueError):
            node = TextNode(None,TextType.TEXT)
            text_node_to_html_node(node)

    def test_TN_to_HTMLN_Link_without_URL(self):
        with self.assertRaises(ValueError):
            node = TextNode("click me", TextType.LINK)
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()