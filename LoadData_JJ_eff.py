from ROOT import *
from array import array
import os
dirMC_102 = '/eos/uscms/store/user/muahmad/FourMuon_Analysis/NTuples/NTuples_JJ/Background_MC/SPS_match'
gen_dirMC_102 = '/eos/uscms/store/user/muahmad/FourMuon_Analysis/NTuples/NTuples_JJ/GENonly_MC'
SamplesMC_102 = [
'SPSToJJ_13TeV_pythia8.root',
#'DPSToJJ_13TeV_pythia8.root',
#'HToJJ_m6200_13TeV_JHUpythia8.root',
#'HToJJ_m6300_13TeV_JHUpythia8.root',
#'HToJJ_m6400_13TeV_JHUpythia8.root',
#'HToJJ_m6500_13TeV_JHUpythia8.root',
#'HToJJ_m6900_13TeV_JHUpythia8.root',
#'HToJJ_13TeV_JHUpythia8.root', # All above added together to gain statistics
#'Chib0_6300_ToJpsiJpsi_TuneCP5_13TeV-pythia.root',
#'Chib0_6500_ToJpsiJpsi_TuneCP5_13TeV-pythia.root',
#'Chib0_6700_ToJpsiJpsi_TuneCP5_13TeV-pythia.root',
#'Chib0_6900_ToJpsiJpsi_TuneCP5_13TeV-pythia.root',
#'Chib0_6X00_ToJpsiJpsi_TuneCP5_13TeV-pythia.root', 
#'Chib0_7100_ToJpsiJpsi_TuneCP5_13TeV-pythia.root',
#'Chib0_7300_ToJpsiJpsi_TuneCP5_13TeV-pythia.root', 
#'Chib0_7500_ToJpsiJpsi_TuneCP5_13TeV-pythia.root',
#'Chib0_7700_ToJpsiJpsi_TuneCP5_13TeV-pythia.root',
#'Chib0_7X00_ToJpsiJpsi_TuneCP5_13TeV-pythia.root' 
]
gen_SamplesMC_102 = [
'SPSToJJ_13TeV_pythia8.root',
'DPSToJJ_13TeV_pythia8.root'
]
###################################################### 
RootFile = {} 
GRootFile = {}
Tree = {}
GTree = {} 
nEvents = {} 


# 102X MC
for i in range(0,len(SamplesMC_102)):

    sample = SamplesMC_102[i].replace('.root','')

    RootFile[sample] = TFile(dirMC_102+'/'+sample+'.root',"READ")
    Tree[sample]  = RootFile[sample].Get("rootuple/oniaTree")
    h_nevents = RootFile[sample].Get("rootuple/Total_events")

    if (h_nevents): nEvents[sample] = h_nevents.Integral()
    else: nEvents[sample] = 0.

    if (not Tree[sample]): print sample+' has no reco. tree'
    else:
        print sample
# gen_102X MC
#for i in range(0,len(gen_SamplesMC_102)):
#
#    sample = gen_SamplesMC_102[i].replace('.root','')
#
#    GRootFile[sample] = TFile(gen_dirMC_102+'/'+sample+'.root',"READ")
#    GTree[sample]  = GRootFile[sample].Get("GenAnalyzer/gen_tree")
#
#    if (not GTree[sample]): print sample+' has no gen. tree'

#    else:
#        print sample
                      

