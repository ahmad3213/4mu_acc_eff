from ROOT import *
from math import *
from LoadData_JJ_eff import *
from sample_shortnames_JJ_eff import *
import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *
from inputs_sig_JJpT2mu_rapidity2mu_inc import *
from inputs_sig_JJpT2mu_rapidity2mu_eff_inc import *
from inputs_sig_JJpT2mu_pT2mu_evteff_inc import *
List = []
for long, short in sample_shortnames.iteritems():
    List.append(long)
print '\documentclass{article}'
print '\usepackage[utf8]{inputenc}'
print '\\begin{document}'
channel = '4mu'
OBSNAME = 'pT2mu_rapidity2mu'
OBSNAME_2 = 'pT2mu_pT2mu'
i_sample = 0
factors = ['acc_eta','acc_pteta','recoeff','recoeff_id','recoeff_id_vtx','recoeff_trg_evt','recoeff_evt']
print '\\begin{table}[htb!]'
print '\\begin{tabular}{|c|c|c|c|c|c|c|c|c|}'
print '\\hline'
print 'SAMPLE & acc(eta) & acc(pt) & recoeff & id($#mu$) & vtx(2#mu) & HLT & cuts(4#mu) & total \\\\'
print '\\hline'
temp = ''
prod = 1.0 
for Sample in List:
    i_sample = i_sample+1
    sample_test = sample_shortnames[Sample].replace('_','-')
    shortname_temp = sample_test.split('to4mu')[0]
    shortname = sample_shortnames[Sample]
    temp = temp + shortname_temp+' & '
    prod = 1.0
    for acc_eff in factors:
        if (acc_eff == 'recoeff_trg_evt') or (acc_eff == 'recoeff_evt'):
            processBin = shortname+'_'+channel+'_'+OBSNAME_2+'_genbin0_genbin0'
        else: 
            processBin = shortname+'_'+channel+'_'+OBSNAME+'_genbin0_genbin0'
        if (acc_eff == 'acc_eta'):
    		temp = temp+str(round(acc_a_eta[processBin]*acc_b_eta[processBin],2))+' & '
                prod = prod*acc_a_eta[processBin]*acc_b_eta[processBin]
        if (acc_eff == 'acc_pteta'):
    	        temp = temp+str(round(acc_a_etapt[processBin]*acc_b_etapt[processBin],2))+' & '
                prod = prod*acc_a_etapt[processBin]*acc_b_etapt[processBin]
        if (acc_eff == 'recoeff'):
    		temp= temp+str(round(recoeff_a[processBin]*recoeff_b[processBin],2))+' & '
                prod = prod*recoeff_a[processBin]*recoeff_b[processBin]
        if (acc_eff == 'recoeff_id'):
    		temp = temp+str(round(recoeff_id_a[processBin]*recoeff_id_b[processBin],2))+' & ' 
                prod = prod*recoeff_id_a[processBin]*recoeff_id_b[processBin]
        if (acc_eff == 'recoeff_id_vtx'):
    		temp = temp+str(round(recoeff_id_vtx_a[processBin]*recoeff_id_vtx_b[processBin],2))+' & '
                prod = prod*recoeff_id_vtx_a[processBin]*recoeff_id_vtx_b[processBin]
    	if (acc_eff == 'recoeff_trg_evt'):
 		temp = temp+str(round(recoeff_trg_evt[processBin],2))+' & '
                prod = prod*recoeff_trg_evt[processBin]
        if (acc_eff == 'recoeff_evt'):
    		temp = temp+str(round(recoeff_evt[processBin],2))+' & '
                prod = prod*recoeff_evt[processBin]
    temp =temp+str(round(prod,6))+'\\\\'  
print temp
print '\\hline'
print '\end{tabular}'
print '\caption{acceptance and efficiency factors}'
print '\end{table}'
print '\end{document}'
