import unittest
from textnode import TextNode, TextType
from nodehandle import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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

    def test_extract_markdown_2_img(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])

    def test_extract_markdown_3_img(self):
        text = "This is text with a ![crunchy cat luna](https://pbs.twimg.com/media/GFpyGffWIAAawRM.jpg), a ![husky](https://www.rinti.de/fileadmin/_processed_/8/2/csm_Husky-Haltung_c825940057.jpg) and ![luke skywalker](https://lumiere-a.akamaihd.net/v1/images/luke-skywalker-main_7ffe21c7.jpeg?region=130%2C147%2C1417%2C796)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [('crunchy cat luna', 'https://pbs.twimg.com/media/GFpyGffWIAAawRM.jpg'), ('husky', 'https://www.rinti.de/fileadmin/_processed_/8/2/csm_Husky-Haltung_c825940057.jpg'), ('luke skywalker', 'https://lumiere-a.akamaihd.net/v1/images/luke-skywalker-main_7ffe21c7.jpeg?region=130%2C147%2C1417%2C796')])

    def test_extract_markdown_no_img(self):
        text = "This is text with no images at all"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_2_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')])

    def test_extract_markdown_1_link(self):
        text = "This is text with a link [to the artist 5ushiroll](https://www.5ushiroll.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [('to the artist 5ushiroll', 'https://www.5ushiroll.com')])

    def test_extract_markdown_no_links(self):
        text = "This is text with no links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()