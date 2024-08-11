
#!/usr/bin/python3
"""
convert a Markdown file to HTML
"""

import argparse
import pathlib
import re


def convert_md_to_html(input_file, output_file):
    '''
    file to HTML file
    '''
    with open(input_file, encoding='utf-8') as f:
        md_content = f.readlines()

    html_content = []
    for line in md_content:
        match = re.match(r'(#){1,6} (.*)', line)
        if match:
            h_level = len(match.group(1))
            h_content = match.group(2)
            html_content.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
        else:
            html_content.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(html_content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert markdown to HTML')
    parser.add_argument('input_file', help='path to input markdown file')
    parser.add_argument('output_file', help='path to output HTML file')
    args = parser.parse_args()

    input_path = pathlib.Path(args.input_file)
    if not input_path.is_file():
        print(f'Missing {input_path}', file=sys.stderr)
        sys.exit(1)

    convert_md_to_html(args.input_file, args.output_file)
