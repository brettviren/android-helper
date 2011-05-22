#!/usr/bin/env python
'''
A Zenity GUI on top of the droid functions
'''

import sys
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
    toinst = droid.cached_amazon()

    if not toinst:
        zen.InfoMessage('''No Amazon packages to install at this time. Download the package via your phone STOP at the "can't install" message and then re-run this program''')
        return

    desc = []
    for fname in toinst:
        out,err = droid.pull_amazon(fname,fname)
        assert not err,err
        pname,err = droid.package_name(fname)
        assert not err,err
        desc.append((True,fname,pname))
        continue

    pkgs = zen.List(('Select','Package','Filename'),
                    title='Packages to install',
                    data=desc,select_col=3,boolstyle="checklist")
    for apk in pkgs:
        out,err = droid.adb("install " + apk)
        assert not err, err

    return
        

    
if __name__ == '__main__':
    #start_server()
    install_amazon()
