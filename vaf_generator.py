CHROM_INDEX = 0
POS_INDEX = 1
REF_INDEX = 2
DEPTH_INDEX = 3

BASE_INDEX = 5

def get_base_count_dict(base_chunks, sep=':'):
    d = {}
    for chunk in base_chunks:
        base_pieces = chunk.split(sep, 2)
        base = base_pieces[0]
        count = int(base_pieces[1])
        
        d[base] = count
        
    return d

def get_line_info(bamrc_line):
    """Returns chrom, pos, ref, depth, base_dict"""
    bamrc_line = bamrc_line.strip()
    pieces = bamrc_line.split('\t')
    
    chrom = pieces[CHROM_INDEX]
    pos = int(pieces[POS_INDEX])
    ref = pieces[REF_INDEX]
    depth = int(pieces[DEPTH_INDEX])
    
    base_dict = get_base_count_dict(pieces[BASE_INDEX:])
    
    return chrom, pos, ref, depth, base_dict

def calculate_vaf(base_count, depth):
    if depth:
        return base_count / depth
    return 0.0

def get_base_vafs(ref, depth, base_dict):
    """Returns vafs for each base, including a 'minor' vaf representing the combined vaf of all minor alleles"""
    vaf_dict = {}
    
    minor_count = 0
    for base, count in base_dict.items():
        vaf_dict[base] = calculate_vaf(count, depth)
        
        if base != ref:
            minor_count += count
    
    vaf_dict['minor'] = calculate_vaf(minor_count, depth)
    
    return vaf_dict


def process_readcounts(readcount_fp, output_fp):
    f = open(readcount_fp)
    stats = []
    for line in f:
        stats.append(get_line_info(line))

    lines = ['\t'.join(['CHROM', 'POS', 'REF', 'DEPTH', 'MINOR', 'A_vaf', 'C_vaf', 'G_vaf', 'T_vaf', 'N_vaf'])]
    base_order = ['A', 'C', 'G', 'T', 'N']
    for chrom, pos, ref, depth, base_dict in stats:
        vaf_dict = get_base_vafs(ref, depth, base_dict)
        
        l = [chrom, pos, ref, depth] + [vaf_dict['minor']] + [vaf_dict[b] for b in base_order]
        lines.append('\t'.join([str(x) for x in l]))
    
    output = '\n'.join(lines)
    if output_fp is not None:
        f = open(output_fp, 'w')
        f.write(output)
        f.close()
    else:
        print(output)
