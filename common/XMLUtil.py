# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import sys

def parse_from_str(xml_str):
    try:
        tree = ET.fromstring(xml_str)
        return tree
    except Exception, e:
        print e
        return None

def get_children_tag_name(element):
    if element is None:
        return None
    result = []
    for child in element.getchildren():
        result.append(child.tag)
    return result

def get_children_text_dic(element, charset = 'utf-8'):
    if element is None:
        return None
    result = {}
    for child in element.getchildren():
        if child.text is None:
            continue
        key = child.tag
        value = child.text
        if charset:
            key = key.decode(charset)
            value = value.decode(charset)
        result[key] = value
    return result

# reload(sys)
# sys.setdefaultencoding('utf-8')

# etree = parse_from_str('''<xml>
#                                              <ToUserName><![CDATA[toUser]]></ToUserName>
#                                              <FromUserName><![CDATA[fromUser]]></FromUserName>
#                                              <CreateTime>1348831860</CreateTime>
#                                              <MsgType><![CDATA[image]]></MsgType>
#                                              <PicUrl><![CDATA[这是一个图片]]></PicUrl>
#                                              <MediaId><![CDATA[media_id]]></MediaId>
#                                              <MsgId>1234567890123456</MsgId>
#                                          </xml>'''.decode('utf-8'))
# dic = get_children_text_dic(etree)
# print dic
# print dic['PicUrl']



