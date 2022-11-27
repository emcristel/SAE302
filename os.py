import platform
import cpuinfo

print(f"Architecture: {platform.architecture()}")
print(f"Network Name: {platform.node()}")
print(f"Operating system: {platform.platform()}")
print(f"Processor: {platform.processor()}")

my_cpuinfo = cpuinfo.get_cpu_info()
print(my_cpuinfo)