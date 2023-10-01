import codecs
import os

from setuptools import find_packages, setup



with open("README.md") as f:
    long_description = "\n" + f.read()

# with open("./requirements.txt") as f:
#     required = f.read().splitlines()

required = """
requests
pycryptodome
curl_cffi
aiohttp
certifi
browser_cookie3
websockets
js2py
flask
flask-cors
typing-extensions
PyExecJS"""


VERSION = '0.4'
DESCRIPTION = (
    "tui gpt"
)

# Setting up
setup(
    name="tuigpt",
    version=VERSION,
    author="chesnok",
    description=DESCRIPTION,
    author_email='ChesnokovP1107@yandex.ru',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    data_files=["tuigpt/main.py"],
    install_requires=required,
    entry_points={
        "console_scripts": ["tuigpt=main:main"],
    },
    url="https://github.com/chesnokpeter/tuigpt",  # Link to your GitHub repository
    project_urls={
        "Source Code": "https://github.com/chesnokpeter/tuigpt",  # GitHub link
    },
    keywords=[
        "python",
        "chatbot",
        "reverse-engineering",
        "openai",
        "chatbots",
        "gpt",
        "language-model",
        "gpt-3",
        "gpt3",
        "openai-api",
        "gpt-4",
        "gpt4",
        "chatgpt",
        "chatgpt-api",
        "openai-chatgpt",
        "chatgpt-free",
        "chatgpt-4",
        "chatgpt4",
        "chatgpt4-api",
        "free",
        "free-gpt",
        "gpt4free",
        "g4f",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
)
