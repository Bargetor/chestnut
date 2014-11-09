import html5lib

def build_html_dom_from_str(html_str):
    return html5lib.parse(html_str, 'dom')

def find_html_element_list_for_tag(element, tag, class_style = None):
    elements = element.getElementsByTagName(tag)
    if not class_style: return elements
    result = []
    for e in elements:
        e_class_style = e.getAttribute('class')
        if e_class_style == class_style:
            result.append(e)
    return result

def find_element_content(element):
    content = None
    for content_element_text_child in element.childNodes:
        content = content_element_text_child.nodeValue
        if not content: continue
        content = content.strip()
        if not content or content == '':
            content = None
    return content
