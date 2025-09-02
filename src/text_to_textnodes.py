# src/text_to_textnodes.py
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter
from split_nodes_images_links import split_nodes_image, split_nodes_link

def text_to_textnodes(text: str):
    """
    Convert raw markdown text into a list of TextNode objects.
    
    Processes the text through all splitting functions in the correct order:
    1. Split images first
    2. Split links second  
    3. Split code delimiters (backticks)
    4. Split bold delimiters (**)
    5. Split italic delimiters (_)
    
    Args:
        text: Raw markdown text string
        
    Returns:
        List of TextNode objects with appropriate types
    """
    # Start with a single TEXT node
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Split images first
    nodes = split_nodes_image(nodes)
    
    # Split links second
    nodes = split_nodes_link(nodes)
    
    # Split code delimiters (backticks)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Split bold delimiters (**)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # Split italic delimiters (_)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    return nodes
