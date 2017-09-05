#!/bin/python
'''***'''
from tkinter import *
from tkinter.ttk import *

import os
import stat
import struct
import fcntl
import termios


def CheckPipeInfo(tk, fd_pipe, progress_bar, pipe_max_bytes):
        barr = bytearray(4)
        fcntl.ioctl(fd_pipe, termios.FIONREAD, barr, True)
        pipe_unread_bytes = struct.unpack('i',barr)

        pipe_full_perc = int(pipe_unread_bytes[0]/pipe_max_bytes*100)

        progress_bar['value'] = pipe_full_perc

        # wait for 500 ms to update again
        tk.after(500, CheckPipeInfo, tk, fd_pipe, progress_bar, pipe_max_bytes)

def monitorPipeTK(fd_list):
    '''
    fd_list - list, (not tuple, list!)

    List of pipe file descriptors - integers or paths to pipes.
    The file descriptors must be opened for reading only (otherwise pipe synchronization might fail).
    
    Paths to pipes will also be opened read only.

    Path to pipes will usualy be in the form of: 
    /proc/<pid>/fd/<fd>

    <pid> is the process id of one of the processes that uses the pipe.
    <fd> is the file descriptor to monitor.
    '''
    pipe_max_bytes = 16*4096 # 16 pages, should get this from system

    if type(fd_list) is not list:
        fd_list = [fd_list]

    tk = Tk()

    for fd in fd_list:
        fd_desc = 'fd: {:}'.format(fd)
        if type(fd)==str:
            try:
                fd = os.open(fd, os.O_RDONLY)
            except:
                print('failed to open {:}'.format(fd))
                continue

        fd_fstat = os.fstat(fd)
        if not stat.S_ISFIFO(fd_fstat.st_mode):
            print('file descriptor {:} is not a FIFO (pipe)'.format(fd))
            continue
            
        label = Label(tk, text=fd_desc)
        progress_bar = Progressbar(tk, orient=HORIZONTAL, length=100, mode='determinate')
        label.pack()
        progress_bar.pack()

        CheckPipeInfo(tk, fd, progress_bar, pipe_max_bytes)

    mainloop()


'''***'''

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        print('''usage:
        pyton {:} <pipe path> <pipe path>
        
        <pipe path> is a path to a pipe you want to monitor.
        You will usualy find these in /proc/<pid>/fd/ directory
        of your process. You can list multiple paths.'''.format(sys.argv[0]))
    else:
        monitorPipeTK(sys.argv[1:])
