from ROOT import *
from math import *

from LoadData_JJ_eff import *
from sample_shortnames_JJ import *

#read root files/histrograms for closure test
f_acc_DPS = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff/JJ_plots/acc_hist_DPS_JJto4mu.root")
hist_acc2d_b_eta_DPS = f_acc_DPS.Get("acc2d_b_eta")
hist_acc2d_a_eta_DPS = f_acc_DPS.Get("acc2d_a_eta");
hist_dacc2d_b_eta_DPS = f_acc_DPS.Get("dacc2d_b_eta");
hist_dacc2d_a_eta_DPS = f_acc_DPS.Get("dacc2d_a_eta");
hist_acc2d_b_etapt_DPS = f_acc_DPS.Get("acc2d_b_etapt");
hist_acc2d_a_etapt_DPS = f_acc_DPS.Get("acc2d_a_etapt");
hist_dacc2d_b_etapt_DPS = f_acc_DPS.Get("dacc2d_b_etapt");
hist_dacc2d_a_etapt_DPS = f_acc_DPS.Get("dacc2d_a_etapt");
f_acc_Mix = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff/JJ_plots/acc_hist_Mix_SPS_DPS.root");
hist_acc2d_b_eta_Mix = f_acc_Mix.Get("acc2d_b_eta");
hist_acc2d_a_eta_Mix = f_acc_Mix.Get("acc2d_a_eta");
hist_dacc2d_b_eta_Mix = f_acc_Mix.Get("dacc2d_b_eta");
hist_dacc2d_a_eta_Mix = f_acc_Mix.Get("dacc2d_a_eta");
hist_acc2d_b_etapt_Mix = f_acc_Mix.Get("acc2d_b_etapt");
hist_acc2d_a_etapt_Mix = f_acc_Mix.Get("acc2d_a_etapt");
hist_dacc2d_b_etapt_Mix = f_acc_Mix.Get("dacc2d_b_etapt");
hist_dacc2d_a_etapt_Mix = f_acc_Mix.Get("dacc2d_a_etapt");
f_acc_SPS = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff/JJ_plots/acc_hist_SPS_JJto4mu.root");
hist_acc2d_b_eta_SPS = f_acc_SPS.Get("acc2d_b_eta");
hist_acc2d_a_eta_SPS = f_acc_SPS.Get("acc2d_a_eta");
hist_dacc2d_b_eta_SPS = f_acc_SPS.Get("dacc2d_b_eta");
hist_dacc2d_a_eta_SPS = f_acc_SPS.Get("dacc2d_a_eta");
hist_acc2d_b_etapt_SPS = f_acc_SPS.Get("acc2d_b_etapt");
hist_acc2d_a_etapt_SPS = f_acc_SPS.Get("acc2d_a_etapt");
hist_dacc2d_b_etapt_SPS = f_acc_SPS.Get("dacc2d_b_etapt");
hist_dacc2d_a_etapt_SPS = f_acc_SPS.Get("dacc2d_a_etapt");
f_eff_SPS = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff/JJ_plots/eff_hist_SPS_JJto4mu.root");
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
f_evt_eff_SPS = TFile("/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon_slc7/CMSSW_10_2_5/src/Acc_Eff/JJ_plots/evt_eff_hist_SPS_JJto4mu.root");
hist_recoeff2d_evt_SPS = f_evt_eff_SPS.Get("recoeff2d_evt");
hist_drecoeff2d_evt_SPS = f_evt_eff_SPS.Get("drecoeff2d_evt");
hist_recoeff2d_evt_sym_SPS = f_evt_eff_SPS.Get("recoeff2d_evt_sym");
hist_drecoeff2d_evt_sym_SPS = f_evt_eff_SPS.Get("drecoeff2d_evt_sym");

