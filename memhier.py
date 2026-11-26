import math
import sys 
from collections import OrderedDict

CONFIG_PATH = sys.argv[1] if len(sys.argv) > 1 else "trace.config"
with open(CONFIG_PATH, "r") as config_file: #get data from config file
    for line in config_file:
        line = line.strip()
        if line.startswith("Data TLB configuration"):
            temp = next(config_file)
            dtlb_sets = int(temp.split(":")[1].strip())
            temp = next(config_file)
            dtlb_set_size = int(temp.split(":")[1].strip())
        elif line.startswith("Page Table configuration"):
            temp = next(config_file)
            pt_virtual_pages = int(temp.split(":")[1].strip())
            temp = next(config_file)
            pt_physical_pages = int(temp.split(":")[1].strip())
            pt_page_size = int(next(config_file).split(":")[1].strip())
        elif line.startswith("Data Cache configuration"):
            temp = next(config_file)
            dc_sets = int(temp.split(":")[1].strip())
            temp = next(config_file)
            dc_set_size = int(temp.split(":")[1].strip())
            temp = next(config_file)
            dc_line_size = int(temp.split(":")[1].strip())
            temp = next(config_file)
            dc_write_policy = temp.split(":")[1].strip()
        elif line.startswith("L2 Cache configuration"):
            temp = next(config_file)
            l2_sets = int(temp.split(":")[1].strip())
            temp = next(config_file)
            l2_set_size = int(temp.split(":")[1].strip())
            temp = next(config_file)
            l2_line_size = int(temp.split(":")[1].strip())
            temp = next(config_file)
            l2_write_policy = temp.split(":")[1].strip()
        elif line.startswith("Virtual addresses"):
            virtual_addresses = line.split(":")[1].strip()
        elif line.startswith("TLB"):
            tlb_enabled = line.split(":")[1].strip()
        elif line.startswith("L2 cache"):
            l2_cache_enabled = line.split(":")[1].strip()

dtlb_index_bits = int(math.log2(dtlb_sets)) #calculate bits
dtlb_offset_bits = int(math.log2(pt_page_size))
pt_index_bits = int(math.log2(pt_virtual_pages))
pt_offset_bits = int(math.log2(pt_page_size))
dc_index_bits = int(math.log2(dc_sets))
dc_offset_bits = int(math.log2(dc_line_size))
l2index_bits = int(math.log2(l2_sets))
l2offset_bits = int(math.log2(l2_line_size))

physOffset = int(math.log2(pt_page_size))
physIndex = int(math.log2(pt_physical_pages))


