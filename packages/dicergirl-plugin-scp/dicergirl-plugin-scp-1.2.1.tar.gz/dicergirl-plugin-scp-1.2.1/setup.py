import setuptools
import sys

from pathlib import Path

sys.path.append(str(Path("dicergirl").resolve() / "plugins"))

import scp

setuptools.setup(
    name='dicergirl-plugin-scp',
    version=scp.__version__,
    author = "Night Resurgent <fu050409@163.com>",
    author_email = "fu050409@163.com",
    description="Dicergirl SCP 模式插件",
    url='https://gitee.com/unvisitor/dicergirl-plugin-scp/',
    project_urls = {
        "Bug Tracker": "https://gitee.com/unvisitor/dicergirl-plugin-scp/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license = "Apache-2.0",
    packages = ['dicergirl.plugins.scp'],
    install_requires=[
        'dicergirl',
    ],
    python_requires=">=3",
)