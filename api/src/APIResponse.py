import hashlib
import time
from common import ArrayUtil
from api.APISettings import MY_WECHAT_TOKEN
from api.src.APIRequest import *
from common.XMLUtil import *
from api.APISettings import *
from api.src.ReplyData import *

class BaseAPIResponse(object):
    """docstring for BaseAPIResponse"""
    def __init__(self):
        super(BaseAPIResponse, self).__init__()

    def response(self, reqeust):
        return None

class SignatureAPIResponse(BaseAPIResponse):
    """docstring for SignatureAPIResponse"""
    def __init__(self):
        super(SignatureAPIResponse, self).__init__()

    def response(self, request):
        if not request:
            return super(SignatureAPIResponse, self).response(request)
        if self.__signature(MY_WECHAT_TOKEN, request.signature, request.timestamp, request.nonce, request.echostr):
            return request.echostr
        return None

    def __signature(self, token, signature, timestamp, nonce, echostr):
        if token is None or signature is None or timestamp is None or nonce is None or echostr is None:
            return False
        array = [token, timestamp, nonce]
        array.sort()
        splice_str =  ArrayUtil.str_array_splice(array)
        sha1= hashlib.sha1()
        sha1.update(splice_str)
        sha1_str = sha1.hexdigest()
        return sha1_str == signature

class MessageAPIResponse(BaseAPIResponse):
    """docstring for MessageAPIResponse"""
    def __init__(self):
        super(MessageAPIResponse, self).__init__()

    def response(self, request):
        if not request:
            return super(MessageAPIResponse, self).response(request)

        if isinstance(request, TextAPIRequest):
            response_data = TextReplyData(request)
            response_data.content = "hello, this's great system, it's called chestnut!"
            return response_data.get_json_str()

        if isinstance(request, PicAPIRequest):
            response_data = ImageReplyData(request)
            response_data.media_id = "media_id12345678"
            return response_data.get_json_str()

        if isinstance(request, VoiceAPIRequest):
            response_data = VoiceReplyData(request)
            response_data.media_id = "media_id12345678"
            return response_data.get_json_str()

        if isinstance(request, VideoAPIRequest):
            response_data = VideoReplyData(request)
            response_data.media_id = "media_id12345678"
            response_data.thumb_media_id = "thumb_media_id1234"
            response_data.title = "bargetor"
            response_data.description = "bargetor and chestnut"
            return response_data.get_json_str()

        if isinstance(request, LocationAPIRequest):
            response_data = NewsReplyData(request)
            response_data.set_article_item('article title', 'article description', 'pic url', 'url')
            response_data.set_article_item('article title', 'article description', 'pic url', 'url')
            return response_data.get_json_str()

        if isinstance(request, LinkAPIRequest):
            response_data = MusicReplyData(request)
            response_data.media_id = "media_id12345678"
            response_data.music_url = "music url"
            response_data.hq_music_url = "hq music url"
            response_data.thumb_media_id = "thumb_media_id"
            response_data.title = "music title"
            response_data.description = "music description"
            return response_data.get_json_str()

class EventAPIResponse(BaseAPIResponse):
    """docstring for EventAPIResponse"""
    def __init__(self):
        super(EventAPIResponse, self).__init__()

    def response(self, request):
        if not request:
            return super(EventAPIResponse, self).response(request)
        return request.event



# class BaseResponseXMLData(object):
#     """docstring for BaseResponseXMLData"""
#     def __init__(self, request):
#         super(BaseResponseXMLData, self).__init__()

#         self.to_user_name = request.from_user_name
#         self.from_user_name = request.to_user_name
#         self.create_time = str(time.time())
#         self.msg_type = None

#     def build_xml_tree(self):
#         etree = get_new_etree('xml')
#         write_cdata_text_child(etree.getroot(), POST_DATA_TAG_NAME_TO_USER_NAME, self.to_user_name)
#         write_cdata_text_child(etree.getroot(), POST_DATA_TAG_NAME_FROM_USER_NAME, self.from_user_name)
#         write_text_child(etree.getroot(), POST_DATA_TAG_NAME_CREATE_TIME, self.create_time)
#         write_cdata_text_child(etree.getroot(), POST_DATA_TAG_NAME_MSG_TYPE, self.msg_type)
#         return etree

#     def get_xml_str(self):
#         etree = self.build_xml_tree()
#         return to_etree_xml_str(etree)

# class TextResponseXMLData(BaseResponseXMLData):
#     """docstring for TextResponseXMLData"""
#     def __init__(self, request):
#         super(TextResponseXMLData, self).__init__(request)

#         self.content = None
#         self.msg_type = POST_DATA_MSG_TYPE_TEXT

#     def build_xml_tree(self):
#         etree = super(TextResponseXMLData, self).build_xml_tree()
#         write_cdata_text_child(etree.getroot(), POST_DATA_TAG_NAME_CONTENT, self.content)
#         return etree

# class ImageResponseXMLData(BaseResponseXMLData):
#     """docstring for ImageResponseXMLData"""
#     def __init__(self, request):
#         super(ImageResponseXMLData, self).__init__(request)
#         self.media_id = None
#         self.msg_type = POST_DATA_MSG_TYPE_IMAGE

