from ROOT import *
from math import *

from LoadData_JJ_eff import *
from sample_shortnames_JJ_eff import *
import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *

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
    parser.add_option('',   '--makeTable',action='store_true', dest='TABLE',default=True,   help='print output as latex table')
    parser.add_option('',   '--symmetrize', action='store_true', dest='SYMMETRIZE', default=False, help='symmetrized to be independent of the ordering of the candidates, default is False')
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



#read root files/histrograms for closure test
f_acc_DPS = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/acc_hist_DPS_JJto4mu.root")
hist_acc2d_b_eta_DPS = f_acc_DPS.Get("acc2d_b_eta")
hist_acc2d_a_eta_DPS = f_acc_DPS.Get("acc2d_a_eta");
hist_dacc2d_b_eta_DPS = f_acc_DPS.Get("dacc2d_b_eta");
hist_dacc2d_a_eta_DPS = f_acc_DPS.Get("dacc2d_a_eta");
hist_acc2d_b_etapt_DPS = f_acc_DPS.Get("acc2d_b_etapt");
hist_acc2d_a_etapt_DPS = f_acc_DPS.Get("acc2d_a_etapt");
hist_dacc2d_b_etapt_DPS = f_acc_DPS.Get("dacc2d_b_etapt");
hist_dacc2d_a_etapt_DPS = f_acc_DPS.Get("dacc2d_a_etapt");

f_acc_HJJ = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/acc_hist_HToJJto4mu.root")
hist_acc2d_b_eta_HJJ = f_acc_HJJ.Get("acc2d_b_eta")
hist_acc2d_a_eta_HJJ = f_acc_HJJ.Get("acc2d_a_eta");
hist_dacc2d_b_eta_HJJ = f_acc_HJJ.Get("dacc2d_b_eta");
hist_dacc2d_a_eta_HJJ = f_acc_HJJ.Get("dacc2d_a_eta");
hist_acc2d_b_etapt_HJJ = f_acc_HJJ.Get("acc2d_b_etapt");
hist_acc2d_a_etapt_HJJ = f_acc_HJJ.Get("acc2d_a_etapt");
hist_dacc2d_b_etapt_HJJ = f_acc_HJJ.Get("dacc2d_b_etapt");
hist_dacc2d_a_etapt_HJJ = f_acc_HJJ.Get("dacc2d_a_etapt");

f_acc_Mix = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/acc_hist_Mix_SPS_DPS.root");
hist_acc2d_b_eta_Mix = f_acc_Mix.Get("acc2d_b_Mix_eta");
hist_acc2d_a_eta_Mix = f_acc_Mix.Get("acc2d_a_Mix_eta");
hist_dacc2d_b_eta_Mix = f_acc_Mix.Get("dacc2d_b_Mix_eta");
hist_dacc2d_a_eta_Mix = f_acc_Mix.Get("dacc2d_a_Mix_eta");
hist_acc2d_b_etapt_Mix = f_acc_Mix.Get("acc2d_b_Mix_etapt");
hist_acc2d_a_etapt_Mix = f_acc_Mix.Get("acc2d_a_Mix_etapt");
hist_dacc2d_b_etapt_Mix = f_acc_Mix.Get("dacc2d_b_Mix_etapt");
hist_dacc2d_a_etapt_Mix = f_acc_Mix.Get("dacc2d_a_Mix_etapt");
f_acc_SPS = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/acc_hist_SPS_JJto4mu.root");
hist_acc2d_b_eta_SPS = f_acc_SPS.Get("acc2d_b_eta");
hist_acc2d_a_eta_SPS = f_acc_SPS.Get("acc2d_a_eta");
hist_dacc2d_b_eta_SPS = f_acc_SPS.Get("dacc2d_b_eta");
hist_dacc2d_a_eta_SPS = f_acc_SPS.Get("dacc2d_a_eta");
hist_acc2d_b_etapt_SPS = f_acc_SPS.Get("acc2d_b_etapt");
hist_acc2d_a_etapt_SPS = f_acc_SPS.Get("acc2d_a_etapt");
hist_dacc2d_b_etapt_SPS = f_acc_SPS.Get("dacc2d_b_etapt");
hist_dacc2d_a_etapt_SPS = f_acc_SPS.Get("dacc2d_a_etapt");
f_acc_Chib_6 = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/acc_hist_Chib0_6X00_JJto4mu.root");
hist_acc2d_b_eta_Chib_6 = f_acc_Chib_6.Get("acc2d_b_eta");
hist_acc2d_a_eta_Chib_6 = f_acc_Chib_6.Get("acc2d_a_eta");
hist_dacc2d_b_eta_Chib_6 = f_acc_Chib_6.Get("dacc2d_b_eta");
hist_dacc2d_a_eta_Chib_6 = f_acc_Chib_6.Get("dacc2d_a_eta");
hist_acc2d_b_etapt_Chib_6 = f_acc_Chib_6.Get("acc2d_b_etapt");
hist_acc2d_a_etapt_Chib_6 = f_acc_Chib_6.Get("acc2d_a_etapt");
hist_dacc2d_b_etapt_Chib_6 = f_acc_Chib_6.Get("dacc2d_b_etapt");
hist_dacc2d_a_etapt_Chib_6 = f_acc_Chib_6.Get("dacc2d_a_etapt");
f_acc_Chib_7 = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/acc_hist_Chib0_7X00_JJto4mu.root");
hist_acc2d_b_eta_Chib_7 = f_acc_Chib_7.Get("acc2d_b_eta");
hist_acc2d_a_eta_Chib_7 = f_acc_Chib_7.Get("acc2d_a_eta");
hist_dacc2d_b_eta_Chib_7 = f_acc_Chib_7.Get("dacc2d_b_eta");
hist_dacc2d_a_eta_Chib_7 = f_acc_Chib_7.Get("dacc2d_a_eta");
hist_acc2d_b_etapt_Chib_7 = f_acc_Chib_7.Get("acc2d_b_etapt");
hist_acc2d_a_etapt_Chib_7 = f_acc_Chib_7.Get("acc2d_a_etapt");
hist_dacc2d_b_etapt_Chib_7 = f_acc_Chib_7.Get("dacc2d_b_etapt");
hist_dacc2d_a_etapt_Chib_7 = f_acc_Chib_7.Get("dacc2d_a_etapt");

f_eff_SPS = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/eff_hist_SPS_JJto4mu.root");
hist_recoeff2d_a_SPS = f_eff_SPS.Get("recoeff2d_a");
hist_drecoeff2d_a_SPS = f_eff_SPS.Get("drecoeff2d_a");
hist_recoeff2d_id_a_SPS = f_eff_SPS.Get("recoeff2d_id_a");
hist_drecoeff2d_id_a_SPS = f_eff_SPS.Get("drecoeff2d_id_a");
hist_recoeff2d_id_vtx_a_SPS = f_eff_SPS.Get("recoeff2d_id_vtx_a");
hist_drecoeff2d_id_vtx_a_SPS = f_eff_SPS.Get("drecoeff2d_id_vtx_a");
hist_recoeff2d_b_SPS = f_eff_SPS.Get("recoeff2d_b");
hist_drecoeff2d_b_SPS = f_eff_SPS.Get("drecoeff2d_b");
hist_recoeff2d_id_b_SPS = f_eff_SPS.Get("recoeff2d_id_b");
hist_drecoeff2d_id_b_SPS = f_eff_SPS.Get("drecoeff2d_id_b");
hist_recoeff2d_id_vtx_b_SPS = f_eff_SPS.Get("recoeff2d_id_vtx_b");
hist_drecoeff2d_id_vtx_b_SPS = f_eff_SPS.Get("drecoeff2d_id_vtx_b");
f_evt_eff_SPS = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/evt_eff_hist_SPS_JJto4mu.root");
hist_recoeff2d_evt_SPS = f_evt_eff_SPS.Get("recoeff2d_evt");
hist_drecoeff2d_evt_SPS = f_evt_eff_SPS.Get("drecoeff2d_evt");
hist_recoeff2d_evt_sym_SPS = f_evt_eff_SPS.Get("recoeff2d_evt_sym");
hist_drecoeff2d_evt_sym_SPS = f_evt_eff_SPS.Get("drecoeff2d_evt_sym");
hist_recoeff2d_trg_SPS = f_evt_eff_SPS.Get("recoeff2d_trg");
hist_drecoeff2d_trg_SPS = f_evt_eff_SPS.Get("drecoeff2d_trg");
hist_recoeff2d_trg_sym_SPS = f_evt_eff_SPS.Get("recoeff2d_trg_sym");
hist_drecoeff2d_trg_sym_SPS = f_evt_eff_SPS.Get("drecoeff2d_trg_sym");

f_eff_DPS = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/eff_hist_DPS_JJto4mu.root");
hist_recoeff2d_a_DPS = f_eff_DPS.Get("recoeff2d_a");
hist_drecoeff2d_a_DPS = f_eff_DPS.Get("drecoeff2d_a");
hist_recoeff2d_id_a_DPS = f_eff_DPS.Get("recoeff2d_id_a");
hist_drecoeff2d_id_a_DPS = f_eff_DPS.Get("drecoeff2d_id_a");
hist_recoeff2d_id_vtx_a_DPS = f_eff_DPS.Get("recoeff2d_id_vtx_a");
hist_drecoeff2d_id_vtx_a_DPS = f_eff_DPS.Get("drecoeff2d_id_vtx_a");
hist_recoeff2d_b_DPS = f_eff_DPS.Get("recoeff2d_b");
hist_drecoeff2d_b_DPS = f_eff_DPS.Get("drecoeff2d_b");
hist_recoeff2d_id_b_DPS = f_eff_DPS.Get("recoeff2d_id_b");
hist_drecoeff2d_id_b_DPS = f_eff_DPS.Get("drecoeff2d_id_b");
hist_recoeff2d_id_vtx_b_DPS = f_eff_DPS.Get("recoeff2d_id_vtx_b");
hist_drecoeff2d_id_vtx_b_DPS = f_eff_DPS.Get("drecoeff2d_id_vtx_b");

