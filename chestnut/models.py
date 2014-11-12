from django.db import models

class ChestnutUser(models.Model):
    """docstring for ChestnutUser"""
    user_name = models.CharField(max_length = 40, unique = True)
    user_wechat_default_id = models.CharField(max_length = 40, unique = True)
    user_wechat_id = models.CharField(max_length = 40, null = True)
    user_password = models.CharField(max_length = 128)
    user_wechat_token = models.CharField(max_length = 32, null = True)
    app_id = models.CharField(max_length = 40)
    app_secret = models.CharField(max_length = 40)
    create_time = models.DateTimeField(auto_now_add = True)
    modify_time = models.DateTimeField(auto_now = True)
    state = models.IntegerField(default = 0)
    user_email = models.TextField(null = True)
    display_name = models.TextField(null = True)
    user_mobile_number = models.TextField(null = True)


class ChestnutShellPost(models.Model):
    """docstring for ChestnutShellPost"""
    chestnut_user = models.ForeignKey(ChestnutUser)

    post_id = models.IntegerField()
    post_author = models.CharField(max_length = 40)
    post_date = models.DateTimeField(null = True)
    post_date_gmt = models.DateTimeField(null = True)
    post_content = models.TextField(null = True)
    post_title = models.TextField(null = True)
    post_excerpt = models.TextField(null = True)
    post_status = models.CharField(max_length = 10)
    comment_status = models.CharField(max_length = 10)
    ping_status = models.CharField(max_length = 10)
    post_password = models.CharField(max_length = 40)
    post_name = models.TextField(null = True)
    to_ping = models.TextField(null = True)
    pinged = models.TextField(null = True)
    post_modified = models.TextField(null = True)
    post_modified_gmt = models.TextField(null = True)
    post_content_filtered = models.TextField(null = True)
    post_parent = models.IntegerField(null = True)
    guid = models.TextField(null = True)
    menu_order = models.IntegerField(default = 0)
    post_type = models.CharField(max_length = 10)
    post_mime_type = models.CharField(max_length = 10)
    comment_count = models.IntegerField(default = 0)
    post_pic = models.TextField(null = True)
