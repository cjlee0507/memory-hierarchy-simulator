# Memory Hierarchy Simulator

A Python simulator that models how a CPU memory hierarchy handles a stream of memory references. It simulates a data TLB, a page table, an L1 data cache, and an L2 cache, then reports per-reference results and hit/miss statistics for each level.

Built for COSC 530 at the University of Tennessee, Knoxville.

## Features

- **Configurable hierarchy**: sets, associativity, line sizes, and page sizes are all read from a config file, with validation (powers of two, maximum sizes).
- **Virtual to physical translation** through a DTLB and page table, including page faults.
- **LRU replacement** for the DTLB, page table, L1, and L2.
- **Write policies**: write-back with write-allocate, or write-through with no write-allocate, for both L1 and L2.
- **Inclusive caching**: lines in L1 are always present in L2, and a page fault invalidates the matching DTLB entries and cache lines.
- **Optional components**: virtual addressing, the TLB, and the L2 can each be turned off.

## How to run

Requires Python 3 (standard library only).

```bash
python memhier.py < sample_trace.dat                  # uses ./trace.config
python memhier.py my.config < my_trace.dat            # custom config
```

### Trace format

Each line is an access type (`R` or `W`) and a hex address:

```
R:0a10
W:0a14
R:1f20
```

### Config format

See [`trace.config`](trace.config) for a full example. It sets the number of sets and set size for each level, line sizes, the page table size, the write policy (`y`/`n` for write-through/no write-allocate), and whether virtual addresses, the TLB, and the L2 are enabled.

## Output

1. The hierarchy configuration, including the index and offset bit widths for each level.
2. A row per reference: virtual address, page number, page offset, TLB tag/index/result, page table result, physical page, L1 tag/index/result, and L2 tag/index/result.
3. Summary statistics: hits, misses, and hit ratio for each level; read/write counts; and main memory, page table, and disk reference totals.

Example summary from `sample_trace.dat`:

```
dtlb hits        : 8
dtlb misses      : 7
dtlb hit ratio   : 0.533333

dc hits          : 7
dc misses        : 8
dc hit ratio     : 0.466667
```
