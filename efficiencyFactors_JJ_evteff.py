import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *
from sample_shortnames_JJ_eff import *
grootargs = []
def callback_rootargs(option, opt, value, parser):
    grootargs.append(opt)
    
### Define function for parsing options
def parseOptions():

    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)
    
    # input options
    parser.add_option('-d', '--dir',    dest='SOURCEDIR',  type='string',default='./', help='run from the SOURCEDIR as working area, skip if SOURCEDIR is an empty string')
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observalbe, supported: "mass4mu", "pT2mu", "rapidity2mu"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string, 2D bining should be seperated by "_"')
    parser.add_option("-l",action="callback",callback=callback_rootargs)
    parser.add_option("-q",action="callback",callback=callback_rootargs)
    parser.add_option("-b",action="callback",callback=callback_rootargs)
                       
    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

# parse the arguments and options
global opt, args, runAllSteps
parseOptions()
sys.argv = grootargs

from ROOT import *
from LoadData_JJ_eff import *
#LoadData(opt.SOURCEDIR)
save = ""
if (os.path.isfile('tdrStyle.py')):
    from tdrStyle import setTDRStyle
    setTDRStyle()
Histos = {}
recoeff_id_vtx_ab = {}
drecoeff_id_vtx_ab = {}
recoeff_evt = {}
drecoeff_evt = {}
recoeff_trg_evt = {}
drecoeff_trg_evt = {}
def geteffs(channel, List, obs_bins_pt_a, obs_bins_pt_b, obs_gen_pT_a, obs_gen_pT_b, genbin_pt_a, genbin_pt_b):

    recoweight = "1.0"
    genweight = "1.0"
    obs_gen_low_pt_a = obs_bins_pt_a[genbin_pt_a]
    obs_gen_high_pt_a = obs_bins_pt_a[genbin_pt_a+1]
    obs_gen_low_pt_b = obs_bins_pt_b[genbin_pt_b]
    obs_gen_high_pt_b = obs_bins_pt_b[genbin_pt_b+1]
    print obs_gen_low_pt_a, "-",obs_gen_high_pt_a
    print obs_gen_low_pt_b,"-",obs_gen_high_pt_b
    i_sample = -1
    print List
    obs_gen_low_y = -2.0
    obs_gen_high_y = 2.0
    for Sample in List:
        i_sample = i_sample+1
        shortname = sample_shortnames[Sample]
        processBin = shortname+'_'+channel+'_'+opt.OBSNAME+'_genbin'+str(genbin_pt_a)+'_genbin'+str(genbin_pt_b)
        recoeff_id_vtx_ab[processBin] = 0.0
        drecoeff_id_vtx_ab[processBin] = 0.0
        
        recoeff_evt[processBin] = 0.0
        drecoeff_evt[processBin] = 0.0
        recoeff_trg_evt[processBin]  = 0.0
        drecoeff_trg_evt[processBin]  = 0.0
        
        cut_ups_reco_ya     = "(ups1_y_GenMatched > "+str(obs_gen_low_y)+ " && ups1_y_GenMatched < " + str(obs_gen_high_y) + ")"
        cut_ups_reco_ID_ya     = "(ups1_y_GenMatched_ID > "+str(obs_gen_low_y)+ " && ups1_y_GenMatched_ID < " + str(obs_gen_high_y) + ")"
        cut_ups_reco_ID_OS_VTX_ya     = "(ups1_y_GenMatched_ID_OS_VTX > "+str(obs_gen_low_y)+ " && ups1_y_GenMatched_ID_OS_VTX < " + str(obs_gen_high_y) + ")"
        cut_ups_reco_ya     = "(GENups_y[0] > "+str(obs_gen_low_y)+ " && GENups_y[0] < " + str(obs_gen_high_y) + ")"
        cut_ups_gen_ya     = "(GENups_y[0] > "+str(obs_gen_low_y)+ " && GENups_y[0] < " + str(obs_gen_high_y) + ")"
        cut_ups_gen_yb     = "(GENups_y[1] > "+str(obs_gen_low_y)+ " && GENups_y[1] < " + str(obs_gen_high_y) + ")"
        cut_ups_reco_yb     = "(ups2_y_GenMatched > "+str(obs_gen_low_y)+ " && ups2_y_GenMatched < " + str(obs_gen_high_y) + ")"
        cut_ups_reco_ID_yb     = "(ups2_y_GenMatched_ID > "+str(obs_gen_low_y)+ " && ups2_y_GenMatched_ID < " + str(obs_gen_high_y) + ")"
        cut_ups_reco_ID_OS_VTX_yb     = "(ups2_y_GenMatched_ID_OS_VTX > "+str(obs_gen_low_y)+ " && ups2_y_GenMatched_ID_OS_VTX < " + str(obs_gen_high_y) + ")"
        cut_ups_reco_yb     = "(GENups_y[1] > "+str(obs_gen_low_y)+ " && GENups_y[1] < " + str(obs_gen_high_y) + ")"
    	cut_ups_gen_pta    = "(GENups_pt[0] > "+str(obs_gen_low_pt_a)+ " && GENups_pt[0] < " + str(obs_gen_high_pt_a) + ")"
        cut_ups_reco_pta    = "(ups1_pt_GenMatched > "+str(obs_gen_low_pt_a)+ " && ups1_pt_GenMatched < " + str(obs_gen_high_pt_a) + ")"    
        cut_ups_reco_pta    = "(GENups_pt[0] > "+str(obs_gen_low_pt_a)+ " && GENups_pt[0] < " + str(obs_gen_high_pt_a) + ")"
        cut_ups_reco_ID_pta    = "(ups1_pt_GenMatched_ID > "+str(obs_gen_low_pt_a)+ " && ups1_pt_GenMatched_ID < " + str(obs_gen_high_pt_a) + ")"
        cut_ups_reco_ID_OS_VTX_pta    = "(ups1_pt_GenMatched_ID_OS_VTX > "+str(obs_gen_low_pt_a)+ " && ups1_pt_GenMatched_ID_OS_VTX < " + str(obs_gen_high_pt_a) + ")"
    	cut_ups_gen_ptb    = "(GENups_pt[1] > "+str(obs_gen_low_pt_b)+ " && GENups_pt[1] < " + str(obs_gen_high_pt_b) + ")"  
        cut_ups_reco_ptb    = "(ups2_pt_GenMatched > "+str(obs_gen_low_pt_b)+ " && ups2_pt_GenMatched < " + str(obs_gen_high_pt_b) + ")"
        cut_ups_reco_ptb    = "(GENups_pt[1] > "+str(obs_gen_low_pt_b)+ " && GENups_pt[1] < " + str(obs_gen_high_pt_b) + ")" 
        cut_ups_reco_ID_ptb    = "(ups2_pt_GenMatched_ID > "+str(obs_gen_low_pt_b)+ " && ups2_pt_GenMatched_ID < " + str(obs_gen_high_pt_b) + ")"
        cut_ups_reco_ID_OS_VTX_ptb    = "(ups2_pt_GenMatched_ID_OS_VTX > "+str(obs_gen_low_pt_b)+ " && ups2_pt_GenMatched_ID_OS_VTX < " + str(obs_gen_high_pt_b) + ")"
    	cut_mu_gen_eta_a   = "(abs(GENups_Daughter_mueta[0]) < "+str(gen_mu_eta_cut)+ " && abs(GENups_Daughter_mueta[1]) < "+str(gen_mu_eta_cut)+")"
        cut_mu_gen_pt_a   = "(GENups_Daughter_mupt[0] > "+str(gen_mu_pt_cut)+ " && GENups_Daughter_mupt[1] > "+str(gen_mu_pt_cut)+")"
    	cut_mu_gen_eta_b   = "(abs(GENups_Daughter_mueta[2]) < "+str(gen_mu_eta_cut)+ " && abs(GENups_Daughter_mueta[3]) < "+str(gen_mu_eta_cut)+")"
        cut_mu_gen_pt_b   = "(GENups_Daughter_mupt[2] > "+str(gen_mu_pt_cut)+ " && GENups_Daughter_mupt[3] > "+str(gen_mu_pt_cut)+")"
    	cut_mu_gen_Momid_a = "(GENups_DaughtersId[0]==13 && GENups_DaughtersId[1]==13)"
    	cut_mu_gen_Momid_b = "(GENups_DaughtersId[2]==13 && GENups_DaughtersId[3]==13)"
        cut_reco_ups_a    = "ups1_mass_GenMatched>0"
        cut_reco_ups_b    = "ups2_mass_GenMatched>0"
        cut_reco_id_ups_a    = "ups1_mass_GenMatched_ID>0"
        cut_reco_id_ups_b    = "ups2_mass_GenMatched_ID>0"
        cut_reco_id_vtx_ups_a    = "ups1_mass_GenMatched_ID_OS_VTX>0"
        cut_reco_id_vtx_ups_b    = "ups2_mass_GenMatched_ID_OS_VTX>0"