#     def build_xml_tree(self):
#         etree = super(ImageResponseXMLData, self).build_xml_tree()
#         image_element = get_new_element(POST_DATA_TAG_NAME_IMAGE)
#         write_cdata_text_child(image_element, POST_DATA_TAG_NAME_MEDIA_ID, self.media_id)
#         etree.getroot().append(image_element)
#         return etree

# class VoiceResponseXMLData(BaseResponseXMLData):
#     """docstring for ImageResponseXMLData"""
#     def __init__(self, request):
#         super(VoiceResponseXMLData, self).__init__(request)
#         self.media_id = None
#         self.msg_type = POST_DATA_MSG_TYPE_VOICE

#     def build_xml_tree(self):
#         etree = super(VoiceResponseXMLData, self).build_xml_tree()
#         voice_element = get_new_element(POST_DATA_TAG_NAME_VOICE)
#         write_cdata_text_child(voice_element, POST_DATA_TAG_NAME_MEDIA_ID, self.media_id)
#         etree.getroot().append(voice_element)
#         return etree

# class VideoResponseXMLData(BaseResponseXMLData):
#     """docstring for ImageResponseXMLData"""
#     def __init__(self, request):
#         super(VideoResponseXMLData, self).__init__(request)
#         self.media_id = None
#         self.title = None
#         self.description = None
#         self.msg_type = POST_DATA_MSG_TYPE_VIDEO

#     def build_xml_tree(self):
#         etree = super(VideoResponseXMLData, self).build_xml_tree()
#         video_element = get_new_element(POST_DATA_TAG_NAME_VIDEO)
#         write_cdata_text_child(video_element, POST_DATA_TAG_NAME_MEDIA_ID, self.media_id)
#         write_cdata_text_child(video_element, POST_DATA_TAG_NAME_TITLE, self.title)
#         write_cdata_text_child(video_element, POST_DATA_TAG_NAME_DESCRIPTION, self.description)
#         etree.getroot().append(video_element)
#         return etree

# class MusicResponseXMLData(BaseResponseXMLData):
#     """docstring for MusicResponseXMLData"""
#     def __init__(self, request):
#         super(MusicResponseXMLData, self).__init__(request)
#         self.music_url = None
#         self.hq_music_url = None
#         self.thumb_media_id = None
#         self.media_id = None
#         self.title = None
#         self.description = None
#         self.msg_type = POST_DATA_MSG_TYPE_VIDEO

#     def build_xml_tree(self):
#         etree = super(MusicResponseXMLData, self).build_xml_tree()
#         music_element = get_new_element(POST_DATA_TAG_NAME_MUSIC)
#         write_cdata_text_child(music_element, POST_DATA_TAG_NAME_MUSIC_URL, self.music_url)
#         write_cdata_text_child(music_element, POST_DATA_TAG_NAME_HQ_MUSIC_URL, self.hq_music_url)
#         write_cdata_text_child(music_element, POST_DATA_TAG_NAME_THUMB_MEDIA_ID, self.thumb_media_id)
#         write_cdata_text_child(music_element, POST_DATA_TAG_NAME_MEDIA_ID, self.media_id)
#         write_cdata_text_child(music_element, POST_DATA_TAG_NAME_TITLE, self.title)
#         write_cdata_text_child(music_element, POST_DATA_TAG_NAME_DESCRIPTION, self.description)
#         etree.getroot().append(music_element)
#         return etree


# class NewsResponseXMLData(BaseResponseXMLData):
#     """docstring for NewsResponseXMLData"""
#     def __init__(self, request):
#         super(NewsResponseXMLData, self).__init__(request)
#         self.article_list = []
#         self.msg_type = POST_DATA_MSG_TYPE_NEWS

#     def build_xml_tree(self):
#         etree = super(NewsResponseXMLData, self).build_xml_tree()
#         write_text_child(etree.getroot(), POST_DATA_TAG_NAME_ARTICLE_COUNT, str(len(self.article_list)))
#         articles_element = get_new_element(POST_DATA_TAG_NAME_ARTICLES)
#         article_item_list = self.__build_articles_element_list()
#         for item in article_item_list:
#             articles_element.append(item)
#         etree.getroot().append(articles_element)
#         return etree

#     def set_article_item(self, title, description, pic_url, url):
#         article = {
#                     POST_DATA_TAG_NAME_TITLE : title,
#                     POST_DATA_TAG_NAME_DESCRIPTION : description,
#                     POST_DATA_TAG_NAME_PIC_URL : pic_url,
#                     POST_DATA_TAG_NAME_URL : url,
#         }
#         self.article_list.append(article)

#     def __build_articles_element_list(self):
#         result = []
#         for article in self.article_list:
#             element = self.__build_article_element(article)
#             if element is not None:
#                 result.append(element)
#         return result

#     def __build_article_element(self, article):
#         if not article:
#             return None
#         element = get_new_element(POST_DATA_TAG_NAME_ITEM)
#         for key, value in article.items():
#             write_cdata_text_child(element, key, value)

#         return element
