import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_ParentNode_to_html_multiple_children(self):
        pnode = ParentNode("p",[LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text"),])
        self.assertEqual(pnode.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_ParentNode_to_html_no_children(self):
        with self.assertRaises(ValueError):
            pnode = ParentNode("p", None)
            pnode.to_html()

    def test_ParentNode_to_html_two_parents(self):
        inner_pnode = ParentNode("p",[LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text"),])
        pnode = ParentNode("div",[inner_pnode])
        self.assertEqual(pnode.to_html(), "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>")

    def test_ParentNode_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            pnode = ParentNode(None, [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text"),])
            pnode.to_html()       

    def test_ParentNode_to_html_one_child_w_prop(self):
        pnode = ParentNode("p", [LeafNode("a", "Click the Link!", {"href": "https://www.5ushiroll.com"})])
        self.assertEqual(pnode.to_html(), '<p><a href="https://www.5ushiroll.com">Click the Link!</a></p>')

    def test_ParentNode_to_html_with_props(self):
        pnode = ParentNode("div",[LeafNode("span", "Some text")],{"class": "container", "id": "main"})
        self.assertEqual(pnode.to_html(), '<div class="container" id="main"><span>Some text</span></div>')

    def test_ParentNode_to_html_multiple_parents(self):
        inner_pnode1 = ParentNode("p",[LeafNode("b", "Bold text"), LeafNode(None, "Normal text"),])
        inner_pnode2 = ParentNode("a",[LeafNode("i", "italic text"), LeafNode(None, "Normal text"),])
        inner_pnode3 = ParentNode("div",[LeafNode(None, "Normal text"),])
        pnode = ParentNode("h1",[inner_pnode1, inner_pnode2, inner_pnode3])
        self.assertEqual(pnode.to_html(), "<h1><p><b>Bold text</b>Normal text</p><a><i>italic text</i>Normal text</a><div>Normal text</div></h1>")

if __name__ == "__main__":
    unittest.main()