def printConfig(): #print config information
    if dtlb_set_size > 8: #error check
        print('hierarchy: error - dtlb set size requested exceeds MAXSETSIZE')
        exit()
    if dtlb_sets > 256:
        print('hierarchy: error - number of dtlb sets requested exceeds MAXTLBSETS')
        exit()
    print(f"Data TLB contains {dtlb_sets} sets.")
    if not math.log2(dtlb_sets).is_integer():
        print("hierarchy: number of dtlb sets is not a power of two")
        exit() 
    print(f"Each set contains {dtlb_set_size} entries.")
    print(f"Number of bits used for the index is {dtlb_index_bits}.\n")
    if int(pt_virtual_pages) > 8192:
        print('hierarchy: error - number of virtual pages requested exceeds MAXVIRTPAGES')
        exit()
    if int(pt_physical_pages) > 1024:
        print('hierarchy: error - number of virtual pages requested exceeds MAXVIRTPAGES')
        exit()
    print(f"Number of virtual pages is {pt_virtual_pages}.")
    if not math.log2(pt_virtual_pages).is_integer():
        print("hierarchy: number of virtual pages is not a power of two")
        exit() 
    print(f"Number of physical pages is {pt_physical_pages}.")
    if not math.log2(pt_physical_pages).is_integer():
        print("hierarchy: number of physical pages is not a power of two")
        exit() 
    print(f"Each page contains {pt_page_size} bytes.")
    if not math.log2(pt_page_size).is_integer():
        print("hierarchy: page size is not a power of two")
        exit() 
    print(f"Number of bits used for the page table index is {pt_index_bits}.")
    print(f"Number of bits used for the page offset is {pt_offset_bits}.\n")
    if dc_set_size > 8:
        print('hierarchy: error - data cache set size requested exceeds MAXSETSIZE')
        exit()
    if int(dc_sets) > 8192:
        print('hierarchy: error - number of dc sets requested exceeds MAXDCSETS')
        exit()
    if dc_line_size < 8 :
        print('hierarchy: data cache line size is less than MINDCLINESIZE')
        exit()
    print(f"D-cache contains {dc_sets} sets.")
    if not math.log2(dc_sets).is_integer():
        print("hierarchy: number of dc sets is not a power of two")
        exit() 

    print(f"Each set contains {dc_set_size} entries.")
    print(f"Each line is {dc_line_size} bytes.")
    if not math.log2(dc_line_size).is_integer():
        print("hierarchy: number of bytes in dc line is not a power of two")
        exit() 
    if dc_write_policy == 'n':
        print(f"The cache uses a write-allocate and write-back policy.")
    elif dc_write_policy == 'y':
        print(f"The cache uses a no write-allocate and write-through policy.")
    print(f"Number of bits used for the index is {dc_index_bits}.")
    print(f"Number of bits used for the offset is {dc_offset_bits}.\n")


    if l2_line_size < 8 :
        print('hierarchy: L2 cache line size is less than MINL2LINESIZE')
        exit()
    if l2_set_size > 8:
        print('hierarchy: error - L2 cache set size requested exceeds MAXSETSIZE')
        exit()
    if l2_line_size < dc_line_size:
        print("hierarchy: L2 cache line size must be >= to the data cache line size")
        exit()
    print(f"L2-cache contains {l2_sets} sets.")
    if not math.log2(l2_sets).is_integer():
        print("hierarchy: number of L2 sets is not a power of two")
        exit() 
    print(f"Each set contains {l2_set_size} entries.")
    print(f"Each line is {l2_line_size} bytes.")
    if not math.log2(l2_line_size).is_integer():
        print("hierarchy: number of bytes in L2 line is not a power of two")
        exit() 


    if l2_write_policy == 'n':
        print(f"The cache uses a write-allocate and write-back policy.")
    elif l2_write_policy == 'y':
        print(f"The cache uses a no write-allocate and write-through policy.")
    print(f"Number of bits used for the index is {l2index_bits}.")
    print(f"Number of bits used for the offset is {l2offset_bits}.\n")

    if virtual_addresses == 'y':
        print('The addresses read in are virtual addresses.')
    elif virtual_addresses == 'n':
        print('The addresses read in are physical addresses.')
    if tlb_enabled == 'y':
        pass
    elif tlb_enabled == 'n':
        print('TLB is disabled in this configuration.')
    if l2_cache_enabled == 'y':
        pass
    elif l2_cache_enabled == 'n':
        print('L2 cache is disabled in this configuration.')
    print()

#dc tag = total - index - offset
#ordered dictionary to mimic LRU 

class printData: #data to print
    def __init__(self):
        self.virtualAddress = ""
        self.virtualPageNum = ""
        self.pageOffset = ""
        self.TLBTag = ""
        self.TLBIndex = ""
        self.TLBRef = ""
        self.ptRef = ""
        self.physPageNum = ""
        self.cacheTag = ""
        self.cacheIndex = ""
        self.cacheRef = ""
        self.L2Tag = ""
        self.L2Ind = ""
        self.L2Res = ""
        self.temp = ""

DCACHE = dict() #dict to hold d cache 
TLB = dict() #dict to hold TLB 
PT = OrderedDict() #dict to hold Page table 
L2CACHE = dict() #dict to hold l2 cache


dtlbhits = 0 #stats
dtlbmisses = 0
pthits = 0
ptfaults = 0
dchits = 0
dcmisses = 0
l2hits = 0
l2misses = 0
totalreads = 0
totalwrites = 0
mainmemoryref = 0
pagetableref = 0
diskmemoryref = 0

