from bargetor.wechat.Wechat import Wechat

import logging

log = logging.getLogger(__name__)

class WechatCenter(object):
    """docstring for WechatCenter"""
    _instance = None

    _wechat_set = {}

    def __new__(clz, *args, **kwargs):
        if not clz._instance:
            clz._instance = super(WechatCenter, clz).__new__(clz, *args, **kwargs)
        return clz._instance

    def __init__(self):
        super(WechatCenter, self).__init__()

    def get_wechat(self, username):
        if not username: return None

        log_info = "get_wechat %s" % (username)
        log.info(log_info)

        return self._wechat_set.get(username)

    def build_wechat(self, username, password):
        if not username or not password : return None
        wechat = self.get_wechat(username)

        if wechat is not None and wechat.is_login(): return wechat
        if wechat is not None and not wechat.is_login():
            wechat.password = password
            self.__refresh_wechat(wechat)
            return wechat

        log_info = "build_wechat %s" % (username)
        log.info(log_info)

        wechat = Wechat(username, password)
        self.__refresh_wechat(wechat)
        self._wechat_set[username] = wechat
        return wechat

    def __refresh_wechat(self, wechat):
        if not wechat: return
        wechat.wechat_login()
        wechat.request_user_setting_page()
        # wechat.request_wechat_follower_page()
        # wechat.request_wechat_image_page()
        # wechat.request_wechat_dev_setting_page()
        wechat.request_create_app_msg()
        # app_msgs = wechat.request_get_app_msgs_list()
        # wechat.request_update_app_msg(app_msgs[0])


