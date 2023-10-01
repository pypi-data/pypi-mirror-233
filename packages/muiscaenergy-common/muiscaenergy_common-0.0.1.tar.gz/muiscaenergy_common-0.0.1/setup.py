from setuptools import setup, find_packages
import os
import re
import codecs

# python setup.py sdist bdist_wheel
# https://pypi.org/project/muisca1492-commom

NAME = 'common'
META_PATH = os.path.join(NAME, '__init__.py')
REQUIREMENTS = []
CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3.8',
]
HERE = os.path.abspath(os.path.dirname(__file__))

# extract meta-data from __init__.py
# lee the file and extract the meta-data
def read(*parts):
    """
    Build an absolute path from *parts* and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    :param parts:
    """
    with codecs.open(os.path.join(HERE, *parts), 'r') as fp:
        return fp.read()

META_FILE = read(META_PATH)

def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    :param meta:
    """
    # extract __*meta*__ from META_FILE
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(f"Unable to find __{meta}__ string.".format(meta=meta))


if __name__ == '__main__':
    setup(
        name=find_meta('title'),
        version=find_meta('version'),
        url=find_meta('url'),
        author=find_meta('author'),
        emai=find_meta('email'),
        description=find_meta('description'),
        license=find_meta('license'),
        long_description=open('README.md').read(),
        packages=find_packages(),
        zip_safe=False,
        install_requires=['timezonefinder >= 6.2.0',
                          'pandas >= 1.5.3',
                          ],
        extras_require={
            'dev': ["pytest >= 7.0",
                    "twine >= 4.0.2",
                    ],
        },
        python_requires='>=3.10',
    )