printConfig()

traceIndex = 0
traceData = []
for trace in sys.stdin.readlines():
    traceIndex += 1
    traceData.append(printData())
    traceNum = int(trace[2:].strip(), 16)
    binary = str(bin(int(trace[2:], 16)).replace("0b", "").zfill(32))
    if virtual_addresses == 'y':
        offsetBits = int(math.log2(pt_page_size)) # of 1's of bits
        maskTemp = (1 << offsetBits) - 1
        offset = traceNum & maskTemp
        TLBtag = int(trace[2:], 16) >> (pt_offset_bits + dtlb_index_bits)
        TLBindex = int(trace[2:], 16) >> (pt_offset_bits) & ((1 << dtlb_index_bits) - 1)
        vpn = traceNum >> (offsetBits)
        traceData[traceIndex - 1].virtualAddress = trace[2:].replace("\n", "").zfill(8)
        #print(TLBindex)
        #vpn key
        #len(tlb) value
        if tlb_enabled == 'y': #if TLB enabled
            if TLBindex not in TLB: #if not in tlb, make new OrderedDict for LRU
                TLB[TLBindex] = OrderedDict()
            
            TLBtemp = TLB[TLBindex]
            if vpn in TLBtemp: #TLB hit
                #print(traceIndex)

                dtlbhits += 1
                #print(dtlbhits)
                traceData[traceIndex - 1].TLBRef = 'hit'
                traceData[traceIndex - 1].TLBTag = hex(TLBtag)
                traceData[traceIndex - 1].TLBIndex = hex(TLBindex)
                TLBtemp.move_to_end(vpn) #LRU
            else: #TLB miss
                dtlbmisses += 1 #increment dtlb misses
                pagetableref += 1 #increment page talbe refs
                traceData[traceIndex - 1].TLBRef = 'miss'
                traceData[traceIndex - 1].TLBTag = hex(TLBtag)
                traceData[traceIndex - 1].TLBIndex = hex(TLBindex)
                if vpn in PT: #PT hit
                    pthits += 1
                    traceData[traceIndex - 1].ptRef = 'hit'
                    PT.move_to_end(vpn) #LRU
                else: #PT miss
                    ptfaults += 1
                    traceData[traceIndex - 1].ptRef = 'miss'
                    diskmemoryref += 1
                    if len(PT) >= pt_physical_pages: #if the PT is full, evict
                        temp = PT.popitem(last=False)
                        PT[vpn] = temp[1]
                        PT.move_to_end(vpn)
                    else: #if the PT has space, store
                        PT[vpn] = len(PT)
                        PT.move_to_end(vpn)

                if len(TLBtemp) >= dtlb_set_size: #if TLB is full, evict
                    temp1 = TLBtemp.popitem(last=False)
                TLBtemp[vpn] = PT[vpn] #store
                TLBtemp.move_to_end(vpn)

            #print(TLB)
            #print(TLBtemp[vpn])
            #print(TLB[TLBindex][vpn])
            traceNum = (TLBtemp[vpn] << offsetBits) | offset #new address = page number + offset
            
            #print(traceNum)
            offsetBits = int(math.log2(dc_line_size)) # of 1's of bits
            maskTemp = (1 << offsetBits) - 1
            offset = traceNum & maskTemp
            indexBits = int(math.log2(dc_sets))
            maskTemp = (1 << indexBits) - 1
            index = (traceNum >> offsetBits) & maskTemp
            tag = traceNum >> (offsetBits + indexBits) #when we make tag, do we do the same calculations as we did for dcache earlier?
            traceData[traceIndex - 1].virtualAddress = trace[2:].replace("\n", "").zfill(8)

            if index not in DCACHE:
                DCACHE[index] = OrderedDict()

            # index is the set
            # tag is the associativity
            temp = DCACHE[index]
            if tag in temp: #if cache hit

                if trace[0:1] == 'W':
                    totalwrites += 1 #increment total writes
                    temp[tag] = 1 #change to dirty bit since write
                elif trace[0:1] == 'R':
                    totalreads += 1 #increment total reads
                temp.move_to_end(tag)
                traceData[traceIndex - 1].cacheRef = 'hit'
                dchits += 1 
                traceData[traceIndex - 1].physPageNum = hex(traceNum >> physOffset)
                traceData[traceIndex - 1].pageOffset = hex(traceNum & (pt_page_size - 1))
                traceData[traceIndex - 1].cacheTag = hex(tag)
                traceData[traceIndex - 1].cacheIndex = hex(index)
                traceData[traceIndex - 1].virtualPageNum = hex(vpn)

            else: #if cache miss
                if len(temp) >= dc_set_size:
                    test = temp.popitem(last=False)
                    if l2_cache_enabled == 'n': #if l2 not enabled
                        if test[1] == 1: #check for dirty bit, if there is one, increment main memory reference
                            mainmemoryref += 1 
                if l2_cache_enabled == 'n': #if l2 not enabled
                    mainmemoryref += 1 #increase main memory ref
                if trace[0:1] == 'R':
                    totalreads += 1 #increment if read
                    temp[tag] = 0 #dirty bit = 0
                elif trace[0:1] == 'W':
                    totalwrites += 1 #increment if write
                    temp[tag] = 1 #dirty bit = 1
                temp.move_to_end(tag) #LRU
                traceData[traceIndex - 1].cacheRef = 'miss'
                dcmisses += 1
                traceData[traceIndex - 1].physPageNum = hex(traceNum >> physOffset)
                traceData[traceIndex - 1].pageOffset = hex(traceNum & (pt_page_size - 1))
                traceData[traceIndex - 1].cacheTag = hex(tag)
                traceData[traceIndex - 1].cacheIndex = hex(index)
                traceData[traceIndex - 1].virtualPageNum = hex(vpn)

                # L2 cache
                if l2_cache_enabled == 'y':
                    offsetBits = int(math.log2(l2_line_size))
                    indexBits = int(math.log2(l2_sets))
                    offset_mask = l2_line_size - 1

                    l2offset = traceNum & offset_mask
                    l2index = (traceNum >> offsetBits) & ((1 << indexBits) - 1)
                    l2tag = traceNum >> (offsetBits + indexBits)

                    if l2index not in L2CACHE:
                        L2CACHE[l2index] = OrderedDict()

                    l2temp = L2CACHE[l2index]

                    if l2tag in l2temp: #if L2 hit, LRU and increment hit
                        l2temp.move_to_end(l2tag)
                        l2hits += 1 
                        traceData[traceIndex - 1].L2Tag = hex(l2tag)
                        traceData[traceIndex - 1].L2Ind = hex(l2index)
                        traceData[traceIndex - 1].L2Res = 'hit'

                    else: #else L2 miss
                        mainmemoryref += 1
                        l2misses += 1
                        traceData[traceIndex - 1].L2Tag = hex(l2tag)
                        traceData[traceIndex - 1].L2Ind = hex(l2index)
                        traceData[traceIndex - 1].L2Res = 'miss'

                        if len(l2temp) >= l2_set_size:
                            test = l2temp.popitem(last=False)
                            #print('test', test[0])
                            if test[1] == 1:
                                mainmemoryref += 1
                                
                            for i in range(l2_line_size):
                                tester = (l2tag << (l2index + offsetBits)) | (l2index << offsetBits) | l2offset
                                offsetBits = int(math.log2(dc_line_size)) # of 1's of bits
                                maskTemp = (1 << i) - 1
                                offset = tester & maskTemp
                                indexBits = int(math.log2(dc_sets))
                                maskTemp = (1 << indexBits) - 1
                                index = (tester >> i) & maskTemp
                                tag = tester >> (i + indexBits)
                                if index in DCACHE and tag in DCACHE[index]:
                                    test = DCACHE[index].popitem(tag)
                                    if test[1] == 1:
                                        mainmemoryref += 1
                                    
                        if trace[0:1] == 'R':
                            l2temp[l2tag] = 0 #dirty bit = 0
                        elif trace[0:1] == 'W':
                            l2temp[l2tag] = 1 #dirty bit = 1
                        l2temp.move_to_end(l2tag)

        elif tlb_enabled == 'n': #if TLB not enabled
            pagetableref += 1
            if vpn in PT: #PT hit
                pthits += 1
                traceData[traceIndex - 1].ptRef = 'hit'
                PT.move_to_end(vpn)
            else: #PT miss
                ptfaults += 1
                traceData[traceIndex - 1].ptRef = 'miss'
                diskmemoryref += 1
                if len(PT) >= pt_physical_pages: #if the PT is full
                    temp = PT.popitem(last=False)
                    PT[vpn] = temp[1]
                    PT.move_to_end(vpn)
                else: #if the PT has space
                    PT[vpn] = len(PT)
                    PT.move_to_end(vpn)

            traceNum = (PT[vpn] << offsetBits) | offset #page number + offset
            
            offsetBits = int(math.log2(dc_line_size)) # of 1's of bits
            maskTemp = (1 << offsetBits) - 1
            offset = traceNum & maskTemp
            indexBits = int(math.log2(dc_sets))
            maskTemp = (1 << indexBits) - 1
            index = (traceNum >> offsetBits) & maskTemp
            tag = traceNum >> (offsetBits + indexBits) #when we make tag, do we do the same calculations as we did for dcache earlier?
            traceData[traceIndex - 1].virtualAddress = trace[2:].replace("\n", "").zfill(8)

            if index not in DCACHE:
                DCACHE[index] = OrderedDict()

            # index is the set
            # tag is the associativity
            temp = DCACHE[index]
            if tag in temp: #if cache hit

                if trace[0:1] == 'W':
                    totalwrites += 1
                    temp[tag] = 1
                elif trace[0:1] == 'R':
                    totalreads += 1
                temp.move_to_end(tag)
                traceData[traceIndex - 1].cacheRef = 'hit'
                dchits += 1
                traceData[traceIndex - 1].physPageNum = hex(traceNum >> physOffset)
                traceData[traceIndex - 1].pageOffset = hex(traceNum & (pt_page_size - 1))
                traceData[traceIndex - 1].cacheTag = hex(tag)
                traceData[traceIndex - 1].cacheIndex = hex(index)
                traceData[traceIndex - 1].virtualPageNum = hex(vpn)

            else: #if Dcache miss
                if len(temp) >= dc_set_size:
                    test = temp.popitem(last=False)
                    if test[1] == 1:
                        if l2_cache_enabled == 'n':
                            mainmemoryref += 1
                if l2_cache_enabled == 'n':
                    mainmemoryref += 1
                if trace[0:1] == 'R':
                    totalreads += 1
                    temp[tag] = 0
                elif trace[0:1] == 'W':
                    totalwrites += 1
                    temp[tag] = 1
                temp.move_to_end(tag)
                traceData[traceIndex - 1].cacheRef = 'miss'
                dcmisses += 1
                traceData[traceIndex - 1].physPageNum = hex(traceNum >> physOffset)
                traceData[traceIndex - 1].pageOffset = hex(traceNum & (pt_page_size - 1))
                traceData[traceIndex - 1].cacheTag = hex(tag)
                traceData[traceIndex - 1].cacheIndex = hex(index)
                traceData[traceIndex - 1].virtualPageNum = hex(vpn)

                if l2_cache_enabled == 'y':
                    offsetBits = int(math.log2(l2_line_size))
                    indexBits = int(math.log2(l2_sets))

                    l2index = (traceNum >> offsetBits) & ((1 << indexBits) - 1)
                    l2tag = traceNum >> (offsetBits + indexBits)

                    if l2index not in L2CACHE:
                        L2CACHE[l2index] = OrderedDict()

                    l2temp = L2CACHE[l2index]

                    if l2tag in l2temp: #if L2 hit, LRU and increment hit
                        # if trace[0:1] == 'W':
                        #     totalwrites += 1
                        #     l2temp[l2tag] = 1
                        # elif trace[0:1] == 'R':
                        #     totalreads += 1
                        l2temp.move_to_end(l2tag)
                        l2hits += 1
                        traceData[traceIndex - 1].L2Tag = hex(l2tag)
                        traceData[traceIndex - 1].L2Ind = hex(l2index)
                        traceData[traceIndex - 1].L2Res = 'hit'
                        
                    else: 
                        mainmemoryref += 1
                        l2misses += 1
                        traceData[traceIndex - 1].L2Tag = hex(l2tag)
                        traceData[traceIndex - 1].L2Ind = hex(l2index)
                        traceData[traceIndex - 1].L2Res = 'miss'

                        if len(l2temp) >= l2_set_size:
                            test = l2temp.popitem(last=False)
                            if test[1] == 1:
                                mainmemoryref += 1
                            test = temp.popitem(test[0])
                        l2temp[l2tag] = 0
                        l2temp.move_to_end(l2tag)
            
    elif virtual_addresses == 'n':
        offsetBits = int(math.log2(dc_line_size)) # of 1's of bits
        maskTemp = (1 << offsetBits) - 1
        offset = traceNum & maskTemp
        indexBits = int(math.log2(dc_sets))
        maskTemp = (1 << indexBits) - 1
        index = (traceNum >> offsetBits) & (maskTemp)
        tag = traceNum >> (offsetBits + indexBits)
        traceData[traceIndex - 1].virtualAddress = trace[2:].replace("\n", "").zfill(8)

        if index not in DCACHE:
            DCACHE[index] = OrderedDict()

        # index is the set
        # tag is the associativity
        temp = DCACHE[index]
        if tag in temp: #if cache hit

            if trace[0:1] == 'W':
                totalwrites += 1
                temp[tag] = 1
            elif trace[0:1] == 'R':
                totalreads += 1
            temp.move_to_end(tag)
            traceData[traceIndex - 1].cacheRef = 'hit'
            dchits += 1
            traceData[traceIndex - 1].physPageNum = hex(traceNum >> physOffset)
            traceData[traceIndex - 1].pageOffset = hex(traceNum & (pt_page_size - 1))
            traceData[traceIndex - 1].cacheTag = hex(tag)
            traceData[traceIndex - 1].cacheIndex = hex(index)

        else: #if cache miss
            if len(temp) >= dc_set_size:
                test = temp.popitem(last=False)
                if test[1] == 1:
                    mainmemoryref += 1
            mainmemoryref += 1
            if trace[0:1] == 'R':
                totalreads += 1
                temp[tag] = 0
            elif trace[0:1] == 'W':
                totalwrites += 1
                temp[tag] = 1
            temp.move_to_end(tag)
            traceData[traceIndex - 1].cacheRef = 'miss'
            dcmisses += 1
            traceData[traceIndex - 1].physPageNum = hex(traceNum >> physOffset)
            traceData[traceIndex - 1].pageOffset = hex(traceNum & (pt_page_size - 1))
            traceData[traceIndex - 1].cacheTag = hex(tag)
            traceData[traceIndex - 1].cacheIndex = hex(index)
            if l2_cache_enabled == 'y':
                offsetBits = int(math.log2(l2_line_size))
                indexBits = int(math.log2(l2_sets))
                offset_mask = l2_line_size - 1

                l2offset = traceNum & offset_mask
                l2index = (traceNum >> offsetBits) & ((1 << indexBits) - 1)
                l2tag = traceNum >> (offsetBits + indexBits)

                if l2index not in L2CACHE:
                    L2CACHE[l2index] = OrderedDict()

                l2temp = L2CACHE[l2index]

                if l2tag in l2temp: #if L2 hit, LRU and increment hit
                    l2temp.move_to_end(l2tag)
                    l2hits += 1 
                    traceData[traceIndex - 1].L2Tag = hex(l2tag)
                    traceData[traceIndex - 1].L2Ind = hex(l2index)
                    traceData[traceIndex - 1].L2Res = 'hit'

                else: #else L2 miss
                    mainmemoryref += 1
                    l2misses += 1
                    traceData[traceIndex - 1].L2Tag = hex(l2tag)
                    traceData[traceIndex - 1].L2Ind = hex(l2index)
                    traceData[traceIndex - 1].L2Res = 'miss'

                    if len(l2temp) >= l2_set_size:
                        test = l2temp.popitem(last=False)
                        #print('test', test[0])
                        if test[1] == 1:
                            mainmemoryref += 1

                        for i in range(l2_line_size):
                            tester = (l2tag << (l2index + offsetBits)) | (l2index << offsetBits) | l2offset
                            offsetBits = int(math.log2(dc_line_size)) # of 1's of bits
                            maskTemp = (1 << i) - 1
                            offset = tester & maskTemp
                            indexBits = int(math.log2(dc_sets))
                            maskTemp = (1 << indexBits) - 1
                            index = (tester >> i) & maskTemp
                            tag = tester >> (i + indexBits)
                            if index in DCACHE and tag in DCACHE[index]:
                                test = DCACHE[index].popitem(tag)
                                if test[1] == 1:
                                    mainmemoryref += 1
                                
                    if trace[0:1] == 'R':
                        l2temp[l2tag] = 0 #dirty bit = 0
                    elif trace[0:1] == 'W':
                        l2temp[l2tag] = 1 #dirty bit = 1
                    l2temp.move_to_end(l2tag)

