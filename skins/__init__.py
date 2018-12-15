import commands

#!cpu
def __cpu_count():
    with open('/proc/stat', 'r') as f:
        data = f.readlines()
    nb = -1
    for line in data:
        if line.startswith('cpu'): nb += 1
    return nb

def __cpu_stat(proc_num=0):
    with open('/proc/stat', 'r') as f:
        data = f.readlines()
    if proc_num == 0: suffix = ''
    else: suffix = str(proc_num - 1)
    line = data[proc_num]
    if line.startswith('cpu%s ' % suffix):
        junk, cuse, cn, csys, tail = line.split(None, 4)
        if suffix == '':
            return (int(cuse) +int(csys) +int(cn)) /__cpu_count()
        else:
            return int(cuse) +int(cn)
    return 0

__cpu = 0
def cpu_x(proc_num=0):
    global __cpu
    cpu = __cpu_stat(proc_num)
    p = cpu -__cpu
    __cpu = cpu
    return int(p)

def cpu_freq():
    with open('/proc/cpuinfo', 'r') as f:
        data = f.readlines()
    for l in data:
        if l.startswith('cpu MHz'): break
    op = l.split(': ')[1].split('.')[0]
    return int(op)

#!mem
def __mem_info():
    with open('/proc/meminfo', 'r') as f:
        data = f.readlines()
    mem = {}
    for l in data:
        for i in ('MemTotal','MemFree','Cached','Buffers'):
            if l.startswith(i):
                c = l.index(':')
                e = l.index('kB')
                mem[l[:c].replace('Mem','')] = int(l[c+1:e])
        if len(mem) >= 4: break
    return mem

def mem_x():
    m = __mem_info()
    f = m['Total'] -m['Cached'] -m['Buffers'] -m['Free']
    p = 100 *(f) /m['Total']
    return int(p)

def mem_free():
    m = __mem_info()
    return int(m['Cached'] +m['Buffers'] +m['Free'] /1024)

def mem_used():
    m = __mem_info()
    return int(m['Total'] -m['Cached'] -m['Buffers'] -m['Free'] /1024)

#!nvidia
def gpu_temp():
    op = commands.getoutput('nvidia-settings -q GPUCoreTemp -t')
    try: return int(op)
    except: return 0

def gpu_type():
    op = commands.getoutput('nvidia-settings -q Gpus -t | cut -d "(" -f 2 -s')
    if op[:3] != 'sh:': return op.replace(')','')
    else: return 'unknow gpu type'

#!hdd
def hdd_temp(drive='sda1'):
    op = commands.getoutput('hddtemp -n '+drive)
    try: return int(op)
    except: return 0

#!net
def __net_active():
    return int(commands.getoutput("netstat -n | grep -c tcp"))

def __net_speed(device='lo'):
    with open('/proc/net/dev', 'r') as f:
        data = f.readlines()
    for l in data:
        if device in l:
            v = l.split(':')[1].split()
            dl = float(v[0])
            ul = float(v[8])
            return dl /1024, ul /1024
    return 0, 0

__dl, __ul, __tl = 0, 0, 10
def net_x(device):
    global __dl, __ul, __tl
    dl, ul = __net_speed(device)
    dx = dl -__dl
    ux = ul -__ul
    __ul = dl
    __ul = ul
    if __tl <= dx:
        __tl = dx +10 # kb/s
    #op = commands.getoutput("ifconfig -a %s | grep Byte" % device)
    #bp = [i for i in op.split('  ') if i.startswith('Byte')]
    #print bp
    return int(dx), int(ux)#, int(__tl)

def ip():
    cmd = "ifconfig | grep 'inet:' | cut -d: -f2 | awk '{ print $1}'"
    op = commands.getoutput(cmd)
    for ip in op.split('\n'):
        if ip != '127.0.0.1': break
    return ip
