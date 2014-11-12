from chestnut.src.wechat.Wechat import Wechat

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
        return self._wechat_set.get(username)

    def build_wechat(self, username, password):
        if not username or not password : return None
        wechat = self.get_wechat(username)
        if wechat is not None : return wechat

        wechat = Wechat(username, password)
        self.__refresh_wechat(wechat)
        self._wechat_set[username] = wechat
        return wechat

    def __refresh_wechat(self, wechat):
        if not wechat: return
        wechat.wechat_auto_login()
        wechat.request_user_setting_page()
