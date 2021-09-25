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
#from LoadData_JJ import *
from LoadData_JJ_eff import *
#LoadData(opt.SOURCEDIR)
save = ""
if (os.path.isfile('tdrStyle.py')):
    from tdrStyle import setTDRStyle
    setTDRStyle()
Histos = {}
acceptance_a_eta = {}
dacceptance_a_eta = {}
acceptance_b_eta = {}
dacceptance_b_eta = {}
acceptance_a_etapt = {}
dacceptance_a_etapt = {}
acceptance_b_etapt = {}
dacceptance_b_etapt = {}
reco = {}
dreco = {}
eff = {}
deff = {}
eff_vtx = {}
deff_vtx= {}
eff_evt = {}
deff_evt = {}
def geteffs(channel, List, obs_bins_pt, obs_bins_y, obs_gen_pT, obs_gen_y, genbin_pt, genbin_y):

    recoweight = "1.0"
    genweight = "1.0"
    obs_gen_low_pt = obs_bins_pt[genbin_pt]
    obs_gen_high_pt = obs_bins_pt[genbin_pt+1]
    obs_gen_low_y = obs_bins_y[genbin_y]
    obs_gen_high_y = obs_bins_y[genbin_y+1]
    print obs_gen_low_pt, "-",obs_gen_high_pt
    print obs_gen_low_y,"-",obs_gen_high_y
    i_sample = -1
    print List
    for Sample in List:
        i_sample = i_sample+1
        shortname = sample_shortnames[Sample]
        processBin = shortname+'_'+channel+'_'+opt.OBSNAME+'_genbin'+str(genbin_pt)+'_genbin'+str(genbin_y)
        acceptance_a_eta[processBin] = 0.0
        dacceptance_a_eta[processBin] = 0.0
        acceptance_b_eta[processBin] = 0.0
        dacceptance_b_eta[processBin] = 0.0
        acceptance_a_etapt[processBin] = 0.0
        dacceptance_a_etapt[processBin] = 0.0
        acceptance_b_etapt[processBin] = 0.0
        dacceptance_b_etapt[processBin] = 0.0
        reco[processBin] = 0.0
        dreco[processBin] = 0.0
        eff[processBin] = 0.0
        deff[processBin] = 0.0
        eff_vtx[processBin] = 0.0
        deff_vtx[processBin]= 0.0
        eff_evt[processBin] = 0.0
        deff_evt[processBin] = 0.0

        cut_ups_gen_ya     = "(GENdimu_y[0] > "+str(obs_gen_low_y)+ " && GENdimu_y[0] < " + str(obs_gen_high_y) + ")"
    	cut_ups_gen_yb     = "(GENdimu_y[1] > "+str(obs_gen_low_y)+ " && GENdimu_y[1] < " + str(obs_gen_high_y) + ")"
    	cut_ups_gen_pta    = "(GENdimu_pt[0] > "+str(obs_gen_low_pt)+ " && GENdimu_pt[0] < " + str(obs_gen_high_pt) + ")"  
    	cut_ups_gen_ptb    = "(GENdimu_pt[1] > "+str(obs_gen_low_pt)+ " && GENdimu_pt[1] < " + str(obs_gen_high_pt) + ")"  
    	cut_mu_gen_eta_a   = "(abs(GENmu_eta[GEN_ups1_mu1_index]) < "+str(gen_mu_eta_cut)+ " && abs(GENmu_eta[GEN_ups1_mu2_index]) < "+str(gen_mu_eta_cut)+")"
        cut_mu_gen_pt_a   = "(GENmu_pt[GEN_ups1_mu1_index] > "+str(gen_mu_pt_cut)+ " && GENmu_pt[GEN_ups1_mu2_index] > "+str(gen_mu_pt_cut)+")"
    	cut_mu_gen_eta_b   = "(abs(GENmu_eta[GEN_ups2_mu1_index]) < "+str(gen_mu_eta_cut)+ " && abs(GENmu_eta[GEN_ups2_mu2_index]) < "+str(gen_mu_eta_cut)+")"
        cut_mu_gen_pt_b   = "(GENmu_pt[GEN_ups2_mu1_index] > "+str(gen_mu_pt_cut)+ " && GENmu_pt[GEN_ups2_mu2_index] > "+str(gen_mu_pt_cut)+")"
    	# GEN level
    	Histos[processBin+"fid_a_etapt"] = TH1D(processBin+"fid_a_etapt", processBin+"fid_a_etapt", 25, 0, 10000)  
    	Histos[processBin+"fid_a_etapt"].Sumw2()
        Histos[processBin+"fid_a_eta"] = TH1D(processBin+"fid_a_eta", processBin+"fid_a_eta", 25, 0, 10000)
        Histos[processBin+"fid_a_eta"].Sumw2()
    	Histos[processBin+"fs_a"] = TH1D(processBin+"fs_a", processBin+"fs_a", 25, 0, 10000)
    	Histos[processBin+"fs_a"].Sumw2()
    	Histos[processBin+"fid_b_etapt"] = TH1D(processBin+"fid_b_etapt", processBin+"fid_b_etapt", 25, 0, 10000)
    	Histos[processBin+"fid_b_etapt"].Sumw2()
        Histos[processBin+"fid_b_eta"] = TH1D(processBin+"fid_b_eta", processBin+"fid_b_eta", 25, 0, 10000)
        Histos[processBin+"fid_b_eta"].Sumw2()
    	Histos[processBin+"fs_b"] = TH1D(processBin+"fs_b", processBin+"fs_b", 25, 0, 10000)
    	Histos[processBin+"fs_b"].Sumw2()
    	# GEN level 
    	Tree[Sample].Draw("GENups_mass[0] >> "+processBin+"fid_a_etapt","("+genweight+")*("+cut_ups_gen_ya+" && "+cut_ups_gen_pta+" && "+cut_mu_gen_eta_a+" && "+ cut_mu_gen_pt_a+")","goff")
        Tree[Sample].Draw("GENups_mass[0] >> "+processBin+"fid_a_eta","("+genweight+")*("+cut_ups_gen_ya+" && "+cut_ups_gen_pta+" && "+cut_mu_gen_eta_a+")","goff")
    	Tree[Sample].Draw("GENups_mass[0]>> "+processBin+"fs_a","("+genweight+")*("+cut_ups_gen_ya+" && " + cut_ups_gen_pta + ")","goff")

    	Tree[Sample].Draw("GENups_mass[1] >> "+processBin+"fid_b_etapt","("+genweight+")*("+cut_ups_gen_yb+" && "+cut_ups_gen_ptb+" && "+cut_mu_gen_eta_b+" && "+ cut_mu_gen_pt_b+")","goff")
        Tree[Sample].Draw("GENups_mass[1] >> "+processBin+"fid_b_eta","("+genweight+")*("+cut_ups_gen_yb+" && "+cut_ups_gen_ptb+" && "+cut_mu_gen_eta_b+")","goff")
    	Tree[Sample].Draw("GENups_mass[1] >> "+processBin+"fs_b","("+genweight+")*("+cut_ups_gen_yb+" && " + cut_ups_gen_ptb+")","goff")
         
    	if (Histos[processBin+"fs_a"].Integral()>0):
        	acceptance_a_eta[processBin] = Histos[processBin+"fid_a_eta"].Integral()/Histos[processBin+"fs_a"].Integral()
        	dacceptance_a_eta[processBin] = sqrt(acceptance_a_eta[processBin]*(1.0-acceptance_a_eta[processBin])/Histos[processBin+"fs_a"].Integral())
    	else:
        	acceptance_a_eta[processBin] = -1.0
        	dacceptance_a_eta[processBin] = -1.0

    	if (Histos[processBin+"fs_b"].Integral()>0):
        	acceptance_b_eta[processBin] = Histos[processBin+"fid_b_eta"].Integral()/Histos[processBin+"fs_b"].Integral()
        	dacceptance_b_eta[processBin] = sqrt(acceptance_b_eta[processBin]*(1.0-acceptance_b_eta[processBin])/Histos[processBin+"fs_b"].Integral())

    	else:
        	acceptance_b_eta[processBin] = -1.0
        	dacceptance_b_eta[processBin] = -1.0

        if (Histos[processBin+"fid_a_eta"].Integral()>0):
                acceptance_a_etapt[processBin] = Histos[processBin+"fid_a_etapt"].Integral()/Histos[processBin+"fid_a_eta"].Integral()
                dacceptance_a_etapt[processBin] = sqrt(acceptance_a_etapt[processBin]*(1.0-acceptance_a_etapt[processBin])/Histos[processBin+"fid_a_eta"].Integral())
        else:
                acceptance_a_etapt[processBin] = -1.0
                dacceptance_a_etapt[processBin] = -1.0
        if (Histos[processBin+"fid_b_eta"].Integral()>0):
                acceptance_b_etapt[processBin] = Histos[processBin+"fid_b_etapt"].Integral()/Histos[processBin+"fid_b_eta"].Integral()
                dacceptance_b_etapt[processBin] = sqrt(acceptance_b_etapt[processBin]*(1.0-acceptance_b_etapt[processBin])/Histos[processBin+"fid_b_eta"].Integral())

        else:
                acceptance_b_etapt[processBin] = -1.0
                dacceptance_b_etapt[processBin] = -1.0

    	print processBin,"acc_a_eta: ",round(acceptance_a_eta[processBin],3), " acc_b_eta: ", round(acceptance_b_eta[processBin],3)
        print processBin,"dacc_a_eta: ",round(dacceptance_a_eta[processBin],3), " dacc_b_eta: ", round(dacceptance_b_eta[processBin],3)

        print processBin,"acc_a_etapt: ",round(acceptance_a_etapt[processBin],3), " acc_b_etapt: ", round(acceptance_b_etapt[processBin],3)
        print processBin,"dacc_a_etapt: ",round(dacceptance_a_etapt[processBin],3), " dacc_b_etapt: ", round(dacceptance_b_etapt[processBin],3)
