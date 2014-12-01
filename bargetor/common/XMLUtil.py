
import xml.etree.ElementTree as ET
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
        # if charset:
        #     key = key.decode(charset)
        #     value = value.decode(charset)
        result[key] = value
    return result

def get_new_etree(root_name):
    if not root_name:
        return None
    root = ET.Element(root_name)
    etree = ET.ElementTree()
    etree._setroot(root)
    return etree

def get_new_element(element_name):
    return ET.Element(element_name)

def write_cdata_text_child(root, tag_name, text):
    e = ET.Element(tag_name)
    cdata = CDATA(text)
    e.append(cdata)
    root.append(e)
    return root

def write_text_child(root, tag_name, text):
    e = ET.Element(tag_name)
    e.text = text
    root.append(e)
    return root
def to_etree_xml_str(etree):
    return ET.tostring(etree.getroot())

def CDATA(text=None):
    element = ET.Element('![CDATA[')
    element.text = text
    return element

ET._original_serialize_xml = ET._serialize_xml
def _serialize_xml(write, elem, encoding, qnames, namespaces):
    if elem.tag == '![CDATA[':
        write("<%s%s]]>" % (elem.tag, elem.text))
        return
    return ET._original_serialize_xml(
        write, elem, encoding, qnames, namespaces)
ET._serialize_xml = ET._serialize['xml'] = _serialize_xml


# reload(sys)
# sys.setdefaultencoding('utf-8')

# etree = parse_from_str('''<xml>
#                                              <ToUserName><![CDATA[toUser]]></ToUserName>
#                                              <FromUserName><![CDATA[fromUser]]></FromUserName>
#                                              <CreateTime>1348831860</CreateTime>
#                                              <MsgType><![CDATA[image]]></MsgType>
#                                              <MediaId><![CDATA[media_id]]></MediaId>
#                                              <MsgId>1234567890123456</MsgId>
#                                          </xml>'''.decode('utf-8'))
# dic = get_children_text_dic(etree)
# print dic
# print dic['PicUrl']


# etree = get_new_etree('xml')
# print etree
# e = ET.Element('a')
# e.text = 'b'
# etree.getroot().append(e)
# write_cdata_text_child(etree.getroot(), 'c', 'e')
# print ET.tostring(etree.getroot())
# etree = parse_from_str(ET.tostring(etree.getroot()))
# dic = get_children_text_dic(etree)
# print dic
