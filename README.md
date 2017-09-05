# unix_pipe_monitor
A simple python script to monitor the capacity of unix pipes.
Uses Linux specific FIONREAD with ioctl to get current unread bytes in a pipe and display them as a bar.

### Dependencies
 - tkinter for GUI
 - fcntl, termios - unix API

### Usage

As an cmd application simply pass paths to file nodes that are potential pipes to monitor. 
The script will check all potential nodes and display only FIFOs.
Example that will monitor all pipes of process 12345:
```
$ python pyPipeStats.py /proc/12345/fd/*
```