#        cut_reco_evt = "fourmu_mass_allcuts>0"   
        cut_trg_evt = "!((trigger&16)==0)"
        cut_reco_evt = "fourMuFit_mu12overlap[0]==0 &&  fourMuFit_mu13overlap[0]==0 && fourMuFit_mu14overlap[0]==0 &&fourMuFit_mu23overlap[0]==0 && fourMuFit_mu24overlap[0]==0 && fourMuFit_mu34overlap[0]==0&& !(fabs(fourMuFit_wrong_ups1_mass[0] - 0.78265) < 2.0*fourMuFit_wrong_ups1_massError[0])&& !(fabs(fourMuFit_wrong_ups2_mass[0] - 0.78265) < 2.0*fourMuFit_wrong_ups2_massError[0])&& !(fabs(fourMuFit_wrong_ups1_mass[0] - 1.01946) < 2.0*fourMuFit_wrong_ups1_massError[0])&& !(fabs(fourMuFit_wrong_ups2_mass[0] - 1.01946) < 2.0*fourMuFit_wrong_ups2_massError[0])&& fourMuFit_VtxProb[0]> 0.01 && fourMuFit_ups1_VtxProb[0]>0.005 && fourMuFit_ups2_VtxProb[0]>0.005 && !((trigger&16)==0)"  
        Histos[processBin+"reco_eff_id_vtx_ab"] = TH1D(processBin+"reco_eff_id_vtx_ab", processBin+"reco_eff_id_vtx_ab", 25, 0, 10000)
        Histos[processBin+"reco_eff_id_vtx_ab"].Sumw2()
        Histos[processBin+"reco_eff_trg_evt"] = TH1D(processBin+"reco_eff_trg_evt", processBin+"reco_eff_trg_evt", 25, 0, 10000)
        Histos[processBin+"reco_eff_trg_evt"].Sumw2()
        Histos[processBin+"reco_eff_evt"] = TH1D(processBin+"reco_eff_evt", processBin+"reco_eff_evt", 25, 0, 10000)
        Histos[processBin+"reco_eff_evt"].Sumw2()


        # RECO level
        ''' 
        Tree[Sample].Draw("ups1_mass_GenMatched_ID_OS_VTX>> " +processBin+"reco_eff_id_vtx_ab","("+recoweight+")*("+cut_reco_id_vtx_ups_a+" && "+cut_ups_reco_pta+" && "+cut_ups_reco_ya+" && "+cut_mu_gen_eta_a+" && "+ cut_mu_gen_pt_a + "  && "+cut_mu_gen_Momid_a+" && "+cut_reco_id_vtx_ups_b+" &&  "+cut_ups_reco_ptb+" && "+cut_ups_reco_yb+" && "+cut_mu_gen_eta_b+" && "+ cut_mu_gen_pt_b+" && "+cut_mu_gen_Momid_b+ ")","goff")

        Tree[Sample].Draw("fourMuFit_Mass[0] >> " +processBin+"reco_eff_evt","("+recoweight+")*("+cut_reco_evt+" && "+cut_ups_reco_pta+" && "+cut_ups_reco_ya+" && "+cut_mu_gen_eta_a+" && "+ cut_mu_gen_pt_a + "  && "+cut_mu_gen_Momid_a+" && "+cut_ups_reco_ptb+" && "+cut_ups_reco_yb+" && "+cut_mu_gen_eta_b+" && "+ cut_mu_gen_pt_b+" && "+cut_mu_gen_Momid_b+ ")","goff")
        '''
        Tree[Sample].Draw("ups1_mass_GenMatched_ID_OS_VTX>> " +processBin+"reco_eff_id_vtx_ab","("+recoweight+")*("+cut_reco_id_vtx_ups_a+" && "+cut_ups_reco_ID_OS_VTX_pta+" && "+cut_ups_reco_ID_OS_VTX_ya+" && "+cut_reco_id_vtx_ups_b+" &&  "+cut_ups_reco_ID_OS_VTX_ptb+" && "+cut_ups_reco_ID_OS_VTX_yb+")","goff")
        Tree[Sample].Draw("fourMuFit_Mass[0] >> " +processBin+"reco_eff_trg_evt","("+recoweight+")*("+cut_trg_evt+" && "+cut_ups_reco_ID_OS_VTX_pta+" && "+cut_ups_reco_ID_OS_VTX_ya+" && "+cut_ups_reco_ID_OS_VTX_ptb+" && "+cut_ups_reco_ID_OS_VTX_yb+")","goff")
        Tree[Sample].Draw("fourMuFit_Mass[0] >> " +processBin+"reco_eff_evt","("+recoweight+")*("+cut_reco_evt+" && "+cut_ups_reco_ID_OS_VTX_pta+" && "+cut_ups_reco_ID_OS_VTX_ya+" && "+cut_ups_reco_ID_OS_VTX_ptb+" && "+cut_ups_reco_ID_OS_VTX_yb+")","goff")

        if (Histos[processBin+"reco_eff_id_vtx_ab"].Integral()>0):
                recoeff_trg_evt[processBin]  =  Histos[processBin+"reco_eff_trg_evt"].Integral()/Histos[processBin+"reco_eff_id_vtx_ab"].Integral()
                drecoeff_trg_evt[processBin] = sqrt(recoeff_trg_evt[processBin]*(1.0-recoeff_trg_evt[processBin])/Histos[processBin+"reco_eff_id_vtx_ab"].Integral())
        else:
                recoeff_trg_evt[processBin] = -1.0
                drecoeff_trg_evt[processBin] = -1.0
        
        if (Histos[processBin+"reco_eff_trg_evt"].Integral()>0):
                recoeff_evt[processBin]  =  Histos[processBin+"reco_eff_evt"].Integral()/Histos[processBin+"reco_eff_trg_evt"].Integral()
                drecoeff_evt[processBin] = sqrt(recoeff_evt[processBin]*(1.0-recoeff_evt[processBin])/Histos[processBin+"reco_eff_trg_evt"].Integral())
        else:
                recoeff_evt[processBin] = -1.0
                drecoeff_evt[processBin] = -1.0

        print 'Histos_reco_eff_id_vtx_ab', Histos[processBin+"reco_eff_id_vtx_ab"].Integral(), "Histos_reco_cut_trg_evt", Histos[processBin+"reco_eff_trg_evt"].Integral()
        print processBin,"recoeff_trg_evt: ",round(recoeff_trg_evt[processBin],3), " drecoeff_trg_evt: ", round(drecoeff_trg_evt[processBin],3)
        print 'Histos_reco_cut_trg_evt', Histos[processBin+"reco_eff_trg_evt"].Integral(), 'Histos_reco_eff_evt', Histos[processBin+"reco_eff_evt"].Integral()
        print processBin,"reco_eff_evt: ",round(recoeff_evt[processBin],3), "drecoeff_evt: ",round(drecoeff_evt[processBin],3)

