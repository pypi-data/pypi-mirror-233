# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

from django.conf import settings

# Choices are: "semantic", "bootstrap"
MARTOR_THEME = getattr(settings, 'MARTOR_THEME', 'semantic')

# Global martor_markdown_plus.settings
# Input: string boolean, `true/false`
MARTOR_ENABLE_CONFIGS = getattr(
    settings, 'MARTOR_ENABLE_CONFIGS', {
        'emoji': 'true',  # enable/disable emoji icons.
        'imgur': 'true',  # enable/disable imgur/custom uploader.
        'mention': 'false',  # enable/disable mention
        'jquery': 'true',  # include/revoke jquery (require for admin django)
        'living': 'false',  # enable/disable live updates in preview
        'spellcheck': 'false',  # enable/disable spellcheck in form textareas
        'hljs': 'true',  # enable/disable hljs highlighting in preview
    }
)

# To show the toolbar buttons
MARTOR_TOOLBAR_BUTTONS = getattr(
    settings, 'MARTOR_TOOLBAR_BUTTONS', [
        'bold', 'italic', 'horizontal', 'heading', 'pre-code', 'admonition', 'table',
        'blockquote', 'unordered-list', 'ordered-list',
        'link', 'image-link', 'image-upload', 'emoji',
        'direct-mention', 'toggle-maximize', 'help'
    ]
)

# To setup the martor_markdown_plus.editor with title label or not (default is False)
MARTOR_ENABLE_LABEL = getattr(
    settings, 'MARTOR_ENABLE_LABEL', False
)

# Imgur API Keys
MARTOR_IMGUR_CLIENT_ID = getattr(
    settings, 'MARTOR_IMGUR_CLIENT_ID', ''
)
MARTOR_IMGUR_API_KEY = getattr(
    settings, 'MARTOR_IMGUR_API_KEY', ''
)

# Markdownify
MARTOR_MARKDOWNIFY_FUNCTION = getattr(
    settings, 'MARTOR_MARKDOWNIFY_FUNCTION', 'martor_markdown_plus.utils.markdownify'
)
MARTOR_MARKDOWNIFY_URL = getattr(
    settings, 'MARTOR_MARKDOWNIFY_URL', '/martor_markdown_plus/markdownify/'
)

# Custom images upload path
MARTOR_UPLOAD_PATH = 'images/uploads/{}'.format(time.strftime("%Y/%m/%d/"))
# Maximum Upload Image
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_IMAGE_UPLOAD_SIZE = 5242880  # 5MB
# Media Path
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/carlos/DEV/promedevusdep/media/'

# Markdown extensions
MARTOR_MARKDOWN_EXTENSIONS = getattr(
    settings, 'MARTOR_MARKDOWN_EXTENSIONS', [
        'markdown.extensions.extra',
        'markdown.extensions.nl2br',
        'markdown.extensions.smarty',
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',

        # Custom markdown extensions.
        'markdown.extensions.admonition',
        'martor_markdown_plus.extensions.urlize',
        'martor_markdown_plus.extensions.del_ins',  # ~~strikethrough~~ and ++underscores++
        'martor_markdown_plus.extensions.mention',  # to parse markdown mention
        'martor_markdown_plus.extensions.emoji',  # to parse markdown emoji
        'martor_markdown_plus.extensions.mdx_video',  # to parse embed/iframe video
        'martor_markdown_plus.extensions.escape_html',  # to handle the XSS vulnerabilities
    ]
)

# Markdown Extensions Configs
MARTOR_MARKDOWN_EXTENSION_CONFIGS = getattr(
        settings, 'MARTOR_MARKDOWN_EXTENSION_CONFIGS', { 'markdown.extensions.codehilite': {'linenums': True}}
)

# Markdown urls
MARTOR_UPLOAD_URL = getattr(
    settings, 'MARTOR_UPLOAD_URL',
    '/martor_markdown_plus/local_uploader/'  # for imgur
)
MARTOR_SEARCH_USERS_URL = getattr(
    settings, 'MARTOR_SEARCH_USERS_URL',
    '/martor_markdown_plus.search-user/'  # for mention
)

# Markdown Extensions
MARTOR_MARKDOWN_BASE_EMOJI_URL = getattr(
    settings, 'MARTOR_MARKDOWN_BASE_EMOJI_URL',
    'https://github.githubassets.com/images/icons/emoji/'
)

MARTOR_MARKDOWN_BASE_MENTION_URL = getattr(
    settings, 'MARTOR_MARKDOWN_BASE_MENTION_URL',
    'https://python.web.id/author/'
)

# If you need to use your own themed "bootstrap" or "semantic ui" dependency
# replace the values with the file in your static files dir
MARTOR_ALTERNATIVE_JS_FILE_THEME = getattr(
    settings, 'MARTOR_ALTERNATIVE_JS_FILE_THEME', None
)
MARTOR_ALTERNATIVE_CSS_FILE_THEME = getattr(
    settings, 'MARTOR_ALTERNATIVE_CSS_FILE_THEME', None
)
MARTOR_ALTERNATIVE_JQUERY_JS_FILE = getattr(
    settings, 'MARTOR_ALTERNATIVE_JQUERY_JS_FILE', None
)
