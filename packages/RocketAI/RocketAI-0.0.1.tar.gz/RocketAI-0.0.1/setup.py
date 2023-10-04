from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'RocketAI'
LONG_DESCRIPTION = 'PixelVerseIT RocketAI Python Package'

# Setting up
setup(
    name="RocketAI",
    version=VERSION,
    author="PixelVerseIT",
    author_email="<contact@pixelverse.tech>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['google.generativeai', 'time'],
    keywords=['python', 'AI', 'pixelverseit', 'simple ai', 'smart ai', 'artifiical intelligence'],
    classifiers=[
        "Development Status :: 4 - Beta ",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)