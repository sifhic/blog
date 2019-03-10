from django.conf import settings
from django.contrib.auth.hashers import check_password

from django.contrib.auth import get_user_model

User  = get_user_model()

class SettingsBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$37vfsTPxkZ2N$5JCLjrA2WWPSnqP2oHul9JFswSvHeSOLGhxw9YL6p4E='
    """

    def authenticate(self, request, username=None, password=None):
        login_valid = (settings.ADMIN_LOGIN == username)
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        # TODO  account uses email as username field
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.

                user = User(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.email = 'admin@{}.com'.format(settings.PROJECT_NAME)
                user.save()

            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None