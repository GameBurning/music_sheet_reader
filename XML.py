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

#- 读取乐谱页及小节 -#
p = []
m = []
pi = 0
for page in root.findall('part'):
    p.append(page)
    temp_m = []
    for measure in page.findall('measure'):
        temp_m.append(measure)
    m.append(temp_m)
if p[0].attrib['id'] != "P1" or m[0][0].attrib["number"] != "1":
    sys.exit("Not P1 or M1")

#- 读取Tempo -#
beat-unit = m[0][0].find('direction/direction-type/metronome/beat-unit').text
per-minute = m[0][0].find('direction/direction-type/metronome/per-minute').text
tempo = "曲速" + beat-unit + per-minute + "每分钟"
print tempo
