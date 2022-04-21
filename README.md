# EZPCSpec
An easy and fast way to look at all specs detectable in your computer. 

# What is it?

EZPCSpec is a fast, free and very intuitive way to look at all components detected in your system currently*

*Components like the power supply cannot be detected as it is not digitally connected to the motherboard or CPU

# How do you make it work?

* First, you download either the executable or the raw Python file. Make sure the contents are extracted first into a folder
* Next, you execute or run the file
* Finally, you open the "Systeminfo.txt" file that will be made in the same directory as the source file or executable was placed.

# What does it scan?

* Operating System (OS) information (Base Operating System, Operating System Version, Operating System Architecture)
* Boot time
* CPU Information (Name, Vendor ID String, Architecture, xXX Architecture (x64, x86), Frequency (GHz & Hz), Physical Cores, Logical Cores, L2 Cache, L3 Cache)**
* Motherboard Information (Manufacturer, Name (Based on Vendor ID), Serial Number, Version)
* Memory Information (Total Memory, Available Memory, Used Memory, Memory Percentage, Total Swap, Available Swap, Free Swap, Swap Percentage)
* Disk Information (Path, Total Capacity, Used Capacity, Free Capacity, Percentage, File System Type, Mountpoint)
* Network information (Physical and Virtual Networks / Drivers / Devices, IP Addresses, MAC Addresses, Default Gateway, Subnet Mask, DCHP)
* GPU Information (GPU ID, Name, Current Load, Free Memory, Used Memory, Total Memory, Temperature, UUID)

**L1 Cache is not available in software. Email me if you know a way to implement it. Would be much appreciated

# What do I need to get started?

* Python with pip support
* Windows 10 or newer
* If running the raw python code:
*   Libraries:
*     platform
*     cpuinfo
*     sys
*     os
*     psutil
*     gputil
*     tabulate
*     datetime

(Big thanks to all that made the above iibraries)

# Thanks for checking my project out!
  @GitBingus
