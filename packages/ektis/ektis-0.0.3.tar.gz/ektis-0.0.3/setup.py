from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ektis',
    version="0.0.3",
    description='이 프로젝트는 훅누와 플큐를 위한 모듈입니다',
    author='arin6145',
    author_email='help@hooknu.xyz',
    url='https://github.com/Arin6145/ektis',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['py-cord-dev[voice]', 'koreanbots', 'pymongo', 'pomice', 'Pillow', 'discord-cooldown', 'jsonly'],
    packages=find_packages(),
    keywords=['hooknu', 'timeelss', 'ektis', 'plq', 'fiter'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.11',
    ],
)