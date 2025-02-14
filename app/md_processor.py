from flask import url_for

from markdown.extensions import Extension
from markdown.inlinepatterns import ImageInlineProcessor, IMAGE_LINK_RE
import xml.etree.ElementTree as etree


class CustomImageInlineProcessor(ImageInlineProcessor):
    """自定义 Markdown 图片处理器"""

    def handleMatch(self, m, data):
        el = etree.Element("img")
        src = m.group(2)
        if src.startswith("/static/"):
            src = url_for('static', filename=src[8:])  # 将 /static/ 路径转换为 Flask 的静态文件 URL
        el.set("src", src)
        el.set("alt", m.group(1))
        return el, m.start(0), m.end(0)


class CustomMarkdownExtension(Extension):
    """自定义 Markdown 扩展"""

    def extendMarkdown(self, md):
        md.inlinePatterns.register(CustomImageInlineProcessor(IMAGE_LINK_RE, md), 'image', 150)
