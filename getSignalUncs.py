from ROOT import *
from math import *

from LoadData4l import *
gRandom.SetSeed(101)
List = [
'ZpTomumu_M5_13TeV_MadGraph5_pythia8-v52016',
'ZpTomumu_M15_13TeV_MadGraph5_pythia8-v52016',
'ZpTomumu_M30_13TeV_MadGraph5_pythia8-v52016',
'ZpTomumu_M45_13TeV_MadGraph5_pythia8-v52016',
'ZpTomumu_M60_13TeV_MadGraph5_pythia8-v52016',
'ZpTomumu_M70_13TeV_MadGraph5_pythia8-v52016',
]
for Type in List:

  nbins=20
  lo=80
  hi=100

  hnom4mu = TH1F("hnom4mu", "hnom4mu", nbins, lo, hi)
  hnom4mu.Sumw2()
  hrecodn4mu = TH1F("hrecodn4mu", "hrecodn4mu", nbins, lo, hi)
  hrecodn4mu.Sumw2()
  hrecoup4mu = TH1F("hrecoup4mu", "hrecoup4mu", nbins, lo, hi)
  hrecoup4mu.Sumw2()
###reco only
  hrecoonlydn4mu = TH1F("hrecoonlydn4mu", "hrecoonlydn4mu", nbins, lo, hi)
  hrecoonlydn4mu.Sumw2()
  hrecoonlyup4mu = TH1F("hrecoonlyup4mu", "hrecoonlyup4mu", nbins, lo, hi)
  hrecoonlyup4mu.Sumw2()


  hnom4e = TH1F("hnom4e", "hnom4e", nbins, lo, hi)
  hnom4e.Sumw2()
  hrecodn4e = TH1F("hrecodn4e", "hrecodn4e", nbins, lo, hi)
  hrecodn4e.Sumw2()
  hrecoup4e = TH1F("hrecoup4e", "hrecoup4e", nbins, lo, hi)
  hrecoup4e.Sumw2()
  
  hnom2e2mu = TH1F("hnom2e2mu", "hnom2e2mu", nbins, lo, hi)
  hnom2e2mu.Sumw2()
  hrecodn2e2mu_e = TH1F("hrecodn2e2mu_e", "hrecodn2e2mu_e", nbins, lo, hi)
  hrecodn2e2mu_e.Sumw2()
  hrecoup2e2mu_e = TH1F("hrecoup2e2mu_e", "hrecoup2e2mu_e", nbins, lo, hi)
  hrecoup2e2mu_e.Sumw2()
  hrecodn2e2mu_mu = TH1F("hrecodn2e2mu_mu", "hrecodn2e2mu_mu", nbins, lo, hi)
  hrecodn2e2mu_mu.Sumw2()
  hrecoup2e2mu_mu = TH1F("hrecoup2e2mu_mu", "hrecoup2e2mu_mu", nbins, lo, hi)
  hrecoup2e2mu_mu.Sumw2()

  tree = Tree[Type]
  sumweights = sumw[Type]
  sumweights = 200000

  nentries = tree.GetEntries()
  for i in range(nentries):
    tree.GetEntry(i)

    if (i%10000==0): print Type,i,'/',nentries
    if (i>200000): break

    if (not tree.passedFullSelection==1): continue

    mass4l = tree.mass4l
    idL1 = abs(tree.idL1)
    idL3 = abs(tree.idL3)

    k_qcd = tree.k_ggZZ
    #GENmassZZ = tree.GENmassZZ

    genWeight = tree.genWeight
    dataMCWeight = tree.dataMCWeight
    crossSection = tree.crossSection

    # Nominal
    if (idL1==11 and idL3==11): hnom4e.Fill(mass4l,dataMCWeight*genWeight*crossSection*(2763./float(sumweights)))
    elif (idL1==13 and idL3==13): hnom4mu.Fill(mass4l,dataMCWeight*genWeight*crossSection*(2763./float(sumweights)))
    elif (abs(idL1-idL3)==2): hnom2e2mu.Fill(mass4l,dataMCWeight*genWeight*crossSection*(2763./float(sumweights)))

    recoerre=1.0
    recoerrmu=1.0

    # Reconstruction efficiencies errors
    for l in range(0,4):
      if abs(tree.lep_id[tree.lep_Hindex[l]])==11:
        # uncertainty on ID/Iso/SIP, stored in tree per lepton
        recoerre *= (1.0+gRandom.Gaus(0.0,abs(tree.lep_dataMCErr[tree.lep_Hindex[l]])))

        # old way
        # uncertainty on GSF track eff. for crack electrons, hard coded
        #if (abs(tree.lep_eta[tree.lep_Hindex[l]])>1.4442 and abs(tree.lep_eta[tree.lep_Hindex[l]])<1.566): 
        #  recoerre *= (1.0+gRandom.Gaus(0.0,0.08))
        ## uncertainty on GSF track eff. for low pt non-crack electrons, hard coded
        #elif (tree.lep_pt[tree.lep_Hindex[l]]<20): 
        #  recoerre *= (1.0+gRandom.Gaus(0.0,0.08))
        ## uncertainty on GSF track eff. for high pt non-crack electrons, hard coded
        #else:
        #  recoerre *= (1.0+gRandom.Gaus(0.0,0.04))
      else:
        recoerrmu *= (1.0+gRandom.Gaus(0.0,abs(tree.lep_dataMCErr[tree.lep_Hindex[l]])))
        # old way
        # total uncertainty on low pt muons, hard coded
        #if (tree.lep_pt[tree.lep_Hindex[l]]<10.0 or abs(tree.lep_eta[tree.lep_Hindex[l]])>2.0): recoerrmu *= (1.0+gRandom.Gaus(0.0,0.02))
        # total uncertainty on high pt muons, hard coded
        #else: recoerrmu *= (1.0+gRandom.Gaus(0.0,0.005))    

    if (recoerre<1.0): 
      recoerrupe=1.0/recoerre
      recoerrdne=recoerre
    else:
      recoerrupe=recoerre
      recoerrdne=(1.0/recoerre)

    if (recoerrmu<1.0): 
      recoerrupmu=1.0/recoerrmu
      recoerrdnmu=recoerrmu
    else:
      recoerrupmu=recoerrmu
      recoerrdnmu=(1.0/recoerrmu)
    recoonlyerrupmu= 1.0+sqrt((1.0-recoerrupmu)**2)
    recoonlyerrdnmu= 1.0-sqrt((1.0-recoerrdnmu)**2)
    # Trigger uncertainties, hard coded
    if(idL1==11 and idL3==11):
      #pt(4th lep)<12: +0.010/-0.11
      #12<pt(4th lep): +0.005/-0.010
      recoerrupe = 1.0+sqrt((1.0-recoerrupe)**2+0.01**2)
      recoerrdne = 1.0-sqrt((1.0-recoerrdne)**2+0.04**2)
    if(idL1==13 and idL3==13):
      #pt(4th lep)<7: +0.001/-0.032
      #7<pt(4th lep)<12: +0.001/-0.015
      #12<pt(4th lep): +0.001/-0.015
      recoerrupmu = 1.0+sqrt((1.0-recoerrupmu)**2+0.001**2)
      if (tree.pTL4<7):
        recoerrdnmu = 1.0-sqrt((1.0-recoerrdnmu)**2+0.032**2)
      elif (tree.pTL4<12):
        recoerrdnmu = 1.0-sqrt((1.0-recoerrdnmu)**2+0.015**2)
      else:
        recoerrdnmu = 1.0-sqrt((1.0-recoerrdnmu)**2+0.015**2)
    if(abs(idL1-idL3)==2):
      #pt(4th lep)<7: +0.005/-0.08
      #7<pt(4th lep)<12: +0.005/-0.032
      #12<pt(4th lep): +0.001/-0.010
      recoerrupe = 1.0+sqrt((1.0-recoerrupe)**2+0.01**2)
      recoerrdne = 1.0-sqrt((1.0-recoerrdne)**2+0.01**2)
      recoerrupmu = 1.0+sqrt((1.0-recoerrupmu)**2+0.01**2)
      recoerrdnmu = 1.0-sqrt((1.0-recoerrdnmu)**2+0.01**2)

    if (idL1==11 and idL3==11): 
      hrecoup4e.Fill(mass4l,recoerrupe*dataMCWeight*genWeight*crossSection*(2763./float(sumweights)))
      hrecodn4e.Fill(mass4l,recoerrdne*dataMCWeight*genWeight*crossSection*(2763./float(sumweights)))
    elif (idL1==13 and idL3==13): 
      hrecoup4mu.Fill(mass4l,recoerrupmu*dataMCWeight*genWeight*crossSection*(2763./float(sumweights)))
      hrecodn4mu.Fill(mass4l,recoerrdnmu*dataMCWeight*genWeight*crossSection*(2763./float(sumweights)))
      hrecoonlyup4mu.Fill(mass4l,recoonlyerrupmu*dataMCWeight*genWeight*crossSection*(2763./float(sumweights)))
      hrecoonlydn4mu.Fill(mass4l,recoonlyerrdnmu*dataMCWeight*genWeight*crossSection*(2763./float(sumweights)))
    elif (abs(idL1-idL3)==2): 
      hrecoup2e2mu_e.Fill(mass4l,recoerrupe*dataMCWeight*genWeight*crossSection*(2763./float(sumweights)))
      hrecodn2e2mu_e.Fill(mass4l,recoerrdne*dataMCWeight*genWeight*crossSection*(2763./float(sumweights)))
      hrecoup2e2mu_mu.Fill(mass4l,recoerrupmu*dataMCWeight*genWeight*crossSection*(2763./float(sumweights)))
      hrecodn2e2mu_mu.Fill(mass4l,recoerrdnmu*dataMCWeight*genWeight*crossSection*(2763./float(sumweights)))

  #print Type,'Reco/Id'
  #print '4e +',round((hrecoup4e.Integral()/hnom4e.Integral()-1.0),3),'-',round((1.0-hrecodn4e.Integral()/hnom4e.Integral()),3)
  #print '4mu +',round((hrecoup4mu.Integral()/hnom4mu.Integral()-1.0),3),'-',round((1.0-hrecodn4mu.Integral()/hnom4mu.Integral()),3)
  #print '2e2mu +',round((hrecoup2e2mu.Integral()/hnom2e2mu.Integral()-1.0),3),'-',round((1.0-hrecodn2e2mu.Integral()/hnom2e2mu.Integral()),3)

  print Type,'Reco/Id/Trig'
  #print '4e +',round((hrecoup4e.Integral()/hnom4e.Integral()-1.0),3),'-',round((1.0-hrecodn4e.Integral()/hnom4e.Integral()),3)
  print '4mu +',round((hrecoup4mu.Integral()/hnom4mu.Integral()-1.0),13),'-',round((1.0-hrecodn4mu.Integral()/hnom4mu.Integral()),3)
  print '4mu(recoonly) +',round((hrecoonlyup4mu.Integral()/hnom4mu.Integral()-1.0),13),'-',round((1.0-hrecoonlydn4mu.Integral()/hnom4mu.Integral()),3)
  #print '2e2mu el +',round((hrecoup2e2mu_e.Integral()/hnom2e2mu.Integral()-1.0),3),'-',round((1.0-hrecodn2e2mu_e.Integral()/hnom2e2mu.Integral()),3)
  #print '2e2mu mu +',round((hrecoup2e2mu_mu.Integral()/hnom2e2mu.Integral()-1.0),3),'-',round((1.0-hrecodn2e2mu_mu.Integral()/hnom2e2mu.Integral()),3)


