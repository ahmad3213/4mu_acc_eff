# 4mu_acc_eff

## Setting up the area 

cmsrel CMSSW_10_2_5

cd CMSSW_10_2_5/src

cmsenv

git clone https://github.com/ahmad3213/4mu_acc_eff

## Scripts to Caluclate Acceptances:
To calcualte acceptance maps for Jpsi, please run following command

``
nohup python -u efficiencyFactors_JJ.py -l -q -b --dir="/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon/CMSSW_9_4_14_patch1/src/FourMuonAna/Onia/test/" --obsName="pT2mu_rapidity2mu" --obsBins="|0|1|2|3.5|5|6|7|8|9|10|12|15|20|30|40|10000|_|-2.0|-1.75|-1.5|-1.0|-0.5|0.5|1.0|1.5|1.75|2.0|" >& effs_pT2mu_rapidity2mu_JJ_4mu.log & 
``

It may take a while to calculate everything, progress can be checked by command 

``
tail -f effs_pT2mu_rapidity2mu_JJ_4mu.log
``

### Explaining some contents:

``efficiencyFactors_JJ.py``: is the main script which does all the work

``--obsName``: acceptances are caluclated with respect to this variable, currently only supports ``pT2mu_rapidity2mu`` (pT and rapidity of Jpsi) but it can easily be ehanced to adapt for more variables  

``--obsBins``: is the binning of acceptance map, ``|0|1|2|3.5|5|6|7|8|9|10|12|15|20|30|40|10000|`` is ``pT2mu`` bins and ``|-2.0|-1.75|-1.5|-1.0|-0.5|0.5|1.0|1.5|1.75|2.0|`` is rapidity bins of Jpsi. Changing binning only requires changes here (on command line)

Inside ``efficiencyFactors_JJ.py`` script: we are importing ``sample_shortnames_JJ_eff.py`` which contains samples name strings and ``LoadData_JJ_eff.py`` which reads input files/Trees for each sample. In case you want to change input sample, you need to make change in ``LoadData_JJ_eff.py`` script

Once acceptance are calucalted the results would be stored in ``inputs_sig_JJpT2mu_rapidity2mu.py`` in the form of a python dictonary. which is not easy read by eye. You can use following command to make plot(s) which will read numbers from this python dictionary and plot acceptance maps

``
python -u plot2dsigeffs_JJ.py -l -q -b --obsName="pT2mu_rapidity2mu" --obsBins="|0|1|2|3.5|5|6|7|8|9|10|12|15|20|30|40|_|-2.0|-1.75|-1.5|-1.0|-0.5|0.5|1.0|1.5|1.75|2.0|" --Mix >& sigeffs_pT2mu_rapidity2mu_JJ_4mu.log & 
``

Similary progress can be monitored by 
``tail -f sigeffs_pT2mu_rapidity2mu_JJ_4mu.log ``

Here ``plot2dsigeffs_JJ.py`` is the main plotting script, ``--obsName`` and ``--obsBins`` should match with acceptance calucations. 

You can keep ``--Mix`` option or remove it. What it does: it takes SPS and DPS acceptance and mix them with ratio of 80(SPS):20(DPS) and then calculate & plot acceptance for Mix along with all models. All plots will appear under directory ``JJ_plots``. Plots naming convention is explained as follows 

``acc2d_a_eta_SPS``:  means acceptance of first Jpsi due to eta cut on its daugter muons using SPS sample. you would have similar plot for each model (i.e DPS, JHU,Mix)

``dacc2d_a_eta_SPS``: means erros on acceptance of first Jpsi due to eta cut on its daugter muons using SPS sample. you would have similar plot for each model (i.e DPS, JHU,Mix)

``acc2d_b_eta_SPS``:  means acceptance of second Jpsi due to eta cut on its daugter muons using SPS sample. you would have similar plot for each model (i.e DPS, JHU,Mix)

``dacc2d_b_eta_SPS``: means erros on acceptance of second Jpsi due to eta cut on its daugter muons using SPS sample. you would have similar plot for each model (i.e DPS, JHU,Mix)

``acc2d_a_etapt_SPS``: means acceptance of first Jpsi due to eta and pT cuts on its daugter muons using SPS sample. you would have similar plot for each model (i.e DPS, JHU,Mix)

``dacc2d_a_etapt_SPS``: means erros on acceptance of first Jpsi due to eta and pT cuts on its daugter muons using SPS sample. you would have similar plot for each model (i.e DPS, JHU,Mix)

### Similary For effiency calucaltions

``
nohup python -u efficiencyFactors_JJ_eff.py -l -q -b --dir="/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon/CMSSW_9_4_14_patch1/src/FourMuonAna/Onia/test/" --obsName="pT2mu_rapidity2mu" --obsBins="|0|1|2|3.5|5|6|7|8|9|10|12|15|20|30|40|10000|_|-2.0|-1.75|-1.5|-1.0|-0.5|0.5|1.0|1.5|1.75|2.0|" >& effs_pT2mu_rapidity2mu_JJ_4mu_eff.log &
``
This is similar like acceptance, one factor per Jpsi.

``
nohup python -u efficiencyFactors_JJ_evteff.py -l -q -b --dir="/uscms/home/muahmad/nobackup/Four_Mu_analysis/DoubleUpsilon/CMSSW_9_4_14_patch1/src/FourMuonAna/Onia/test/" --obsName="pT2mu_pT2mu" --obsBins="|0|2.5|5.0|7.5|10.0|20.0|40.0|_|0|2.5|5.0|7.5|10.0|20.0|40.0|" >& effs_pT2mu_pT2mu_JJ_4mu_evteff.log &
``

This is one factor per event (each event has two Jpsi mesons)

Plotting effciencies:

``
python -u plot2dsigeffs_JJ_eff.py -l -q -b --obsName="pT2mu_rapidity2mu" --obsBins="|0|1|2|3.5|5|6|7|8|9|10|12|15|20|30|40|_|-2.0|-1.75|-1.5|-1.0|-0.5|0.5|1.0|1.5|1.75|2.0|" --Mix >& sigeffs_pT2mu_rapidity2mu_JJ_4mu_eff.log &
python -u plot2dsigeffs_JJ_evteff.py -l -q -b --obsName="pT2mu_pT2mu" --obsBins="|0|2.5|5.0|7.5|10.0|20.0|40.0|_|0|2.5|5.0|7.5|10.0|20.0|40.0|" --symmetrize --Mix >& sigeffs_pT2mu_pT2mu_JJ_4mu_eff.log &
``

Running Closure test: 

``python closure.py``

This read all acceptance and efficiency factors histrograms in root file and perfrom the closure test 

closure test resutls will be saved in ``closure_test_results.py`` after running, which is again python dictionary hard to read by eye. But you can run following script to make latex table code 
``python makeTable.py`` 
This will print out the latex code to make the table, just copy paste this code on latex and you will get a beautiful table

### NTuples production: 
All NTuples needed as input exist on cmslpc machine. If needs to reporduce for some reason, please follow instructions here 
code is here. git branch ``test_only`` of following repository 

``
https://github.com/ahmad3213/FourMuonAna
``

