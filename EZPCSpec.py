# -*- coding: utf-8 -*-

toImport = [
    "os",
    "platform",
    "psutil",
    "GPUtil",
    "time",
    "io",
    "msvcrt"
]

try:
    import os, platform, psutil, GPUtil, time, io, msvcrt
except (ImportError):
    print("Some libraries are not installed. Would you like the program to automatically install them? Y/N")
    confirmLibInstall = msvcrt.getch().decode().lower()
    if confirmLibInstall == "y":
        print("Okay. Installing libraries... ")
        for lib in toImport:
            os.system(f"pip install {lib}")
            
    else:
        print("Okay. No libraries will be installed. ")
        quit()
        
    print("All required libraries should be installed. Restart the app to confirm changes. ")
    quit()

print("Welcome to the EZPCSpec app built by GitBingus!\n\nPress 'y' to start, or press any other key to abort, and exit the app.\n")
choice = msvcrt.getch().decode()

if choice != 'y':
    print("Okay. Will not continue. ")
    quit()
    
os.system("cls || clear")
print("Retrieving system data...")

# Retreives and processes all necessary data about user's system using WMIC and platform.uname to 'list comp []' function: CPU, Memory, Mainboard, OS, Drives, GPU
# All code uses os.popen() to get the data direct from WMIC, then reads it and only reads the required data

def bytestoint(bytes, suffix='B'):
    factor = 1024 # 1024 bytes in 1KB, 1024KB in 1MB, etc
    for unit in ["", "K", "M", "G", "T", "P"]: # Byte, Kilobyte, Megabyte etc -- Petabyte
        if bytes < factor: # checks to see if the bytes needs to be formatted or not and what too
            return f"{bytes:.2f}{unit}{suffix}" # returns formatted number with unit
        bytes /= factor # divides bytes by factor on every iteration until bytes < factor

class Cpu:
        cpuName = f'Name : {" ".join(os.popen("wmic cpu get name").read().split()[1:])}'
        cpuArch = f'Architecture : {platform.uname().machine}'
        cpuMan = f'Manufacturer : {os.popen("wmic cpu get manufacturer").read().split()[1]}'
        cpuSocketType = f'Socket Type : {os.popen("wmic cpu get socketdesignation").read().split()[1]}'
        cpuCurrFreq = f'Current Frequency : {"".join(os.popen("wmic cpu get currentclockspeed").read().split()[1:])} MHz'
        cpuCurrVolt = f'Current Voltage : {int("".join(os.popen("wmic cpu get currentvoltage").read().split()[1:])) / 10} V'
        cpuPhysCores = f'Physical Cores : {"".join(os.popen("wmic cpu get numberofcores").read().split()[1:])}'
        cpuEnabledPhysCores = f'Enabled Physical Cores : {"".join(os.popen("wmic cpu get numberofenabledcore").read().split()[1:])}'
        cpuLogCores = f'Logical Cores : {"".join(os.popen("wmic cpu get numberoflogicalprocessors").read().split()[1:])}'
        cpuL2Cache = f'L2 Cache : {"".join(os.popen("wmic cpu get l2cachesize").read().split()[1:])} MiB'
        cpuL3Cache = f'L3 Cache : {"".join(os.popen("wmic cpu get l3cachesize").read().split()[1:])} MiB'
    
class Mobo:
        moboMan = f"Manufacturer : {os.popen('wmic baseboard get manufacturer').read().removeprefix('Manufacturer').strip()}", # gets manufacturer for motherboard
        moboName = f"Name : {os.popen('wmic baseboard get product').read().removeprefix('Product').strip()}" # gets product name 
        moboSN = f"Serial Number: {os.popen('wmic baseboard get serialnumber').read().removeprefix('SerialNumber').strip()}" # gets serial number
        moboVer = f"Version : {os.popen('wmic baseboard get version').read().removeprefix('Version').strip()}" # gets version
    
class System:
        sysName = f'Name : {os.popen("wmic os get caption").read().removeprefix("Caption").strip()}'
        sysBuild = f'Build : {os.popen("wmic os get buildnumber").read().removeprefix("BuildNumber").strip()}'
        sysArch = f'Architecture : {os.popen("wmic os get osarchitecture").read().removeprefix("OSArchitecture").strip()}'
        sysName = f'Current Name : {os.popen("wmic os get csname").read().removeprefix("CSName").strip()}'

# As WMIC does not have a good GPU data set, GPUtil retrieves the data for the GPU instead
        
