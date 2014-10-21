import xml.etree.cElementTree as ET

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

def get_children_text_dic(element):
    if element is None:
        return None
    result = {}
    for child in element.getchildren():
        if child.text is None:
            continue
        result[child.tag] = child.text
    return result

# etree = parseFromStr('''<xml>
#                                              <ToUserName><![CDATA[toUser]]></ToUserName>
#                                              <FromUserName><![CDATA[fromUser]]></FromUserName>
#                                              <CreateTime>1348831860</CreateTime>
#                                              <MsgType><![CDATA[image]]></MsgType>
#                                              <PicUrl><![CDATA[this is a url]]></PicUrl>
#                                              <MediaId><![CDATA[media_id]]></MediaId>
#                                              <MsgId>1234567890123456</MsgId>
#                                          </xml>''')
# print getChildrenTextDic(etree)


