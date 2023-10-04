from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.3.0'
DESCRIPTION = 'Template for discord.py bots'
LONG_DESCRIPTION = 'A package that allows users to build simple discord.py bots with configurations and environmental setup.'

setup(
    name="botipy",
    version=VERSION,
    author="Pang Hua Yen",
    author_email="<panghua.yen@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    package_data={
        'botipy': ['src/*'],
    },
    install_requires=['virtualenv', 'discord', 'flask', 'gunicorn', 'python-dotenv'],
    keywords=['python', 'discord', 'bot', 'discord.py', 'discord bot'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': [
            'botipy = botipy.cli:main',
        ]
    }
)