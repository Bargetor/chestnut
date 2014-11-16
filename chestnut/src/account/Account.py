from bargetor.common import UserUtil
from chestnut.src import ChestnutModelDao

def signup(wechat_username, wechat_password, wechat_default_id, wecaht_token = None):
    ChestnutModelDao.create_chestnut_user(wechat_username, wechat_password, wechat_default_id, wecaht_token)

    django_user = UserUtil.get_django_user_by_username(wechat_username)
    if not django_user:
        UserUtil.create_normal_django_user(wechat_username, wechat_default_id)
