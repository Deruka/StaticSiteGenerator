import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        node = HTMLNode("h1","This is a test with no props.")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode("a", "This is test with one prop", None, {"href": "https://www.5ushiroll.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.5ushiroll.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode("h1", "This is a test with three props", None, {"map1": "Ancient Forest", "map2": "Wildspire Waste", "map3": "Coral Highlands"})
        self.assertEqual(node.props_to_html(), ' map1="Ancient Forest" map2="Wildspire Waste" map3="Coral Highlands"')

    def test_LeafNode_to_html_no_props(self):
        lnode = LeafNode("p", "This is a normal text.")
        self.assertEqual(lnode.to_html(), "<p>This is a normal text.</p>")

    def test_LeafNode_to_html_no_tag(self):
        lnode = LeafNode("", "Here is no tag to use.")
        self.assertEqual(lnode.to_html(), "Here is no tag to use.")

    def test_LeafNode_to_html_no_value(self):
        with self.assertRaises(ValueError):
            lnode = LeafNode("h1", "")
            lnode.to_html()

    def test_LeafNode_to_html_props(self):
        lnode = LeafNode("a", "Click here!", {"href": "https://www.5ushiroll.com"})
        self.assertEqual(lnode.to_html(), '<a href="https://www.5ushiroll.com">Click here!</a>')

if __name__ == "__main__":
    unittest.main()