class WechatAppMsg(object):
    """docstring for WechatAppMsg"""
    def __init__(self):
        self.app_msg_id = None
        self.create_time = -1
        self.update_time = -1
        self.items = []

    def add_app_msg_item_by_info(self, title, content, file_id, digest = None, author = None, source_url = None):
        if not title or not content or not file_id : return
        app_msg_item = WechatAppMsgItem()
        app_msg_item.title = title
        app_msg_item.content = content
        app_msg_item.file_id = file_id
        app_msg_item.digest = digest
        app_msg_item.author = author
        app_msg_item.source_url = source_url
        self.add_app_msg_item(app_msg_item)

    def add_app_msg_item(self, app_msg_item):
        if not app_msg_item : return
        if not isinstance(app_msg_item, WechatAppMsgItem) : return
        self.items.append(app_msg_item)

    def add_app_msg_items(self, app_msg_items):
        if not app_msg_items : return
        if isinstance(app_msg_items, list):
            for app_msg_item in app_msg_items:
                self.add_app_msg_item(app_msg_item)
        else:
            self.add_app_msg_item(app_msg_items)

    def remove_item_by_index(self, index):
        if len(self.items) - 1 >= index and index >= 0 :
            del self.items[index]

    def remove_item_by_seq(self, seq):
        for i in xrange(len(self.items)):
            item = self.items[i]
            if item.seq == seq:
                del self.items[i]
                break

    def remove_all_items(self):
        del self.items
        self.items = []


class WechatAppMsgItem(object):
    """docstring for WechatAppMsgItem"""
    def __init__(self):
        self.title = None
        self.content = None
        self.digest = None
        self.author = None
        self.file_id = None
        self.show_cover_pic = True
        self.source_url = None
        self.content_url = None
        self.img_url = None
        self.seq = -1

