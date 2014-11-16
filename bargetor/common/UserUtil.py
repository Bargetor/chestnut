from django.contrib.auth.models import User

def create_normal_django_user(username, password):
    user = User()
    user.username = username
    user.set_password(password)
    user.is_staff = False
    user.is_superuser = False
    user.is_active = True

    user.save()

def get_django_user_by_username(username):
    users = User.objects.filter(username = username)
    if len(users) >= 1 :
        return users[0]
    return None

def reset_django_user_password(username_or_user, password):
    if username_or_user is None: return

    user = None
    if isinstance(username_or_user, User):
        user = username_or_user
    elif isinstance(username_or_user, str):
        user = get_django_user_by_username(username = username_or_user)

    if not user: return

    user.set_password(password)
    user.save()
