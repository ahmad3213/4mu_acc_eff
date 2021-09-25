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
acceptance_a_eta = {}
dacceptance_a_eta = {}

acceptance_b_eta = {}
dacceptance_b_eta = {}

acceptance_a_etapt = {}
dacceptance_a_etapt = {}

acceptance_b_etapt = {}
dacceptance_b_etapt = {}

recoeff_a = {}
drecoeff_a = {}
recoeff_b = {}
drecoeff_b = {}

recoeff_id_a = {}
drecoeff_id_a = {}
recoeff_id_b = {}
drecoeff_id_b = {}

recoeff_id_vtx_a = {}
drecoeff_id_vtx_a = {}
recoeff_id_vtx_b = {}
drecoeff_id_vtx_b = {}

recoeff_evt = {}
drecoeff_evt = {}

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

        recoeff_a[processBin] = 0.0
        drecoeff_a[processBin] = 0.0
        recoeff_b[processBin] = 0.0
        drecoeff_b[processBin] = 0.0

        recoeff_id_a[processBin] = 0.0
        drecoeff_id_a[processBin] = 0.0
        recoeff_id_b[processBin] = 0.0
        drecoeff_id_b[processBin] = 0.0

        recoeff_id_vtx_a[processBin] = 0.0
        drecoeff_id_vtx_a[processBin] = 0.0
        recoeff_id_vtx_b[processBin] = 0.0
        drecoeff_id_vtx_b[processBin] = 0.0
        
        recoeff_evt[processBin] = 0.0
        drecoeff_evt[processBin] = 0.0
        
        cut_ups_gen_ya     = "(GENdimu_y[0] > "+str(obs_gen_low_y)+ " && GENdimu_y[0] < " + str(obs_gen_high_y) + ")"
        cut_ups_gen_yb     = "(GENdimu_y[1] > "+str(obs_gen_low_y)+ " && GENdimu_y[1] < " + str(obs_gen_high_y) + ")"
        cut_ups_gen_pta    = "(GENdimu_pt[0] > "+str(obs_gen_low_pt)+ " && GENdimu_pt[0] < " + str(obs_gen_high_pt) + ")"
        cut_ups_gen_ptb    = "(GENdimu_pt[1] > "+str(obs_gen_low_pt)+ " && GENdimu_pt[1] < " + str(obs_gen_high_pt) + ")"
        cut_mu_gen_eta_a   = "(abs(GENmu_eta[GEN_ups1_mu1_index]) < "+str(gen_mu_eta_cut)+ " && abs(GENmu_eta[GEN_ups1_mu2_index]) < "+str(gen_mu_eta_cut)+")"
        cut_mu_gen_pt_a   = "(GENmu_pt[GEN_ups1_mu1_index] > "+str(gen_mu_pt_cut)+ " && GENmu_pt[GEN_ups1_mu2_index] > "+str(gen_mu_pt_cut)+")"
        cut_mu_gen_eta_b   = "(abs(GENmu_eta[GEN_ups2_mu1_index]) < "+str(gen_mu_eta_cut)+ " && abs(GENmu_eta[GEN_ups2_mu2_index]) < "+str(gen_mu_eta_cut)+")"
        cut_mu_gen_pt_b   = "(GENmu_pt[GEN_ups2_mu1_index] > "+str(gen_mu_pt_cut)+ " && GENmu_pt[GEN_ups2_mu2_index] > "+str(gen_mu_pt_cut)+")"

        cut_ups_reco_ya     = "(ups1_y_GenMatched > "+str(obs_gen_low_y)+ " && ups1_y_GenMatched < " + str(obs_gen_high_y) + ")"
        cut_ups_reco_ID_ya     = "(ups1_y_GenMatched_ID > "+str(obs_gen_low_y)+ " && ups1_y_GenMatched_ID < " + str(obs_gen_high_y) + ")"
        cut_ups_reco_ID_OS_VTX_ya     = "(ups1_y_GenMatched_ID_OS_VTX > "+str(obs_gen_low_y)+ " && ups1_y_GenMatched_ID_OS_VTX < " + str(obs_gen_high_y) + ")"
        cut_ups_gen_ya     = "(GENdimu_y[0] > "+str(obs_gen_low_y)+ " && GENdimu_y[0] < " + str(obs_gen_high_y) + ")"
    	cut_ups_gen_yb     = "(GENdimu_y[1] > "+str(obs_gen_low_y)+ " && GENdimu_y[1] < " + str(obs_gen_high_y) + ")"
        cut_ups_reco_yb     = "(ups2_y_GenMatched > "+str(obs_gen_low_y)+ " && ups2_y_GenMatched < " + str(obs_gen_high_y) + ")"
        cut_ups_reco_ID_yb     = "(ups2_y_GenMatched_ID > "+str(obs_gen_low_y)+ " && ups2_y_GenMatched_ID < " + str(obs_gen_high_y) + ")"
        cut_ups_reco_ID_OS_VTX_yb     = "(ups2_y_GenMatched_ID_OS_VTX > "+str(obs_gen_low_y)+ " && ups2_y_GenMatched_ID_OS_VTX < " + str(obs_gen_high_y) + ")"
    	cut_ups_gen_pta    = "(GENdimu_pt[0] > "+str(obs_gen_low_pt)+ " && GENdimu_pt[0] < " + str(obs_gen_high_pt) + ")"
        cut_ups_reco_pta    = "(ups1_pt_GenMatched > "+str(obs_gen_low_pt)+ " && ups1_pt_GenMatched < " + str(obs_gen_high_pt) + ")"    
        cut_ups_reco_ID_pta    = "(ups1_pt_GenMatched_ID > "+str(obs_gen_low_pt)+ " && ups1_pt_GenMatched_ID < " + str(obs_gen_high_pt) + ")"
        cut_ups_reco_ID_OS_VTX_pta    = "(ups1_pt_GenMatched_ID_OS_VTX > "+str(obs_gen_low_pt)+ " && ups1_pt_GenMatched_ID_OS_VTX < " + str(obs_gen_high_pt) + ")"
    	cut_ups_gen_ptb    = "(GENdimu_pt[1] > "+str(obs_gen_low_pt)+ " && GENdimu_pt[1] < " + str(obs_gen_high_pt) + ")"  
        cut_ups_reco_ptb    = "(ups2_pt_GenMatched > "+str(obs_gen_low_pt)+ " && ups2_pt_GenMatched < " + str(obs_gen_high_pt) + ")"
        cut_ups_reco_ID_ptb    = "(ups2_pt_GenMatched_ID > "+str(obs_gen_low_pt)+ " && ups2_pt_GenMatched_ID < " + str(obs_gen_high_pt) + ")"
        cut_ups_reco_ID_OS_VTX_ptb    = "(ups2_pt_GenMatched_ID_OS_VTX > "+str(obs_gen_low_pt)+ " && ups2_pt_GenMatched_ID_OS_VTX < " + str(obs_gen_high_pt) + ")"
        cut_mu_gen_eta_a   = "(abs(GENmu_eta[GEN_ups1_mu1_index]) < "+str(gen_mu_eta_cut)+ " && abs(GENmu_eta[GEN_ups1_mu2_index]) < "+str(gen_mu_eta_cut)+")"
        cut_mu_gen_pt_a   = "(GENmu_pt[GEN_ups1_mu1_index] > "+str(gen_mu_pt_cut)+ " && GENmu_pt[GEN_ups1_mu2_index] > "+str(gen_mu_pt_cut)+")"
        cut_mu_gen_eta_b   = "(abs(GENmu_eta[GEN_ups2_mu1_index]) < "+str(gen_mu_eta_cut)+ " && abs(GENmu_eta[GEN_ups2_mu2_index]) < "+str(gen_mu_eta_cut)+")"
        cut_mu_gen_pt_b   = "(GENmu_pt[GEN_ups2_mu1_index] > "+str(gen_mu_pt_cut)+ " && GENmu_pt[GEN_ups2_mu2_index] > "+str(gen_mu_pt_cut)+")"
        cut_mu_reco_eta_a   = "(abs(AllRecoMuons_Eta[RECO_ups1_mu1_index]) < "+str(gen_mu_eta_cut)+ " && abs(AllRecoMuons_Eta[RECO_ups1_mu2_index]) < "+str(gen_mu_eta_cut)+")"
        cut_mu_reco_eta_b   = "(abs(AllRecoMuons_Eta[RECO_ups2_mu1_index]) < "+str(gen_mu_eta_cut)+ " && abs(AllRecoMuons_Eta[RECO_ups2_mu2_index]) < "+str(gen_mu_eta_cut)+")"
        cut_mu_reco_pta_a   = "(AllRecoMuons_Pt[RECO_ups1_mu1_index] > "+str(gen_mu_pt_cut)+ " && AllRecoMuons_Pt[RECO_ups1_mu2_index] > "+str(gen_mu_pt_cut)+")"
        cut_mu_reco_pta_b   = "(AllRecoMuons_Pt[RECO_ups2_mu1_index] > "+str(gen_mu_pt_cut)+ " && AllRecoMuons_Pt[RECO_ups2_mu2_index] > "+str(gen_mu_pt_cut)+")"
        cut_reco_ups_a    = "ups1_mass_GenMatched>0"
        cut_reco_ups_b    = "ups2_mass_GenMatched>0"
        cut_reco_id_ups_a    = "ups1_mass_GenMatched_ID>0"
        cut_reco_id_ups_b    = "ups2_mass_GenMatched_ID>0"
        cut_reco_id_vtx_ups_a    = "ups1_mass_GenMatched_ID_OS_VTX>0"
        cut_reco_id_vtx_ups_b    = "ups2_mass_GenMatched_ID_OS_VTX>0"
        cut_reco_evt = "fourmu_mass_allcuts>0"   

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

        # RECO level
        Histos[processBin+"reco_eff_a"] = TH1D(processBin+"reco_eff_a", processBin+"reco_eff_a", 25, 0, 10000)
        Histos[processBin+"reco_eff_a"].Sumw2()
        Histos[processBin+"reco_eff_b"] = TH1D(processBin+"reco_eff_b", processBin+"reco_eff_b", 25, 0, 10000)
        Histos[processBin+"reco_eff_b"].Sumw2()
        Histos[processBin+"reco_eff_a_temp"] = TH1D(processBin+"reco_eff_a_temp", processBin+"reco_eff_a_temp", 25, 0, 10000)
        Histos[processBin+"reco_eff_a_temp"].Sumw2()
        Histos[processBin+"reco_eff_b_temp"] = TH1D(processBin+"reco_eff_b_temp", processBin+"reco_eff_b", 25, 0, 10000)
        Histos[processBin+"reco_eff_b_temp"].Sumw2()

        Histos[processBin+"reco_eff_id_a"] = TH1D(processBin+"reco_eff_id_a", processBin+"reco_eff_id_a", 25, 0, 10000)
        Histos[processBin+"reco_eff_id_a"].Sumw2()
        Histos[processBin+"reco_eff_id_b"] = TH1D(processBin+"reco_eff_id_b", processBin+"reco_eff_id_b", 25, 0, 10000)
        Histos[processBin+"reco_eff_id_b"].Sumw2()

        Histos[processBin+"reco_eff_id_vtx_a"] = TH1D(processBin+"reco_eff_id_vtx_a", processBin+"reco_eff_id_vtx_a", 25, 0, 10000)
        Histos[processBin+"reco_eff_id_vtx_a"].Sumw2()
        Histos[processBin+"reco_eff_id_vtx_b"] = TH1D(processBin+"reco_eff_id_vtx_b", processBin+"reco_eff_id_vtx_b", 25, 0, 10000)
        Histos[processBin+"reco_eff_id_vtx_b"].Sumw2()
        Histos[processBin+"cut_eff_evt"] = TH1D(processBin+"cut_eff_evt", processBin+"cut_eff_evt", 25, 0, 10000)
        Histos[processBin+"cut_eff_evt"].Sumw2()


    	# GEN level 
    	Tree[Sample].Draw("GENups_mass[0] >> "+processBin+"fid_a_etapt","("+genweight+")*("+cut_ups_gen_ya+" && "+cut_ups_gen_pta+" && "+cut_mu_gen_eta_a+" && "+ cut_mu_gen_pt_a+")","goff")

    	Tree[Sample].Draw("GENups_mass[1] >> "+processBin+"fid_b_etapt","("+genweight+")*("+cut_ups_gen_yb+" && "+cut_ups_gen_ptb+" && "+cut_mu_gen_eta_b+" && "+ cut_mu_gen_pt_b+")","goff")

        # RECO level

        '''
        Tree[Sample].Draw("ups1_mass_GenMatched >> "+processBin+"reco_eff_a","("+recoweight+")*("+cut_reco_ups_a+" && " +cut_ups_reco_ya+" && "+cut_ups_reco_pta+" && "+cut_mu_gen_eta_a+" && "+ cut_mu_gen_pt_a+" && "+cut_mu_gen_Momid_a+")","goff")
        Tree[Sample].Draw("ups2_mass_GenMatched >> "+processBin+"reco_eff_b","("+recoweight+")*("+cut_reco_ups_b+ " && " +cut_ups_reco_yb+" && "+cut_ups_reco_ptb+")","goff")
        Tree[Sample].Draw("ups1_mass_GenMatched_ID >> "+processBin+"reco_eff_id_a","("+recoweight+")*("+cut_reco_id_ups_a+" && "+cut_ups_reco_ya+" && "+cut_ups_reco_pta+" && "+cut_mu_gen_eta_a+" && "+ cut_mu_gen_pt_a+" && "+cut_mu_gen_Momid_a+")","goff")
        Tree[Sample].Draw("ups2_mass_GenMatched_ID >> "+processBin+"reco_eff_id_b","("+recoweight+")*("+cut_reco_id_ups_b+" && "+cut_ups_reco_yb+" && "+cut_ups_reco_ptb+" && "+cut_mu_gen_eta_b+" && "+ cut_mu_gen_pt_b+" && "+cut_mu_gen_Momid_b+")","goff")

        Tree[Sample].Draw("ups1_mass_GenMatched_ID_OS_VTX >> "+processBin+"reco_eff_id_vtx_a","("+recoweight+")*("+cut_reco_id_vtx_ups_a+" && "+cut_ups_reco_ya+" && "+cut_ups_reco_pta+" && "+cut_mu_gen_eta_a+" && "+ cut_mu_gen_pt_a+" && "+cut_mu_gen_Momid_a+")","goff")
        Tree[Sample].Draw("ups2_mass_GenMatched_ID_OS_VTX >> "+processBin+"reco_eff_id_vtx_b","("+recoweight+")*("+cut_reco_id_vtx_ups_b+" && "+cut_ups_reco_yb+" && "+cut_ups_reco_ptb+" && "+cut_mu_gen_eta_b+" && "+ cut_mu_gen_pt_b+" && "+cut_mu_gen_Momid_b+")","goff")
        '''
