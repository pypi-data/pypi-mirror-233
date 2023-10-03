#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Blacknon. All rights reserved.
# Use of this source code is governed by an MIT license
# that can be found in the LICENSE file.
# =======================================================


import sys
from distutils.sysconfig import get_python_lib
import os
import platform

import setuptools

cmdclass = {}
try:
    from sphinx.setup_command import BuildDoc
    cmdclass = {'build_sphinx': BuildDoc}
except ImportError:
    pass

try:
    with open('README.rst') as f:
        readme = f.read()
except IOError:
    readme = ''


# 補完ファイルインストール用関数
def get_data_files():

    # 補完ファイルのインストール先を取得する関数
    def get_completefile_install_location(shell):
        # pathのprefixを定義
        prefix = ''

        # osの種類を取得
        uname = platform.uname()[0]

        # 実行ユーザがrootかどうかでprefixを変更
        if os.geteuid() == 0:
            ''' システムインストール時の挙動 '''
            if uname == 'Linux' and shell == 'bash':
                prefix = '/'
            elif uname == 'Linux' and shell == 'zsh':
                prefix = '/usr/local'
            elif uname == 'Darwin' and shell == 'bash':
                prefix = '/'
            elif uname == 'Darwin' and shell == 'zsh':
                prefix = '/usr'

        # shellの種類に応じてインストール先のlocationを変更
        if shell == 'bash':
            location = os.path.join(prefix, 'etc/bash_completion.d')
        elif shell == 'zsh':
            location = os.path.join(prefix, 'share/zsh/site-functions')
        else:
            raise ValueError('unsupported shell: {0}'.format(shell))

        # locationを返す
        return location

    data_files = []

    # data_files形式でreturn
    return data_files


name = 'pywhois2'
version = '0.1.2'
release = '0.1.2'

if __name__ == "__main__":
    setuptools.setup(
        name=name,
        version=version,
        author='blacknon',
        author_email='blacknon@orebibou.com',
        maintainer='blacknon',
        maintainer_email='blacknon@orebibou.com',
        description='',
        long_description=readme,
        license='MIT License',
        install_requires=[
            "pyyaml",
            "ipaddress",
            "tld",
            "stringcase",
        ],
        url='https://github.com/blacknon/pywhois2',
        packages=setuptools.find_packages(),
        package_dir={"pywhois2": "pywhois2"},
        package_data={
            'pywhois2': [
                "data/*",
                "templates/*",
                "templates/cctld/*"
            ]
        },
        include_package_data=True,
        py_modules=['pywhois2'],
        entry_points={
            'console_scripts': [
                'whois2 = pywhois2:main',
            ],
        },
        classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'License :: OSI Approved :: MIT License',
        ],
        data_files=get_data_files(),
        cmdclass=cmdclass,
        command_options={
            'build_sphinx': {
                'project': ('setup.py', name),
                'version': ('setup.py', version),
                'release': ('setup.py', release)}},
        setup_requires=[
            "sphinx",
            "sphinx-rtd-theme",
            "sphinx-autobuild",
        ],
    )
