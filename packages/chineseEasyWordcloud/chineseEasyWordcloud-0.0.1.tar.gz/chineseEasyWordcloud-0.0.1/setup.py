# -*- coding: utf-8 -*-

from distutils.core import setup


setup(
    name='chineseEasyWordcloud',
    version = '0.0.1',
    keywords=['wordcloud', "jieba", "词云","中文","Chinese"],
    description='帮助初学者更轻松地制作中文词云。',
    long_description=open("./chineseEasyWordcloud/README.md",
                          "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author = 'kuankuan',
    author_email = '2163826131@qq.com',
    url="https://kuankuan2007.gitee.io/docs/docsPage/?name=chinese-easy-wordcloud",
    install_requires = [
        'wordcloud',
        "jieba",
        "doFolder"
    ],
    packages=['chineseEasyWordcloud', 'chineseEasyWordcloud/data'],
    
    license = 'Mulan PSL v2',
    platforms=[
        "windows",
        "linux",
        "macos"
    ] ,
    classifiers = [
        "Natural Language :: Chinese (Simplified)",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)'
    ],
    entry_points = {
        'console_scripts': [
            'chinese-wordcloud = chineseEasyWordcloud.terminal:chineseWordcloud',
        ],
    }
)