f_evt_eff_DPS = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/evt_eff_hist_DPS_JJto4mu.root");
hist_recoeff2d_evt_DPS = f_evt_eff_DPS.Get("recoeff2d_evt");
hist_drecoeff2d_evt_DPS = f_evt_eff_DPS.Get("drecoeff2d_evt");
hist_recoeff2d_evt_sym_DPS = f_evt_eff_DPS.Get("recoeff2d_evt_sym");
hist_drecoeff2d_evt_sym_DPS = f_evt_eff_DPS.Get("drecoeff2d_evt_sym");
hist_recoeff2d_trg_DPS = f_evt_eff_DPS.Get("recoeff2d_trg");
hist_drecoeff2d_trg_DPS = f_evt_eff_DPS.Get("drecoeff2d_trg");
hist_recoeff2d_trg_sym_DPS = f_evt_eff_DPS.Get("recoeff2d_trg_sym");
hist_drecoeff2d_trg_sym_DPS = f_evt_eff_DPS.Get("drecoeff2d_trg_sym");
f_eff_Mix = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/eff_hist_Mix_JJto4mu_SPS_DPS.root")
hist_recoeff2d_a_Mix = f_eff_Mix.Get("recoeff2d_a_Mix");
hist_drecoeff2d_a_Mix = f_eff_Mix.Get("drecoeff2d_a_Mix");
hist_recoeff2d_id_a_Mix = f_eff_Mix.Get("recoeff2d_id_a_Mix");
hist_drecoeff2d_id_a_Mix = f_eff_Mix.Get("drecoeff2d_id_a_Mix");
hist_recoeff2d_id_vtx_a_Mix = f_eff_Mix.Get("recoeff2d_id_vtx_a_Mix");
hist_drecoeff2d_id_vtx_a_Mix = f_eff_Mix.Get("drecoeff2d_id_vtx_a_Mix");
hist_recoeff2d_b_Mix = f_eff_Mix.Get("recoeff2d_b_Mix");
hist_drecoeff2d_b_Mix = f_eff_Mix.Get("drecoeff2d_b_Mix");
hist_recoeff2d_id_b_Mix = f_eff_Mix.Get("recoeff2d_id_b_Mix");
hist_drecoeff2d_id_b_Mix = f_eff_Mix.Get("drecoeff2d_id_b_Mix");
hist_recoeff2d_id_vtx_b_Mix = f_eff_Mix.Get("recoeff2d_id_vtx_b_Mix");
hist_drecoeff2d_id_vtx_b_Mix = f_eff_Mix.Get("drecoeff2d_id_vtx_b_Mix");

f_evt_eff_Mix = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/evt_eff_hist_Mix_JJto4mu_SPS_DPS.root") 
hist_recoeff2d_evt_Mix = f_evt_eff_Mix.Get("recoeff2d_evt_Mix");
hist_drecoeff2d_evt_Mix = f_evt_eff_Mix.Get("drecoeff2d_evt_Mix");
hist_recoeff2d_evt_sym_Mix = f_evt_eff_Mix.Get("recoeff2d_evt_sym_Mix");
hist_drecoeff2d_evt_sym_Mix = f_evt_eff_Mix.Get("drecoeff2d_evt_sym_Mix");
hist_recoeff2d_trg_Mix = f_evt_eff_Mix.Get("recoeff2d_trg_Mix");
hist_drecoeff2d_trg_Mix = f_evt_eff_Mix.Get("drecoeff2d_trg_Mix");
hist_recoeff2d_trg_sym_Mix = f_evt_eff_Mix.Get("recoeff2d_trg_sym_Mix");
hist_drecoeff2d_trg_sym_Mix = f_evt_eff_Mix.Get("drecoeff2d_trg_sym_Mix");

f_eff_HJJ = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/eff_hist_HToJJto4mu.root");
hist_recoeff2d_a_HJJ = f_eff_HJJ.Get("recoeff2d_a");
hist_drecoeff2d_a_HJJ = f_eff_HJJ.Get("drecoeff2d_a");
hist_recoeff2d_id_a_HJJ = f_eff_HJJ.Get("recoeff2d_id_a");
hist_drecoeff2d_id_a_HJJ = f_eff_HJJ.Get("drecoeff2d_id_a");
hist_recoeff2d_id_vtx_a_HJJ = f_eff_HJJ.Get("recoeff2d_id_vtx_a");
hist_drecoeff2d_id_vtx_a_HJJ = f_eff_HJJ.Get("drecoeff2d_id_vtx_a");
hist_recoeff2d_b_HJJ = f_eff_HJJ.Get("recoeff2d_b");
hist_drecoeff2d_b_HJJ = f_eff_HJJ.Get("drecoeff2d_b");
hist_recoeff2d_id_b_HJJ = f_eff_HJJ.Get("recoeff2d_id_b");
hist_drecoeff2d_id_b_HJJ = f_eff_HJJ.Get("drecoeff2d_id_b");
hist_recoeff2d_id_vtx_b_HJJ = f_eff_HJJ.Get("recoeff2d_id_vtx_b");
hist_drecoeff2d_id_vtx_b_HJJ = f_eff_HJJ.Get("drecoeff2d_id_vtx_b");

f_evt_eff_HJJ = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/evt_eff_hist_HToJJto4mu.root");
hist_recoeff2d_evt_HJJ = f_evt_eff_HJJ.Get("recoeff2d_evt");
hist_drecoeff2d_evt_HJJ = f_evt_eff_HJJ.Get("drecoeff2d_evt");
hist_recoeff2d_evt_sym_HJJ = f_evt_eff_HJJ.Get("recoeff2d_evt_sym");
hist_drecoeff2d_evt_sym_HJJ = f_evt_eff_HJJ.Get("drecoeff2d_evt_sym");
hist_recoeff2d_trg_HJJ = f_evt_eff_HJJ.Get("recoeff2d_trg");
hist_drecoeff2d_trg_HJJ = f_evt_eff_HJJ.Get("drecoeff2d_trg");
hist_recoeff2d_trg_sym_HJJ = f_evt_eff_HJJ.Get("recoeff2d_trg_sym");
hist_drecoeff2d_trg_sym_HJJ = f_evt_eff_HJJ.Get("drecoeff2d_trg_sym");

f_eff_Chib_6 = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/eff_hist_Chib0_6X00_JJto4mu.root");
hist_recoeff2d_a_Chib_6 = f_eff_Chib_6.Get("recoeff2d_a");
hist_drecoeff2d_a_Chib_6 = f_eff_Chib_6.Get("drecoeff2d_a");
hist_recoeff2d_id_a_Chib_6 = f_eff_Chib_6.Get("recoeff2d_id_a");
hist_drecoeff2d_id_a_Chib_6 = f_eff_Chib_6.Get("drecoeff2d_id_a");
hist_recoeff2d_id_vtx_a_Chib_6 = f_eff_Chib_6.Get("recoeff2d_id_vtx_a");
hist_drecoeff2d_id_vtx_a_Chib_6 = f_eff_Chib_6.Get("drecoeff2d_id_vtx_a");
hist_recoeff2d_b_Chib_6 = f_eff_Chib_6.Get("recoeff2d_b");
hist_drecoeff2d_b_Chib_6 = f_eff_Chib_6.Get("drecoeff2d_b");
hist_recoeff2d_id_b_Chib_6 = f_eff_Chib_6.Get("recoeff2d_id_b");
hist_drecoeff2d_id_b_Chib_6 = f_eff_Chib_6.Get("drecoeff2d_id_b");
hist_recoeff2d_id_vtx_b_Chib_6 = f_eff_Chib_6.Get("recoeff2d_id_vtx_b");
hist_drecoeff2d_id_vtx_b_Chib_6 = f_eff_Chib_6.Get("drecoeff2d_id_vtx_b");
f_evt_eff_Chib_6 = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/evt_eff_hist_Chib0_6X00_JJto4mu.root");
hist_recoeff2d_evt_Chib_6 = f_evt_eff_Chib_6.Get("recoeff2d_evt");
hist_drecoeff2d_evt_Chib_6 = f_evt_eff_Chib_6.Get("drecoeff2d_evt");
hist_recoeff2d_evt_sym_Chib_6 = f_evt_eff_Chib_6.Get("recoeff2d_evt_sym");
hist_drecoeff2d_evt_sym_Chib_6 = f_evt_eff_Chib_6.Get("drecoeff2d_evt_sym");
hist_recoeff2d_trg_Chib_6 = f_evt_eff_Chib_6.Get("recoeff2d_trg");
hist_drecoeff2d_trg_Chib_6 = f_evt_eff_Chib_6.Get("drecoeff2d_trg");
hist_recoeff2d_trg_sym_Chib_6 = f_evt_eff_Chib_6.Get("recoeff2d_trg_sym");
hist_drecoeff2d_trg_sym_Chib_6 = f_evt_eff_Chib_6.Get("drecoeff2d_trg_sym");

