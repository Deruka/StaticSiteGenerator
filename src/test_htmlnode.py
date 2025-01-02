import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()