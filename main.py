import autoxml
import configparser
import subprocess
import sys
import os

config = configparser.ConfigParser()
config.read('config.ini')

unattendxml.create_answerfile(config)

isofile = config['MISC']['PATH_TO_ISO']
if isofile:
    if not os.path.isfile(isofile):
        sys.exit('Iso file not found!')
    script = os.path.join(os.getcwd(), 'insert.ps1')
    script = os.path.normpath(script)
    media = os.path.dirname(isofile)[:-1]
    autofile = os.path.join(os.getcwd(), 'Autounattend.xml')
    autofile = os.path.normpath(autofile)
    p = subprocess.Popen(['powershell.exe', script, media, isofile, autofile],
            stdout=sys.stdout)
    p.communicate()
