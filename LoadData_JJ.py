from ROOT import *
from array import array
import os
#dirMC_102 = '/eos/uscms/store/user/muahmad/FourMuon_Analysis/NTuples/NTuples_JJ/Signal_MC'
dirMC_102 = '/eos/uscms/store/user/muahmad/FourMuon_Analysis/NTuples/NTuples_JJ/GENonly_MC'
SamplesMC_102 = [
'SPSToJJ_13TeV_pythia8.root',
'DPSToJJ_13TeV_pythia8.root',
#'HToJJ_m6500_13TeV_JHUpythia8.root',
#'HToJJ_m6900_13TeV_JHUpythia8.root'
#'Rootuple_JHU_JJto4mu_0p_mass6dot2.root',
#'Rootuple_JHU_JJto4mu_0p_mass6dot3.root',  
#'Rootuple_JHU_JJto4mu_0p_mass6dot5.root',
#'Rootuple_JHU_JJto4mu_0p_mass7dot5.root'
]
###################################################### 
RootFile = {} 
Tree = {} 
nEvents = {} 


# 102X MC
for i in range(0,len(SamplesMC_102)):

    sample = SamplesMC_102[i].replace('.root','')

    RootFile[sample] = TFile(dirMC_102+'/'+sample+'.root',"READ")
    Tree[sample]  = RootFile[sample].Get("GenAnalyzer/gen_tree")
    #h_nevents = RootFile[sample].Get("rootuple/Total_events")

    #if (h_nevents): nEvents[sample] = h_nevents.Integral()
    #else: nEvents[sample] = 0.

    if (not Tree[sample]): print sample+' has no gen. tree'
    else:
        print sample

