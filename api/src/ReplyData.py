#-*- coding: utf-8 -*-
#客户请求与被动消息响应属于两个应用场景，但属于同等数据结构
import time
from common.XMLUtil import *
from api.APISettings import *

class BaseReplyData(object):
    """docstring for BaseReplyData"""
    def __init__(self, request):
        super(BaseReplyData, self).__init__()

        self.to_user_name = request.from_user_name
        self.from_user_name = request.to_user_name
        self.create_time = str(time.time())
        self.msg_type = None

    def build_xml_tree(self):
        etree = get_new_etree('xml')
        write_cdata_text_child(etree.getroot(), POST_DATA_TAG_NAME_TO_USER_NAME, self.to_user_name)
        write_cdata_text_child(etree.getroot(), POST_DATA_TAG_NAME_FROM_USER_NAME, self.from_user_name)
        write_text_child(etree.getroot(), POST_DATA_TAG_NAME_CREATE_TIME, self.create_time)
        write_cdata_text_child(etree.getroot(), POST_DATA_TAG_NAME_MSG_TYPE, self.msg_type)
        return etree

    def get_xml_str(self):
        etree = self.build_xml_tree()
        return to_etree_xml_str(etree)

class TextReplyData(BaseReplyData):
    """docstring for TextReplyData"""
    def __init__(self, request):
        super(TextReplyData, self).__init__(request)

        self.content = None
        self.msg_type = POST_DATA_MSG_TYPE_TEXT

    def build_xml_tree(self):
        etree = super(TextReplyData, self).build_xml_tree()
        write_cdata_text_child(etree.getroot(), POST_DATA_TAG_NAME_CONTENT, self.content)
        return etree

class ImageReplyData(BaseReplyData):
    """docstring for ImageReplyData"""
    def __init__(self, request):
        super(ImageReplyData, self).__init__(request)
        self.media_id = None
        self.msg_type = POST_DATA_MSG_TYPE_IMAGE

    def build_xml_tree(self):
        etree = super(ImageReplyData, self).build_xml_tree()
        image_element = get_new_element(POST_DATA_TAG_NAME_IMAGE)
        write_cdata_text_child(image_element, POST_DATA_TAG_NAME_MEDIA_ID, self.media_id)
        etree.getroot().append(image_element)
        return etree

class VoiceReplyData(BaseReplyData):
    """docstring for ImageReplyData"""
    def __init__(self, request):
        super(VoiceReplyData, self).__init__(request)
        self.media_id = None
        self.msg_type = POST_DATA_MSG_TYPE_VOICE

    def build_xml_tree(self):
        etree = super(VoiceReplyData, self).build_xml_tree()
        voice_element = get_new_element(POST_DATA_TAG_NAME_VOICE)
        write_cdata_text_child(voice_element, POST_DATA_TAG_NAME_MEDIA_ID, self.media_id)
        etree.getroot().append(voice_element)
        return etree

class VideoReplyData(BaseReplyData):
    """docstring for ImageReplyData"""
    def __init__(self, request):
        super(VideoReplyData, self).__init__(request)
        self.media_id = None
        self.title = None
        self.description = None
        self.msg_type = POST_DATA_MSG_TYPE_VIDEO

    def build_xml_tree(self):
        etree = super(VideoReplyData, self).build_xml_tree()
        video_element = get_new_element(POST_DATA_TAG_NAME_VIDEO)
        write_cdata_text_child(video_element, POST_DATA_TAG_NAME_MEDIA_ID, self.media_id)
        write_cdata_text_child(video_element, POST_DATA_TAG_NAME_TITLE, self.title)
        write_cdata_text_child(video_element, POST_DATA_TAG_NAME_DESCRIPTION, self.description)
        etree.getroot().append(video_element)
        return etree

class MusicReplyData(BaseReplyData):
    """docstring for MusicReplyData"""
    def __init__(self, request):
        super(MusicReplyData, self).__init__(request)
        self.music_url = None
        self.hq_music_url = None
        self.thumb_media_id = None
        self.media_id = None
        self.title = None
        self.description = None
        self.msg_type = POST_DATA_MSG_TYPE_VIDEO

    def build_xml_tree(self):
        etree = super(MusicReplyData, self).build_xml_tree()
        music_element = get_new_element(POST_DATA_TAG_NAME_MUSIC)
        write_cdata_text_child(music_element, POST_DATA_TAG_NAME_MUSIC_URL, self.music_url)
        write_cdata_text_child(music_element, POST_DATA_TAG_NAME_HQ_MUSIC_URL, self.hq_music_url)
        write_cdata_text_child(music_element, POST_DATA_TAG_NAME_THUMB_MEDIA_ID, self.thumb_media_id)
        write_cdata_text_child(music_element, POST_DATA_TAG_NAME_MEDIA_ID, self.media_id)
        write_cdata_text_child(music_element, POST_DATA_TAG_NAME_TITLE, self.title)
        write_cdata_text_child(music_element, POST_DATA_TAG_NAME_DESCRIPTION, self.description)
        etree.getroot().append(music_element)
        return etree


class NewsReplyData(BaseReplyData):
    """docstring for NewsReplyData"""
    def __init__(self, request):
        super(NewsReplyData, self).__init__(request)
        self.article_list = []
        self.msg_type = POST_DATA_MSG_TYPE_NEWS

    def build_xml_tree(self):
        etree = super(NewsReplyData, self).build_xml_tree()
        write_text_child(etree.getroot(), POST_DATA_TAG_NAME_ARTICLE_COUNT, str(len(self.article_list)))
        articles_element = get_new_element(POST_DATA_TAG_NAME_ARTICLES)
        article_item_list = self.__build_articles_element_list()
        for item in article_item_list:
            articles_element.append(item)
        etree.getroot().append(articles_element)
        return etree

    def set_article_item(self, title, description, pic_url, url):
        article = {
                    POST_DATA_TAG_NAME_TITLE : title,
                    POST_DATA_TAG_NAME_DESCRIPTION : description,
                    POST_DATA_TAG_NAME_PIC_URL : pic_url,
                    POST_DATA_TAG_NAME_URL : url,
        }
        self.article_list.append(article)

    def __build_articles_element_list(self):
        result = []
        for article in self.article_list:
            element = self.__build_article_element(article)
            if element is not None:
                result.append(element)
        return result

    def __build_article_element(self, article):
        if not article:
            return None
        element = get_new_element(POST_DATA_TAG_NAME_ITEM)
        for key, value in article.items():
            write_cdata_text_child(element, key, value)

        return element
