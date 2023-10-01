# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page
from mkdocs.utils import warning_filter
import openai


class TranslationPlugin(BasePlugin):
    name = "mkdocs_auto_i18n"
    config_scheme = (
        ("api_key", config_options.Type(str)),
        ("max_length", config_options.Type(int, default=1000)),
        ("languages", config_options.Type(dict, default={})),
    )

    def __init__(self):
        super().__init__()
        self.api_key = None
        self.max_length = None
        self.languages = None

    def on_config(self, config, **kwargs):
        self.api_key = self.config["api_key"]
        self.max_length = self.config["max_length"]
        self.languages = self.config["languages"]

        # 设置OpenAI API Key和API Base
        openai.api_key = self.api_key
        openai.api_base = "https://api.chatanywhere.com.cn/v1"

        return config

    def on_pre_build(self, **kwargs):
        # 遍历docs目录下的所有.md文件，并翻译为指定语言
        for filename in os.listdir("./docs"):
            if filename.endswith(".md"):
                input_file = os.path.join("./docs", filename)
                for language, folder in self.languages.items():
                    output_file = os.path.join("./docs", folder, filename)
                    self.translate_file(input_file, output_file, language)

        # 将翻译后的文件添加到mkdocs的Page对象中
        for language, folder in self.languages.items():
            for root, dirs, files in os.walk(os.path.join("./docs", folder)):
                for filename in files:
                    if filename.endswith(".md"):
                        file_path = os.path.join(root, filename)
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            page = Page(
                                title=filename[:-3],
                                file=File(
                                    os.path.relpath(file_path, "./docs"),
                                    file_path,
                                    config=self.config,
                                ),
                                content=content,
                                url=self.get_url(language, filename),
                                is_homepage=False,
                                config=self.config,
                            )
                            config_pages = self.config["pages"]
                            if page.file.src_path not in [
                                p.file.src_path for p in config_pages
                            ]:
                                config_pages.append(page)

        return kwargs

    def on_page_markdown(self, markdown, page, **kwargs):
        language = page.url.split("/")[1]
        if language in self.languages:
            # 将当前语言的翻译文件路径替换为原始文件路径
            filename = os.path.basename(page.file.src_path)
            original_path = os.path.join("./docs", filename)
            translated_path = os.path.join(
                "./docs", self.languages[language], filename
            )
            markdown = markdown.replace(translated_path, original_path)

        return markdown

    def get_url(self, language, filename):
        if language == "en":
            return "/" + filename
        else:
            return "/" + language + "/" + filename

    def translate_file(self, input_file, output_file, language):
        # 读取输入文件内容
        with open(input_file, "r", encoding="utf-8") as f:
            input_text = f.read()

        # 拆分文章
        paragraphs = input_text.split("\n\n")
        input_text = ""
        output_paragraphs = []
        current_paragraph = ""

        for paragraph in paragraphs:
            if len(current_paragraph) + len(paragraph) + 2 <= self.max_length:
                # 如果当前段落加上新段落的长度不超过最大长度，就将它们合并
                if current_paragraph:
                    current_paragraph += "\n\n"
                current_paragraph += paragraph
            else:
                # 否则翻译当前段落，并将翻译结果添加到输出列表中
                output_paragraphs.append(
                    self.translate_text(current_paragraph, language)
                )
                current_paragraph = paragraph

        # 处理最后一个段落
        if current_paragraph:
            if len(current_paragraph) + len(input_text) <= self.max_length:
                # 如果当前段落加上之前的文本长度不超过最大长度，就将它们合并
                input_text += "\n\n" + current_paragraph
            else:
                # 否则翻译当前段落，并将翻译结果添加到输出列表中
                output_paragraphs.append(
                    self.translate_text(current_paragraph, language)
                )

        # 如果还有未翻译的文本，就将它们添加到输出列表中
        if input_text:
            output_paragraphs.append(self.translate_text(input_text, language))

        # 将输出段落合并为字符串
        output_text = "\n\n".join(output_paragraphs)

        # 写入输出文件
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output_text)

    def translate_text(self, text, language):
        # 使用OpenAI API进行翻译
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Translate the following Chinese article into {language}, and maintain the original markdown format.\n\n{text}\n\n{language}:",
                }
            ],
        )

        # 获取翻译结果
        output_text = completion.choices[0].message.content

        return output_text
