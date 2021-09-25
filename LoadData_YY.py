from ROOT import *
from array import array
import os
#dirMC_102 = '/eos/uscms/store/user/muahmad/FourMuon_Analysis/NTuples/NTuples_JJ/Signal_MC'
dirMC_102 = '/eos/uscms/store/user/muahmad/FourMuon_Analysis/NTuples/2018/DoubleUpsilon/MuOnia_v3/Background_MC/Pythia8_SPStoYY_Direct/MC2018_SKIM_RECO_zhliang_vJY4s-MuMuGammaRootuple-/210406_095508/0000/'
SamplesMC_102 = [
'pythiaToYY_13TeV_pythia8_1.root'
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