f_eff_Chib_7 = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/eff_hist_Chib0_7X00_JJto4mu.root");
hist_recoeff2d_a_Chib_7 = f_eff_Chib_7.Get("recoeff2d_a");
hist_drecoeff2d_a_Chib_7 = f_eff_Chib_7.Get("drecoeff2d_a");
hist_recoeff2d_id_a_Chib_7 = f_eff_Chib_7.Get("recoeff2d_id_a");
hist_drecoeff2d_id_a_Chib_7 = f_eff_Chib_7.Get("drecoeff2d_id_a");
hist_recoeff2d_id_vtx_a_Chib_7 = f_eff_Chib_7.Get("recoeff2d_id_vtx_a");
hist_drecoeff2d_id_vtx_a_Chib_7 = f_eff_Chib_7.Get("drecoeff2d_id_vtx_a");
hist_recoeff2d_b_Chib_7 = f_eff_Chib_7.Get("recoeff2d_b");
hist_drecoeff2d_b_Chib_7 = f_eff_Chib_7.Get("drecoeff2d_b");
hist_recoeff2d_id_b_Chib_7 = f_eff_Chib_7.Get("recoeff2d_id_b");
hist_drecoeff2d_id_b_Chib_7 = f_eff_Chib_7.Get("drecoeff2d_id_b");
hist_recoeff2d_id_vtx_b_Chib_7 = f_eff_Chib_7.Get("recoeff2d_id_vtx_b");
hist_drecoeff2d_id_vtx_b_Chib_7 = f_eff_Chib_7.Get("drecoeff2d_id_vtx_b");
f_evt_eff_Chib_7 = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff_v2/JJ_plots/evt_eff_hist_Chib0_7X00_JJto4mu.root");
hist_recoeff2d_evt_Chib_7 = f_evt_eff_Chib_7.Get("recoeff2d_evt");
hist_drecoeff2d_evt_Chib_7 = f_evt_eff_Chib_7.Get("drecoeff2d_evt");
hist_recoeff2d_evt_sym_Chib_7 = f_evt_eff_Chib_7.Get("recoeff2d_evt_sym");
hist_drecoeff2d_evt_sym_Chib_7 = f_evt_eff_Chib_7.Get("drecoeff2d_evt_sym");
hist_recoeff2d_trg_Chib_7 = f_evt_eff_Chib_7.Get("recoeff2d_trg");
hist_drecoeff2d_trg_Chib_7 = f_evt_eff_Chib_7.Get("drecoeff2d_trg");
hist_recoeff2d_trg_sym_Chib_7 = f_evt_eff_Chib_7.Get("recoeff2d_trg_sym");
hist_drecoeff2d_trg_sym_Chib_7 = f_evt_eff_Chib_7.Get("drecoeff2d_trg_sym");

####acceptance related cuts strings
gen_mu_eta_cut = 2.4
gen_mu_pt_cut = 2.0
obs_gen_low_y = -2.0
obs_gen_high_y = 2.0
obs_gen_low_pt = 0 
obs_gen_high_pt = 40
cut_ups_gen_ya     = "(GENdimu_y[0] > "+str(obs_gen_low_y)+ " && GENdimu_y[0] < " + str(obs_gen_high_y) + ")"
cut_ups_reco_ya     = "(ups1_y_GenMatched > "+str(obs_gen_low_y)+ " && ups1_y_GenMatched < " + str(obs_gen_high_y) + ")"
cut_ups_reco_ID_ya     = "(ups1_y_GenMatched_ID > "+str(obs_gen_low_y)+ " && ups1_y_GenMatched_ID < " + str(obs_gen_high_y) + ")"
cut_ups_reco_ID_OS_VTX_ya     = "(ups1_y_GenMatched_ID_OS_VTX > "+str(obs_gen_low_y)+ " && ups1_y_GenMatched_ID_OS_VTX < " + str(obs_gen_high_y) + ")"
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
cut_reco_id_ups_a = "ups1_mass_GenMatched_ID>0"
cut_reco_id_ups_b = "ups2_mass_GenMatched_ID>0"
cut_reco_id_vtx_ups_a = "ups1_mass_GenMatched_ID_OS_VTX>0"
cut_reco_id_vtx_ups_b = "ups2_mass_GenMatched_ID_OS_VTX>0"
#cut_reco_evt = "fourmu_mass_allcuts>0"
cut_reco_trg = "!((trigger&16)==0)"
cut_reco_evt = "fourMuFit_mu12overlap[0]==0 &&  fourMuFit_mu13overlap[0]==0 && fourMuFit_mu14overlap[0]==0 &&fourMuFit_mu23overlap[0]==0 && fourMuFit_mu24overlap[0]==0 && fourMuFit_mu34overlap[0]==0&& !(fabs(fourMuFit_wrong_ups1_mass[0] - 0.78265) < 2.0*fourMuFit_wrong_ups1_massError[0])&& !(fabs(fourMuFit_wrong_ups2_mass[0] - 0.78265) < 2.0*fourMuFit_wrong_ups2_massError[0])&& !(fabs(fourMuFit_wrong_ups1_mass[0] - 1.01946) < 2.0*fourMuFit_wrong_ups1_massError[0])&& !(fabs(fourMuFit_wrong_ups2_mass[0] - 1.01946) < 2.0*fourMuFit_wrong_ups2_massError[0])&& fourMuFit_VtxProb[0]> 0.01 && fourMuFit_ups1_VtxProb[0]>0.005 && fourMuFit_ups2_VtxProb[0]>0.005 && !((trigger&16)==0)"
genweight = '1.0'
recoweight = '1.0'
channel = '4mu'
OBSNAME = 'pT2mu_rapidity2mu'
List = []
closure = {}
#Weight_From = ['SPS','DPS','Mix','HJJ','Chib_6','Chib_7']
Weight_From = ['Chib_6']
Histos = {}
for long, short in sample_shortnames.iteritems():
    List.append(long)

