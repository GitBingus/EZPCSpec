import platform
import cpuinfo
import sys
import os
import psutil
import GPUtil
from tabulate import tabulate
from datetime import datetime as dt

file = "Systeminfo.txt"

sep = "="*50

print("Fetching computer information... ")

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

class disk:
    def get_disk_info():
        disk_info = []
        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    continue
            usage = psutil.disk_usage(part.mountpoint)
            disk_info.append("-'Device':\t{:<},'Total':\t{:^1}GiB,'Used':\t{:^2}GiB,'Free':\t{:^3}GiB,'Percent':\t{:^2}%,'File System Type':\t{:^1},'Mountpoint':\t{:>}\n".format(
                part.device, usage.total // 1024 // 1024 // 1024, usage.used // 1024 // 1024 // 1024, usage.free // 1024 // 1024 // 1024, usage.percent, part.fstype, part.mountpoint
            ))
        
        disk_info = ''.join(disk_info).replace(',','\t').replace("'","").replace(' ','\t')
        disk_info = ''.join(disk_info.split('-'))
        
        return disk_info

class bt:
    btstamp = psutil.boot_time()
    bt = dt.fromtimestamp(btstamp)
    btout = f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"

class system:
    OS = platform.uname().system
    if sys.getwindowsversion().build > 20000:
        Version = platform.uname().version.replace('10','11')
    else:
        Version = platform.uname().version
        
    OSArch = os.environ['PROCESSOR_ARCHITECTURE']

class cpu:
    cpuName = cpuinfo.get_cpu_info()['brand_raw']
    cpuString = platform.processor()
    cpuArch = cpuinfo.get_cpu_info()['arch']
    cpuBits = cpuinfo.get_cpu_info()['bits']
    cpuHzTrue = cpuinfo.get_cpu_info()['hz_actual'][0]
    cpuHzGHz = cpuinfo.get_cpu_info()['hz_actual_friendly']
    cpuPhysicalCores = psutil.cpu_count(logical=False)
    cpuLogicalCores = psutil.cpu_count(logical=True)
    cpuL2 = int(cpuinfo.get_cpu_info()['l2_cache_size'] // 1024)
    cpuL3 = int(cpuinfo.get_cpu_info()['l3_cache_size'] // 1024)
    
class motherboard:
    manufacturer = os.popen("wmic baseboard get Manufacturer").read().split('\n')[2]
    product = os.popen("wmic baseboard get product").read().split('\n')[2]
    sn = os.popen("wmic baseboard get serialnumber").read().split('\n')[2]
    ver = os.popen("wmic baseboard get version").read().split('\n')[2]

class memory:
    svmem = psutil.virtual_memory()
    total = get_size(svmem.total)
    available = get_size(svmem.available)
    used = get_size(svmem.used)
    percentage = svmem.percent
    
    swap = psutil.swap_memory()
    swaptotal = get_size(swap.total)
    swapfree = get_size(swap.free)
    swapused = get_size(swap.used)
    swappercentage = swap.percent
    
class gpu:
    def Gpu():
        gpus = GPUtil.getGPUs()
        gpuList = []
        for gpu in gpus:
            gpu_id = gpu.id
            gpuname = gpu.name
            gpuload = f"{gpu.load*100}%"
            gpufree_memory = f"{gpu.memoryFree}MB"
            gpuused_memory = f"{gpu.memoryUsed}MB"
            gputotal_memory = f"{gpu.memoryTotal}MB"
            gputemperature = f"{gpu.temperature} C"
            gpuuuid = gpu.uuid
            gpuList.append((
                gpu_id, gpuname, gpuload, gpufree_memory, gpuused_memory, gputotal_memory, gputemperature, gpuuuid
            ))
        
        return tabulate(gpuList, headers=("ID","Name","Load","Free Memory","Used Memory","Total Memory","Temperature","UUID"))

print("Generating file...")

output = (f'''
{sep} *System Info* {sep}

Base Operating System: {system.OS}
Operating System Version: {system.Version}
Operating System Architecture: {system.OSArch}

{sep} *Boot time* {sep}

{bt.btout}

{sep} *CPU Info* {sep}

CPU Name: {cpu.cpuName}
CPU String: {cpu.cpuString}
CPU Architecture: {cpu.cpuArch}
CPU Bit Architecture: x{cpu.cpuBits}
CPU Frequency (True Freq): {cpu.cpuHzGHz} ({cpu.cpuHzTrue} Hz)
CPU Physical Cores: {cpu.cpuPhysicalCores}
CPU Logical Cores: {cpu.cpuLogicalCores}
CPU L2 Cache: {cpu.cpuL2}KiB
CPU L3 Cache: {cpu.cpuL3}KiB

{sep} *Motherboard Info* {sep}

Motherboard Manufacturer: {motherboard.manufacturer}
Motherboard Name: {motherboard.product}
Motherboard Serial Number: {motherboard.sn}
Motherboard Version: {motherboard.ver}

{sep} *Memory Info* {sep}

Memory Total: {memory.total}
Memory Available: {memory.available}
Memory Used: {memory.used}
Memory Percentage: {memory.percentage}%

{"="*25} *Swap* {"="*25}

Swap Total: {memory.swaptotal}
Swap Free: {memory.swapfree}
Swap Used: {memory.swapused}
Swap Percentage: {memory.swappercentage}%

{sep} *Disk Info* {sep}

{disk.get_disk_info()}

{sep} *Network Info* {sep}

{os.popen("ipconfig /all").read()}

{sep} *Graphics Card Info* {sep}

{gpu.Gpu()}

''')

with open(file, 'w+') as f:
    f.write(f"# System information as of {dt.now().strftime('%x')} {dt.now().strftime('%X')}")
    f.write(output)
    f.close()

cwd = os.getcwd()
drvltr = cwd[0].capitalize()

print(f'Success! You can open the file at "{drvltr+cwd[1:]}\\{file}"')