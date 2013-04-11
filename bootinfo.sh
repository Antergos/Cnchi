#!/bin/bash

#  If partition is mounted, try to identify the Operating System (OS) by looking for files specific to the OS.
OS='';

grep -q "W.i.n.d.o.w.s. .V.i.s.t.a"  "${mountname}"/{windows,Windows,WINDOWS}/{System32,system32}/{Winload,winload}.exe 2>> ${Trash} && OS='Windows Vista';

grep -q "W.i.n.d.o.w.s. .7" "${mountname}"/{windows,Windows,WINDOWS}/{System32,system32}/{Winload,winload}.exe 2>> ${Trash} && OS='Windows 7';

for WinOS in 'MS-DOS' 'MS-DOS 6.22' 'MS-DOS 6.21' 'MS-DOS 6.0' 'MS-DOS 5.0' 'MS-DOS 4.01' 'MS-DOS 3.3' 'Windows 98' 'Windows 95'; do
  grep -q "${WinOS}" "${mountname}"/{IO.SYS,io.sys} 2>> ${Trash} && OS="${WinOS}";
done        

[ -s "${mountname}/Windows/System32/config/SecEvent.Evt" ] || [ -s "${mountname}/WINDOWS/system32/config/SecEvent.Evt" ] || [ -s "${mountname}/WINDOWS/system32/config/secevent.evt" ] || [ -s "${mountname}/windows/system32/config/secevent.evt" ] && OS='Windows XP';

[ -s "${mountname}/ReactOS/system32/config/SecEvent.Evt" ] && OS='ReactOS';

[ -s "${mountname}/etc/issue" ] && OS=$(sed -e 's/\\. //g' -e 's/\\.//g' -e 's/^[ \t]*//' "${mountname}"/etc/issue);

[ -s "${mountname}/etc/slackware-version" ] && OS=$(sed -e 's/\\. //g' -e 's/\\.//g' -e 's/^[ \t]*//' "${mountname}"/etc/slackware-version);
