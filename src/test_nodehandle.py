import unittest
from textnode import TextNode, TextType
from nodehandle import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title

class TestNodehandle(unittest.TestCase):
    # -----------------------------------------------------------------
    #           Tests for function split_nodes_delimiter
    # -----------------------------------------------------------------
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
                
    # -----------------------------------------------------------------
    #          Tests for function extract_markdown_images
    # -----------------------------------------------------------------
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

    # -----------------------------------------------------------------
    #         Tests for function extract_markdown_links
    # -----------------------------------------------------------------
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

    # -----------------------------------------------------------------
    #           Tests for function split_nodes_image
    # -----------------------------------------------------------------
    def test_splitnode_Image_text_frontandafter(self):
        node = TextNode("This is text with an image ![to a cat meme](https://i.imgur.com/xFly57e.jpeg). Isn't that funny?", TextType.TEXT,)
        result = split_nodes_image([node])
        self.assertEqual(result, [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("to a cat meme", TextType.IMAGE, "https://i.imgur.com/xFly57e.jpeg"),
                TextNode(". Isn't that funny?", TextType.TEXT),
            ])

    def test_splitnode_Image_text_onlyafter(self):
        node = TextNode("![A cat meme](https://i.imgur.com/xFly57e.jpeg). Isn't that funny?", TextType.TEXT,)
        result = split_nodes_image([node])
        self.assertEqual(result, [
                TextNode("A cat meme", TextType.IMAGE, "https://i.imgur.com/xFly57e.jpeg"),
                TextNode(". Isn't that funny?", TextType.TEXT),
            ])
        
    def test_splitnode_Image_text_frontonly(self):
        node = TextNode("Hey look, ![a cat meme](https://i.imgur.com/xFly57e.jpeg)", TextType.TEXT,)
        result = split_nodes_image([node])
        self.assertEqual(result, [
                TextNode("Hey look, ", TextType.TEXT),
                TextNode("a cat meme", TextType.IMAGE, "https://i.imgur.com/xFly57e.jpeg"),
            ])    

    def test_splitnode_Image_noimage(self):
        node = TextNode("This is a Textnode without any image links to a funny cat meme.", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [TextNode("This is a Textnode without any image links to a funny cat meme.", TextType.TEXT)])

    def test_splitnode_Image_2_links(self):
        node = TextNode("here is a ![funny cat meme](https://i.imgur.com/xFly57e.jpeg) and a ![funny dog meme](https://i.imgur.com/0iFWjrp.jpeg)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [
                TextNode("here is a ", TextType.TEXT),
                TextNode("funny cat meme", TextType.IMAGE, "https://i.imgur.com/xFly57e.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("funny dog meme", TextType.IMAGE, "https://i.imgur.com/0iFWjrp.jpeg")
        ])

    # -----------------------------------------------------------------
    #           Tests for function split_nodes_link
    # -----------------------------------------------------------------
    def test_splitnode_Link_text_frontandafter(self):
        node = TextNode("This is text with a link [to youtube](https://www.youtube.com). What are we watching today?", TextType.TEXT,)
        result = split_nodes_link([node])
        self.assertEqual(result, [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com"),
                TextNode(". What are we watching today?", TextType.TEXT),
            ])

    def test_splitnode_Link_text_onlyafter(self):
        node = TextNode("[boot.dev](https://www.boot.dev) is an amazing site to learn programming", TextType.TEXT,)
        result = split_nodes_link([node])
        self.assertEqual(result, [
                TextNode("boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" is an amazing site to learn programming", TextType.TEXT),
            ])
        
    def test_splitnode_Link_text_frontonly(self):
        node = TextNode("You should commission this artist: [5ushiroll](https://www.5ushiroll.com)", TextType.TEXT,)
        result = split_nodes_link([node])
        self.assertEqual(result, [
                TextNode("You should commission this artist: ", TextType.TEXT),
                TextNode("5ushiroll", TextType.LINK, "https://www.5ushiroll.com"),
            ])    

    def test_splitnode_Link_nolink(self):
        node = TextNode("This is a Textnode without any links to a website.", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [TextNode("This is a Textnode without any links to a website.", TextType.TEXT)])

    def test_splitnode_Link_2_links(self):
        node = TextNode("This link goes to [youtube](https://www.youtube.com) and this one to [boot.dev](https://www.boot.dev). Where will you go?", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [
                TextNode("This link goes to ", TextType.TEXT),
                TextNode("youtube", TextType.LINK, "https://www.youtube.com"),
                TextNode(" and this one to ", TextType.TEXT),
                TextNode("boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(". Where will you go?", TextType.TEXT),
        ])

    def test_splitnode_mixed_image_and_link(self):
        node = TextNode(
            "Here's a ![cute cat](https://cats.com/cat.jpg) and a link to [more cats](https://cats.com)",
            TextType.TEXT
        )
        # First split images
        nodes_after_images = split_nodes_image([node])
        # Then split links in the resulting nodes
        final_nodes = split_nodes_link(nodes_after_images)
        
        self.assertEqual(final_nodes, [
            TextNode("Here's a ", TextType.TEXT),
            TextNode("cute cat", TextType.IMAGE, "https://cats.com/cat.jpg"),
            TextNode(" and a link to ", TextType.TEXT),
            TextNode("more cats", TextType.LINK, "https://cats.com")
        ])

    # -----------------------------------------------------------------
    #           Tests for function text_to_textnodes
    # -----------------------------------------------------------------
    def test_text_to_node_all_in_one(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
])

    def test_text_to_node_missing_delimiter(self):
        with self.assertRaises(Exception):
            text ="This is text with a `code block` word, **a bold word block* an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
            text_to_textnodes(text)

    def test_text_to_node_simple_text(self):
        text = "this here is just very simple text that has nothing special to it, no formatting or anything else."
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("this here is just very simple text that has nothing special to it, no formatting or anything else.", TextType.TEXT),])

    def test_text_to_node_empty_string(self):
        text = ""
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("",TextType.TEXT)])

    def test_text_to_node_mult_syntax(self):
        text = "This is text with not **one**, but **two** bold syntaxes, aswell as not `one` or `two`, but `three` code block syntaxes and one ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is text with not ",TextType.TEXT),
            TextNode("one", TextType.BOLD),
            TextNode(", but ",TextType.TEXT),
            TextNode("two", TextType.BOLD),
            TextNode(" bold syntaxes, aswell as not ",TextType.TEXT),
            TextNode("one", TextType.CODE),
            TextNode(" or ",TextType.TEXT),
            TextNode("two", TextType.CODE),
            TextNode(", but ",TextType.TEXT),
            TextNode("three", TextType.CODE),
            TextNode(" code block syntaxes and one ",TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ])

    # -----------------------------------------------------------------
    #           Tests for function markdown_to_blocks
    # -----------------------------------------------------------------
    def test_markdown_to_blocks_standard(self):
        mdraw = """# This is a heading
        
        This is a paragraph of text. It has some **bold** and *italic* words inside of it.
        
        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""
        result = markdown_to_blocks(mdraw)
        self.assertEqual(result, [
            '# This is a heading', 
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
            '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
            ])

    def test_markdown_to_blocks_multlines(self):
        mdraw = """# Heading

    

        Paragraph"""
        result = markdown_to_blocks(mdraw)
        self.assertEqual(result, [
            '# Heading', 
            'Paragraph',
            ])

    def test_markdown_to_blocks_mixed_indentation(self):
        mdraw = """* List item 1
          * List item 2
         * List item 3"""
        result = markdown_to_blocks(mdraw)
        self.assertEqual(result, [
            '* List item 1\n* List item 2\n* List item 3'
            ])

    def test_markdown_to_blocks_empty(self):
        mdraw = """"""
        result = markdown_to_blocks(mdraw)
        self.assertEqual(result, [])

    def test_markdown_to_blocks_singleline(self):
        mdraw = """Just a single line"""
        result = markdown_to_blocks(mdraw)
        self.assertEqual(result, ["Just a single line"])

    # -----------------------------------------------------------------
    #           Tests for function block_to_block_type
    # -----------------------------------------------------------------
    def test_block_to_block_heading_2(self):
        block = "## Heading 2"
        result = block_to_block_type(block)
        self.assertEqual(result, "heading")

    def test_block_to_block_heading_5(self):
        block = "##### Heading 5"
        result = block_to_block_type(block)
        self.assertEqual(result, "heading")

    def test_block_to_block_notaheading(self):
        block = "#Not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")            

    def test_block_to_block_heading_6(self):
        block = "###### Valid Heading"
        result = block_to_block_type(block)
        self.assertEqual(result, "heading")

    def test_block_to_block_invalid_heading(self):
        block = "####### Invalid Heading"
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_block_to_block_quote_singleline(self):
        block = "> This is a single-line quote"
        result = block_to_block_type(block)
        self.assertEqual(result, "quote")

    def test_block_to_block_quote_multiline(self):
        block = "> Line one\n> Line two\n> Line three"
        result = block_to_block_type(block)
        self.assertEqual(result, "quote")

    def test_block_to_block_quote_invalid(self):
        block = "> Line one\nNot a quote line\n> Line three"
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_block_to_block_code_single_line(self):
        block = "```\nprint('Hello, world!')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, "code")

    def test_block_to_block_code_multiline(self):
        block = "```\ndef hello():\n    return 'world'\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, "code")

    def test_block_to_block_code_empty(self):
        block = "```\n\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, "code")

    def test_block_to_block_code_all_single_line(self):
        block = "```print('Hello, world!')```"
        result = block_to_block_type(block)
        self.assertEqual(result, "code")

    def test_block_to_block_code_fullempty(self):
        block = "``````"
        result = block_to_block_type(block)
        self.assertEqual(result, "code")

    def test_block_to_block_code_invalid(self):
        block = "```\ndef hello():\nprint('Oops missing backticks')"
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_block_to_block_unordered_list_single_line(self):
        block = "* Item one"
        result = block_to_block_type(block)
        self.assertEqual(result, "unordered_list")

    def test_block_to_block_unordered_list_multiline(self):
        block = "- Item one\n- Item two\n- Item three"
        result = block_to_block_type(block)
        self.assertEqual(result, "unordered_list")

    def test_block_to_block_unordered_list_mixed_markers(self):
        block = "* Item one\n- Item two"
        result = block_to_block_type(block)
        self.assertEqual(result, "unordered_list")

    def test_block_to_block_unordered_list_invalid(self):
        block = "* Item one\nNot a list line\n* Item three"
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    def test_block_to_block_ordered_list_single_line(self):
        block = "1. First item"
        result = block_to_block_type(block)
        self.assertEqual(result, "ordered_list")

    def test_block_to_block_ordered_list_multiline(self):
        block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, "ordered_list")

    def test_block_to_block_ordered_list_invalid_increment(self):
        block = "1. First item\n3. Third item"
        result = block_to_block_type(block)
        self.assertEqual(result, "paragraph")

    # -----------------------------------------------------------------
    #          Tests for function markdown_to_html_node
    # -----------------------------------------------------------------
    def test_markdown_to_html_heading_block(self):
            markdown = """# Heading 1

            ## Heading 2

            ### Heading 3""".strip()
            result = markdown_to_html_node(markdown)
            assert result.to_html() == (
                "<div>"
                "<h1>Heading 1</h1>"
                "<h2>Heading 2</h2>"
                "<h3>Heading 3</h3>"
                "</div>"
            )
    
    def test_markdown_to_html_code_block(self):
        markdown = "```\ndef test():\n    return True\n```"
        result = markdown_to_html_node(markdown)
        assert result.to_html() == (
            "<div>"
            "<pre><code>def test():\nreturn True</code></pre>"
            "</div>"
        )

    def test_markdown_to_html_quote_block(self):
        markdown = "> This is a quote"
        result = markdown_to_html_node(markdown)
        assert result.to_html() == (
            "<div>"
            "<blockquote>This is a quote</blockquote>"
            "</div>"
        )

    def test_markdown_to_html_unordered_list(self):
        markdown = "- Item 1\n- Item 2\n- Item 3"
        result = markdown_to_html_node(markdown)
        assert result.to_html() == (
            "<div>"
            "<ul>"
            "<li>Item 1</li>"
            "<li>Item 2</li>"
            "<li>Item 3</li>"
            "</ul>"
            "</div>"
        )

    def test_markdown_to_html_ordered_list(self):
        markdown = "1. First Item\n2. Second Item\n3. Third Item"
        result = markdown_to_html_node(markdown)
        assert result.to_html() == (
            "<div>"
            "<ol>"
            "<li>First Item</li>"
            "<li>Second Item</li>"
            "<li>Third Item</li>"
            "</ol>"
            "</div>"
        )

    def test_markdown_to_html_paragraph_block(self):
        markdown = "This is a simple paragraph."
        result = markdown_to_html_node(markdown)
        assert result.to_html() == (
            "<div>"
            "<p>This is a simple paragraph.</p>"
            "</div>"
        )

    def test_markdown_to_html_mixed_markdown(self):
        markdown = """
    # Heading

    This is a paragraph.

    - Item 1
    - Item 2

    > Blockquote here
        """.strip()
        result = markdown_to_html_node(markdown)
        # Remove all whitespace for comparison
        actual = ''.join(result.to_html().split())
        expected = ''.join((
            "<div>"
            "<h1>Heading</h1>"
            "<p>This is a paragraph.</p>"
            "<ul><li>Item 1</li><li>Item 2</li></ul>"
            "<blockquote>Blockquote here</blockquote>"
            "</div>"
        ).split())
        actual == expected

    # -----------------------------------------------------------------
    #           Tests for function extract_title
    # -----------------------------------------------------------------
    def test_extract_title_simple(self):
        markdown = "# Simple Title"
        result = extract_title(markdown)
        self.assertEqual(result, "Simple Title")

    def test_extract_title_more_spaces(self):
        markdown = "#    Spaced Title"
        result = extract_title(markdown)
        self.assertEqual(result, "Spaced Title")

    def test_extract_title_h2_Exception(self):
        with self.assertRaises(Exception):
            markdown = "## Second Level"
            extract_title(markdown)

    def test_extract_title_Exception(self):
        with self.assertRaises(Exception):
            markdown = "This is a normal Paragraph"
            extract_title(markdown)       

    def test_extract_title_two_h1(self):
        markdown = "# First Title\n# Second Title"
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")

if __name__ == "__main__":
    unittest.main()