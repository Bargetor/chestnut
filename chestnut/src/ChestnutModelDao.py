from chestnut.models import *

def get_chestnut_user(user_name):
    chestnut_user = None
    if user_name is not None:
        chestnut_user_list = ChestnutUser.objects.filter(user_name = user_name)
    if len(chestnut_user_list) == 1:
        chestnut_user = chestnut_user_list[0]

    return chestnut_user

def get_chestnut_user_for_wechat_default_id(user_wechat_default_id):
    chestnut_user = None
    if user_wechat_default_id is not None:
        chestnut_user_list = ChestnutUser.objects.filter(user_wechat_default_id = user_wechat_default_id)
    if len(chestnut_user_list) == 1:
        chestnut_user = chestnut_user_list[0]

    return chestnut_user

def get_post(chestnut_user, post_id):
    post = None
    if not chestnut_user:
        return post

    post_list = chestnut_user.chestnutshellpost_set.filter(post_id = post_id)
    if len(post_list) >= 1:
        post = post_list[0]
    return post

def get_post_list_for_wechat_default_id(user_wechat_default_id, count = -1):
    chestnut_user = get_chestnut_user_for_wechat_default_id(user_wechat_default_id)
    return get_post_list_for_user(chestnut_user, count)


def get_post_list_for_user_name(user_name, count = -1):
    chestnut_user = get_chestnut_user_for_user_name(user_wechat_id)
    return get_post_list_for_user(chestnut_user, count)

def get_post_list_for_user(chestnut_user, count = -1):
    if not chestnut_user:
        return
    if count > 0 :
        return chestnut_user.chestnutshellpost_set.order_by('-post_modified')
    else:
        return chestnut_user.chestnutshellpost_set.order_by('-post_modified')[0 : count]

def create_chestnut_user_for_request(request):
    user_name = request.chestnut_user
    user_wechat_default_id = request.chestnut_wechat_id
    user_wechat_token = request.chestnut_wechat_token
    user_password = request.chestnut_password
    chestnut_user = get_chestnut_user(user_name)
    return create_chestnut_user(user_name, user_password, user_wechat_default_id, user_wechat_token)

def create_chestnut_user(user_name, user_password, user_wechat_default_id, user_wechat_token):
    if not user_name or not user_password or not user_wechat_default_id : return
    chestnut_user = get_chestnut_user(user_name)
    if not chestnut_user:
        chestnut_user = ChestnutUser()
    chestnut_user.user_name = user_name
    chestnut_user.user_password = user_password
    chestnut_user.user_wechat_default_id = user_wechat_default_id
    chestnut_user.user_wechat_token = user_wechat_token

    chestnut_user.save()
    return chestnut_user

def save_post_for_request(chestnut_user, request):
    if not chestnut_user:
        return
    post = get_post(chestnut_user, request.post_id)
    if not post:
        post = ChestnutShellPost()
        post.chestnut_user = chestnut_user

    for key in post.__dict__:
        value = None
        try:
            value = getattr(request, key)
        except Exception, e:
            pass
        if value is not None:
            post.__dict__[key] = value

    print request

    post.save()
