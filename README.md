# 4mu_acc_eff


cmsrel CMSSW_10_2_5
cd CMSSW_10_2_5/src
cmsenv
git clone https://github.com/ahmad3213/4mu_acc_eff
git checkout main 
To calcualte acceptance maps for Jpsi, please run following scripts

The commands inside the scripts are as follows 
nohup python -u efficiencyFactors_JJ.py -l -q -b --dir="/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon/CMSSW_9_4_14_patch1/src/FourMuonAna/Onia/test/" --obsName="pT2mu_rapidity2mu" --obsBins="|0|1|2|3.5|5|6|7|8|9|10|12|15|20|30|40|10000|_|-2.0|-1.75|-1.5|-1.0|-0.5|0.5|1.0|1.5|1.75|2.0|" >& effs_pT2mu_rapidity2mu_JJ_4mu.log &
Once you run this, it may take a while to calculate everything, progress can be checked by command "tail -f effs_pT2mu_rapidity2mu_JJ_4mu.log"

Explaining some contents 

efficiencyFactors_JJ.py: is the main script which does all the work
--obsName: acceptance are caluclated with respect to this variable, currently only supports "pT2mu_rapidity2mu" (pT and rapidity of Jpsi) but it can easily be ehanced to adapt for more variables  
--obsBins: is bins of acceptance map, "|0|1|2|3.5|5|6|7|8|9|10|12|15|20|30|40|10000|" is "pT2mu" bins and "|-2.0|-1.75|-1.5|-1.0|-0.5|0.5|1.0|1.5|1.75|2.0|" is rapidity bins of Jpsi. Changing binning only requires change here
inside "efficiencyFactors_JJ.py" script: we are importing "sample_shortnames_JJ_eff.py" which contains samples name strings and "LoadData_JJ_eff.py" which reads input files/Tree for each sample.In case you want to change input sample, you need to make change in "LoadData_JJ_eff.py" script

Once acceptance are calucalted the results would be stored in "inputs_sig_JJpT2mu_rapidity2mu.py" in the form of a python dictonary. which is essentially not easy read by eye. You can use following command to make plot(s) which will read numbers from this python dictionary and plot acceptance map
python -u plot2dsigeffs_JJ.py -l -q -b --obsName="pT2mu_rapidity2mu" --obsBins="|0|1|2|3.5|5|6|7|8|9|10|12|15|20|30|40|_|-2.0|-1.75|-1.5|-1.0|-0.5|0.5|1.0|1.5|1.75|2.0|" --Mix >& sigeffs_pT2mu_rapidity2mu_JJ_4mu.log & 

Similary progress can be monitored by "tail -f sigeffs_pT2mu_rapidity2mu_JJ_4mu.log "
Here "plot2dsigeffs_JJ.py" is the main plotting script, "--obsName" and "--obsBins" should match with acceptance calucations. 
you can keep "--Mix" option or remove it. what it does: it takes SPS and DPS acceptance and mix them by ratio of 80(SPS):20(DPS) and then calcualte & plot acceptance for Mix along with all models. All plots should appear under directory "JJ_plots". Plots nameing convention as follows 
acc2d_a_eta_SPS:  means acceptance due First Jpsi due to eta cut on its daugter muons using SPS sample. you would have similar plot for each model (i.e DPS, JHU,Mix)
dacc2d_a_eta_SPS: means erros on acceptance due First Jpsi due to eta cut on its daugter muons using SPS sample. you would have similar plot for each model (i.e DPS, JHU,Mix)
acc2d_a_etapt_SPS: means acceptance due First Jpsi due to eta and pT cuts on its daugter muons using SPS sample. you would have similar plot for each model (i.e DPS, JHU,Mix)
dacc2d_a_etapt_SPS: means erros on acceptance due First Jpsi due to eta and pT cuts on its daugter muons using SPS sample. you would have similar plot for each model (i.e DPS, JHU,Mix)
