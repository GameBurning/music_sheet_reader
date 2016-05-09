#coding:utf-8
import xml.etree.ElementTree as ET
import sys
reload(sys)
sys.setdefaultencoding('utf8')
Note = {'A': '拉','B': '西','C': '多','D': '來','E': '咪','F': '发','G': '娑'}

#- 读取XML文件 -#
tree = ET.parse('Yani.xml')
root = tree.getroot()

#- 获取标题信息 -#
work = root.find('work')
worktitle = ""
if work != None:
    worktitle = work.find('work-title')
else:
    worktitle = root.find('movement-title')
title_string = "乐谱标题: " + worktitle.text
print title_string

identification = root.find('identification')
#- 获取作者 -#
creator = identification.find('creator')
composer = ""
if creator.attrib['type'] == "composer":
    composer = creator.text
print composer

#- 获取乐谱谱头信息 -#
