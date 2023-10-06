from django.conf import settings

settings.INSTALLED_APPS += [
    'baykeshop.common.AdminConfig',
    'baykeshop.apps.user',
    'baykeshop.apps.article',
    'baykeshop.apps.system',
    'baykeshop.apps.shop',
    'baykeshop.apps.stats',
    'rest_framework',
    'captcha',
    'tinymce',
]

TINYMCE_CONFIG = {
    'menubar': True,
    'relative_urls': False,
    'toolbar_sticky': False,
    'plugins_exclude': 'upgrade'  # 禁用升级插件
}