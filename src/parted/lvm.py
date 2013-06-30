import subprocess
import misc

@misc.raise_privileges
def get_lvm_partitions():
    vgmap = {}
    x = subprocess.getoutput("pvdisplay")
    for e in x.split("\n"):
        if "PV Name" in e:
            pvn = e.split()[-1]
        if "VG Name" in e:
            vgn = e.split()[-1]
            try:
                vgmap[vgn].append(pvn)
            except:
                vgmap[vgn] = [pvn]
    return vgmap

@misc.raise_privileges
def get_volume_groups():
    vg = []
    x = subprocess.getoutput("vgdisplay")
    for e in x.split("\n"):
        if "VG Name" in e:
            vg.append(e.split()[-1])
    return vg

@misc.raise_privileges
def get_logical_volumes(vg):
    lv = []
    x = subprocess.getoutput("lvdisplay %s" % vg)
    for e in x.split("\n"):
        if "LV Name" in e:
            lv.append(e.split()[-1])
    return lv

