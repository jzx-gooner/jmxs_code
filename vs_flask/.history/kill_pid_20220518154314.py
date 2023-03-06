import psutil
import os
import signal
import subprocess

def kill_deepstream():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == 'deepstream-test5-analytics':
            os.kill(pid,signal.SIGKILL)

def kill_arcface():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == 'pro':
            os.kill(pid,signal.SIGKILL)

def start_deepstream():
    subprocess.Popen("sh go_deepstream.sh",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)

def start_arcface():
    subprocess.Popen("sh go_arcface.sh",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)