if (opt.OBSNAME == "pT2mu_pT2mu"):
    obs_gen_pT_a = "pT2mu"
    obs_gen_pT_b = "pT2mu"
    
obs_bins_PT_a = opt.OBSBINS.split("_")[0]
obs_bins_PT_b = opt.OBSBINS.split("_")[1] 
obs_bins_pt_a = obs_bins_PT_a.split("|")
obs_bins_pt_b = obs_bins_PT_b.split("|")
if (not (obs_bins_pt_a[0] == '' and obs_bins_pt_a[len(obs_bins_pt_a)-1]=='')): 
    print 'BINS OPTION MUST START AND END WITH A |' 
obs_bins_pt_a.pop()
obs_bins_pt_a.pop(0) 
if (not (obs_bins_pt_b[0] == '' and obs_bins_pt_b[len(obs_bins_pt_b)-1]=='')): 
    print 'BINS OPTION MUST START AND END WITH A |' 
obs_bins_pt_b.pop()
obs_bins_pt_b.pop(0) 

List = []
chans = ['4mu']
gen_mu_eta_cut = 2.4
gen_mu_pt_cut = 2.0
for long, short in sample_shortnames.iteritems():
    List.append(long)
for chan in chans:
    for genbin_pt_a in range(len(obs_bins_pt_a)-1):
        for genbin_pt_b in range(len(obs_bins_pt_b)-1):
            geteffs(chan, List, obs_bins_pt_a, obs_bins_pt_b, obs_gen_pT_a, obs_gen_pT_b, genbin_pt_a, genbin_pt_b) 
#with open('inputs_sig_JJ'+opt.OBSNAME+'_evteff.py', 'w') as f:
with open('inputs_sig_JJ'+opt.OBSNAME+'_evteff_inc.py', 'w') as f:
     f.write('recoeff_trg_evt = '+str(recoeff_trg_evt)+' \n')
     f.write('drecoeff_trg_evt = '+str(drecoeff_trg_evt)+' \n')
     f.write('recoeff_evt = '+str(recoeff_evt)+' \n')
     f.write('drecoeff_evt = '+str(drecoeff_evt)+' \n')
