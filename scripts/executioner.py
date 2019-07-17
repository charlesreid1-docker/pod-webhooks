#!/usr/bin/env python3
import subprocess
import os

def execute(cmd):
    """
    A function to run a command and return the
    lines of output as they are generated,
    allowing the calling function to "stream"
    the output of the command to print() or etc.
    """
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(p.stdout.readline, ""):
        yield stdout_line
    p.stdout.close()
    err = "".join([j for j in iter(p.stderr.readline,"")])
    return_code = p.wait()
    if return_code:
        yield err
        raise subprocess.CalledProcessError(return_code, cmd)

