# Automate Windows Setup

This python script generates an answer file for Windows setup process. With this answer file you can
boot the installation, leave it and come back when setup is done completely.

## Features

* Minimal configuration through a config file
* Configure UEFI or MBR boot
* Insert Autounattend.xml right in to a Windows installation iso file

## Getting started

### Answer file for USB flash drive

1. Adjust `config.ini`; see `Configuration`
2. Run the script
```
python main.py
```
3. Copy `Autounattend.xml` to your USB Flash drive
4. Boot it

### Answer file for .iso

Prerequisites:
* Windows OS
* Windows ADK installed
* Enough disk space
* Allowed to run PowerShell scripts

1. Adjust the path to `C:\your_windows.iso` file in the `config.ini`
2. Run the script
```
python main.py
```
3. Boot `C:\your_windows_updated.iso` file (for example in VirtualBox)

## Configuration

Choose your keyboard layout.
```
INPUT_LOCALE = en-US
```
Choose your language of user interface on Windows desktop.
```
UI_LOCALE = en-US
```
Choose formatting of dates, times and currency.
```
USER_LOCALE = en-US
```
Choose your disk partitioning configuration (`mbr` or `uefi`). CAUTION: The first disk will be wiped!
```
DISK_PART = mbr
```
Choose a generic production key or use your own. You can change the production after the
installation. Defaults to Windows 10 Professional.
Windows 10 Home = TX9XD-98N7V-6WMQ6-BX7FG-H8Q99
Windows 10 Professional = VK7JG-NPHTM-C97JM-9MPGT-3V66T
Windows 10 Enterprise = NPPR9-FWDCX-D2C8J-H872K-2YT43
```
PROD_KEY = VK7JG-NPHTM-C97JM-9MPGT-3V66T
```
Choose your username. The displayed username in Windows equals the username. You can change the displayed name
after installation.
```
USER_NAME = admin
```
Choose a password. I urge you to leave this at default or choose another simple one, but change the password afterwards! 
```
USER_PWD = admin
```
Set the path to your Windows installtion .iso file. For example `ISO_FILE = C:\Downloads\Windows.iso`. Leave it
empty, to not use this feature. This feature works only on Windows and the Windows ADK must be
installed. Also there must be enough disk space to extract the .iso file and create the updated .iso
file.
```
ISO_FILE = 
```

## Reading sources

- [Windows Setup Automation Overview](https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-setup-automation-overview)
- [Sample: Configure UEFI/GPT-Based Hard Drive Partitions by Using Windows Setup](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-8.1-and-8/hh825702%28v%3dwin.10%29)
- [Sample: Configure BIOS/MBR-Based Hard Drive Partitions by Using Windows Setup](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-8.1-and-8/hh825701%28v%3dwin.10%29)

## Yes, Cortana was the motivation for this script ;)

https://www.youtube.com/watch?v=Rp2rhM8YUZY

## Licensing

MIT License
