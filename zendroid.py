#!/usr/bin/env python
'''
A Zenity GUI on top of the droid functions
'''

import sys,os
try:
    import PyZenity as zen
except ImportError:
    print 'No PyZenity, do "sudo easy_install pyzenity"'
    sys.exit(1)
import droid

def start_server():
    'Start the server if needed'
    pid,err = droid.server_pid()
    if pid:
        zen.InfoMessage("Server running on %s" % pid)
        return

    out,err = droid.cmd('gksudo',[droid.adbcmd,'start-server'])
    if not out:
        msg = "Failed to start server.  Wrong password?"
        zen.ErrorMessage(msg)
    else:
        zen.InfoMessage(out)
    return

def install_amazon():
    'Try to sideload waiting packages from Amazon app store'
    try:
        toinst = droid.cached_amazon()
    except OSError,err:
        zen.ErrorMessage("Can't get amazon package listing, server started?")
        return

    if not toinst:
        zen.InfoMessage('''No Amazon packages to install at this time. Download the package via your phone STOP at the "can't install" message and then re-run this program''')
        return

    desc = []
    for fname in toinst:
        out,err = droid.pull_amazon(fname,fname)
        assert not err,err
        pname,err = droid.package_name(fname)
        assert not err,err
        desc.append((True,pname,fname))
        continue

    pkgs = zen.List(('Select','Package','Filename'),
                    title='Packages to install',
                    data=desc,select_col=3,boolstyle="checklist")
    for apk in pkgs:
        out,err = droid.adb("install " + apk)
        if err:
            zen.ErrorMessage('Installation of "%s" failed.  Error is "%s"' % (apk,err))
        
    pkgs = zen.InfoMessage("Installation done")

    return
        

def check_install():
    if not os.path.exists(droid.adbcmd):
        zen.ErrorMessage('It looks like you have not installed the Android SDK.  I checked here: "%s"' % droid.adbcmd)
        return False

    return True

    
def main():
    pid,err = droid.server_pid()
    need_server = not pid

    cmds = zen.List(('Select','Description','Function'),
                    title='What do you want me to do?',
                    select_col=3,boolstyle="checklist",
                    data=[(need_server,'Start the ADB server','start_server'),
                          (True,'Install downloaded Amazon Apps','install_amazon')]
                    )
    for cmd in cmds:
        func = eval(cmd)
        func()
        continue
    return



if __name__ == '__main__':
    if not check_install():
        sys.exit(1)

    func = eval(sys.argv[1])
    func(*sys.argv[2:])
