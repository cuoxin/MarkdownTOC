'''
Author: Adrian_Yan
Title: md创建目录
Creat: 2020-7-14
Version: 1.1

'''


import re
import os
str_re_flag = "<br id=\".+\">"
re_ed_flag = re.compile(str_re_flag)

def creatTOC(file_path):
    ## 匹配标题
    str_re_title = r"#+ .+"
    str_re_code = r"```.*" ## 匹配代码块
    re_ed_title = re.compile(str_re_title)
    re_ed_code = re.compile(str_re_code)

    code_bool = False

    TOC = {}
    TOC_line = 0

    with open(file_path, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            list_code = None
            list_code = re_ed_code.findall(line)
            if list_code:
                code_bool = not code_bool

            if not code_bool:
                re_find_ed = None

                if line in ["[TOC]\n"]:
                    TOC_line = i

                re_find_ed = re_ed_title.findall(line)
                if re_find_ed:
                    str_title = re_find_ed[0]
                    list_title = str_title.split(" ")

                    ## 计算有几个井号
                    length_first = len(list_title[0])
                    list_title = list_title[1:]
                    title = " ".join(list_title)
                    title = re.sub(re_ed_flag, "", title)

                    TOC[i] = [length_first, title]
    
    return TOC, TOC_line


def creatTOCStr(TOC):
    TOC_str = ''

    for key in TOC:
        value = TOC[key]
        first_str = " " * 4 * (value[0] - 1) + "-" + " "
        title = "[{}]".format(value[1])
        quote = "(#{})".format(key)

        new_str = first_str + title + quote + "\n"

        TOC_str += new_str

    return TOC_str


def newTitle(i, title):
    title = re.sub(re_ed_flag, "", title)

    apd = "<br id=\"{}\">".format(i)

    title = title[:-1]
    title += apd
    title += "\n"

    return title


def finallyFile(new_file, old_file, new_path, old_path):
    new_file.close()
    old_file.close()

    os.remove(old_path)
    os.rename(new_path, old_path)



def creatNewFile(file_path, TOC, TOC_line):
    ## 创建一个同名新文件
    list_path = file_path.split(".")
    list_path.pop(-1)
    list_path.append("txt")
    new_file_path = ".".join(list_path)

    new_file = open(new_file_path, "w", encoding="UTF-8")
    old_file = open(file_path, "r", encoding="UTF-8")

    lines = old_file.readlines()
    lines_ = lines[::]
    for i, line in enumerate(lines_):
        if i in TOC:
            lines[i] = newTitle(i, line)

    str_TOC = creatTOCStr(TOC)
    try:
        lines.remove("[TOC]\n")
    except ValueError:
        print("没有标志[TOC]，将在第一行生成")
    lines.insert(TOC_line, str_TOC)
    
    new_file.writelines(lines)

    finallyFile(new_file, old_file, new_file_path, file_path)



def main():
    md_path = input(">")
    TOC, TOC_line = creatTOC(md_path)
    creatNewFile(md_path, TOC, TOC_line)

if __name__ == "__main__":
    main()