if (opt.OBSNAME == "pT2mu_rapidity2mu"):
    obs_gen_pT = "pT2mu"
    obs_gen_y = "rapidity2mu"
    
obs_bins_PT = opt.OBSBINS.split("_")[0]
obs_bins_Y = opt.OBSBINS.split("_")[1] 
obs_bins_pt = obs_bins_PT.split("|")
obs_bins_y = obs_bins_Y.split("|")
if (not (obs_bins_pt[0] == '' and obs_bins_pt[len(obs_bins_pt)-1]=='')): 
    print 'BINS OPTION MUST START AND END WITH A |' 
obs_bins_pt.pop()
obs_bins_pt.pop(0) 
if (not (obs_bins_y[0] == '' and obs_bins_y[len(obs_bins_y)-1]=='')): 
    print 'BINS OPTION MUST START AND END WITH A |' 
obs_bins_y.pop()
obs_bins_y.pop(0) 

List = []
chans = ['4mu']
gen_mu_eta_cut = 2.4
gen_mu_pt_cut = 2.0
for long, short in sample_shortnames.iteritems():
    List.append(long)
for chan in chans:
    for genbin_pt in range(len(obs_bins_pt)-1):
        for genbin_y in range(len(obs_bins_y)-1):
            geteffs(chan, List, obs_bins_pt, obs_bins_y, obs_gen_pT, obs_gen_y, genbin_pt, genbin_y) 
with open('inputs_sig_JJ'+opt.OBSNAME+'.py', 'w') as f:
    f.write('acc_a_eta = '+str(acceptance_a_eta)+' \n')
    f.write('dacc_a_eta = '+str(dacceptance_a_eta)+' \n')
    f.write('acc_b_eta = '+str(acceptance_b_eta)+' \n')
    f.write('dacc_b_eta = '+str(dacceptance_b_eta)+' \n')
    f.write('acc_a_etapt = '+str(acceptance_a_etapt)+' \n')
    f.write('dacc_a_etapt = '+str(dacceptance_a_etapt)+' \n')
    f.write('acc_b_etapt = '+str(acceptance_b_etapt)+' \n')
    f.write('dacc_b_etapt = '+str(dacceptance_b_etapt)+' \n')
