#coding:utf-8
import xml.etree.ElementTree as ET
import sys
reload(sys)
sys.setdefaultencoding('utf8')
note_dict = {'A': '拉','B': '西','C': '多','D': '來','E': '咪', 'F': '发',\
'G': '娑'}
octave_dict = {'1': '大字二组','2': '大字一组','3': '大字组','4': '小字组',\
'5': '小字一组','6': '小字二组','7': '小字三组','8': '小字四组','9': '小字五组'}

#- 读取XML文件 -#
tree = ET.parse('Yani.xml')
_root = tree.getroot()

#- 获取标题信息 -#
_work = _root.find('work')
worktitle = "乐谱标题："
if _work != None:
    worktitle += _work.find('work-title').text
else:
    worktitle += _root.find('movement-title').text
print worktitle

identification = _root.find('identification')
#- 获取作者 -#
_creator = identification.find('creator')
composer = "作者"
if _creator != None and _creator.attrib['type'] == "composer":
    composer = _creator.text
print composer

#- 读取乐谱页及小节 -#
p = []
m = []
pi = 0
for page in _root.findall('part'):
    p.append(page)
    temp_m = []
    for measure in page.findall('measure'):
        temp_m.append(measure)
    m.append(temp_m)
if p[0].attrib['id'] != "P1" or m[0][0].attrib["number"] != \
"1" and m[0][0].attrib['number'] != '0':
    sys.exit("Not P1 or M1")

#- 读取Tempo -#
_beatunit = m[0][0].find('direction/direction-type/metronome/beat-unit')
beatunit = "未指定"
if _beatunit != None:
    beatunit = _beatunit.text
    print beatunit
_perminute = m[0][0].find('direction/direction-type/metronome/per-minute')
if _perminute != None:
    beatunit += _perminute.text + " 每分钟"
tempo = "曲速为: " + beatunit
print tempo

#- 读取声部 -#
clef = 0
_stafflayout = p[0].find('measure/print/staff-layout')
if _stafflayout == None:
    clef = 1
else:
    clef = _stafflayout.attrib['number']
print clef

#- 分小结读取乐谱内容 -#
m_text = []
for m_page in m:
    m_text_temp = ""
    for m_single in m_page:
        