with io.open("EZPCSpec\\results.txt","w+") as writeToFile:
    writeToFile.write(f"Results.txt written as of: {time.strftime('%X')} - {time.strftime('%x')}\n\n")
    writeToFile.write("CPU Details: ")
    for v in vars(Cpu).values():
        cpuValues = str(v)
        if not "__" in cpuValues:
            if not cpuValues == "None":
                writeToFile.write(f"{cpuValues}\n")
                
    writeToFile.write("\nMemory Details: \n")
    memData = {}
    
    memNameList = os.popen('wmic memorychip get partnumber').read().split()[1:]
    writeToFile.write("\n"+"-"*10+"Per dimm data"+"-"*10+"\n")
    for i in range(len(memNameList)):
        writeToFile.write("\n"+"-"*5+f"Module {i} data"+"-"*5+"\n")
        writeToFile.write(f"Module {i} Name : {memNameList[i]}"+"\n")
        writeToFile.write(f'Module {i} Type : {os.popen("wmic memorychip get description").read().removeprefix("Description").split()[0]}'+"\n")
        writeToFile.write(f'Module {i} Manufacturer : {os.popen("wmic memorychip get manufacturer").read().split()[i+1]}'+"\n")
        writeToFile.write(f'Module {i} Capacity : {bytestoint(int(os.popen("wmic memorychip get capacity").read().split()[i+1]))}'+"\n")
        writeToFile.write(f'Module {i} Frequency : {os.popen("wmic memorychip get configuredclockspeed").read().split()[i+1]} MT/s'+"\n")
        writeToFile.write(f'Module {i} Voltage : {int(os.popen("wmic memorychip get configuredvoltage").read().split()[i+1]) / 1000} V'+"\n")
        writeToFile.write(f'Module {i} Location : {os.popen("wmic memorychip get devicelocator").read().split()[i+1]}'+"\n")
        writeToFile.write("\n"+"-"*5+f"End of module {i} data"+"-"*5+"\n")
        
    writeToFile.write("\n"+"-"*10+"Whole memory data"+"-"*10+"\n"+"\n")
    writeToFile.write(f"Total : {bytestoint(psutil.virtual_memory().total)}"+"\n")
    writeToFile.write(f'Available : {bytestoint(psutil.virtual_memory().available)}'+"\n")
    writeToFile.write(f'Used : {bytestoint(psutil.virtual_memory().used)}'+"\n")
    writeToFile.write(f'Percent : {psutil.virtual_memory().percent}%'+"\n")
    writeToFile.write(f'TotalSwap : {bytestoint(psutil.swap_memory().total)}'+"\n")
    writeToFile.write(f'FreeSwap : {bytestoint(psutil.swap_memory().free)}'+"\n")
    writeToFile.write(f'UsedSwap : {bytestoint(psutil.swap_memory().used)}'+"\n")
    writeToFile.write(f'SwapPercentage : {psutil.swap_memory().percent}%'+"\n")
    
    writeToFile.write("\nMotherboard Details: \n\n")
    for v in vars(Mobo).values():
        moboValues = str(v)
        if not "__" in moboValues:
            if not moboValues == "None":
                writeToFile.write(f"{moboValues}\n".replace(",", "").replace("(","").replace(")", "").replace("'",""))
                
    writeToFile.write("\nSystem Details: \n\n")
    for v in vars(System).values():
        sysValues = str(v)
        if not "__" in sysValues:
            if not sysValues == "None":
                writeToFile.write(f"{sysValues}\n")
                
    writeToFile.write("\nDisk Details: \n")
    diskNameList = os.popen("wmic diskdrive get model").read().removeprefix("Model").strip().split('\n')
    diskNames = []
    for i in diskNameList:
        i = i.strip()
        diskNames = [i for i in diskNames if i]
        diskNames.append(i)
        
    for i in range(len(diskNames)):
        MediaType = os.popen('wmic diskdrive get mediatype').read().removeprefix('MediaType').strip().split('\n')[i]
        writeToFile.write('\n'+"-"*10+f'Disk {i}'+"-"*10+'\n\n')
        writeToFile.write(f"Name : {diskNames[i]}"+"\n"+"\n")
        writeToFile.write(f"Capacity : {bytestoint(int(os.popen('wmic diskdrive get size').read().split()[i+1]))}"+"\n")
        writeToFile.write(f"Sector Size : {bytestoint(int(os.popen('wmic diskdrive get bytespersector').read().split()[i+1]))}"+"\n")
        writeToFile.write(f"Device ID : {os.popen('wmic diskdrive get deviceid').read().split()[i+1]}"+"\n")
        writeToFile.write(f"Firmware Version : {os.popen('wmic diskdrive get firmwarerevision').read().split()[i+1]}"+"\n")
        writeToFile.write(f"Interface : {os.popen('wmic diskdrive get interfacetype').read().split()[i+1]}"+"\n")
        writeToFile.write(f"Media Type : {MediaType}"+"\n")
        writeToFile.write(f"Serial Number : {os.popen('wmic diskdrive get serialnumber').read().split()[i+1]}"+"\n")
        writeToFile.write('\n'+'-'*10+f'End of disk {i} data'+'-'*10+"\n")
        
    writeToFile.write("\nGPU Details: \n\n")

    gpus = GPUtil.getGPUs()
                
    for gpu in gpus:
        GPUID = gpu.id
        GPUName = gpu.name
        CurrentGPULoad = gpu.load*100
        FreeGPUMemory = gpu.memoryFree
        UsedGPUMemory = gpu.memoryUsed
        TotalGPUMemory = gpu.memoryTotal
        CurrentGPUTemperature = gpu.temperature
        GPUUUID = gpu.uuid
    
    writeToFile.write(f'ID : {GPUID}'+'\n')
    writeToFile.write(f'Name : {GPUName}'+'\n')
    writeToFile.write(f'Load : {round(int(CurrentGPULoad))}%'+'\n')
    writeToFile.write(f'Free Memory : {int(FreeGPUMemory)} MiB'+'\n')
    writeToFile.write(f'Used Memory : {int(UsedGPUMemory)} MiB'+'\n')
    writeToFile.write(f'Total Memory : {int(TotalGPUMemory)} MiB'+'\n')
    writeToFile.write(f'Temperature : {CurrentGPUTemperature} ' + u"\xc2\xb0" + 'C' +'\n')
    writeToFile.write(f'UUID : {GPUUUID}'+'\n')
    
    writeToFile.write("------------------End of hardware section------------------")
    
    writeToFile.write("\nNetworking Details: \n\n")
    
    command = os.popen("ipconfig /all").read().split('\n')
    
    for i in command:
        writeToFile.write(i)
    
    writeToFile.write("\n"+"-"*50)