#!/usr/bin/python3
"""
Markdown to HTML converter script.
"""

import sys
import os
import hashlib

def convert_md_to_html(md_file, html_file):
    try:
        with open(md_file, 'r') as md:
            lines = md.readlines()
    except FileNotFoundError:
        print(f"Missing {md_file}", file=sys.stderr)
        sys.exit(1)

    html_content = []
    in_list = False
    for line in lines:
        line = line.rstrip()

        # Convert headings
        if line.startswith('#'):
            heading_level = len(line.split()[0])
            content = line[heading_level+1:]
            html_content.append(f"<h{heading_level}>{content}</h{heading_level}>")
        
        # Convert unordered list items
        elif line.startswith('- '):
            if not in_list:
                html_content.append("<ul>")
                in_list = True
            html_content.append(f"<li>{line[2:]}</li>")
        
        # Convert ordered list items
        elif line.startswith('* '):
            if not in_list:
                html_content.append("<ol>")
                in_list = True
            html_content.append(f"<li>{line[2:]}</li>")

        # End list when encountering non-list lines
        else:
            if in_list:
                html_content.append("</ul>" if line.startswith('-') else "</ol>")
                in_list = False

            # Convert paragraphs and line breaks
            if line:
                line = line.replace("**", "<b>").replace("__", "<em>")
                while "**" in line:
                    line = line.replace("**", "</b>", 1)
                while "__" in line:
                    line = line.replace("__", "</em>", 1)
                while "[[" in line and "]]" in line:
                    start = line.find("[[") + 2
                    end = line.find("]]")
                    to_hash = line[start:end]
                    hashed = hashlib.md5(to_hash.encode()).hexdigest()
                    line = line[:start-2] + hashed + line[end+2:]
                while "((" in line and "))" in line:
                    start = line.find("((") + 2
                    end = line.find("))")
                    to_replace = line[start:end]
                    line = line[:start-2] + to_replace.replace("c", "").replace("C", "") + line[end+2:]
                html_content.append(f"<p>{line}</p>")
            else:
                html_content.append("<br/>")

    if in_list:
        html_content.append("</ul>" if line.startswith('-') else "</ol>")

    with open(html_file, 'w') as html:
        html.write("\n".join(html_content))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]
    convert_md_to_html(md_file, html_file)
    sys.exit(0)
