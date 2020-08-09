#!/usr/bin/env python3
import sys
import mimetypes
from glob import glob

import lib


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
        self.exfunc_list = [self.sources_in_dir, self.file_expand, self.index]

    def __del__(self):
        # file closure
        self.md_file.close()
    

    def compile(self):
        for f in self.exfunc_list:
            f()
    

    def file_expand(self):
        return_md = """"""
        line_array = self.output_md_text.split('\n')
        for line in line_array:
            if not lib.match_tag(line, 'SOURCE'):
                # not found or not in the head of line
                return_md += '\n' + line
                continue

            include_filename = lib.tag_param(line)

            mime, encode = mimetypes.guess_type(include_filename)
            if mime is not None:
                text_or_binary, filetype = mime.split('/')
            else:
                text_or_binary = 'text'
                filetype = ''

            line = f"{include_filename}\n"
            with open(include_filename, 'r') as in_file:
                try:
                    in_file_content = in_file.read()
                except UnicodeDecodeError:
                    # binary
                    continue

                line += f'```{filetype}:{include_filename}\n'
                line += in_file_content
                line += '\n```'

            line = '\n' + line
            return_md += line

        # return
        self.output_md_text = return_md
    

    def sources_in_dir(self):
        ignore_tags = ['```']
        try:
            with open('.mdexignore', 'r') as igfp:
                ignore_list = igfp.read().split('\n')
        except FileNotFoundError:
            ignore_list = []
        return_md = ''

        for line in self.output_md_text.split('\n'):
            if not lib.match_tag(line, 'SOURCES_IN_DIR'):
                return_md += f'{line}\n'
                continue

            dirname = lib.tag_param(line)
            filelist = lib.glob_tree(dirname, ignore_list)
            return_md += lib.hoge(filelist)

        self.output_md_text = return_md
    

    def index(self):
        ignore_tags = ['```']
        index_list = []
        ignore_flag = False
        for idx, line in enumerate(self.output_md_text.split('\n')):
            for ignore_tag in ignore_tags:
                if lib.match_tag(line, ignore_tag):
                    ignore_flag = lib.reverse_bool(ignore_flag)

            if len(line) <= 0 or line[0] != '#' or ignore_flag:
                # not found or not in the head of line
                continue
            
            # count header level
            level = 0
            while True:
                try:
                    if line[level] != '#':
                        break
                except IndexError:
                    break
                level += 1
            if level >= 2:
                index_list.append({'level': level, 'title': line.replace('#', '')[1:], 'line': idx})

        return_md = ''
        for line in self.output_md_text.split('\n'):
            if lib.match_tag(line, 'INDEX'):
                for index in index_list:
                    space = "    " * (index['level']-2)
                    return_md += f'{space}- [{index["title"]}](#{index["title"]})\n'
            else:
                return_md += f'{line}\n'
        
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
    md.compile()
    md.save()
