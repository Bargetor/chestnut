REQUEST_PARSER_CONFIG_NAME = 'parser'
REQUEST_RESPONSER_CONFIG_NAME = 'responser'
REQUEST_LISTENER_CONFIG_NAME = 'listener'

request_processer_list = [
                            {REQUEST_PARSER_CONFIG_NAME:"bargetor.wechat.WechatAPIParser.SignatureRequestParser",
                             REQUEST_RESPONSER_CONFIG_NAME:"bargetor.wechat.WechatAPIResponse.SignatureAPIResponse",
                             REQUEST_LISTENER_CONFIG_NAME:[
                                "",
                             ]},

                             {REQUEST_PARSER_CONFIG_NAME:"bargetor.wechat.WechatAPIParser.MessageRequestParser",
                              REQUEST_RESPONSER_CONFIG_NAME:"chestnut.src.ChestnutAPI.ChestnutWeChatMessageAPIResponse",
                              REQUEST_LISTENER_CONFIG_NAME:[
                                 "chestnut.src.ChestnutAPI.ChestnutWeChatTextMessageAPIListener",
                             ]},
                             {REQUEST_PARSER_CONFIG_NAME:"bargetor.wechat.WechatAPIParser.EventRequestParser",
                              REQUEST_RESPONSER_CONFIG_NAME:"bargetor.api.src.APIResponse.EventAPIResponse",
                              REQUEST_LISTENER_CONFIG_NAME:[
                                 "",
                             ]},
                             {REQUEST_PARSER_CONFIG_NAME:"chestnut.src.ChestnutAPI.ChestnutAPIParser",
                              REQUEST_RESPONSER_CONFIG_NAME:"chestnut.src.ChestnutAPI.ChestnutAPIResponse",
                              REQUEST_LISTENER_CONFIG_NAME:[
                                 "",
                             ]},
                             {REQUEST_PARSER_CONFIG_NAME:"chestnut.src.ChestnutAPI.ChestnutSignupAPIParser",
                              REQUEST_RESPONSER_CONFIG_NAME:"chestnut.src.ChestnutAPI.ChestnutSignupAPIResponse",
                              REQUEST_LISTENER_CONFIG_NAME:[
                                 "",
                             ]},
                          ]


CHARSET = 'utf-8'

MY_WECHAT_TOKEN = 'bargetor_chestnut'
