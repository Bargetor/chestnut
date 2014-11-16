import html5lib
import traceback

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
    try:
        content = None

        for content_element_text_child in element.childNodes:
            content = content_element_text_child.nodeValue

            if content is not None:
                content = content.strip()

            if content is not None and content != '' : return content

            if not hasattr(content_element_text_child, 'childNodes') : continue

            if (content is None or content == '') and (content_element_text_child.childNodes is None or len(content_element_text_child.childNodes) == 0):
                continue

            content = find_element_content(content_element_text_child)

            if content is not None and content != '' : return content

        return content
    except Exception, e:
        exstr = traceback.format_exc()
        print exstr







