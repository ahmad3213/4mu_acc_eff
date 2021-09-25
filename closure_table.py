from ROOT import *
from math import *

from LoadData_JJ_eff import *
from sample_shortnames_JJ import *
import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *

_temp = __import__('closure_test_results', globals(), locals(), ['closure_results'], -1)
closure_results = _temp.closure_results
List = []
Weight_From = ['SPS','DPS','Mix','HJJ']
for long, short in sample_shortnames.iteritems():
    List.append(long)
i_sample = -1
for Sample in List:
    i_sample = i_sample+1
    shortname = sample_shortnames[Sample]
    processBin = shortname+'_'+channel+'_'+OBSNAME
    print '\documentclass{article}'
    print '\usepackage[utf8]{inputenc}'
    print '\\begin{document}'
    print '\\begin{table}[]'
    print '\centering'
    print '\\begin{tabular}{c|c}'
    print '\end{tabular}'
    print '\caption{Caption}' 
    print '\label{tab:my_label}'
    print '\end{table}'
    print '\end{document}'
