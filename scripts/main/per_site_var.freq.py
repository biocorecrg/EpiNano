#!/usr/bin/env python2

import sys
from collections import defaultdict
from collections import OrderedDict
import numpy as np
import warnings
import re

def clear_warnings (fn):
    warnings.filterwarnings('error')
    try:
        return fn
    except RuntimeWarning:
        return 'na'

#sam2tsv file
#READ_NAME      FLAG    CHROM   READ_POS        BASE    QUAL    REF_POS REF     OP
'''
reference position is 1-based
read position is 0-based
'''
qual = defaultdict(list) # qulity scores
mis = defaultdict(int) # mismatches
ins = defaultdict(int) # insertions
dele = defaultdict(int) # deletions
cov = OrderedDict ()  # coverage
ins_q = defaultdict(lambda: defaultdict (list)) # store quality scores of inserted read bases
pos = defaultdict(list) # reference positions
base = {} # ref base
Q = defaultdict(list)
with open (sys.argv[1],'r') as fh:
    for line in fh:
        if line.startswith ('#'):
            continue
        ary = line.strip().split()
        if ary[-1] == 'M':
            k = (ary[2], ary[-3]) # 
            cov[k] = cov.get(k,0) + 1
            qual[k].append (ord(ary[-4])- 33)
            Q[k].append(ary[-4])
            base[k] = ary[-2]
            if (ary[-2] != ary[4]):
                mis[k] +=1
        if ary[-1] == 'D':
            k = (ary[2], ary[-3])
            cov[k] = cov.get(k,0) + 1
            base[k] = ary[-2]
            dele[k] = dele.get(k,0) + 1
        if ary[-1] == 'I':
            k = list (cov.keys())[-1]
            next_k = (ary[2], str(int(k[-1]) + 1))
            if ary[0] not in ins_q[k]:
                ins[k] = ins.get(k,0) + 0.5
                ins[next_k] = ins.get(next_k,0) + 0.5
            ins_q[k][ary[0]].append(ord(ary[-4]) - 33)
            

header = '#Ref,pos,base,cov,mis,ins,del,q_sum'

for k in cov.keys():
    depth = float (cov[k])
    Mis = mis[k]
    Del = dele[k]
    num_ins = 0 
    if k in ins:
        num_ins = ins[k] # len (ins_q[k].keys())
        #qs_ins = ins_q[k].values()
    q_lst = [0]
    if k in qual:
        q_lst = qual[k]	
    inf = map (str, [k[0], k[1], base[k], depth, Mis, num_ins, Del, ':'.join (map (str, q_lst))])
    print ",".join ( inf) 
