# 杀掉进程函数
import psutil
import os
import signal
import subprocess

def kill_deepstream():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == 'deepstream-app':
            os.kill(pid,signal.SIGKILL)

def kill_arcface():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == 'pro':
            os.kill(pid,signal.SIGKILL)