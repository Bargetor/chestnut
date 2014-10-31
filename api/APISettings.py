GET_DATA_NAME_ACCESS_TOKEN = "access_token"

POST_DATA_TAG_NAME_MSG_TYPE = 'MsgType'
POST_DATA_TAG_NAME_TO_USER_NAME = 'ToUserName'
POST_DATA_TAG_NAME_FROM_USER_NAME = 'FromUserName'
POST_DATA_TAG_NAME_CREATE_TIME = 'CreateTime'
POST_DATA_TAG_NAME_MSG_ID = 'MsgId'
POST_DATA_TAG_NAME_CONTENT = 'Content'
POST_DATA_TAG_NAME_PIC_URL = 'PicUrl'
POST_DATA_TAG_NAME_IMAGE = 'Image'
POST_DATA_TAG_NAME_MEDIA_ID = 'MediaId'
POST_DATA_TAG_NAME_VOICE = 'Voice'
POST_DATA_TAG_NAME_VIDEO = 'Video'
POST_DATA_TAG_NAME_MUSIC = 'Music'
POST_DATA_TAG_NAME_MUSIC_URL = 'MusicUrl'
POST_DATA_TAG_NAME_HQ_MUSIC_URL = 'HQMusicUrl'
POST_DATA_TAG_NAME_FORMAT = 'Format'
POST_DATA_TAG_NAME_THUMB_MEDIA_ID = 'ThumbMediaId'
POST_DATA_TAG_NAME_LOCATION_X = 'Location_X'
POST_DATA_TAG_NAME_LOCATION_Y = 'Location_Y'
POST_DATA_TAG_NAME_LABEL = 'Label'
POST_DATA_TAG_NAME_SCALE = 'Scale'
POST_DATA_TAG_NAME_TITLE = 'Title'
POST_DATA_TAG_NAME_DESCRIPTION = 'Description'
POST_DATA_TAG_NAME_URL = 'Url'
POST_DATA_TAG_NAME_EVENT = 'Event'
POST_DATA_TAG_NAME_EVENT_KEY = 'EventKey'
POST_DATA_TAG_NAME_TICKET = 'Ticket'
POST_DATA_TAG_NAME_ARTICLE_COUNT = 'ArticleCount'
POST_DATA_TAG_NAME_ARTICLES = 'Articles'
POST_DATA_TAG_NAME_ITEM = 'item'
POST_DATA_TAG_NAME_LATITUDE = 'Latitude'
POST_DATA_TAG_NAME_LONGITUDE = 'Longitude'
POST_DATA_TAG_NAME_PRECISION = 'Precision'


REPLY_DATA_JSON_TAG_NAME_TO_USER_NAME = 'touser'
REPLY_DATA_JSON_TAG_NAME_MSG_TYPE = 'msgtype'
REPLY_DATA_JSON_TAG_NAME_TEXT = 'text'
REPLY_DATA_JSON_TAG_NAME_CONTENT = 'content'
REPLY_DATA_JSON_TAG_NAME_IMAGE = 'image'
REPLY_DATA_JSON_TAG_NAME_MEDIA_ID = 'media_id'
REPLY_DATA_JSON_TAG_NAME_VOICE = 'image'
REPLY_DATA_JSON_TAG_NAME_VIDEO = 'video'
REPLY_DATA_JSON_TAG_NAME_TITLE = 'title'
REPLY_DATA_JSON_TAG_NAME_DESCTIPTION = 'description'
REPLY_DATA_JSON_TAG_NAME_THUMB_MEIDA_ID = 'thumb_media_id'
REPLY_DATA_JSON_TAG_NAME_MUSIC = 'music'
REPLY_DATA_JSON_TAG_NAME_MUSIC_URL = 'musicurl'
REPLY_DATA_JSON_TAG_NAME_HQ_MUSIC_URL = 'hqmusicurl'
REPLY_DATA_JSON_TAG_NAME_NEWS = 'title'
REPLY_DATA_JSON_TAG_NAME_ARTICLES = 'articles'
REPLY_DATA_JSON_TAG_NAME_URL = 'url'
REPLY_DATA_JSON_TAG_NAME_PIC_URL = 'picurl'



POST_DATA_MSG_TYPE_TEXT = 'text'
POST_DATA_MSG_TYPE_IMAGE = 'image'
POST_DATA_MSG_TYPE_VOICE = 'voice'
POST_DATA_MSG_TYPE_VIDEO = 'video'
POST_DATA_MSG_TYPE_LOCATION = 'location'
POST_DATA_MSG_TYPE_LINK = 'link'
POST_DATA_MSG_TYPE_EVENT = 'event'
POST_DATA_MSG_TYPE_MUSIC = 'music'
POST_DATA_MSG_TYPE_NEWS = 'news'

POST_DATA_EVENT_TYPE_SUBSCRIBE = 'subscribe'
POST_DATA_EVENT_TYPE_UNSUBSCRIBE = 'unsubscribe'

REQUEST_PARSER_CONFIG_NAME = 'parser'
REQUEST_RESPONSER_CONFIG_NAME = 'responser'
REQUEST_LISTENER_CONFIG_NAME = 'listener'

request_processer_list = [
                            {REQUEST_PARSER_CONFIG_NAME:"api.src.APIParser.SignatureRequestParser",
                             REQUEST_RESPONSER_CONFIG_NAME:"api.src.APIResponse.SignatureAPIResponse",
                             REQUEST_LISTENER_CONFIG_NAME:[
                                "",
                             ]},

                             {REQUEST_PARSER_CONFIG_NAME:"api.src.APIParser.MessageRequestParser",
                              REQUEST_RESPONSER_CONFIG_NAME:"api.src.APIResponse.MessageAPIResponse",
                              REQUEST_LISTENER_CONFIG_NAME:[
                                 "chestnut.src.ChestnutAPI.ChestnutWeChatTextMessageAPIListener",
                             ]},
                             {REQUEST_PARSER_CONFIG_NAME:"api.src.APIParser.EventRequestParser",
                              REQUEST_RESPONSER_CONFIG_NAME:"api.src.APIResponse.EventAPIResponse",
                              REQUEST_LISTENER_CONFIG_NAME:[
                                 "",
                             ]},
                             {REQUEST_PARSER_CONFIG_NAME:"chestnut.src.ChestnutAPI.ChestnutAPIParser",
                              REQUEST_RESPONSER_CONFIG_NAME:"chestnut.src.ChestnutAPI.ChestnutAPIResponse",
                              REQUEST_LISTENER_CONFIG_NAME:[
                                 "",
                             ]},
                          ]


CHARSET = 'utf-8'

MY_WECHAT_TOKEN = 'bargetor_chestnut'
