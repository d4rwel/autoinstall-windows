import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

skeleton = '''<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
</unattend>
'''

def create_answerfile(config):
    ET.register_namespace('', 'urn:schemas-microsoft-com:unattend')
    root = ET.fromstring(skeleton)

    elem_settings = insert_settings('windowsPE', root)

    elem_component = insert_component('Microsoft-Windows-International-Core-WinPE', elem_settings)

    elem = ET.SubElement(elem_component, 'SetupUILanguage')
    elem = ET.SubElement(elem, 'UILanguage')
    elem.text = config['UNATTEND']['UI_LOCALE']
    elem = ET.SubElement(elem_component, 'InputLocale')
    elem.text = config['UNATTEND']['INPUT_LOCALE']
    elem = ET.SubElement(elem_component, 'LayeredDriver')
    elem.text = '1'
    elem = ET.SubElement(elem_component, 'SystemLocale')
    elem.text = config['UNATTEND']['UI_LOCALE']
    elem = ET.SubElement(elem_component, 'UILanguage')
    elem.text = config['UNATTEND']['UI_LOCALE']
    elem = ET.SubElement(elem_component, 'UILanguageFallback')
    elem.text = 'en-US'
    elem = ET.SubElement(elem_component, 'UserLocale')
    elem.text = config['UNATTEND']['USER_LOCALE']

    elem_component = insert_component('Microsoft-Windows-Setup', elem_settings)

    elem_diskconfig = ET.SubElement(elem_component, 'DiskConfiguration')

    elem = ET.SubElement(elem_diskconfig, 'DisableEncryptedDiskProvisioning')
    elem.text = 'true'

    elem = ET.SubElement(elem_diskconfig, 'WillShowUI')
    elem.text = 'OnError'

    elem_disk = ET.SubElement(elem_diskconfig, 'Disk')
    elem_disk.set('wcm:action', 'add')
    elem = ET.SubElement(elem_disk, 'DiskID')
    elem.text = '0'
    elem = ET.SubElement(elem_disk, 'WillWipeDisk')
    elem.text = 'true'

    elem_cparts = ET.SubElement(elem_disk, 'CreatePartitions')
    elem_mparts = ET.SubElement(elem_disk, 'ModifyPartitions')
    if config['UNATTEND']['DISK_PART'] == 'uefi':
        insert_cpart(elem_cparts, '1', 'Primary', size='300')
        insert_cpart(elem_cparts, '2', 'EFI', size='260')
        insert_cpart(elem_cparts, '3', 'MSR', size='128')
        insert_cpart(elem_cparts, '4', 'Primary')
        insert_mpart(elem_mparts, '1', '1', partformat='NTFS', label='WINRE')
        insert_mpart(elem_mparts, '2', '2', partformat='FAT32', label='System')
        insert_mpart(elem_mparts, '3', '3')
        insert_mpart(elem_mparts, '4', '4', partformat='NTFS', label='Windows', letter='C')
    else:
        # master boot record
        insert_cpart(elem_cparts, '1', 'Primary', size='350')
        insert_cpart(elem_cparts, '2', 'Primary')
        insert_mpart(elem_mparts, '1', '1', partformat='NTFS', label='System', active=True)
        insert_mpart(elem_mparts, '2', '2', partformat='NTFS', label='Windows', letter='C')

    elem = ET.SubElement(elem_component, 'ImageInstall')
    elem = ET.SubElement(elem, 'OSImage')
    elem_installto = ET.SubElement(elem, 'InstallTo')
    elem = ET.SubElement(elem_installto, 'DiskID')
    elem.text = '0'
    elem = ET.SubElement(elem_installto, 'PartitionID')
    if config['UNATTEND']['DISK_PART'] == 'uefi':
        elem.text = '4'
    else:
        # master boot record
        elem.text = '2'

    elem_userdata = ET.SubElement(elem_component, 'UserData')
    elem = ET.SubElement(elem_userdata, 'ProductKey')
    elem = ET.SubElement(elem, 'Key')
    elem.text = config['UNATTEND']['PROD_KEY']
    elem = ET.SubElement(elem_userdata, 'AcceptEula')
    elem.text = 'true'

    elem_settings = insert_settings('specialize', root)

    elem_component = insert_component('Microsoft-Windows-Shell-Setup', elem_settings)

    elem = ET.SubElement(elem_component, 'ComputerName')
    elem.text = '*'
    elem = ET.SubElement(elem_component, 'TimeZone')
    elem.text = 'W. Europe Standard Time'

    elem_settings = insert_settings('oobeSystem', root)

    elem_component = insert_component('Microsoft-Windows-International-Core', elem_settings)

    elem = ET.SubElement(elem_component, 'InputLocale')
    elem.text = config['UNATTEND']['INPUT_LOCALE']
    elem = ET.SubElement(elem_component, 'SystemLocale')
    elem.text = config['UNATTEND']['UI_LOCALE']
    elem = ET.SubElement(elem_component, 'UILanguage')
    elem.text = config['UNATTEND']['UI_LOCALE']
    elem = ET.SubElement(elem_component, 'UILanguageFallback')
    elem.text = 'en-US'
    elem = ET.SubElement(elem_component, 'UserLocale')
    elem.text = config['UNATTEND']['USER_LOCALE']

    elem_component = insert_component('Microsoft-Windows-Shell-Setup', elem_settings)

    elem_oobe = ET.SubElement(elem_component, 'OOBE')
    elem = ET.SubElement(elem_oobe, 'HideEULAPage')
    elem.text = 'true'
    elem = ET.SubElement(elem_oobe, 'HideLocalAccountScreen')
    elem.text = 'true'
    elem = ET.SubElement(elem_oobe, 'HideOEMRegistrationScreen')
    elem.text = 'true'
    elem = ET.SubElement(elem_oobe, 'HideOnlineAccountScreens')
    elem.text = 'true'
    elem = ET.SubElement(elem_oobe, 'HideWirelessSetupInOOBE')
    elem.text = 'true'
    elem = ET.SubElement(elem_oobe, 'ProtectYourPC')
    elem.text = '3' 
    elem = ET.SubElement(elem_oobe, 'UnattendEnableRetailDemo')
    elem.text = 'false'

    elem_useraccounts = ET.SubElement(elem_component, 'UserAccounts')
    elem_localaccounts = ET.SubElement(elem_useraccounts, 'LocalAccounts')
    elem_localaccount = ET.SubElement(elem_localaccounts, 'LocalAccount')
    elem_localaccount.set('wcm:action', 'add')
    elem = ET.SubElement(elem_localaccount, 'Group')
    elem.text = 'Administrators'
    elem = ET.SubElement(elem_localaccount, 'Name')
    elem.text = config['UNATTEND']['USER_NAME']
    if config['UNATTEND']['USER_PWD']:
        elem_pwd = ET.SubElement(elem_localaccount, 'Password')
        elem = ET.SubElement(elem_pwd, 'Value')
        elem.text = config['UNATTEND']['USER_PWD']
        elem = ET.SubElement(elem_pwd, 'PlainText')
        elem.text = 'true'

    elem = ET.SubElement(elem_component, 'TimeZone')
    elem.text = 'W. Europe Standard Time'

    # ElementTree has no pretty print!? Oo
    root_string = prettify(root)
    with open('Autounattend.xml', 'w') as xml_file:
        xml_file.write(root_string)

