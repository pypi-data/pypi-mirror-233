# coding: utf-8
from os.path import abspath
from os.path import dirname
from os.path import join
import re

from pkg_resources import Requirement
from setuptools import find_packages
from setuptools import setup


_COMMENT_RE = re.compile(r'(^|\s)+#.*$')


def _get_requirements(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = _COMMENT_RE.sub('', line)
            line = line.strip()
            if line.startswith('-r '):
                for req in _get_requirements(
                    join(dirname(abspath(file_path)), line[3:])
                ):
                    yield req
            elif line:
                req = Requirement(line)
                req_str = req.name + str(req.specifier)
                if req.marker:
                    req_str += '; ' + str(req.marker)
                yield req_str


def main():
    setup(
        name='m3-data-import',
        author='БАРС Груп',
        author_email='dev@bars-open.ru',
        description='Пакет импорта данных - UI',
        classifiers=[
            'Intended Audience :: Developers',
            'Natural Language :: Russian',
            'Operating System :: OS Independent',
            'Framework :: Django :: 1.8',
            'Framework :: Django :: 1.9',
            'Framework :: Django :: 1.10',
            'Framework :: Django :: 1.11',
            'Framework :: Django :: 2.0',
            'Framework :: Django :: 2.1',
            'Framework :: Django :: 2.2',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation :: CPython',
            'Development Status :: 5 - Production/Stable',
            'Topic :: Software Development',
        ],
        package_dir={'': 'src'},
        packages=find_packages('src', exclude=('tests', 'tests.*')),
        include_package_data=True,
        dependency_links=(
            'https://pypi.bars-open.ru/simple/m3-builder',
        ),
        setup_requires=(
            'm3-builder>=1.2,<2',
        ),
        install_requires=tuple(_get_requirements('requirements/prod.txt')),
        set_build_info=join(dirname(__file__)),
    )


if __name__ == '__main__':
    main()
