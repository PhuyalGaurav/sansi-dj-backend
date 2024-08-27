import re

disallowed_usernames = ['admin', 'settings', 'static', 'media', 'images', 'img', 'javascript', 'js', 'css', 'accounts',
                        'users', 'user', 'login', 'logout', 'administrator', 'root', 'email', 'join', 'code', 'about',
                        'chat', 'profile', 'upload', 'uploads', 'adminarea', 'admincontrol', 'adminpanel', 'webmaster',
                        'website', 'websites', 'site', 'sites', 'support', 'portal', 'log', 'logs', 'gaurav', 'gauravphuyal']

username_regex = re.compile(r'^[a-zA-Z][a-zA-Z0-9_.]*$')


def username_validator(value):
    if value in disallowed_usernames:
        return False
    if not username_regex.match(value):
        return False
    return True
