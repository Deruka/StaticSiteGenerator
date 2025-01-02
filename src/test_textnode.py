import unittest

from textnode import TextNode, TextType


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

    def test_eq5(self):
        node = TextNode("I am normal", TextType.TEXT)
        node2 = TextNode("I am normal", TextType.TEXT)
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()