def printInfo():
    if virtual_addresses == 'y' and l2_cache_enabled == 'y':
        print("Virtual  Virt.  Page TLB    TLB TLB  PT   Phys        DC  DC          L2  L2")
        print("Address  Page # Off  Tag    Ind Res. Res. Pg # DC Tag Ind Res. L2 Tag Ind Res.")
        print("-------- ------ ---- ------ --- ---- ---- ---- ------ --- ---- ------ --- ----")
        for a in traceData:
            print(
                f"{str(a.virtualAddress.rjust(8))} {str(a.virtualPageNum[2:].rjust(6))} {str(a.pageOffset[2:].rjust(4))} {str(a.TLBTag[2:]).rjust(6)} "
                f"{str(a.TLBIndex[2:]).rjust(3)} {a.TLBRef.ljust(4)} {a.ptRef.ljust(4)} {str(a.physPageNum[2:].rjust(4))} "
                f"{str(a.cacheTag[2:]).rjust(6)} {str(a.cacheIndex[2:]).rjust(3)} {a.cacheRef.ljust(4)} ", end = '')
            if a.cacheRef == 'miss':
                print(f"{str(a.L2Tag[2:]).rjust(6)} {str(a.L2Ind[2:]).rjust(3)} {a.L2Res.ljust(4)}")
            else:
                print()
    elif virtual_addresses == 'n' and l2_cache_enabled == 'n':
        print("Physical Virt.  Page TLB    TLB TLB  PT   Phys        DC  DC          L2  L2")
        print("Address  Page # Off  Tag    Ind Res. Res. Pg # DC Tag Ind Res. L2 Tag Ind Res.")
        print("-------- ------ ---- ------ --- ---- ---- ---- ------ --- ---- ------ --- ----")
        for a in traceData:
            print(
                f"{str(a.virtualAddress).rjust(8)} {str(a.virtualPageNum[2:].rjust(6))} {str(a.pageOffset[2:].rjust(4))} {str(a.TLBTag[2:]).rjust(6)} "
                f"{str(a.TLBIndex[2:]).rjust(3)} {a.TLBRef.ljust(4)} {a.ptRef.ljust(4)} {str(a.physPageNum[2:].rjust(4))} "
                f"{str(a.cacheTag[2:]).rjust(6)} {str(a.cacheIndex[2:]).rjust(3)} {a.cacheRef.ljust(4)} {a.L2Tag}"
                )
    elif virtual_addresses == 'n' and l2_cache_enabled == 'y':
        print("Physical Virt.  Page TLB    TLB TLB  PT   Phys        DC  DC          L2  L2")
        print("Address  Page # Off  Tag    Ind Res. Res. Pg # DC Tag Ind Res. L2 Tag Ind Res.")
        print("-------- ------ ---- ------ --- ---- ---- ---- ------ --- ---- ------ --- ----")
        for a in traceData:
            print(
                f"{str(a.virtualAddress).rjust(8)} {str(a.virtualPageNum[2:].rjust(6))} {str(a.pageOffset[2:].rjust(4))} {str(a.TLBTag[2:]).rjust(6)} "
                f"{str(a.TLBIndex[2:]).rjust(3)} {a.TLBRef.ljust(4)} {a.ptRef.ljust(4)} {str(a.physPageNum[2:].rjust(4))} "
                f"{str(a.cacheTag[2:]).rjust(6)} {str(a.cacheIndex[2:]).rjust(3)} {a.cacheRef.ljust(4)} {str(a.L2Tag[2:]).rjust(6)} {str(a.L2Ind[2:]).rjust(3)} {a.L2Res.ljust(4)}{a.temp}"
                )
    elif virtual_addresses == 'y' and l2_cache_enabled == 'n':
        print("Virtual  Virt.  Page TLB    TLB TLB  PT   Phys        DC  DC          L2  L2")
        print("Address  Page # Off  Tag    Ind Res. Res. Pg # DC Tag Ind Res. L2 Tag Ind Res.")
        print("-------- ------ ---- ------ --- ---- ---- ---- ------ --- ---- ------ --- ----")
        for a in traceData:
            print(
                f"{str(a.virtualAddress.rjust(8))} {str(a.virtualPageNum[2:].rjust(6))} {str(a.pageOffset[2:].rjust(4))} {str(a.TLBTag[2:]).rjust(6)} "
                f"{str(a.TLBIndex[2:]).rjust(3)} {a.TLBRef.ljust(4)} {a.ptRef.ljust(4)} {str(a.physPageNum[2:].rjust(4))} "
                f"{str(a.cacheTag[2:]).rjust(6)} {str(a.cacheIndex[2:]).rjust(3)} {a.cacheRef.ljust(4)} {a.L2Tag}"
                )
    print()

