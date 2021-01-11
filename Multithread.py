#!/usr/bin/env python38
# -*- coding: utf-8 -*-
# @File  : PyAppTool.py
# @Author: HandsomeFa
# @Date  : 2020/12/14
# @Desc  : Multi threading
"""
There are two ways to use threads: functions or classes to wrap Thread objects.
https://zhuanlan.zhihu.com/p/35944711
https://www.runoob.com/python3/python3-multithreading.html
https://xufive.blog.csdn.net/article/details/104633575
"""
import threading
import multiprocessing as mp
import time
import requests


class ProcessService:
    """
    进程类，使用进程处理计算密集型任务
    和线程相比，进程的最大优势是可以充分利用计算资源这一点不难理解，因为不同的进程可以运行的不同CPU的不同的核上。
    假如一台计算机的CPU共有16核，则可以启动16个或更多个进程来并行处理任务。
    """
    def __init__(self, process_num=2, queue_num=10):
        mp.freeze_support()
        self.process = None
        self.process_num = process_num
        self.queue = mp.Queue(queue_num)

    def run(self, process_name, *process_args):
        self.process = mp.Process(target=process_name, args=process_args)
        sub_process_list = []
        for i in range(1, self.process_num + 1):
            sub_process = mp.Process(target=process_name, args=process_args)
            sub_process_list.append(sub_process)
        for sub_process in sub_process_list:
            sub_process.daemon = True
            sub_process.start()
        for sub_process in sub_process_list:
            sub_process.join()

    def __del__(self):
        pass


def f2(x, y):
    for i in range(x, y):
        print(i)


class ThreadService(threading.Thread):
    """
    抓取线程类，注意需要继承线程类Thread
    Queue.qsize(队列名) #返回队列的大小
    Queue.empty(队列名) # 队列为空返回true，否则为false
    Queue.full(队列名) # 队列满返回true
    Queue.get(队列名,值) # 出队
    Queue.put(队列名,值) # 入队
    FIFO 先进先出
    """
    def __init__(self, thread_num, fun, *fun_args):
        # fun_args要与thread_num有关系，共同完成所有的任务数。
        # 比如请求task_num=100次，可以设置thread_num=2，那么fun_args内参数p1=task_num/thread_num=50
        super().__init__()
        self.thread_num = thread_num
        self.fun_name = fun
        self.fun_args = fun_args
        self.t1 = time.time()

    @staticmethod
    def test_fun(request_times=50):
        urls = ['https://www.baidu.com', 'https://cn.bing.com']
        for i in range(request_times):
            url = urls[i % 2]
            requests.get(url)
            print(i, url, sep='---')

    @staticmethod
    def test_fun2(request_times=50):
        for i in range(request_times):
            url = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_%d.html' % i
            requests.get(url)
            print(i, url, sep='---')

    def run(self):
        thread_list = []
        for i in range(1, self.thread_num+1):
            thread_list.append(threading.Thread(name="thread_%d" % i, target=self.fun_name, args=self.fun_args))
            thread_list[-1].setDaemon(True)
            thread_list[-1].start()
        for thread in thread_list:
            thread.join()

    def __del__(self):
        t1 = time.time()
        print('run %d threads, taking %s seconds' % (self.thread_num, t1 - self.t1))


def test_function(request_times=50):
    urls = ['https://www.baidu.com', 'https://cn.bing.com']
    for i in range(request_times):
        url = urls[i % 2]
        requests.get(url)
        print(i, url, sep='---')


if __name__ == "__main__":
    print('')
    a = ThreadService(10, ThreadService.test_fun2, 2)
    a.run()
