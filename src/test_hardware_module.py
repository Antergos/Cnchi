import logging

# Get packages needed for detected hardware
try:
    import hardware.hardware as hardware
    hardware_install = hardware.HardwareInstall()
    hardware_pkgs = hardware_install.get_packages()
    print("Hardware module added these packages : ", hardware_pkgs)
except ImportError:
    print("Can't import hardware module.")
except Exception as err:
    print("Unknown error in hardware module. Output: %s" % err)
