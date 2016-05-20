#coding:utf-8
import xml.etree.ElementTree as ET
import sys
reload(sys)
sys.setdefaultencoding('utf8')
note_dict = {'A': '拉','B': '西','C': '多','D': '來','E': '咪', 'F': '发',\
'G': '娑'}
octave_dict = {'1': '大字二组','2': '大字一组','3': '大字组','4': '小字组',\
'5': '小字一组','6': '小字二组','7': '小字三组','8': '小字四组','9': '小字五组'}
note_type = {'whole': '全音符', 'half': '二分音符', 'quarter': '四分音符', \
'eighth':'八分音符', '16th':'十六分音符', '32th':'三十二音符'}
digit_dict = dict(zip(['1', '2', '3' ,'4' , '5', '6', '7', '8', '9', '0'],\
['一','二','三','四','五','六','七','八','九','零']))
fifthkey_dict = dict(zip(['-5', '-4', '-3' ,'-2' , '-1', '0', '1', '2', '3',\
 '4', '5'],['5个降号','4个降号','3个降号','2个降号','1个降号','没有升降号','1个升号',\
 '2个升号','3个升号','4个升号','5个升号']))

#- 读取XML文件 -#
tree = ET.parse('599/1-2.xml')
_root = tree.getroot()

#- 获取标题信息 -#
_work = _root.find('work')
r_worktitle = "乐谱标题："
if _work != None:
    r_worktitle += _work.find('work-title').text
else:
    r_worktitle += _root.find('movement-title').text

identification = _root.find('identification')
#- 获取作者 -#
_creator = identification.find('creator')
r_composer = "作者"
if _creator != None and _creator.attrib['type'] == "composer":
    r_composer += _creator.text
else:
    r_composer = ""

#- 读取乐谱页及小节 -#
p = [] #乐谱的页元素列表
m = [] #小节组成的二维列表,第一维表征页数,第二维表征小节.如m[0][2]就是第一页第三小节

for page in _root.findall('part'):
    p.append(page)
    temp_m = []
    for measure in page.findall('measure'):
        temp_m.append(measure)
    m.append(temp_m)
if p[0].attrib['id'] != "P1" or m[0][0].attrib["number"] != \
"1" and m[0][0].attrib['number'] != '0':
    sys.exit("Not P1 or M1")
print len(m[0])

#- 读取Tempo -#
_beatunit = m[0][0].find('direction/direction-type/metronome/beat-unit')
beatunit = "未指定"
if _beatunit != None:
    beatunit = _beatunit.text
_perminute = m[0][0].find('direction/direction-type/metronome/per-minute')
if _perminute != None:
    beatunit += _perminute.text + " 每分钟"
r_tempo = "曲速为: " + beatunit

#- 读取Attributes#
clef_num = 0
#_stafflayout = p[0].find('measure/print/staff-layout')
_attrib = m[0][0].find('attributes')
_stafflayout = _attrib.find('staves')
if _stafflayout == None:
    clef_num = 1
else:
    clef_num = int(_stafflayout.text)
print clef_num

#- 读取division -#
divisions = _attrib.find('divisions').text
key = _attrib.find('key/fifths').text
r_key = fifthkey_dict[key]
beats = _attrib.find('time/beats').text
beat_type = _attrib.find('time/beat-type').text
r_beat = digit_dict[beat_type] + digit_dict[beats] + "拍"

sign = []
for clef in _attrib.findall('clef'):
    sign.append(clef.find('sign').text)

whole_text = [] #每小节的文字

#- 分小结读取乐谱内容 -#
for m_page in m:
    for m_single in page:
        m_text = []
        for i in range(0, clef_num):
            m_text.append([])
        for note in m_single.findall('note'):
            _step = note.find('pitch/step').text
            _octave = note.find('pitch/octave').text
            _type = note.find('type').text
            #voice元素不知道有没有作用
            _staff = note.find('staff').text
            note_text = octave_dict[_octave] + note_type[_type] + note_dict[_step]
            m_text[int(_staff)-1].append(note_text)
            whole_text.append(m_text)

comma = ", "
read_heading = r_worktitle + comma + \
r_composer + comma + \
r_tempo + comma + \
r_key + comma + \
r_beat
print read_heading


read_body = ""