####acceptance related cuts strings
gen_mu_eta_cut = 2.4
gen_mu_pt_cut = 2.0
obs_gen_low_y = -2.0
obs_gen_high_y = 2.0
obs_gen_low_pt = 0 
obs_gen_high_pt = 40.0
cut_ups_gen_ya     = "(GENups_y[0] > "+str(obs_gen_low_y)+ " && GENups_y[0] < " + str(obs_gen_high_y) + ")"
cut_ups_reco_ya     = "(ups1_y_GenMatched > "+str(obs_gen_low_y)+ " && ups1_y_GenMatched < " + str(obs_gen_high_y) + ")"
cut_ups_gen_yb     = "(GENups_y[1] > "+str(obs_gen_low_y)+ " && GENups_y[1] < " + str(obs_gen_high_y) + ")"
cut_ups_reco_yb     = "(ups2_y_GenMatched > "+str(obs_gen_low_y)+ " && ups2_y_GenMatched < " + str(obs_gen_high_y) + ")"
cut_ups_gen_pta    = "(GENups_pt[0] > "+str(obs_gen_low_pt)+ " && GENups_pt[0] < " + str(obs_gen_high_pt) + ")"
cut_ups_reco_pta    = "(ups1_pt_GenMatched > "+str(obs_gen_low_pt)+ " && ups1_pt_GenMatched < " + str(obs_gen_high_pt) + ")"
cut_ups_gen_ptb    = "(GENups_pt[1] > "+str(obs_gen_low_pt)+ " && GENups_pt[1] < " + str(obs_gen_high_pt) + ")"
cut_ups_reco_ptb    = "(ups2_pt_GenMatched > "+str(obs_gen_low_pt)+ " && ups2_pt_GenMatched < " + str(obs_gen_high_pt) + ")"
cut_mu_gen_eta_a   = "(abs(GENups_Daughter_mueta[0]) < "+str(gen_mu_eta_cut)+ " && abs(GENups_Daughter_mueta[1]) < "+str(gen_mu_eta_cut)+")"
cut_mu_gen_pt_a   = "(GENups_Daughter_mupt[0] > "+str(gen_mu_pt_cut)+ " && GENups_Daughter_mupt[1] > "+str(gen_mu_pt_cut)+")"
cut_mu_gen_eta_b   = "(abs(GENups_Daughter_mueta[2]) < "+str(gen_mu_eta_cut)+ " && abs(GENups_Daughter_mueta[3]) < "+str(gen_mu_eta_cut)+")"
cut_mu_gen_pt_b   = "(GENups_Daughter_mupt[2] > "+str(gen_mu_pt_cut)+ " && GENups_Daughter_mupt[3] > "+str(gen_mu_pt_cut)+")"
cut_mu_gen_Momid_a = "(GENups_DaughtersId[0]==13 && GENups_DaughtersId[1]==13)"
cut_mu_gen_Momid_b = "(GENups_DaughtersId[2]==13 && GENups_DaughtersId[3]==13)"
cut_reco_ups_a    = "ups1_mass_GenMatched>0"
cut_reco_ups_b    = "ups2_mass_GenMatched>0"
cut_reco_id_ups_a = "ups1_mass_GenMatched_ID>0"
cut_reco_id_ups_b = "ups2_mass_GenMatched_ID>0"
cut_reco_id_vtx_ups_a = "ups1_mass_GenMatched_ID_OS_VTX>0"
cut_reco_id_vtx_ups_b = "ups2_mass_GenMatched_ID_OS_VTX>0"
cut_reco_evt = "fourmu_mass_allcuts>0"

genweight = '1.0'
recoweight = '1.0'
channel = '4mu'
OBSNAME = 'pT2mu_rapidity2mu'
List = []
Histos = {}
for long, short in sample_shortnames.iteritems():
    List.append(long)

