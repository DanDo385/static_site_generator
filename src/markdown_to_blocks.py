# src/markdown_to_blocks.py

def markdown_to_blocks(markdown: str):
    """
    Split a markdown document into blocks based on double newlines.
    
    Args:
        markdown: Raw markdown string representing a full document
        
    Returns:
        List of block strings with leading/trailing whitespace stripped
    """
    # Split by double newlines to separate blocks
    blocks = markdown.split("\n\n")
    
    # Strip whitespace from each block and filter out empty blocks
    processed_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:  # Only include non-empty blocks
            processed_blocks.append(stripped_block)
    
    return processed_blocks
