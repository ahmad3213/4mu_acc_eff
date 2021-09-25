from ROOT import *
from math import *

from LoadData_JJ_eff import *
from sample_shortnames_JJ_eff import *
import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *
from closure_test_results import *
List = []
for long, short in sample_shortnames.iteritems():
    List.append(long)
print '\documentclass{article}'
print '\usepackage[utf8]{inputenc}'
print '\\begin{document}'
channel = '4mu'
OBSNAME = 'pT2mu_rapidity2mu'
Weight_From = ['SPS','DPS','Mix','HJJ','Chib_6','Chib_7']
i_sample = 0
for Sample in List:
    temp_eta = ''
    temp_2_eta = ''
    temp_3 = ''

    temp_etapt = ''
    temp_2_etapt = ''

    temp_reco = ''
    temp_2_reco = ''

    temp_reco_id = ''
    temp_2_reco_id = ''

    temp_reco_id_vtx = ''
    temp_2_reco_id_vtx = ''
 
    temp_reco_eff_trg = ''
    temp_2_reco_eff_trg = ''

    temp_reco_eff_evt = ''
    temp_2_reco_eff_evt = ''


    print '\\begin{table}[htb!]'
    i_sample = i_sample+1
    shortname = sample_shortnames[Sample]
    processBin = shortname+'_'+channel+'_'+OBSNAME
    for acc_eff in Weight_From:
        s_eta = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_eta_selected']
        c_eta = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_eta_closure']
        cp_eta = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_eta_closure_up']
        cm_eta = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_eta_closure_dn']
        temp_eta = temp_eta + ' & $'+str(c_eta)+'^{+'+str(cp_eta-c_eta)+'}_{'+str(cm_eta-c_eta)+'}$' 
        temp_2_eta = temp_2_eta+'& N${}_{corr}$('+acc_eff+') '
        temp_3 = temp_3+'c|'
        s_etapt = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_etaPt_selected']
        c_etapt = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_etaPt_closure']
        cp_etapt = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_etaPt_closure_up']
        cm_etapt = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_etaPt_closure_dn']
        temp_etapt = temp_etapt + ' & $'+str(c_etapt)+'^{+'+str(cp_etapt-c_etapt)+'}_{'+str(cm_etapt-c_etapt)+'}$'
        temp_2_etapt = temp_2_etapt+'& N${}_{corr}$('+acc_eff+') '

        s_reco = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_selected']
        c_reco = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_closure']
        cp_reco = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_closure_up']
        cm_reco = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_closure_dn']
        temp_reco = temp_reco + ' & $'+str(c_reco)+'^{+'+str(cp_reco-c_reco)+'}_{'+str(cm_reco-c_reco)+'}$'
        temp_2_reco = temp_2_reco+'& N${}_{corr}$('+acc_eff+') '

        s_reco_id = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_id_selected']
        c_reco_id = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_id_closure']
        cp_reco_id = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_id_closure_up']
        cm_reco_id = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_id_closure_dn']
        temp_reco_id = temp_reco_id + ' & $'+str(c_reco_id)+'^{+'+str(cp_reco_id-c_reco_id)+'}_{'+str(cm_reco_id-c_reco_id)+'}$'
        temp_2_reco_id = temp_2_reco_id+'& N${}_{corr}$('+acc_eff+') '

        s_reco_id_vtx = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_id_vtx_selected']
        c_reco_id_vtx = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_id_vtx_closure']
        cp_reco_id_vtx = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_id_vtx_closure_up']
        cm_reco_id_vtx = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_id_vtx_closure_dn']
        temp_reco_id_vtx = temp_reco_id_vtx + ' & $'+str(c_reco_id_vtx)+'^{+'+str(cp_reco_id_vtx-c_reco_id_vtx)+'}_{'+str(cm_reco_id_vtx-c_reco_id_vtx)+'}$'
        temp_2_reco_id_vtx = temp_2_reco_id_vtx+'& N${}_{corr}$('+acc_eff+') '

        s_reco_eff_trg = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_eff_trg_selected']
        c_reco_eff_trg = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_eff_trg_closure']
        cp_reco_eff_trg = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_eff_trg_closure_up']
        cm_reco_eff_trg = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_eff_trg_closure_dn']
        temp_reco_eff_trg = temp_reco_eff_trg + ' & $'+str(c_reco_eff_trg)+'^{+'+str(cp_reco_eff_trg-c_reco_eff_trg)+'}_{'+str(cm_reco_eff_trg-c_reco_eff_trg)+'}$'
        temp_2_reco_eff_trg = temp_2_reco_eff_trg+'& N${}_{corr}$('+acc_eff+') '

        s_reco_eff_evt = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_eff_evt_selected']
        c_reco_eff_evt = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_eff_evt_closure']
        cp_reco_eff_evt = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_eff_evt_closure_up']
        cm_reco_eff_evt = closure_results[processBin+'_'+acc_eff+'_hgenfid4mu_reco_eff_evt_closure_dn']
        temp_reco_eff_evt = temp_reco_eff_evt + ' & $'+str(c_reco_eff_evt)+'^{+'+str(cp_reco_eff_evt-c_reco_eff_evt)+'}_{'+str(cm_reco_eff_evt-c_reco_eff_evt)+'}$'
        temp_2_reco_eff_evt = temp_2_reco_eff_evt+'& N${}_{corr}$('+acc_eff+') '

    print '{\\small '
    print '\\begin{tabular}{|c|c|'+temp_3+'}'
    print '\\hline'
    print 'cut & N${}_{obs}$ ',temp_2_eta +'\\\\'
    print '\\hline'

    print '$|\eta(\mu)| < 2.4$', '&', '$'+str(s_eta)+'$' , temp_eta+'\\\\'
    print '\\hline'

    print '$p_T(\mu > 2.0$', '&', '$'+str(s_etapt)+'$' , temp_etapt+'\\\\'
    print '\\hline'

    print '$reco.(\mu)$', '&', '$'+str(s_reco)+'$' , temp_reco+'\\\\'
    print '\\hline'

    print '$id.(\mu)$', '&', '$'+str(s_reco_id)+'$' , temp_reco_id+'\\\\'
    print '\\hline'

    print '$vtx(\mu\mu)$', '&', '$'+str(s_reco_id_vtx)+'$' , temp_reco_id_vtx+'\\\\'
    print '\\hline'

    print '$HLT$', '&', '$'+str(s_reco_eff_trg)+'$' , temp_reco_eff_trg+'\\\\'
    print '\\hline'

    print '$4~\mu~cuts$', '&', '$'+str(s_reco_eff_evt)+'$' , temp_reco_eff_evt+'\\\\'
    print '\\hline'

    print '\end{tabular}'
    print '}'
    print '\caption{'+processBin.split('_')[0]+' '+processBin.split('_')[1]+' '+'}' 
    print '\label{tab:'+processBin+'}' 
    print '\end{table}'
print '\end{document}'
