#!/usr/bin/env python

import sys,os

basedir = os.path.expandvars("$HOME/src/android-sdk-linux_x86/")
adbcmd = os.path.join(basedir,'platform-tools/adb')
aaptcmd = os.path.join(basedir,'platform-tools/aapt')
amazon_dir = "/mnt/sdcard/Android/data/com.amazon.venezia/cache"

def cmd(name,args):
    'Return (stdout,stderr) running "name [args]"'

    # Convert to list if given a string
    if type(args) == type(""):
        args = name + " " + args
        args = args.strip()
        cmds = args.split()
        if len(cmds) > 1:
            args = cmds
        pass
    else:
        args.insert(0,name)
    #print args    

    from subprocess import Popen, PIPE, STDOUT
    proc = Popen(args,stdout=PIPE,stderr=STDOUT,universal_newlines=True)
    return proc.communicate()    
    
def adb(args): return cmd(adbcmd,args)
def aapt(args): return cmd(aaptcmd,args)


# --- These functions should all return a tuple of strings
# --- giving (output,errput).  Non-empty errput means an error occurred.

def package_name(apk):
    'Given an Android Package filename, return the app name'
    out,err = aapt("d badging %s application" % apk)
    for line in out.split('\n'):
        chunks = line.strip().split()
        if not chunks[0] == 'application:': continue
        name = line[line.find("label='")+7 : line.find("' icon=")]
        return (name,err)
    return ('',err)
    

def ls_amazon():
    'List the install cache area for Amazon App Store'
    return adb("ls "+amazon_dir)

def pull_amazon(onphone,tohere):
    'Pull the given file from the Amazon App Store cache to the local path'
    return adb("pull " + amazon_dir + "/" + onphone + ' ' + tohere)

def install_amazon_one(apk):
    'Pull the given package down from the phone and install it'
    pull_amazon(apk,apk)
    return adb("install " + apk)

def cached_amazon():
    "Return list of packages in Amazon's package cache"
    lines = ls_amazon()[0].split('\n')
    ret = []
    for line in lines[2:]:
        chunks = line.strip().split()
        if not chunks: break
        print chunks
        ret.append(chunks[3])
        continue
    return ret

def install_amazon():
    'Install all packages in the Amazon App Store'
    installed = []
    for fname in cached_amazon():
        print 'Installing: fname'
        install_amazon_one(fname)
        installed.append(fname)
        continue
    return ("Installed: " + " ".join(installed),"")

def server_pid():
    'Return the server PID or nothing if not running'
    out,err = cmd("ps","-eo pid,args")
    for line in out.splitlines():
        chunks = line.strip().split()
        if 'adb fork-server server' == ' '.join(chunks[1:]):
            return (chunks[0],"")
        continue
    return ('','')

def start_server(password = None):
    '''
    Start the ADB server, return PID.  If password is given, use sudo.
    If server already running, return an error.
    '''
    pid,err = server_pid()
    if pid: return ('','ADB server already running at ' + pid)
    
    if password:
        from subprocess import Popen, PIPE, STDOUT
        args = ['sudo','-S',adbcmd,'start-server']
        proc = Popen(args,stdin=PIPE,stdout=PIPE,stderr=PIPE,
                     shell=True,universal_newlines=True)
        return proc.communicate(password)

    return adb('start-server')


# ----------------- CLI ------------------------------------------------ #

def print_cmd((out,err)):
    print out
    if err: print "Error:",err

def usage():
    print 'droid cmd [options]'

def direct(*args): print_cmd(adb(list(args)))

if __name__ == '__main__':
    try:
        command = sys.argv[1]
    except IndexError:
        usage()
        sys.exit(1)
    command = command.replace("-","_")
    try:
        command = eval(command)
    except NameError:
        direct(*sys.argv[1:])
    else:
        print_cmd(command(*sys.argv[2:]))
    