def insert_settings(pass_name, parent):
    settings = ET.SubElement(parent, 'settings')

    settings.set('pass', pass_name)

    return settings

def insert_component(name, parent, arch='amd64'):
    elem_component = ET.SubElement(parent, 'component')

    elem_component.set('name', name)
    elem_component.set('processorArchitecture', arch)
    elem_component.set('publicKeyToken', '31bf3856ad364e35')
    elem_component.set('language', 'neutral')
    elem_component.set('versionScope', 'nonSxS')
    elem_component.set('xmlns:wcm', 'http://schemas.microsoft.com/WMIConfig/2002/State')
    elem_component.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

    return elem_component

def insert_cpart(parent, order, parttype, size=None):
    createpartition = ET.SubElement(parent, 'CreatePartition')
    createpartition.set('wcm:action', 'add')
    
    elem = ET.SubElement(createpartition, 'Order')
    elem.text = order
    elem = ET.SubElement(createpartition, 'Type')
    elem.text = parttype
    if size:
        elem = ET.SubElement(createpartition, 'Size')
        elem.text = size
    else:
        elem = ET.SubElement(createpartition, 'Extend')
        elem.text = 'true'

def insert_mpart(parent, order, partid, partformat=None, label=None, letter=None, active=False):
    modifypartition = ET.SubElement(parent, 'ModifyPartition')
    modifypartition.set('wcm:action', 'add')
    
    elem = ET.SubElement(modifypartition, 'Order')
    elem.text = order
    elem = ET.SubElement(modifypartition, 'PartitionID')
    elem.text = partid
    if partformat:
        elem = ET.SubElement(modifypartition, 'Format')
        elem.text = partformat
    if label:
        elem = ET.SubElement(modifypartition, 'Label')
        elem.text = label
    if letter:
        elem = ET.SubElement(modifypartition, 'Letter')
        elem.text = letter
    if active:
        elem = ET.SubElement(modifypartition, 'Active')
        elem.text = 'true'
        
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")
