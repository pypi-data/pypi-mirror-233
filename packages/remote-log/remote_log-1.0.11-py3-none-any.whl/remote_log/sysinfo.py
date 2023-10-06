import psutil
import platform
import uuid
import datetime
import sysconfig
import hashlib
import cpuinfo
import time
import os

# Function to convert large number of bytes into a readable format
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_system_info():
    cpu = cpuinfo.get_cpu_info()
    
    # Get system info
    info = {}

    # System
    info["system"] = platform.system()

    # OS Version
    info["os_version"] = platform.version()

    # OS Name
    info["os_name"] = platform.system()

    # System Platform
    info["platform"] = sysconfig.get_platform()

    # Machine
    info["machine"] = platform.machine()

    # Processor Info
    info["processor_type"] = platform.processor()
    info["processor_name"] = cpu["brand_raw"]
    info["processor_architecture"] = cpu["arch"]
    info["processor_version"]= cpu["cpuinfo_version_string"]
    
    info["physical_cores"] = psutil.cpu_count(logical=False)
    info["total_cores"] = psutil.cpu_count(logical=True)

    # Current Time
    current_time = datetime.datetime.now().astimezone()
    info["current_time"] = current_time.strftime("%Y-%m-%d %H:%M:%S") + " " + time.tzname[1]

    # MAC Address
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    hashed_mac = hashlib.sha256(mac_address.encode()).hexdigest()
    info["hashed_mac_address"] = hashed_mac

    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
    info["boot_time"] = f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"

    # Total and available RAM
    svmem = psutil.virtual_memory()
    info["total_ram"] = get_size(svmem.total)
    info["available_ram"] = get_size(svmem.available)
    
    try:
        if os.name == 'posix':
            main_disk = '/'
        else:
            main_disk = 'C:\\'

        # Total and available Disk space for the main disk
        partition_usage = psutil.disk_usage(main_disk)
        info["total_size_of_main_disk"] = get_size(partition_usage.total)
        info["available_space_on_main_disk"] = get_size(partition_usage.free)
    except:
        pass

    return info