i_sample = -1
invalid_events = 0
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

    Histos[processBin+"hgenfid4mu_eta_closure"] = TH1D(processBin+"hgenfid4mu_eta_closure", processBin+"hgenfid4mu_eta_closure", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu_eta_closure"].Sumw2()
    Histos[processBin+"hgenfid4mu_etaPt_closure"] = TH1D(processBin+"hgenfid4mu_etaPt_closure", processBin+"hgenfid4mu_etaPt_closure", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu_etaPt_closure"].Sumw2()
    Histos[processBin+"hgenfid4mu_reco_closure"] = TH1D(processBin+"hgenfid4mu_reco_closure", processBin+"hgenfid4mu_reco_closure", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu_reco_closure"].Sumw2()
    Histos[processBin+"hgenfid4mu_reco_closure_test"] = TH1D(processBin+"hgenfid4mu_reco_closure_test", processBin+"hgenfid4mu_reco_closure_test", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu_reco_closure_test"].Sumw2()
    Histos[processBin+"hgenfid4mu_reco_id_closure"] = TH1D(processBin+"hgenfid4mu_reco_id_closure", processBin+"reco_eff_id_a", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu_reco_id_closure"].Sumw2()
    Histos[processBin+"hgenfid4mu_reco_id_vtx_closure"] = TH1D(processBin+"hgenfid4mu_reco_id_vtx_closure", processBin+"hgenfid4mu_reco_id_vtx_closure", 25, 0, 10000)
    Histos[processBin+"hgenfid4mu_reco_id_vtx_closure"].Sumw2()


    GTree[Sample].Draw("GENups_mass[0]>> "+processBin+"hgenfid4mu","("+genweight+")*("+cut_ups_gen_ya+" && " + cut_ups_gen_pta + " && " +cut_mu_gen_Momid_a + "&&" + cut_ups_gen_yb+" && " + cut_ups_gen_ptb + " && " + cut_mu_gen_Momid_b+")","goff")

    GTree[Sample].Draw("GENups_mass[0] >> "+processBin+"hgenfid4mu_eta_selected","("+genweight+")*("+cut_ups_gen_ya+" && "+cut_ups_gen_pta+" && "+cut_mu_gen_eta_a+" && "+cut_mu_gen_Momid_a+ "&&" + cut_ups_gen_yb+" && "+cut_ups_gen_ptb+" && "+cut_mu_gen_eta_b+" && "+cut_mu_gen_Momid_b+")","goff")

    GTree[Sample].Draw("GENups_mass[0] >> "+processBin+"hgenfid4mu_etaPt_selected","("+genweight+")*("+cut_ups_gen_ya+" && "+cut_ups_gen_pta+" && "+cut_mu_gen_eta_a+" && "+ cut_mu_gen_pt_a + "  && "+cut_mu_gen_Momid_a+ "&&" + cut_ups_gen_yb+" && "+cut_ups_gen_ptb+" && "+cut_mu_gen_eta_b+" && "+ cut_mu_gen_pt_b+" && "+cut_mu_gen_Momid_b+")","goff")
    str_reco_a = cut_reco_ups_a+" && " +cut_ups_reco_ya+" && "+cut_ups_reco_pta+" && "+cut_ups_gen_ya+" && "+cut_ups_gen_pta+" && "+cut_mu_gen_eta_a+" && "+ cut_mu_gen_pt_a + "  && "+cut_mu_gen_Momid_a
    str_reco_b = cut_reco_ups_b+ " && " +cut_ups_reco_yb+" && "+cut_ups_reco_ptb+" && "+cut_ups_gen_yb+" && "+cut_ups_gen_ptb+" && "+cut_mu_gen_eta_b+" && "+ cut_mu_gen_pt_b+" && "+cut_mu_gen_Momid_b
    str_reco_id_a = str_reco_a+" && "+cut_reco_id_ups_a 
    str_reco_id_b = str_reco_b+" && "+cut_reco_id_ups_b 
    str_reco_id_vtx_a= str_reco_id_a+" && "+cut_reco_id_vtx_ups_a
    str_reco_id_vtx_b= str_reco_id_b+" && "+cut_reco_id_vtx_ups_b
    Tree[Sample].Draw("ups1_mass_GenMatched >> "+processBin+"hgenfid4mu_reco_selected","("+recoweight+")*("+str_reco_a+" && "+str_reco_b +")","goff")
    Tree[Sample].Draw("ups1_mass_GenMatched_ID >> " +processBin+"hgenfid4mu_reco_id_selected","("+recoweight+")*("+str_reco_id_a+" && "+str_reco_id_b+")","goff")
    Tree[Sample].Draw("ups1_mass_GenMatched_ID_OS_VTX >> " +processBin+"hgenfid4mu_reco_id_vtx_selected","("+recoweight+")*("+str_reco_id_vtx_a+ " && "+str_reco_id_vtx_b+")","goff")

    nentries = Tree[Sample].GetEntries()
    print 'nentries:', nentries
    for i in range(nentries):
        Tree[Sample].GetEntry(i)
        if (i%1000==0): print Sample,i,'/',nentries
        #if (i>100): break
        if (Tree[Sample].ups1_pt_GenMatched < obs_gen_low_pt or Tree[Sample].ups1_pt_GenMatched > obs_gen_high_pt ): continue
        if (Tree[Sample].ups2_pt_GenMatched < obs_gen_low_pt or Tree[Sample].ups2_pt_GenMatched > obs_gen_high_pt ): continue
        if (Tree[Sample].ups1_y_GenMatched  < obs_gen_low_y  or Tree[Sample].ups1_y_GenMatched  > obs_gen_high_y ): continue
        if (Tree[Sample].ups2_y_GenMatched  < obs_gen_low_y  or Tree[Sample].ups2_y_GenMatched  > obs_gen_high_y ): continue
        #if (not abs(GTree[Sample].GENups_DaughtersId[0])==13 and abs(GTree[Sample].GENups_DaughtersId[1])==13 ): continue
        #if (not abs(GTree[Sample].GENups_DaughtersId[2])==13 and abs(GTree[Sample].GENups_DaughtersId[3])==13 ): continue
        if ('SPS' in Sample):
            bin_a = hist_acc2d_a_eta_SPS.FindBin(Tree[Sample].ups1_pt_GenMatched,Tree[Sample].ups1_y_GenMatched );
            bin_b = hist_acc2d_b_eta_SPS.FindBin(Tree[Sample].ups2_pt_GenMatched,Tree[Sample].ups2_y_GenMatched);
            weight_acc_a_eta = hist_acc2d_a_eta_SPS.GetBinContent(bin_a);
            weight_acc_b_eta = hist_acc2d_b_eta_SPS.GetBinContent(bin_b);
            weight_acc_a_etapt = hist_acc2d_a_etapt_SPS.GetBinContent(bin_a);
            weight_acc_b_etapt = hist_acc2d_b_etapt_SPS.GetBinContent(bin_b);
            weight_recoeff_a = hist_recoeff2d_a_SPS.GetBinContent(bin_a);
            weight_recoeff_b = hist_recoeff2d_b_SPS.GetBinContent(bin_b);
            weight_recoeff_id_a = hist_recoeff2d_id_a_SPS.GetBinContent(bin_a);
            weight_recoeff_id_b = hist_recoeff2d_id_b_SPS.GetBinContent(bin_b);
            weight_recoeff_id_vtx_a = hist_recoeff2d_id_vtx_a_SPS.GetBinContent(bin_a);
            weight_recoeff_id_vtx_b = hist_recoeff2d_id_vtx_b_SPS.GetBinContent(bin_b);

        if ('DPS' in Sample):
            bin_a = hist_acc2d_a_eta_DPS.FindBin(GTree[Sample].GENups_pt[0],GTree[Sample].GENups_y[0]);
            bin_b = hist_acc2d_b_eta_DPS.FindBin(GTree[Sample].GENups_pt[1],GTree[Sample].GENups_y[1]);
            weight_acc_a_eta = hist_acc2d_a_eta_DPS.GetBinContent(bin_a);
            weight_acc_b_eta = hist_acc2d_b_eta_DPS.GetBinContent(bin_b);
            weight_acc_a_etapt = hist_acc2d_a_etapt_DPS.GetBinContent(bin_a);
            weight_acc_b_etapt = hist_acc2d_b_etapt_DPS.GetBinContent(bin_b);
            weight_recoeff_a = hist_recoeff2d_a_DPS.GetBinContent(bin_a);
            weight_recoeff_b = hist_recoeff2d_b_DPS.GetBinContent(bin_b);
            weight_recoeff_id_a = hist_recoeff2d_id_a_DPS.GetBinContent(bin_a);
            weight_recoeff_id_b = hist_recoeff2d_id_b_DPS.GetBinContent(bin_b);
            weight_recoeff_id_vtx_a = hist_recoeff2d_id_vtx_a_DPS.GetBinContent(bin_a);
            weight_recoeff_id_vtx_b = hist_recoeff2d_id_vtx_b_DPS.GetBinContent(bin_b);
        '''         
        print 'GTree[Sample].GENups_pt[0]',GTree[Sample].GENups_pt[0]
        print 'GTree[Sample].GENups_y[0]', GTree[Sample].GENups_y[0]
        print 'GTree[Sample].GENups_pt[1]', GTree[Sample].GENups_pt[1]
        print 'GTree[Sample].GENups_y[1]', GTree[Sample].GENups_y[1]
        print 'bin_a', bin_a
        print 'bin_b', bin_b
        print 'weight_acc_a_eta',weight_acc_a_eta
        print 'weight_acc_b_eta', weight_acc_b_eta
        print 'weight_acc_a_etapt', weight_acc_a_etapt
        print 'weight_acc_b_etapt', weight_acc_b_etapt
        print 'mass', GTree[Sample].GENups_mass[0]
        print 'weight', weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt
        print '======================='
        '''
        Histos[processBin+"hgenfid4mu_eta_closure"].Fill(GTree[Sample].GENups_mass[0],weight_acc_a_eta*weight_acc_b_eta)
        Histos[processBin+"hgenfid4mu_etaPt_closure"].Fill(GTree[Sample].GENups_mass[0],weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt)
        Histos[processBin+"hgenfid4mu_reco_closure"].Fill(Tree[Sample].ups1_mass_GenMatched,weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt*weight_recoeff_a*weight_recoeff_b)
        Histos[processBin+"hgenfid4mu_reco_closure_test"].Fill(Tree[Sample].ups1_mass_GenMatched,weight_recoeff_a*weight_recoeff_b)
#        Histos[processBin+"hgenfid4mu_reco_id_closure"].Fill(GTree[Sample].GENups_mass[0],weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt*weight_recoeff_a*weight_recoeff_b*weight_recoeff_id_a*weight_recoeff_id_b)
#        Histos[processBin+"hgenfid4mu_reco_id_vtx_closure"].Fill(GTree[Sample].GENups_mass[0],weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt*weight_recoeff_a*weight_recoeff_b*weight_recoeff_id_a*weight_recoeff_id_b*weight_recoeff_id_vtx_a*weight_recoeff_id_vtx_b)
'''
        Histos[processBin+"hgenfid4mu_reco_selected"].Fill(GTree[Sample].ups1_mass_GenMatched,weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt*weight_recoeff_a*weight_recoeff_b)
        Histos[processBin+"hgenfid4mu_reco_id_selected"].Fill(Tree[Sample].ups1_mass_GenMatched_ID,weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt*weight_recoeff_a*weight_recoeff_b*weight_recoeff_id_a*weight_recoeff_id_b)
        Histos[processBin+"hgenfid4mu_reco_id_vtx_selected"].Fill(Tree[Sample].ups1_mass_GenMatched_ID_OS_VTX,weight_acc_a_eta*weight_acc_b_eta*weight_acc_a_etapt*weight_acc_b_etapt*weight_recoeff_a*weight_recoeff_b*weight_recoeff_id_a*weight_recoeff_id_b*weight_recoeff_id_vtx_a*weight_recoeff_id_vtx_b)

'''

print "invalid events:", invalid_events
print "hgenfid4mu:" ,round(Histos[processBin+"hgenfid4mu"].Integral(),5)
print "hgenfid4mu_eta_selected:",round(Histos[processBin+"hgenfid4mu_eta_selected"].Integral(),5)
print "hgenfid4mu_eta_closure:", round(Histos[processBin+"hgenfid4mu_eta_closure"].Integral(),5)
print "hgenfid4mu_etaPt_selected:", round(Histos[processBin+"hgenfid4mu_etaPt_selected"].Integral(),5)
print "hgenfid4mu_etaPt_closure:", round(Histos[processBin+"hgenfid4mu_etaPt_closure"].Integral(),5)
print "hgenfid4mu_reco_selected:", round(Histos[processBin+"hgenfid4mu_reco_selected"].Integral(),2)
print "hgenfid4mu_reco_closure:", round(Histos[processBin+"hgenfid4mu_reco_closure"].Integral(),2)
print "hgenfid4mu_reco_closure_test:", round(Histos[processBin+"hgenfid4mu_reco_closure_test"].Integral(),2)
#print "hgenfid4mu_reco_id_selected:", round(Histos[processBin+"hgenfid4mu_reco_id_selected"].Integral(),2)
#print "hgenfid4mu_reco_id_closure:", round(Histos[processBin+"hgenfid4mu_reco_id_closure"].Integral(),2)
#print "hgenfid4mu_reco_id_vtx_selected:", round(Histos[processBin+"hgenfid4mu_reco_id_vtx_selected"].Integral(),2)
#print "hgenfid4mu_reco_id_vtx_closure:", round(Histos[processBin+"hgenfid4mu_reco_id_vtx_closure"].Integral(),5)
