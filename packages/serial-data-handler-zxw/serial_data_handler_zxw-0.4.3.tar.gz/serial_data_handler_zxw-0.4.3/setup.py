"""
# File       : setup.py
# Time       ：2023/9/25 16:54
# Author     ：xuewei zhang
# Email      ：jingmu_predict@qq.com
# version    ：python 3.8
# Description：
"""
from setuptools import setup, find_packages

setup(
    name='serial_data_handler_zxw',
    version='0.4.3',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'tqdm',
        'torch'
    ],
    author='xuewei zhang',
    author_email='jingmu_predict@qq.com',
    description='人工智能_量化交易_金融数据预处理',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