def calcRatio(hits, misses):
    if hits + misses == 0:
        return None
    return hits / (hits + misses)

def printStats():
    print('Simulation statistics\n')
    print('dtlb hits        :', dtlbhits)
    print('dtlb misses      :', dtlbmisses)
    ratio = calcRatio(dtlbhits, dtlbmisses)
    if ratio == None:
        result = "N/A"
    else:
        result = f"{ratio:.6f}"
    print(f'dtlb hit ratio   : {result}')
    print()

    print('pt hits          :', pthits)
    print('pt faults        :', ptfaults)
    ratio = calcRatio(pthits, ptfaults)
    if ratio == None:
        result = "N/A"
    else:
        result = f"{ratio:.6f}"
    print(f'pt hit ratio     : {result}')
    print()

    print('dc hits          :', dchits)
    print('dc misses        :', dcmisses)
    ratio = calcRatio(dchits, dcmisses)
    if ratio == None:
        result = "N/A"
    else:
        result = f"{ratio:.6f}"
    print(f'dc hit ratio     : {result}')
    print()

    print('L2 hits          :', l2hits)
    print('L2 misses        :', l2misses)
    ratio = calcRatio(l2hits, l2misses)
    if ratio == None:
        result = "N/A"
    else:
        result = f"{ratio:.6f}"
    print(f'L2 hit ratio     : {result}')
    print()

    print('Total reads      :', totalreads)
    print('Total writes     :', totalwrites)
    ratio = calcRatio(totalreads, totalwrites)
    if ratio == None:
        result = "N/A"
    else:
        result = f"{ratio:.6f}"
    print(f'Ratio of reads   : {result}')
    print()

    print('main memory refs :', mainmemoryref)
    print('page table refs  :', pagetableref)
    print('disk refs        :', diskmemoryref)

printInfo()
printStats()