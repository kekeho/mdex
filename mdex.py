#!/usr/bin/env python3
import sys
import mimetypes


class NotTextFileError(Exception):
    def __init__(self, mime, encode):
        print(f"""This is not text file.
given {mime}, {encode} file.""")


class UnknownArgvError(Exception):
    def __init__(self):
        print(f"""Usage:
    mdex [filename]""")


class MarkdownEx():
    """Markdown extension converter
    FLAGS:
        @@ filename:    include external file by file_expand function
                        file expands in ```mimetype:
                                        in_file_content
                                        ```
    """

    def __init__(self, filename: str):
        self.md_filename = filename
        self.md_file = open(filename, 'r')
        self.output_md_text = self.md_file.read()

    def __del__(self):
        # file closure
        self.md_file.close()

    def file_expand(self):
        return_md = """"""
        line_array = self.output_md_text.split('\n')
        for line in line_array:
            atmark_position = line.find('@@')

            if atmark_position == -1 or atmark_position != 0:
                # not found or not in the head of line
                return_md += '\n' + line
                continue

            include_filename = line[3:].split(' ')[0]

            mime, encode = mimetypes.guess_type(include_filename)
            text_or_binary, filetype = mime.split('/')
            if text_or_binary != 'text':
                raise NotTextFileError(mime, encode)

            with open(include_filename, 'r') as in_file:
                in_file_content = in_file.read()

                line = f'```{filetype}:{include_filename}\n'
                line += in_file_content
                line += '\n```'

            line = '\n' + line
            return_md += line

        # return
        self.output_md_text = return_md

    def save(self, samefile=False):
        if samefile is True:
            save_filename = self.md_filename
        else:
            dots = self.md_filename.split('.')
            save_filename = ''.join(dots[:-1]) + '_converted.' + dots[-1]

        with open(save_filename, 'w') as savefile:
            savefile.write(self.output_md_text)


if __name__ == "__main__":
    """Usage:
    python3 mdex [filename]
    """
    if len(sys.argv) != 2:
        raise UnknownArgvError()

    filename = sys.argv[1]
    md = MarkdownEx(sys.argv[1])
    md.file_expand()
    md.save()
