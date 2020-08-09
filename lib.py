import os


def match_tag(line: str, tag: str) -> bool:
    return line[:len(tag)+2] == f'%{tag}:' or line[:len(tag)+2] == f'%{tag}%'


def tag_param(line: str) -> str:
    return ''.join(line.split('%')).replace(' ', '').split(':')[1]


def reverse_bool(flag: bool) -> bool:
    if flag:
        return False
    else:
        return True


def glob_tree(dirname: str, ignore_list: list) -> list:
    dic = dict()
    file_or_dirs = filter(lambda x: x not in ignore_list, os.listdir(dirname))
    filelist = list(filter(lambda x: os.path.isfile(os.path.join(dirname, x)), file_or_dirs))
    dic[os.path.join(dirname, '/').split('/')[-1]] = filelist
    for d in filter(lambda x: os.path.isdir(os.path.join(dirname, x)), file_or_dirs):
        dic[d] = glob_tree(os.path.join(dirname, d), ignore_list)
    
    return dic


def hoge(files_dic: dict, header='',deps=1) -> str:
    buf = '## /\n'

    for k, v in files_dic.items():
        if type(v) == list:
            for x in v:
                buf += f'%SOURCE:{os.path.join(header, x)}%\n'
        elif type(v) == dict:
            buf += f'{"#"*(deps+2)} {k}\n'
            buf += hoge(v, os.path.join(header,k),deps+1)
    
    return buf


if __name__ == "__main__":
    a = glob_tree('./', ['.vscode'])
    r = hoge(a)
    print(r)