i_sample = -1
invalid_events = 0
total_events = 0
for Sample in List:
    i_sample = i_sample+1
    shortname = sample_shortnames[Sample]
    processBin = shortname+'_'+channel+'_'+OBSNAME
    Histos[processBin+"hgenfid4mu"] = TH1D(processBin+"hgenfid4mu", processBin+"hgenfid4mu", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu"].Sumw2()
    Histos[processBin+"hgenfid4mu_eta_selected"] = TH1D(processBin+"hgenfid4mu_eta_selected", processBin+"hgenfid4mu_eta_selected", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu_eta_selected"].Sumw2()
    Histos[processBin+"hgenfid4mu_etaPt_selected"] = TH1D(processBin+"hgenfid4mu_etaPt_selected", processBin+"hgenfid4mu_etaPt_selected", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu_etaPt_selected"].Sumw2()
    Histos[processBin+"hgenfid4mu_reco_selected"] = TH1D(processBin+"hgenfid4mu_reco_selected", processBin+"hgenfid4mu_reco_selected", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu_reco_selected"].Sumw2()
    Histos[processBin+"hgenfid4mu_reco_id_selected"] = TH1D(processBin+"hgenfid4mu_reco_id_selected", processBin+"reco_eff_id_a", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu_reco_id_selected"].Sumw2()
    Histos[processBin+"hgenfid4mu_reco_id_vtx_selected"] = TH1D(processBin+"hgenfid4mu_reco_id_vtx_selected", processBin+"hgenfid4mu_reco_id_vtx_selected", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu_reco_id_vtx_selected"].Sumw2()

    Histos[processBin+"hgenfid4mu_reco_eff_evt_selected"] = TH1D(processBin+"hgenfid4mu_reco_eff_evt_selected", processBin+"hgenfid4mu_reco_eff_evt_selected", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu_reco_eff_evt_selected"].Sumw2()
    Histos[processBin+"hgenfid4mu_reco_eff_trg_selected"] = TH1D(processBin+"hgenfid4mu_reco_eff_trg_selected", processBin+"hgenfid4mu_reco_eff_trg_selected", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu_reco_eff_trg_selected"].Sumw2()

    Tree[Sample].Draw("GENdimu_mass[0]>> "+processBin+"hgenfid4mu","("+genweight+")*("+cut_ups_gen_ya+" && " + cut_ups_gen_pta + "&&" + cut_ups_gen_yb+" && " + cut_ups_gen_ptb + ")","goff")

    Tree[Sample].Draw("GENdimu_mass[0] >> "+processBin+"hgenfid4mu_eta_selected","("+genweight+")*("+cut_ups_gen_ya+" && "+cut_ups_gen_pta+" && "+cut_mu_gen_eta_a+" &&" + cut_ups_gen_yb+" && "+cut_ups_gen_ptb+" && "+cut_mu_gen_eta_b+")","goff")

    Tree[Sample].Draw("GENdimu_mass[0] >> "+processBin+"hgenfid4mu_etaPt_selected","("+genweight+")*("+cut_ups_gen_ya+" && "+cut_ups_gen_pta+" && "+cut_mu_gen_eta_a+" && "+ cut_mu_gen_pt_a + " && " + cut_ups_gen_yb+" && "+cut_ups_gen_ptb+" && "+cut_mu_gen_eta_b+" && "+ cut_mu_gen_pt_b+")","goff")

#    Tree[Sample].Draw("ups1_mass_GenMatched >> "+processBin+"hgenfid4mu_reco_selected","("+recoweight+")*("+cut_reco_ups_a+" && " +cut_ups_reco_ya+" && "+cut_ups_reco_pta+ " && "+cut_reco_ups_b+ " && " +cut_ups_reco_yb+" && "+cut_ups_reco_ptb+" && "+cut_mu_reco_eta_a+" && "+cut_mu_reco_pta_b+" && "+cut_mu_reco_eta_b+" && "+cut_mu_reco_pta_b+")","goff")
    Tree[Sample].Draw("ups1_mass_GenMatched >> "+processBin+"hgenfid4mu_reco_selected","("+recoweight+")*("+cut_reco_ups_a+" && " +cut_ups_reco_ya+" && "+cut_ups_reco_pta+ " && "+cut_reco_ups_b+ " && " +cut_ups_reco_yb+" && "+cut_ups_reco_ptb+" && "+cut_mu_reco_eta_a+" && "+cut_mu_reco_pta_b+" && "+cut_mu_reco_eta_b+" && "+cut_mu_reco_pta_b+" && "+ cut_mu_gen_pt_a+" && "+cut_mu_gen_pt_b+" && "+cut_mu_gen_eta_a+" && "+cut_mu_gen_eta_b+" && "+cut_ups_gen_pta+" && "+cut_ups_gen_ptb+" && "+cut_ups_gen_ya+" && "+cut_ups_gen_yb+")","goff")
    Tree[Sample].Draw("ups1_mass_GenMatched_ID >> "+processBin+"hgenfid4mu_reco_id_selected","("+recoweight+")*("+cut_reco_id_ups_a+" && "+cut_ups_reco_ID_ya+" && "+cut_ups_reco_ID_pta+" && "+cut_reco_id_ups_b+" && "+cut_ups_reco_ID_yb+" && "+cut_ups_reco_ID_ptb+" && "+ cut_mu_gen_pt_a+" && "+cut_mu_gen_pt_b+" && "+cut_mu_gen_eta_a+" && "+cut_mu_gen_eta_b+" && "+cut_ups_gen_pta+" && "+cut_ups_gen_ptb+" && "+cut_ups_gen_ya+" && "+cut_ups_gen_yb+")","goff")
    Tree[Sample].Draw("ups1_mass_GenMatched_ID_OS_VTX >> "+processBin+"hgenfid4mu_reco_id_vtx_selected","("+recoweight+")*("+cut_reco_id_vtx_ups_a+" && "+cut_ups_reco_ID_OS_VTX_ya+" && "+cut_ups_reco_ID_OS_VTX_pta+" && "+cut_reco_id_vtx_ups_b+" && "+cut_ups_reco_ID_OS_VTX_yb+" && "+cut_ups_reco_ID_OS_VTX_ptb+" && "+ cut_mu_gen_pt_a+" && "+cut_mu_gen_pt_b+" && "+cut_mu_gen_eta_a+" && "+cut_mu_gen_eta_b+" && "+cut_ups_gen_pta+" && "+cut_ups_gen_ptb+" && "+cut_ups_gen_ya+" && "+cut_ups_gen_yb+")","goff")
    Tree[Sample].Draw("fourMuFit_Mass[0] >> " +processBin+"hgenfid4mu_reco_eff_trg_selected","("+recoweight+")*("+cut_reco_trg+" && "+cut_ups_reco_ID_OS_VTX_pta+" && "+cut_ups_reco_ID_OS_VTX_ya+" && "+cut_ups_reco_ID_OS_VTX_ptb+" && "+cut_ups_reco_ID_OS_VTX_yb+" && "+ cut_mu_gen_pt_a+" && "+cut_mu_gen_pt_b+" && "+cut_mu_gen_eta_a+" && "+cut_mu_gen_eta_b+" && "+cut_ups_gen_pta+" && "+cut_ups_gen_ptb+" && "+cut_ups_gen_ya+" && "+cut_ups_gen_yb+")","goff")
    Tree[Sample].Draw("fourMuFit_Mass[0] >> " +processBin+"hgenfid4mu_reco_eff_evt_selected","("+recoweight+")*("+cut_reco_evt+" && "+cut_ups_reco_ID_OS_VTX_pta+" && "+cut_ups_reco_ID_OS_VTX_ya+" && "+cut_ups_reco_ID_OS_VTX_ptb+" && "+cut_ups_reco_ID_OS_VTX_yb+" && "+ cut_mu_gen_pt_a+" && "+cut_mu_gen_pt_b+" && "+cut_mu_gen_eta_a+" && "+cut_mu_gen_eta_b+" && "+cut_ups_gen_pta+" && "+cut_ups_gen_ptb+" && "+cut_ups_gen_ya+" && "+cut_ups_gen_yb+")","goff")
    for acc_eff_weights in Weight_From:
        Histos[processBin+"hgenfid4mu_eta_closure"] = TH1D(processBin+"hgenfid4mu_eta_closure", processBin+"hgenfid4mu_eta_closure", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_eta_closure"].Sumw2()

        Histos[processBin+"hgenfid4mu_eta_closure_up"] = TH1D(processBin+"hgenfid4mu_eta_closure_up", processBin+"hgenfid4mu_eta_closure_up", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_eta_closure_up"].Sumw2()

        Histos[processBin+"hgenfid4mu_eta_closure_dn"] = TH1D(processBin+"hgenfid4mu_eta_closure_dn", processBin+"hgenfid4mu_eta_closure_dn", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_eta_closure_dn"].Sumw2()

        Histos[processBin+"hgenfid4mu_etaPt_closure"] = TH1D(processBin+"hgenfid4mu_etaPt_closure", processBin+"hgenfid4mu_etaPt_closure", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_etaPt_closure"].Sumw2()

        Histos[processBin+"hgenfid4mu_etaPt_closure_up"] = TH1D(processBin+"hgenfid4mu_etaPt_closure_up", processBin+"hgenfid4mu_etaPt_closure_up", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_etaPt_closure_up"].Sumw2()

        Histos[processBin+"hgenfid4mu_etaPt_closure_dn"] = TH1D(processBin+"hgenfid4mu_etaPt_closure_dn", processBin+"hgenfid4mu_etaPt_closure_dn", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_etaPt_closure_dn"].Sumw2()

        Histos[processBin+"hgenfid4mu_reco_closure"] = TH1D(processBin+"hgenfid4mu_reco_closure", processBin+"hgenfid4mu_reco_closure", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_closure"].Sumw2()

        Histos[processBin+"hgenfid4mu_reco_closure_up"] = TH1D(processBin+"hgenfid4mu_reco_closure_up", processBin+"hgenfid4mu_reco_closure_dn", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_closure_up"].Sumw2()
        Histos[processBin+"hgenfid4mu_reco_closure_dn"] = TH1D(processBin+"hgenfid4mu_reco_closure_dn", processBin+"hgenfid4mu_reco_closure_dn", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_closure_dn"].Sumw2()
        Histos[processBin+"hgenfid4mu_reco_id_closure"] = TH1D(processBin+"hgenfid4mu_reco_id_closure", processBin+"hgenfid4mu_reco_id_closure", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_id_closure"].Sumw2()

        Histos[processBin+"hgenfid4mu_reco_id_closure_up"] = TH1D(processBin+"hgenfid4mu_reco_id_closure_up", processBin+"hgenfid4mu_reco_id_closure_up", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_id_closure_up"].Sumw2()
        Histos[processBin+"hgenfid4mu_reco_id_closure_dn"] = TH1D(processBin+"hgenfid4mu_reco_id_closure_dn", processBin+"hgenfid4mu_reco_id_closure_dn", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_id_closure_dn"].Sumw2()

        Histos[processBin+"hgenfid4mu_reco_id_vtx_closure"] = TH1D(processBin+"hgenfid4mu_reco_id_vtx_closure", processBin+"hgenfid4mu_reco_id_vtx_closure", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_id_vtx_closure"].Sumw2()

        Histos[processBin+"hgenfid4mu_reco_id_vtx_closure_up"] = TH1D(processBin+"hgenfid4mu_reco_id_vtx_closure_up", processBin+"hgenfid4mu_reco_id_vtx_closure_up", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_id_vtx_closure_up"].Sumw2()

        Histos[processBin+"hgenfid4mu_reco_id_vtx_closure_dn"] = TH1D(processBin+"hgenfid4mu_reco_id_vtx_closure_dn", processBin+"hgenfid4mu_reco_id_vtx_closure_dn", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_id_vtx_closure_dn"].Sumw2()

        Histos[processBin+"hgenfid4mu_reco_eff_trg_closure"] = TH1D(processBin+"hgenfid4mu_reco_eff_trg_closure", processBin+"hgenfid4mu_reco_eff_trg_closure", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_eff_trg_closure"].Sumw2()
        Histos[processBin+"hgenfid4mu_reco_eff_trg_closure_up"] = TH1D(processBin+"hgenfid4mu_reco_eff_trg_closure_up", processBin+"hgenfid4mu_reco_eff_trg_closure_up", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_eff_trg_closure_up"].Sumw2()
        Histos[processBin+"hgenfid4mu_reco_eff_trg_closure_dn"] = TH1D(processBin+"hgenfid4mu_reco_eff_trg_closure_dn", processBin+"hgenfid4mu_reco_eff_trg_closure_dn", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_eff_trg_closure_dn"].Sumw2()


        Histos[processBin+"hgenfid4mu_reco_eff_evt_closure"] = TH1D(processBin+"hgenfid4mu_reco_eff_evt_closure", processBin+"hgenfid4mu_reco_eff_evt_closure", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_eff_evt_closure"].Sumw2()
        Histos[processBin+"hgenfid4mu_reco_eff_evt_closure_up"] = TH1D(processBin+"hgenfid4mu_reco_eff_evt_closure_up", processBin+"hgenfid4mu_reco_eff_evt_closure_up", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_eff_evt_closure_up"].Sumw2()
        Histos[processBin+"hgenfid4mu_reco_eff_evt_closure_dn"] = TH1D(processBin+"hgenfid4mu_reco_eff_evt_closure_dn", processBin+"hgenfid4mu_reco_eff_evt_closure_dn", 25, 0, 10000)
        Histos[processBin+"hgenfid4mu_reco_eff_evt_closure_dn"].Sumw2()
        nentries = Tree[Sample].GetEntries()
        total_events = 0 
        invalid_events = 0 
        for i in range(nentries):
            Tree[Sample].GetEntry(i)
            if (i%1000==0): print Sample,i,'/',nentries
            #if (i>100): break
            if (Tree[Sample].GENdimu_y.size()<2 or Tree[Sample].GENdimu_pt.size()<2):
                invalid_events = invalid_events+1   
                continue
            if (Tree[Sample].GENdimu_pt[0] < obs_gen_low_pt or Tree[Sample].GENdimu_pt[0] > obs_gen_high_pt ): continue
            if (Tree[Sample].GENdimu_pt[1] < obs_gen_low_pt or Tree[Sample].GENdimu_pt[1] > obs_gen_high_pt ): continue
            if (Tree[Sample].GENdimu_y[0]  < obs_gen_low_y  or Tree[Sample].GENdimu_y[0]  > obs_gen_high_y ): continue
            if (Tree[Sample].GENdimu_y[1]  < obs_gen_low_y  or Tree[Sample].GENdimu_y[1]  > obs_gen_high_y ): continue
            total_events = total_events+1
            if ('SPS' in acc_eff_weights):
                
                bin_a = hist_acc2d_a_eta_SPS.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_y[0]);
                bin_b = hist_acc2d_b_eta_SPS.FindBin(Tree[Sample].GENdimu_pt[1],Tree[Sample].GENdimu_y[1]);
                weight_acc_a_eta = hist_acc2d_a_eta_SPS.GetBinContent(bin_a);
                weight_dacc_a_eta = hist_dacc2d_a_eta_SPS.GetBinContent(bin_a);
                weight_acc_b_eta = hist_acc2d_b_eta_SPS.GetBinContent(bin_b);
                weight_dacc_b_eta = hist_dacc2d_b_eta_SPS.GetBinContent(bin_b);
                weight_acc_a_etapt = hist_acc2d_a_etapt_SPS.GetBinContent(bin_a);
                weight_dacc_a_etapt = hist_dacc2d_a_etapt_SPS.GetBinContent(bin_a);
                weight_acc_b_etapt = hist_acc2d_b_etapt_SPS.GetBinContent(bin_b);
                weight_dacc_b_etapt = hist_dacc2d_b_etapt_SPS.GetBinContent(bin_b);
                weight_recoeff_a = hist_recoeff2d_a_SPS.GetBinContent(bin_a);
                weight_recoeff_b = hist_recoeff2d_b_SPS.GetBinContent(bin_b);
                weight_drecoeff_a = hist_drecoeff2d_a_SPS.GetBinContent(bin_a);
                weight_drecoeff_b = hist_drecoeff2d_a_SPS.GetBinContent(bin_b);
                weight_recoeff_id_a = hist_recoeff2d_id_a_SPS.GetBinContent(bin_a);
                weight_drecoeff_id_a = hist_drecoeff2d_id_a_SPS.GetBinContent(bin_a);
                weight_recoeff_id_b = hist_recoeff2d_id_b_SPS.GetBinContent(bin_b);
                weight_drecoeff_id_b = hist_drecoeff2d_id_b_SPS.GetBinContent(bin_b);
                weight_recoeff_id_vtx_a = hist_recoeff2d_id_vtx_a_SPS.GetBinContent(bin_a);
                weight_drecoeff_id_vtx_a = hist_drecoeff2d_id_vtx_a_SPS.GetBinContent(bin_a);
                weight_recoeff_id_vtx_b = hist_recoeff2d_id_vtx_b_SPS.GetBinContent(bin_b);
                weight_drecoeff_id_vtx_b = hist_drecoeff2d_id_vtx_b_SPS.GetBinContent(bin_b);
                weight_recoeff_trg_vtx = hist_recoeff2d_trg_SPS.GetBinContent(hist_recoeff2d_trg_SPS.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_drecoeff_trg_vtx = hist_drecoeff2d_trg_SPS.GetBinContent(hist_drecoeff2d_trg_SPS.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_recoeff_evt_vtx = hist_recoeff2d_evt_SPS.GetBinContent(hist_recoeff2d_evt_SPS.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_drecoeff_evt_vtx = hist_drecoeff2d_evt_SPS.GetBinContent(hist_drecoeff2d_evt_SPS.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));

            if ('DPS' in acc_eff_weights):
                bin_a = hist_acc2d_a_eta_DPS.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_y[0]);
                bin_b = hist_acc2d_b_eta_DPS.FindBin(Tree[Sample].GENdimu_pt[1],Tree[Sample].GENdimu_y[1]);
                weight_acc_a_eta = hist_acc2d_a_eta_DPS.GetBinContent(bin_a);
                weight_dacc_a_eta = hist_dacc2d_a_eta_DPS.GetBinContent(bin_a);
                weight_acc_b_eta = hist_acc2d_b_eta_DPS.GetBinContent(bin_b);
                weight_dacc_b_eta = hist_dacc2d_b_eta_DPS.GetBinContent(bin_b);
                weight_acc_a_etapt = hist_acc2d_a_etapt_DPS.GetBinContent(bin_a);
                weight_dacc_a_etapt = hist_dacc2d_a_etapt_DPS.GetBinContent(bin_a);
                weight_acc_b_etapt = hist_acc2d_b_etapt_DPS.GetBinContent(bin_b);
                weight_dacc_b_etapt = hist_dacc2d_b_etapt_DPS.GetBinContent(bin_b);
                weight_recoeff_a = hist_recoeff2d_a_DPS.GetBinContent(bin_a);
                weight_recoeff_b = hist_recoeff2d_b_DPS.GetBinContent(bin_b);
                weight_drecoeff_a = hist_drecoeff2d_a_DPS.GetBinContent(bin_a);
                weight_drecoeff_b = hist_drecoeff2d_a_DPS.GetBinContent(bin_b);
                weight_recoeff_id_a = hist_recoeff2d_id_a_DPS.GetBinContent(bin_a);
                weight_drecoeff_id_a = hist_drecoeff2d_id_a_DPS.GetBinContent(bin_a);
                weight_recoeff_id_b = hist_recoeff2d_id_b_DPS.GetBinContent(bin_b);
                weight_drecoeff_id_b = hist_drecoeff2d_id_b_DPS.GetBinContent(bin_b);
                weight_recoeff_id_vtx_a = hist_recoeff2d_id_vtx_a_DPS.GetBinContent(bin_a);
                weight_drecoeff_id_vtx_a = hist_drecoeff2d_id_vtx_a_DPS.GetBinContent(bin_a);
                weight_recoeff_id_vtx_b = hist_recoeff2d_id_vtx_b_DPS.GetBinContent(bin_b);
                weight_drecoeff_id_vtx_b = hist_drecoeff2d_id_vtx_b_DPS.GetBinContent(bin_b);
                weight_recoeff_trg_vtx = hist_recoeff2d_trg_DPS.GetBinContent(hist_recoeff2d_trg_DPS.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_drecoeff_trg_vtx = hist_drecoeff2d_trg_DPS.GetBinContent(hist_drecoeff2d_trg_DPS.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_recoeff_evt_vtx = hist_recoeff2d_evt_DPS.GetBinContent(hist_recoeff2d_evt_DPS.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_drecoeff_evt_vtx = hist_drecoeff2d_evt_DPS.GetBinContent(hist_drecoeff2d_evt_DPS.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
            if ('Mix' in acc_eff_weights):
                bin_a = hist_acc2d_a_eta_Mix.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_y[0]);
                bin_b = hist_acc2d_b_eta_Mix.FindBin(Tree[Sample].GENdimu_pt[1],Tree[Sample].GENdimu_y[1]);
                weight_acc_a_eta = hist_acc2d_a_eta_Mix.GetBinContent(bin_a);
                weight_dacc_a_eta = hist_dacc2d_a_eta_Mix.GetBinContent(bin_a);
                weight_acc_b_eta = hist_acc2d_b_eta_Mix.GetBinContent(bin_b);
                weight_dacc_b_eta = hist_dacc2d_b_eta_Mix.GetBinContent(bin_b);
                weight_acc_a_etapt = hist_acc2d_a_etapt_Mix.GetBinContent(bin_a);
                weight_dacc_a_etapt = hist_dacc2d_a_etapt_Mix.GetBinContent(bin_a);
                weight_acc_b_etapt = hist_acc2d_b_etapt_Mix.GetBinContent(bin_b);
                weight_dacc_b_etapt = hist_dacc2d_b_etapt_Mix.GetBinContent(bin_b);
                weight_recoeff_a = hist_recoeff2d_a_Mix.GetBinContent(bin_a);
                weight_recoeff_b = hist_recoeff2d_b_Mix.GetBinContent(bin_b);
                weight_drecoeff_a = hist_drecoeff2d_a_Mix.GetBinContent(bin_a);
                weight_drecoeff_b = hist_drecoeff2d_a_Mix.GetBinContent(bin_b);
                weight_recoeff_id_a = hist_recoeff2d_id_a_Mix.GetBinContent(bin_a);
                weight_drecoeff_id_a = hist_drecoeff2d_id_a_Mix.GetBinContent(bin_a);
                weight_recoeff_id_b = hist_recoeff2d_id_b_Mix.GetBinContent(bin_b);
                weight_drecoeff_id_b = hist_drecoeff2d_id_b_Mix.GetBinContent(bin_b);
                weight_recoeff_id_vtx_a = hist_recoeff2d_id_vtx_a_Mix.GetBinContent(bin_a);
                weight_drecoeff_id_vtx_a = hist_drecoeff2d_id_vtx_a_Mix.GetBinContent(bin_a);
                weight_recoeff_id_vtx_b = hist_recoeff2d_id_vtx_b_Mix.GetBinContent(bin_b);
                weight_drecoeff_id_vtx_b = hist_drecoeff2d_id_vtx_b_Mix.GetBinContent(bin_b);
                weight_recoeff_trg_vtx = hist_recoeff2d_trg_Mix.GetBinContent(hist_recoeff2d_trg_Mix.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_drecoeff_trg_vtx = hist_drecoeff2d_trg_Mix.GetBinContent(hist_drecoeff2d_trg_Mix.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_recoeff_evt_vtx = hist_recoeff2d_evt_Mix.GetBinContent(hist_recoeff2d_evt_Mix.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_drecoeff_evt_vtx = hist_drecoeff2d_evt_Mix.GetBinContent(hist_drecoeff2d_evt_Mix.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
            if ('HJJ' in acc_eff_weights):
                bin_a = hist_acc2d_a_eta_HJJ.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_y[0]);
                bin_b = hist_acc2d_b_eta_HJJ.FindBin(Tree[Sample].GENdimu_pt[1],Tree[Sample].GENdimu_y[1]);
                weight_acc_a_eta = hist_acc2d_a_eta_HJJ.GetBinContent(bin_a);
                weight_dacc_a_eta = hist_dacc2d_a_eta_HJJ.GetBinContent(bin_a);
                weight_acc_b_eta = hist_acc2d_b_eta_HJJ.GetBinContent(bin_b);
                weight_dacc_b_eta = hist_dacc2d_b_eta_HJJ.GetBinContent(bin_b);
                weight_acc_a_etapt = hist_acc2d_a_etapt_HJJ.GetBinContent(bin_a);
                weight_dacc_a_etapt = hist_dacc2d_a_etapt_HJJ.GetBinContent(bin_a);
                weight_acc_b_etapt = hist_acc2d_b_etapt_HJJ.GetBinContent(bin_b);
                weight_dacc_b_etapt = hist_dacc2d_b_etapt_HJJ.GetBinContent(bin_b);
                weight_recoeff_a = hist_recoeff2d_a_HJJ.GetBinContent(bin_a);
                weight_recoeff_b = hist_recoeff2d_b_HJJ.GetBinContent(bin_b);
                weight_drecoeff_a = hist_drecoeff2d_a_HJJ.GetBinContent(bin_a);
                weight_drecoeff_b = hist_drecoeff2d_a_HJJ.GetBinContent(bin_b);
                weight_recoeff_id_a = hist_recoeff2d_id_a_HJJ.GetBinContent(bin_a);
                weight_drecoeff_id_a = hist_drecoeff2d_id_a_HJJ.GetBinContent(bin_a);
                weight_recoeff_id_b = hist_recoeff2d_id_b_HJJ.GetBinContent(bin_b);
                weight_drecoeff_id_b = hist_drecoeff2d_id_b_HJJ.GetBinContent(bin_b);
                weight_recoeff_id_vtx_a = hist_recoeff2d_id_vtx_a_HJJ.GetBinContent(bin_a);
                weight_drecoeff_id_vtx_a = hist_drecoeff2d_id_vtx_a_HJJ.GetBinContent(bin_a);
                weight_recoeff_id_vtx_b = hist_recoeff2d_id_vtx_b_HJJ.GetBinContent(bin_b);
                weight_drecoeff_id_vtx_b = hist_drecoeff2d_id_vtx_b_HJJ.GetBinContent(bin_b);
                weight_recoeff_trg_vtx = hist_recoeff2d_trg_HJJ.GetBinContent(hist_recoeff2d_trg_HJJ.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_drecoeff_trg_vtx = hist_drecoeff2d_trg_HJJ.GetBinContent(hist_drecoeff2d_trg_HJJ.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_recoeff_evt_vtx = hist_recoeff2d_evt_HJJ.GetBinContent(hist_recoeff2d_evt_HJJ.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_drecoeff_evt_vtx = hist_drecoeff2d_evt_HJJ.GetBinContent(hist_drecoeff2d_evt_HJJ.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));

            if ('Chib_6' in acc_eff_weights):
                bin_a = hist_acc2d_a_eta_Chib_6.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_y[0]);
                bin_b = hist_acc2d_b_eta_Chib_6.FindBin(Tree[Sample].GENdimu_pt[1],Tree[Sample].GENdimu_y[1]);
                weight_acc_a_eta = hist_acc2d_a_eta_Chib_6.GetBinContent(bin_a);
                weight_dacc_a_eta = hist_dacc2d_a_eta_Chib_6.GetBinContent(bin_a);
                weight_acc_b_eta = hist_acc2d_b_eta_Chib_6.GetBinContent(bin_b);
                weight_dacc_b_eta = hist_dacc2d_b_eta_Chib_6.GetBinContent(bin_b);
                weight_acc_a_etapt = hist_acc2d_a_etapt_Chib_6.GetBinContent(bin_a);
                weight_dacc_a_etapt = hist_dacc2d_a_etapt_Chib_6.GetBinContent(bin_a);
                weight_acc_b_etapt = hist_acc2d_b_etapt_Chib_6.GetBinContent(bin_b);
                weight_dacc_b_etapt = hist_dacc2d_b_etapt_Chib_6.GetBinContent(bin_b);
                weight_recoeff_a = hist_recoeff2d_a_Chib_6.GetBinContent(bin_a);
                weight_recoeff_b = hist_recoeff2d_b_Chib_6.GetBinContent(bin_b);
                weight_drecoeff_a = hist_drecoeff2d_a_Chib_6.GetBinContent(bin_a);
                weight_drecoeff_b = hist_drecoeff2d_a_Chib_6.GetBinContent(bin_b);
                weight_recoeff_id_a = hist_recoeff2d_id_a_Chib_6.GetBinContent(bin_a);
                weight_drecoeff_id_a = hist_drecoeff2d_id_a_Chib_6.GetBinContent(bin_a);
                weight_recoeff_id_b = hist_recoeff2d_id_b_Chib_6.GetBinContent(bin_b);
                weight_drecoeff_id_b = hist_drecoeff2d_id_b_Chib_6.GetBinContent(bin_b);
                weight_recoeff_id_vtx_a = hist_recoeff2d_id_vtx_a_Chib_6.GetBinContent(bin_a);
                weight_drecoeff_id_vtx_a = hist_drecoeff2d_id_vtx_a_Chib_6.GetBinContent(bin_a);
                weight_recoeff_id_vtx_b = hist_recoeff2d_id_vtx_b_Chib_6.GetBinContent(bin_b);
                weight_drecoeff_id_vtx_b = hist_drecoeff2d_id_vtx_b_Chib_6.GetBinContent(bin_b);
                weight_recoeff_trg_vtx = hist_recoeff2d_trg_Chib_6.GetBinContent(hist_recoeff2d_trg_Chib_6.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_drecoeff_trg_vtx = hist_drecoeff2d_trg_Chib_6.GetBinContent(hist_drecoeff2d_trg_Chib_6.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_recoeff_evt_vtx = hist_recoeff2d_evt_Chib_6.GetBinContent(hist_recoeff2d_evt_Chib_6.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_drecoeff_evt_vtx = hist_drecoeff2d_evt_Chib_6.GetBinContent(hist_drecoeff2d_evt_Chib_6.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));

            if ('Chib_7' in acc_eff_weights):
                bin_a = hist_acc2d_a_eta_Chib_7.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_y[0]);
                bin_b = hist_acc2d_b_eta_Chib_7.FindBin(Tree[Sample].GENdimu_pt[1],Tree[Sample].GENdimu_y[1]);
                weight_acc_a_eta = hist_acc2d_a_eta_Chib_7.GetBinContent(bin_a);
                weight_dacc_a_eta = hist_dacc2d_a_eta_Chib_7.GetBinContent(bin_a);
                weight_acc_b_eta = hist_acc2d_b_eta_Chib_7.GetBinContent(bin_b);
                weight_dacc_b_eta = hist_dacc2d_b_eta_Chib_7.GetBinContent(bin_b);
                weight_acc_a_etapt = hist_acc2d_a_etapt_Chib_7.GetBinContent(bin_a);
                weight_dacc_a_etapt = hist_dacc2d_a_etapt_Chib_7.GetBinContent(bin_a);
                weight_acc_b_etapt = hist_acc2d_b_etapt_Chib_7.GetBinContent(bin_b);
                weight_dacc_b_etapt = hist_dacc2d_b_etapt_Chib_7.GetBinContent(bin_b);
                weight_recoeff_a = hist_recoeff2d_a_Chib_7.GetBinContent(bin_a);
                weight_recoeff_b = hist_recoeff2d_b_Chib_7.GetBinContent(bin_b);
                weight_drecoeff_a = hist_drecoeff2d_a_Chib_7.GetBinContent(bin_a);
                weight_drecoeff_b = hist_drecoeff2d_a_Chib_7.GetBinContent(bin_b);
                weight_recoeff_id_a = hist_recoeff2d_id_a_Chib_7.GetBinContent(bin_a);
                weight_drecoeff_id_a = hist_drecoeff2d_id_a_Chib_7.GetBinContent(bin_a);
                weight_recoeff_id_b = hist_recoeff2d_id_b_Chib_7.GetBinContent(bin_b);
                weight_drecoeff_id_b = hist_drecoeff2d_id_b_Chib_7.GetBinContent(bin_b);
                weight_recoeff_id_vtx_a = hist_recoeff2d_id_vtx_a_Chib_7.GetBinContent(bin_a);
                weight_drecoeff_id_vtx_a = hist_drecoeff2d_id_vtx_a_Chib_7.GetBinContent(bin_a);
                weight_recoeff_id_vtx_b = hist_recoeff2d_id_vtx_b_Chib_7.GetBinContent(bin_b);
                weight_drecoeff_id_vtx_b = hist_drecoeff2d_id_vtx_b_Chib_7.GetBinContent(bin_b);
                weight_recoeff_trg_vtx = hist_recoeff2d_trg_Chib_7.GetBinContent(hist_recoeff2d_trg_Chib_7.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_drecoeff_trg_vtx = hist_drecoeff2d_trg_Chib_7.GetBinContent(hist_drecoeff2d_trg_Chib_7.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_recoeff_evt_vtx = hist_recoeff2d_evt_Chib_7.GetBinContent(hist_recoeff2d_evt_Chib_7.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));
                weight_drecoeff_evt_vtx = hist_drecoeff2d_evt_Chib_7.GetBinContent(hist_drecoeff2d_evt_Chib_7.FindBin(Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_pt[1]));

            if (weight_acc_a_eta < 0): weight_acc_a_eta = 0.0
            if (weight_acc_b_eta < 0): weight_acc_b_eta = 0.0
            if (weight_acc_a_etapt < 0): weight_acc_a_etapt = 0.0
            if (weight_acc_b_etapt < 0): weight_acc_b_etapt = 0.0
            if (weight_recoeff_a < 0): weight_recoeff_a = 0.0
            if (weight_recoeff_b < 0): weight_recoeff_b = 0.0
            if (weight_recoeff_id_a < 0): weight_recoeff_id_a = 0.0
            if (weight_recoeff_id_b < 0): weight_recoeff_id_b = 0.0 
            if (weight_recoeff_id_vtx_a < 0): weight_recoeff_id_vtx_a = 0.0
            if (weight_recoeff_id_vtx_b < 0): weight_recoeff_id_vtx_b = 0.0
            if (weight_recoeff_trg_vtx < 0): weight_recoeff_trg_vtx = 0.0
            if (weight_recoeff_evt_vtx < 0): weight_recoeff_evt_vtx = 0.0
            #print '========================'
            #print 'Tree[Sample].GENdimu_pt[0]:Tree[Sample].GENdimu_y[0]', Tree[Sample].GENdimu_pt[0],Tree[Sample].GENdimu_y[0]
            #print 'weight_acc_a_eta:', weight_acc_a_eta
            #print 'weight_acc_a_etapt:', weight_acc_a_etapt
            #print 'Tree[Sample].GENdimu_pt[1]:Tree[Sample].GENdimu_y[1]', Tree[Sample].GENdimu_pt[1],Tree[Sample].GENdimu_y[1]
            #print 'weight_acc_b_eta:', weight_acc_b_eta
            #print 'weight_acc_b_etapt:', weight_acc_b_etapt
            #print '========================'
            Histos[processBin+"hgenfid4mu_eta_closure"].Fill(Tree[Sample].GENdimu_mass[0],weight_acc_a_eta*weight_acc_b_eta)
            Histos[processBin+"hgenfid4mu_eta_closure_up"].Fill(Tree[Sample].GENdimu_mass[0],(weight_acc_a_eta+weight_dacc_a_eta)*(weight_acc_b_eta+weight_dacc_b_eta))
            Histos[processBin+"hgenfid4mu_eta_closure_dn"].Fill(Tree[Sample].GENdimu_mass[0],(weight_acc_a_eta-weight_dacc_a_eta)*(weight_acc_b_eta-weight_dacc_b_eta))
            Histos[processBin+"hgenfid4mu_etaPt_closure"].Fill(Tree[Sample].GENdimu_mass[0],(weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt))
            Histos[processBin+"hgenfid4mu_etaPt_closure_up"].Fill(Tree[Sample].GENdimu_mass[0],((weight_acc_a_eta+weight_dacc_a_eta)*(weight_acc_b_eta+weight_dacc_b_eta)*(weight_acc_a_etapt+weight_dacc_a_etapt)*(weight_acc_b_etapt+weight_dacc_b_etapt)))
            Histos[processBin+"hgenfid4mu_etaPt_closure_dn"].Fill(Tree[Sample].GENdimu_mass[0],((weight_acc_a_eta-weight_dacc_a_eta)*(weight_acc_b_eta-weight_dacc_b_eta)*(weight_acc_a_etapt-weight_dacc_a_etapt)*(weight_acc_b_etapt-weight_dacc_b_etapt)))
            Histos[processBin+"hgenfid4mu_reco_closure"].Fill(Tree[Sample].GENdimu_mass[0],weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt*weight_recoeff_a*weight_recoeff_b)
            Histos[processBin+"hgenfid4mu_reco_closure_up"].Fill(Tree[Sample].GENdimu_mass[0],(weight_acc_a_eta+weight_dacc_a_eta)*(weight_acc_b_eta+weight_dacc_b_eta)*(weight_acc_a_etapt+weight_dacc_a_etapt)*(weight_acc_b_etapt+weight_dacc_b_etapt)*(weight_recoeff_a+weight_drecoeff_a)*(weight_recoeff_b+weight_drecoeff_b))
            Histos[processBin+"hgenfid4mu_reco_closure_dn"].Fill(Tree[Sample].GENdimu_mass[0],(weight_acc_a_eta-weight_dacc_a_eta)*(weight_acc_b_eta-weight_dacc_b_eta)*(weight_acc_a_etapt-weight_dacc_a_etapt)*(weight_acc_b_etapt-weight_dacc_b_etapt)*(weight_recoeff_a-weight_drecoeff_a)*(weight_recoeff_b-weight_drecoeff_b))
            Histos[processBin+"hgenfid4mu_reco_id_closure"].Fill(Tree[Sample].GENdimu_mass[0],weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt*weight_recoeff_a*weight_recoeff_b*weight_recoeff_id_a*weight_recoeff_id_b)
            Histos[processBin+"hgenfid4mu_reco_id_closure_up"].Fill(Tree[Sample].GENdimu_mass[0],(weight_acc_a_eta+weight_dacc_a_eta)*(weight_acc_b_eta+weight_dacc_b_eta)*(weight_acc_a_etapt+weight_dacc_a_etapt)*(weight_acc_b_etapt+weight_dacc_b_etapt)*(weight_recoeff_a+weight_drecoeff_a)*(weight_recoeff_b+weight_drecoeff_b)*(weight_recoeff_id_a+weight_drecoeff_id_a)*(weight_recoeff_id_b+weight_drecoeff_id_b))
            Histos[processBin+"hgenfid4mu_reco_id_closure_dn"].Fill(Tree[Sample].GENdimu_mass[0],(weight_acc_a_eta-weight_dacc_a_eta)*(weight_acc_b_eta-weight_dacc_b_eta)*(weight_acc_a_etapt-weight_dacc_a_etapt)*(weight_acc_b_etapt-weight_dacc_b_etapt)*(weight_recoeff_a-weight_drecoeff_a)*(weight_recoeff_b-weight_drecoeff_b)*(weight_recoeff_id_a-weight_drecoeff_id_a)*(weight_recoeff_id_b-weight_drecoeff_id_b))
            Histos[processBin+"hgenfid4mu_reco_id_vtx_closure"].Fill(Tree[Sample].GENdimu_mass[0],weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt*weight_recoeff_a*weight_recoeff_b*weight_recoeff_id_a*weight_recoeff_id_b*weight_recoeff_id_vtx_a*weight_recoeff_id_vtx_b)
            Histos[processBin+"hgenfid4mu_reco_id_vtx_closure_up"].Fill(Tree[Sample].GENdimu_mass[0],(weight_acc_a_eta+weight_dacc_a_eta)*(weight_acc_b_eta+weight_dacc_b_eta)*(weight_acc_a_etapt+weight_dacc_a_etapt)*(weight_acc_b_etapt+weight_dacc_b_etapt)*(weight_recoeff_a+weight_drecoeff_a)*(weight_recoeff_b+weight_drecoeff_b)*(weight_recoeff_id_a+weight_drecoeff_id_a)*(weight_recoeff_id_b+weight_drecoeff_id_b)*(weight_recoeff_id_vtx_a+weight_drecoeff_id_vtx_a)*(weight_recoeff_id_vtx_b+weight_drecoeff_id_vtx_b))
            Histos[processBin+"hgenfid4mu_reco_id_vtx_closure_dn"].Fill(Tree[Sample].GENdimu_mass[0],(weight_acc_a_eta-weight_dacc_a_eta)*(weight_acc_b_eta-weight_dacc_b_eta)*(weight_acc_a_etapt-weight_dacc_a_etapt)*(weight_acc_b_etapt-weight_dacc_b_etapt)*(weight_recoeff_a-weight_drecoeff_a)*(weight_recoeff_b-weight_drecoeff_b)*(weight_recoeff_id_a-weight_drecoeff_id_a)*(weight_recoeff_id_b-weight_drecoeff_id_b)*(weight_recoeff_id_vtx_a-weight_drecoeff_id_vtx_a)*(weight_recoeff_id_vtx_b-weight_drecoeff_id_vtx_b))
            Histos[processBin+"hgenfid4mu_reco_eff_trg_closure"].Fill(Tree[Sample].GENdimu_mass[0],weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt*weight_recoeff_a*weight_recoeff_b*weight_recoeff_id_a*weight_recoeff_id_b*weight_recoeff_id_vtx_a*weight_recoeff_id_vtx_b*weight_recoeff_trg_vtx)
            Histos[processBin+"hgenfid4mu_reco_eff_trg_closure_up"].Fill(Tree[Sample].GENdimu_mass[0],(weight_acc_a_eta+weight_dacc_a_eta)*(weight_acc_b_eta+weight_dacc_b_eta)*(weight_acc_a_etapt+weight_dacc_a_etapt)*(weight_acc_b_etapt+weight_dacc_b_etapt)*(weight_recoeff_a+weight_drecoeff_a)*(weight_recoeff_b+weight_drecoeff_b)*(weight_recoeff_id_a+weight_drecoeff_id_a)*(weight_recoeff_id_b+weight_drecoeff_id_b)*(weight_recoeff_id_vtx_a+weight_drecoeff_id_vtx_a)*(weight_recoeff_id_vtx_b+weight_drecoeff_id_vtx_b)*(weight_recoeff_trg_vtx+weight_drecoeff_trg_vtx))
            Histos[processBin+"hgenfid4mu_reco_eff_trg_closure_dn"].Fill(Tree[Sample].GENdimu_mass[0],(weight_acc_a_eta-weight_dacc_a_eta)*(weight_acc_b_eta-weight_dacc_b_eta)*(weight_acc_a_etapt-weight_dacc_a_etapt)*(weight_acc_b_etapt-weight_dacc_b_etapt)*(weight_recoeff_a-weight_drecoeff_a)*(weight_recoeff_b-weight_drecoeff_b)*(weight_recoeff_id_a-weight_drecoeff_id_a)*(weight_recoeff_id_b-weight_drecoeff_id_b)*(weight_recoeff_id_vtx_a-weight_drecoeff_id_vtx_a)*(weight_recoeff_id_vtx_b-weight_drecoeff_id_vtx_b)*(weight_recoeff_trg_vtx-weight_drecoeff_trg_vtx))
            Histos[processBin+"hgenfid4mu_reco_eff_evt_closure"].Fill(Tree[Sample].GENdimu_mass[0],weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt*weight_recoeff_a*weight_recoeff_b*weight_recoeff_id_a*weight_recoeff_id_b*weight_recoeff_id_vtx_a*weight_recoeff_id_vtx_b*weight_recoeff_trg_vtx*weight_recoeff_evt_vtx)
            Histos[processBin+"hgenfid4mu_reco_eff_evt_closure_up"].Fill(Tree[Sample].GENdimu_mass[0],(weight_acc_a_eta+weight_dacc_a_eta)*(weight_acc_b_eta+weight_dacc_b_eta)*(weight_acc_a_etapt+weight_dacc_a_etapt)*(weight_acc_b_etapt+weight_dacc_b_etapt)*(weight_recoeff_a+weight_drecoeff_a)*(weight_recoeff_b+weight_drecoeff_b)*(weight_recoeff_id_a+weight_drecoeff_id_a)*(weight_recoeff_id_b+weight_drecoeff_id_b)*(weight_recoeff_id_vtx_a+weight_drecoeff_id_vtx_a)*(weight_recoeff_id_vtx_b+weight_drecoeff_id_vtx_b)*(weight_recoeff_trg_vtx+weight_drecoeff_trg_vtx)*(weight_recoeff_evt_vtx+weight_drecoeff_evt_vtx))
            Histos[processBin+"hgenfid4mu_reco_eff_evt_closure_dn"].Fill(Tree[Sample].GENdimu_mass[0],(weight_acc_a_eta-weight_dacc_a_eta)*(weight_acc_b_eta-weight_dacc_b_eta)*(weight_acc_a_etapt-weight_dacc_a_etapt)*(weight_acc_b_etapt-weight_dacc_b_etapt)*(weight_recoeff_a-weight_drecoeff_a)*(weight_recoeff_b-weight_drecoeff_b)*(weight_recoeff_id_a-weight_drecoeff_id_a)*(weight_recoeff_id_b-weight_drecoeff_id_b)*(weight_recoeff_id_vtx_a-weight_drecoeff_id_vtx_a)*(weight_recoeff_id_vtx_b-weight_drecoeff_id_vtx_b)*(weight_recoeff_trg_vtx-weight_drecoeff_trg_vtx)*(weight_recoeff_evt_vtx-weight_drecoeff_evt_vtx))
        print "Sample: ",processBin
        print "acc_eff_weights", acc_eff_weights
        print "invalid events:", invalid_events
        print 'total_events: ', total_events
        print "hgenfid4mu:" ,round(Histos[processBin+"hgenfid4mu"].Integral(),2)
        print "hgenfid4mu_eta_selected:",round(Histos[processBin+"hgenfid4mu_eta_selected"].Integral(),2)
        print "hgenfid4mu_eta_closure:", round(Histos[processBin+"hgenfid4mu_eta_closure"].Integral(),2)
        print "hgenfid4mu_eta_closure_up:", round(Histos[processBin+"hgenfid4mu_eta_closure_up"].Integral(),2)
        print "hgenfid4mu_eta_closure_dn:", round(Histos[processBin+"hgenfid4mu_eta_closure_dn"].Integral(),2)
        print "hgenfid4mu_etaPt_selected:", round(Histos[processBin+"hgenfid4mu_etaPt_selected"].Integral(),2)
        print "hgenfid4mu_etaPt_closure:", round(Histos[processBin+"hgenfid4mu_etaPt_closure"].Integral(),2)
        print "hgenfid4mu_etaPt_closure_up:", round(Histos[processBin+"hgenfid4mu_etaPt_closure_up"].Integral(),2)
        print "hgenfid4mu_etaPt_closure_dn:", round(Histos[processBin+"hgenfid4mu_etaPt_closure_dn"].Integral(),2)
        print "hgenfid4mu_reco_selected:", round(Histos[processBin+"hgenfid4mu_reco_selected"].Integral(),2)
        print "hgenfid4mu_reco_closure:", round(Histos[processBin+"hgenfid4mu_reco_closure"].Integral(),2)
        print "hgenfid4mu_reco_closure_up:", round(Histos[processBin+"hgenfid4mu_reco_closure_up"].Integral(),2)
        print "hgenfid4mu_reco_closure_dn:", round(Histos[processBin+"hgenfid4mu_reco_closure_dn"].Integral(),2)
        print "hgenfid4mu_reco_id_selected:", round(Histos[processBin+"hgenfid4mu_reco_id_selected"].Integral(),2)
        print "hgenfid4mu_reco_id_closure:", round(Histos[processBin+"hgenfid4mu_reco_id_closure"].Integral(),2)
        print "hgenfid4mu_reco_id_closure_up:", round(Histos[processBin+"hgenfid4mu_reco_id_closure_up"].Integral(),2)
        print "hgenfid4mu_reco_id_closure_dn:", round(Histos[processBin+"hgenfid4mu_reco_id_closure_dn"].Integral(),2)
        print "hgenfid4mu_reco_id_vtx_selected:", round(Histos[processBin+"hgenfid4mu_reco_id_vtx_selected"].Integral(),2)
        print "hgenfid4mu_reco_id_vtx_closure:", round(Histos[processBin+"hgenfid4mu_reco_id_vtx_closure"].Integral(),2)
        print "hgenfid4mu_reco_id_vtx_closure_up:", round(Histos[processBin+"hgenfid4mu_reco_id_vtx_closure_up"].Integral(),2)
        print "hgenfid4mu_reco_id_vtx_closure_dn:", round(Histos[processBin+"hgenfid4mu_reco_id_vtx_closure_dn"].Integral(),2)
        print "hgenfid4mu_reco_eff_trg_selected:", round(Histos[processBin+"hgenfid4mu_reco_eff_trg_selected"].Integral(),2)
        print "hgenfid4mu_reco_eff_trg_closure:", round(Histos[processBin+"hgenfid4mu_reco_eff_trg_closure"].Integral(),2)
        print "hgenfid4mu_reco_eff_trg_closure_up:", round(Histos[processBin+"hgenfid4mu_reco_eff_trg_closure_up"].Integral(),2)
        print "hgenfid4mu_reco_eff_trg_closure_dn:", round(Histos[processBin+"hgenfid4mu_reco_eff_trg_closure_dn"].Integral(),2)
        print "hgenfid4mu_reco_eff_evt_selected:", round(Histos[processBin+"hgenfid4mu_reco_eff_evt_selected"].Integral(),2)
        print "hgenfid4mu_reco_eff_evt_closure:", round(Histos[processBin+"hgenfid4mu_reco_eff_evt_closure"].Integral(),2)
        print "hgenfid4mu_reco_eff_evt_closure_up:", round(Histos[processBin+"hgenfid4mu_reco_eff_evt_closure_up"].Integral(),2)
        print "hgenfid4mu_reco_eff_evt_closure_dn:", round(Histos[processBin+"hgenfid4mu_reco_eff_evt_closure_dn"].Integral(),2)
        print "----------------------------------------------------------------------------------------------------------------"
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_eta_selected"] = round(Histos[processBin+"hgenfid4mu_eta_selected"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_eta_closure"] = round(Histos[processBin+"hgenfid4mu_eta_closure"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_eta_closure_up"] = round(Histos[processBin+"hgenfid4mu_eta_closure_up"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_eta_closure_dn"] = round(Histos[processBin+"hgenfid4mu_eta_closure_dn"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_etaPt_selected"] = round(Histos[processBin+"hgenfid4mu_etaPt_selected"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_etaPt_closure"] = round(Histos[processBin+"hgenfid4mu_etaPt_closure"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_etaPt_closure_up"] = round(Histos[processBin+"hgenfid4mu_etaPt_closure_up"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_etaPt_closure_dn"] = round(Histos[processBin+"hgenfid4mu_etaPt_closure_dn"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_selected"] = round(Histos[processBin+"hgenfid4mu_reco_selected"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_closure"] = round(Histos[processBin+"hgenfid4mu_reco_closure"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_closure_up"] = round(Histos[processBin+"hgenfid4mu_reco_closure_up"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_closure_dn"] = round(Histos[processBin+"hgenfid4mu_reco_closure_dn"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_id_selected"] = round(Histos[processBin+"hgenfid4mu_reco_id_selected"].Integral(),2) 
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_id_closure"] =  round(Histos[processBin+"hgenfid4mu_reco_id_closure"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_id_closure_up"] = round(Histos[processBin+"hgenfid4mu_reco_id_closure_up"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_id_closure_dn"] = round(Histos[processBin+"hgenfid4mu_reco_id_closure_dn"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_id_vtx_selected"] = round(Histos[processBin+"hgenfid4mu_reco_id_vtx_selected"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_id_vtx_closure"] = round(Histos[processBin+"hgenfid4mu_reco_id_vtx_closure"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_id_vtx_closure_up"] = round(Histos[processBin+"hgenfid4mu_reco_id_vtx_closure_up"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_id_vtx_closure_dn"] = round(Histos[processBin+"hgenfid4mu_reco_id_vtx_closure_dn"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_eff_trg_selected"] = round(Histos[processBin+"hgenfid4mu_reco_eff_trg_selected"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_eff_trg_closure"] = round(Histos[processBin+"hgenfid4mu_reco_eff_trg_closure"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_eff_trg_closure_up"] = round(Histos[processBin+"hgenfid4mu_reco_eff_trg_closure_up"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_eff_trg_closure_dn"] = round(Histos[processBin+"hgenfid4mu_reco_eff_trg_closure_dn"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_eff_evt_selected"] = round(Histos[processBin+"hgenfid4mu_reco_eff_evt_selected"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_eff_evt_closure"] = round(Histos[processBin+"hgenfid4mu_reco_eff_evt_closure"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_eff_evt_closure_up"] = round(Histos[processBin+"hgenfid4mu_reco_eff_evt_closure_up"].Integral(),2)
        closure[processBin+"_"+acc_eff_weights+"_hgenfid4mu_reco_eff_evt_closure_dn"] = round(Histos[processBin+"hgenfid4mu_reco_eff_evt_closure_dn"].Integral(),2)
#with open('closure_test_results.py', 'w') as f:
#     f.write('closure_results = '+str(closure)+' \n')
         
