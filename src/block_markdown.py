def markdown_to_blocks(markdown):
    content = markdown.strip()
    if not content:
        return []

    # Split by double newlines to separate blocks
    blocks = []
    for block in content.split('\n\n'):
        # Remove leading/trailing whitespace from the block and each line
        lines = [line.strip() for line in block.split('\n')]
        # Join non-empty lines with single newlines
        cleaned_block = '\n'.join(line for line in lines if line)
        if cleaned_block:  # Only add non-empty blocks
            blocks.append(cleaned_block)

    return blocks
