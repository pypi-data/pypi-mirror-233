from setuptools import setup, find_packages

setup(
    name="mkdocs-auto-i18n",
    version="0.1.1",
    description="A plugin for MkDocs that automatically translates documentation pages and allows users to switch languages.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Power Lin",
    author_email="linyuxuanlin@outlook.com",
    url="https://github.com/linyuxuanlin/mkdocs-auto-i18n",
    packages=find_packages(),
    install_requires=[
        "mkdocs>=1.1",
        "openai>=0.11.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
    ],
)