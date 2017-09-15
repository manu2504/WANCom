#!/usr/bin/python

def check_pid_output(pid, verbose=True):
    # Wait on the proc completion
    out, err = pid.communicate()
    ret = pid.returncode

    if verbose and out:
        print ">>> PROC: normal output:\n%s" % out

    if ret != 0:
        print ">>> PROC: non-zero return code: [%i]. Message:" % ret
        print err

    return ret
