# https://hinchley.net/articles/update-an-iso-using-powershell/
# paths to media.
$media = $args[0]
$old   = "$media\$args[1]" 
$new   = "$media\$args[1]-updated.iso"
$autofile = $args[2]

# paths to tools.
$tools    = 'C:\Program Files (x86)\Windows Kits\10\Assessment and Deployment Kit\Deployment Tools\amd64\oscdimg'
$oscdimg  = "$tools\oscdimg.exe"
$etfsboot = "$tools\etfsboot.com"
$efisys   = "$tools\efisys.bin"

# mount the existing iso.
$mount = mount-diskimage -imagepath $old -passthru

# get the drive letter assigned to the iso.
$drive = ($mount | get-volume).driveletter + ':'

# create a temp folder for extracting the existing iso.
$workspace = "{0}\{1}" -f $env:temp, [system.guid]::newguid().tostring().split('-')[0]
new-item -type directory -path $workspace

# extract the existing iso to the temporary folder.
copy-item $drive\* $workspace -force -recurse

# remove the read-only attribtue from the extracted files.
get-childitem $workspace -recurse | %{ if (! $_.psiscontainer) { $_.isreadonly = $false } }

# insert autounattended file
copy-item -Path $autofile -destination $workspace

# create the updated iso.
$data = '2#p0,e,b"{0}"#pEF,e,b"{1}"' -f $etfsboot, $efisys
start-process $oscdimg -args @("-bootdata:$data",'-u2','-udfver102', $workspace, $new) -wait -nonewwindow

# remove the extracted content.
remove-item $workspace -recurse -force

# dismount the iso.
dismount-diskimage -imagepath $old