#        Tree[Sample].Draw("ups1_mass_GenMatched >> "+processBin+"reco_eff_a","("+recoweight+")*("+cut_reco_ups_a+" && " +cut_ups_reco_ya+" && "+cut_ups_reco_pta+")","goff")
#        Tree[Sample].Draw("ups2_mass_GenMatched >> "+processBin+"reco_eff_b","("+recoweight+")*("+cut_reco_ups_b+ " && " +cut_ups_reco_yb+" && "+cut_ups_reco_ptb+")","goff")
        Tree[Sample].Draw("ups1_mass_GenMatched >> "+processBin+"reco_eff_a","("+recoweight+")*("+cut_reco_ups_a+" && " +cut_ups_gen_ya+" && "+cut_ups_gen_pta+" && "+cut_mu_gen_eta_a+" && "+ cut_mu_gen_pt_a+")","goff")
        Tree[Sample].Draw("ups2_mass_GenMatched >> "+processBin+"reco_eff_b","("+recoweight+")*("+cut_reco_ups_b+ " && " +cut_ups_gen_yb+" && "+cut_ups_gen_ptb+" && "+cut_mu_gen_eta_b+" && "+ cut_mu_gen_pt_b+")","goff")
        Tree[Sample].Draw("ups1_mass_GenMatched >> "+processBin+"reco_eff_a_temp","("+recoweight+")*("+cut_reco_ups_a+" && " +cut_ups_reco_ya+" && "+cut_ups_reco_pta+" && "+cut_mu_reco_eta_a+" && "+cut_mu_reco_pta_a+")","goff")
        Tree[Sample].Draw("ups2_mass_GenMatched >> "+processBin+"reco_eff_b_temp","("+recoweight+")*("+cut_reco_ups_b+ " && " +cut_ups_reco_yb+" && "+cut_ups_reco_ptb+" && "+cut_mu_reco_eta_b+" && "+cut_mu_reco_pta_b+")","goff")
        Tree[Sample].Draw("ups1_mass_GenMatched_ID >> "+processBin+"reco_eff_id_a","("+recoweight+")*("+cut_reco_id_ups_a+" && "+cut_ups_reco_ID_ya+" && "+cut_ups_reco_ID_pta+")","goff")
        Tree[Sample].Draw("ups2_mass_GenMatched_ID >> "+processBin+"reco_eff_id_b","("+recoweight+")*("+cut_reco_id_ups_b+" && "+cut_ups_reco_ID_yb+" && "+cut_ups_reco_ID_ptb+")","goff")
        Tree[Sample].Draw("ups1_mass_GenMatched_ID_OS_VTX >> "+processBin+"reco_eff_id_vtx_a","("+recoweight+")*("+cut_reco_id_vtx_ups_a+" && "+cut_ups_reco_ID_OS_VTX_ya+" && "+cut_ups_reco_ID_OS_VTX_pta+")","goff")
        Tree[Sample].Draw("ups2_mass_GenMatched_ID_OS_VTX >> "+processBin+"reco_eff_id_vtx_b","("+recoweight+")*("+cut_reco_id_vtx_ups_b+" && "+cut_ups_reco_ID_OS_VTX_yb+" && "+cut_ups_reco_ID_OS_VTX_ptb+")","goff")      
        if (Histos[processBin+"fid_a_etapt"].Integral()>0):
                recoeff_a[processBin]  =  Histos[processBin+"reco_eff_a"].Integral()/Histos[processBin+"fid_a_etapt"].Integral()
                drecoeff_a[processBin] = sqrt(recoeff_a[processBin]*(1.0-recoeff_a[processBin])/Histos[processBin+"fid_a_etapt"].Integral())
        else:
                recoeff_a[processBin] = -1.0
                drecoeff_a[processBin] = -1.0
        
        if (Histos[processBin+"fid_b_etapt"].Integral()>0):
                recoeff_b[processBin]  =  Histos[processBin+"reco_eff_b"].Integral()/Histos[processBin+"fid_b_etapt"].Integral()
                drecoeff_b[processBin] = sqrt(recoeff_b[processBin]*(1.0-recoeff_b[processBin])/Histos[processBin+"fid_b_etapt"].Integral())
        else:
                recoeff_b[processBin] = -1.0
                drecoeff_b[processBin] = -1.0
        if (Histos[processBin+"reco_eff_a_temp"].Integral()>0):
                recoeff_id_a[processBin]  =  Histos[processBin+"reco_eff_id_a"].Integral()/Histos[processBin+"reco_eff_a_temp"].Integral()
                drecoeff_id_a[processBin] = sqrt(recoeff_id_a[processBin]*(1.0-recoeff_id_a[processBin])/Histos[processBin+"reco_eff_a_temp"].Integral())
        else:
                recoeff_id_a[processBin] = -1.0
                drecoeff_id_a[processBin] = -1.0

        if (Histos[processBin+"reco_eff_b_temp"].Integral()>0):
                recoeff_id_b[processBin]  =  Histos[processBin+"reco_eff_id_b"].Integral()/Histos[processBin+"reco_eff_b_temp"].Integral()
                drecoeff_id_b[processBin] = sqrt(recoeff_id_b[processBin]*(1.0-recoeff_id_b[processBin])/Histos[processBin+"reco_eff_b_temp"].Integral())
        else:
                recoeff_id_b[processBin] = -1.0
                drecoeff_id_b[processBin] = -1.0

        if (Histos[processBin+"reco_eff_id_a"].Integral()>0):
                recoeff_id_vtx_a[processBin]  =  Histos[processBin+"reco_eff_id_vtx_a"].Integral()/Histos[processBin+"reco_eff_id_a"].Integral()
                drecoeff_id_vtx_a[processBin] = sqrt(recoeff_id_vtx_a[processBin]*(1.0-recoeff_id_vtx_a[processBin])/Histos[processBin+"reco_eff_id_a"].Integral())
        else:
                recoeff_id_vtx_a[processBin] = -1.0
                drecoeff_id_vtx_a[processBin] = -1.0

        if (Histos[processBin+"reco_eff_id_b"].Integral()>0):
                recoeff_id_vtx_b[processBin]  =  Histos[processBin+"reco_eff_id_vtx_b"].Integral()/Histos[processBin+"reco_eff_id_b"].Integral()
                drecoeff_id_vtx_b[processBin] = sqrt(recoeff_id_vtx_b[processBin]*(1.0-recoeff_id_vtx_b[processBin])/Histos[processBin+"reco_eff_id_b"].Integral())
        else:
                recoeff_id_vtx_b[processBin] = -1.0
                drecoeff_id_vtx_b[processBin] = -1.0
        print processBin,"recoeff_a: ",round(recoeff_a[processBin],3), " recoeff_b: ", round(recoeff_b[processBin],3)
        print processBin,"drecoeff_a: ",round(drecoeff_a[processBin],3), " drecoeff_b: ", round(drecoeff_b[processBin],3)
        print processBin,"recoeff_id_a: ",round(recoeff_id_a[processBin],3), " recoeff_id_b: ", round(recoeff_id_b[processBin],3)
        print processBin,"drecoeff_id_a: ",round(drecoeff_id_a[processBin],3), " drecoeff_id_b: ", round(drecoeff_id_b[processBin],3)

        print processBin,"recoeff_id_vtx_a: ",round(recoeff_id_vtx_a[processBin],3), " recoeff_id_vtx_b: ", round(recoeff_id_vtx_b[processBin],3)
        print processBin,"drecoeff_id_vtx_a: ",round(drecoeff_id_vtx_a[processBin],3), " drecoeff_id_vtx_b: ", round(drecoeff_id_vtx_b[processBin],3)

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
integral_Fid_a = 0
integral_Fid_b = 0
integral_reco_a = 0
integral_reco_b = 0
for long, short in sample_shortnames.iteritems():
    List.append(long)
