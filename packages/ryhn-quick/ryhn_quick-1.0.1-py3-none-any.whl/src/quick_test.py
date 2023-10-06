# -*- coding: utf-8 -*- 
# @Time : 2023/9/28 0028 11:00 
# @Author : Ryhn
# @File : quick_test.py
import argparse
import multiprocessing
import os
import sys
import loguru
import pytest


def start_test(suites_url):
	"""
    启动测试框架
    """
	pytest.main(['-v', suites_url, '--disable-warnings'])


class multipool_map:
	"""
    关于进程池的实现类
    """

	def __init__(self, n):
		'''
        所需配置
        '''
		self.process = multiprocessing.Pool(processes=n)

	def __call__(self, fun, list, *args, **kwargs):
		'''
        类名实现方法
        :param args:
        :param kwargs:
        :return:
        '''
		self.process.map(func=fun, iterable=list)
		self.process.close()
		self.process.join()

# todo:命令行参数实例化
parser = argparse.ArgumentParser(description="ryhn")
# todo:命令行参数配置
parser.add_argument('--start', action='store', type=bool, default=False)
parser.add_argument('--num', action='store', type=int, default=1)
parser.add_argument('--url', action='store', type=str, default=None)
args = parser.parse_args()
# todo:命令行参数输入情况判断
if not args.start:
	loguru.logger.error("--start参数未开启，程序退出")
	sys.exit(0)
if not (path := args.url):
	loguru.logger.error("--url参数为None，程序退出")
	sys.exit(0)
# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

#获取指定路径下的文件夹
files_and_folders = os.listdir(path)
# 过滤出文件夹
folders = [f for f in files_and_folders if os.path.isdir(os.path.join(path, f))]

# todo:多进程运行
pool = multipool_map(args.num)
pool(fun=start_test, list=folders)