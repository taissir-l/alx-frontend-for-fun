#!/usr/bin/python3
import sys
import os
import re
import hashlib

def convert_md_to_html(input_file, output_file):
    with open(input_file, 'r') as md_file:
        lines = md_file.readlines()

    html_content = []
    list_type = None  # To handle both <ul> and <ol>

    for line in lines:
        line = line.rstrip()

        # Handle headings
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            html_content.append(f"<h{level}>{text}</h{level}>")
            continue

        # Handle unordered lists
        ul_match = re.match(r'^-\s+(.*)', line)
        if ul_match:
            if list_type != 'ul':
                if list_type == 'ol':
                    html_content.append('</ol>')
                list_type = 'ul'
                html_content.append('<ul>')
            html_content.append(f"<li>{ul_match.group(1)}</li>")
            continue

        # Handle ordered lists
        ol_match = re.match(r'^\*\s+(.*)', line)
        if ol_match:
            if list_type != 'ol':
                if list_type == 'ul':
                    html_content.append('</ul>')
                list_type = 'ol'
                html_content.append('<ol>')
            html_content.append(f"<li>{ol_match.group(1)}</li>")
            continue

        # Handle paragraphs
        if line.strip() != "":
            # Bold and emphasis
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)  # Bold
            line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)  # Emphasis
            
            # Special replacements
            line = re.sub(r'\[\[(.*?)\]\]', lambda x: hashlib.md5(x.group(1).encode()).hexdigest(), line)
            line = re.sub(r'\(\((.*?)\)\)', lambda x: re.sub(r'[cC]', '', x.group(1)), line)

            if list_type:
                html_content.append('</ul>' if list_type == 'ul' else '</ol>')
                list_type = None
            if line != "":
                html_content.append(f"<p>{line}</p>")

    # Close any remaining open list
    if list_type:
        html_content.append('</ul>' if list_type == 'ul' else '</ol>')

    with open(output_file, 'w') as html_file:
        html_file.write('\n'.join(html_content))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <Markdown file> <HTML file>", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    convert_md_to_html(markdown_file, html_file)
    sys.exit(0)