for chan in chans:
    for genbin_pt in range(len(obs_bins_pt)-1):
        for genbin_y in range(len(obs_bins_y)-1):
            geteffs(chan, List, obs_bins_pt, obs_bins_y, obs_gen_pT, obs_gen_y, genbin_pt, genbin_y) 
#with open('inputs_sig_JJ'+opt.OBSNAME+'_eff.py', 'w') as f:
with open('inputs_sig_JJ'+opt.OBSNAME+'_eff_inc.py', 'w') as f:
     f.write('recoeff_a = '+str(recoeff_a)+' \n')
     f.write('drecoeff_a = '+str(drecoeff_a)+' \n')
     f.write('recoeff_b = '+str(recoeff_b)+' \n')
     f.write('drecoeff_b = '+str(drecoeff_b)+' \n')
     f.write('recoeff_id_a = '+str(recoeff_id_a)+' \n')
     f.write('drecoeff_id_a = '+str(drecoeff_id_a)+' \n')
     f.write('recoeff_id_b = '+str(recoeff_id_b)+' \n')
     f.write('drecoeff_id_b = '+str(drecoeff_id_b)+' \n')
     f.write('recoeff_id_vtx_a = '+str(recoeff_id_vtx_a)+' \n')
     f.write('drecoeff_id_vtx_a = '+str(drecoeff_id_vtx_a)+' \n')
     f.write('recoeff_id_vtx_b = '+str(recoeff_id_vtx_b)+' \n')
     f.write('drecoeff_id_vtx_b = '+str(drecoeff_id_vtx_b)+' \n')
