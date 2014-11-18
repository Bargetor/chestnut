#-*- coding: utf-8 -*-
#客户请求与被动消息响应属于两个应用场景，但属于同等数据结构
import time
from bargetor.common.XMLUtil import *
from bargetor.wechat.WechatConstant import *
from bargetor.common.JsonUtil import JsonObject

class BaseReplyData(object):
    """docstring for BaseReplyData"""
    def __init__(self, to_user_name = None):
        super(BaseReplyData, self).__init__()
        self._init_reply_data()

        self.to_user_name = to_user_name

    def __init__(self, request):
        super(BaseReplyData, self).__init__()
        self._init_reply_data()

        self.to_user_name = request.from_user_name
        self.from_user_name = request.to_user_name
        self.create_time = str(time.time())


    def _init_reply_data(self):
        self.to_user_name = None
        self.from_user_name = None
        self.create_time = None
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

    def build_json_object(self):
        json = JsonObject()
        json.append(REPLY_DATA_JSON_TAG_NAME_TO_USER_NAME, self.to_user_name)
        json.append(REPLY_DATA_JSON_TAG_NAME_MSG_TYPE, self.msg_type)
        return json

    def get_json_str(self):
        json = self.build_json_object()
        return json.get_json_str()

class TextReplyData(BaseReplyData):
    """docstring for TextReplyData"""

    def _init_reply_data(self):
        self.content = None
        self.msg_type = POST_DATA_MSG_TYPE_TEXT

    def build_xml_tree(self):
        etree = super(TextReplyData, self).build_xml_tree()
        write_cdata_text_child(etree.getroot(), POST_DATA_TAG_NAME_CONTENT, self.content)
        return etree

    def build_json_object(self):
        json = super(TextReplyData, self).build_json_object()
        text_json = JsonObject()
        text_json.append(REPLY_DATA_JSON_TAG_NAME_CONTENT, self.content)
        json.append_chestnut_json(REPLY_DATA_JSON_TAG_NAME_TEXT, text_json)
        return json

class ImageReplyData(BaseReplyData):
    """docstring for ImageReplyData"""

    def _init_reply_data(self):
        self.media_id = None
        self.msg_type = POST_DATA_MSG_TYPE_IMAGE

    def build_xml_tree(self):
        etree = super(ImageReplyData, self).build_xml_tree()
        image_element = get_new_element(POST_DATA_TAG_NAME_IMAGE)
        write_cdata_text_child(image_element, POST_DATA_TAG_NAME_MEDIA_ID, self.media_id)
        etree.getroot().append(image_element)
        return etree

    def build_json_object(self):
        json = super(ImageReplyData, self).build_json_object()
        image_json = JsonObject()
        image_json.append(REPLY_DATA_JSON_TAG_NAME_MEDIA_ID, self.media_id)
        json.append_chestnut_json(REPLY_DATA_JSON_TAG_NAME_IMAGE, image_json)
        return json

class VoiceReplyData(BaseReplyData):
    """docstring for ImageReplyData"""

    def _init_reply_data(self):
        self.media_id = None
        self.msg_type = POST_DATA_MSG_TYPE_VOICE


    def build_xml_tree(self):
        etree = super(VoiceReplyData, self).build_xml_tree()
        voice_element = get_new_element(POST_DATA_TAG_NAME_VOICE)
        write_cdata_text_child(voice_element, POST_DATA_TAG_NAME_MEDIA_ID, self.media_id)
        etree.getroot().append(voice_element)
        return etree

    def build_json_object(self):
        json = super(VoiceReplyData, self).build_json_object()
        voice_json = JsonObject()
        voice_json.append(REPLY_DATA_JSON_TAG_NAME_MEDIA_ID, self.media_id)
        json.append_chestnut_json(REPLY_DATA_JSON_TAG_NAME_VOICE, voice_json)
        return json

class VideoReplyData(BaseReplyData):
    """docstring for VideoReplyData"""

    def _init_reply_data(self):
        self.media_id = None
        self.thumb_media_id = None
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

    def build_json_object(self):
        json = super(VideoReplyData, self).build_json_object()
        video_json = JsonObject()
        video_json.append(REPLY_DATA_JSON_TAG_NAME_MEDIA_ID, self.media_id)
        video_json.append(REPLY_DATA_JSON_TAG_NAME_THUMB_MEIDA_ID, self.thumb_media_id)
        video_json.append(REPLY_DATA_JSON_TAG_NAME_TITLE, self.title)
        video_json.append(REPLY_DATA_JSON_TAG_NAME_DESCTIPTION, self.description)
        json.append_chestnut_json(REPLY_DATA_JSON_TAG_NAME_VIDEO, video_json)
        return json

class MusicReplyData(BaseReplyData):
    """docstring for MusicReplyData"""

    def _init_reply_data(self):
        self.music_url = None
        self.hq_music_url = None
        self.thumb_media_id = None
        self.media_id = None
        self.title = None
        self.description = None
        self.msg_type = POST_DATA_MSG_TYPE_MUSIC

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

    def build_json_object(self):
        json = super(MusicReplyData, self).build_json_object()
        music_json = JsonObject()
        music_json.append(REPLY_DATA_JSON_TAG_NAME_MEDIA_ID, self.media_id)
        music_json.append(REPLY_DATA_JSON_TAG_NAME_THUMB_MEIDA_ID, self.thumb_media_id)
        music_json.append(REPLY_DATA_JSON_TAG_NAME_TITLE, self.title)
        music_json.append(REPLY_DATA_JSON_TAG_NAME_DESCTIPTION, self.description)
        music_json.append(REPLY_DATA_JSON_TAG_NAME_MUSIC_URL, self.music_url)
        music_json.append(REPLY_DATA_JSON_TAG_NAME_HQ_MUSIC_URL, self.hq_music_url)
        json.append_chestnut_json(REPLY_DATA_JSON_TAG_NAME_MUSIC, music_json)
        return json


class NewsReplyData(BaseReplyData):
    """docstring for NewsReplyData"""

    def _init_reply_data(self):
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

    def build_json_object(self):
        json = super(NewsReplyData, self).build_json_object()
        news_json = JsonObject()
        news_json.append(REPLY_DATA_JSON_TAG_NAME_ARTICLES, self.__build_articles_json_list())
        json.append_chestnut_json(REPLY_DATA_JSON_TAG_NAME_NEWS, news_json)
        return json

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

    def __build_articles_json_list(self):
        result = []
        for article in self.article_list:
            art = {}
            art[REPLY_DATA_JSON_TAG_NAME_TITLE] = article[POST_DATA_TAG_NAME_TITLE]
            art[REPLY_DATA_JSON_TAG_NAME_DESCTIPTION] = article[POST_DATA_TAG_NAME_DESCRIPTION]
            art[REPLY_DATA_JSON_TAG_NAME_PIC_URL] = article[POST_DATA_TAG_NAME_PIC_URL]
            art[REPLY_DATA_JSON_TAG_NAME_URL] = article[POST_DATA_TAG_NAME_URL]
            result.append(art)
        return result

    def __build_article_element(self, article):
        if not article:
            return None
        element = get_new_element(POST_DATA_TAG_NAME_ITEM)
        for key, value in article.items():
            write_cdata_text_child(element, key, value)

        return element
