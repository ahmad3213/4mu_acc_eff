import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *
from sample_shortnames_YY import *

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
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observalbe, supported: "inclusive", "pT", "eta", "Njets"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option("-l",action="callback",callback=callback_rootargs)
    parser.add_option("-q",action="callback",callback=callback_rootargs)
    parser.add_option("-b",action="callback",callback=callback_rootargs)
    
    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()
    
# parse the arguments and options
global opt, args
parseOptions()
sys.argv = grootargs
    
if (not os.path.exists("YY_plots")):
    os.system("mkdir YY_plots")
        
from ROOT import *
from tdrStyle import *
setTDRStyle()

ROOT.gStyle.SetPaintTextFormat("1.2f")
#ROOT.gStyle.SetPalette(55)
ROOT.gStyle.SetNumberContours(99)

obsName = opt.OBSNAME
if (obsName=='pT2mu_rapidity2mu'):
    X_Label = 'p_{T} (#Upsilon)'
    Y_Label = 'rapidity (#Upsilon)'


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

#if float(obs_bins[len(obs_bins)-1])>199:
#    obs_bins[len(obs_bins)-1]='250'
#    obs_bins[len(obs_bins)-1]='4'
                        
_temp = __import__('inputs_sig_YY'+obsName, globals(), locals(), ['acc_a','dacc_a','acc_b','dacc_b'], -1)
acc_a = _temp.acc_a
acc_b = _temp.acc_b
dacc_a = _temp.dacc_a
dacc_b = _temp.dacc_b
recoeff_a = _temp.recoeff_a
recoeff_b  = _temp.recoeff_b
recodeff_a = _temp.recodeff_a
recodeff_b = _temp.recodeff_b
fStates = ['4mu']
channel = '4mu'
a_bins_pt = array('d',[float(obs_bins_pt[i]) for i in range(len(obs_bins_pt))])
a_bins_y = array('d',[float(obs_bins_y[i]) for i in range(len(obs_bins_y))])
print a_bins_pt
print a_bins_y
List = []
for long, short in sample_shortnames.iteritems():
    List.append(long)
i_sample = -1
print List
for Sample in List:
    i_sample = i_sample+1
    shortname = sample_shortnames[Sample]
    for fState in fStates:

        acc2d_a = TH2D("acc2d_a", "acc2d_a", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        dacc2d_a = TH2D("dacc2d_a", "dacc2d_a", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        acc2d_b = TH2D("acc2d_b", "acc2d_b", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        dacc2d_b = TH2D("dacc2d_b", "dacc2d_b", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        eff2d_a = TH2D("eff2d_a", "eff2d_a", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        deff2d_a = TH2D("deff2d_a", "deff2d_a", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        eff2d_b = TH2D("eff2d_b", "eff2d_b", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        deff2d_b = TH2D("deff2d_b", "deff2d_b", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        eff2d_avg = TH2D("eff2d_avg", "eff2d_avg", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        deff2d_avg = TH2D("deff2d_avg", "deff2d_avg", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        for x in range(0,len(obs_bins_pt)-1):
            for y in range(0,len(obs_bins_y)-1):
                processBin = shortname+'_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)
                bin = acc2d_a.GetBin(x+1,y+1)
                acc2d_a.SetBinContent(bin,acc_a[processBin])
                dacc2d_a.SetBinContent(bin,dacc_a[processBin])
                bin = acc2d_b.GetBin(x+1,y+1)
                acc2d_b.SetBinContent(bin,acc_b[processBin])
                dacc2d_b.SetBinContent(bin,dacc_b[processBin])
                bin = eff2d_a.GetBin(x+1,y+1)
                eff2d_a.SetBinContent(bin,recoeff_a[processBin])
                deff2d_a.SetBinContent(bin,recodeff_a[processBin])
                bin = eff2d_b.GetBin(x+1,y+1)
                eff2d_b.SetBinContent(bin,recoeff_b[processBin])
                deff2d_b.SetBinContent(bin,recodeff_b[processBin])
                bin = eff2d_avg.GetBin(x+1,y+1)
                eff2d_avg.SetBinContent(bin,((recoeff_b[processBin]+recoeff_a[processBin])/2))
                deff2d_avg.SetBinContent(bin,(recodeff_b[processBin]+recodeff_a[processBin]))

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        acc2d_a.GetXaxis().SetTitle(X_Label+'(gen.)')
        acc2d_a.GetYaxis().SetTitle(Y_Label+'(gen.)')
        acc2d_a.GetZaxis().SetTitle('acc.')
        acc2d_a.GetXaxis().SetTitleOffset(1.0)
        acc2d_a.GetYaxis().SetTitleOffset(0.8)
        acc2d_a.GetZaxis().SetTitleOffset(0.6)
        acc2d_a.GetZaxis().SetRangeUser(0.7,1.0) 
        acc2d_a.Draw("colzTEXT")
        acc2d_a.GetXaxis().SetNdivisions(505)
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right   
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right  
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.23, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.4, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " (#sqrt{s} = 13 TeV)")
#        c.SaveAs("YY_plots/acc2d_a_"+shortname+".png")
#        c.SaveAs("YY_plots/acc2d_a_"+shortname+".pdf")
        del c
        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        dacc2d_a.GetXaxis().SetTitle(X_Label+'(gen.)')
        dacc2d_a.GetYaxis().SetTitle(Y_Label+'(gen.)')
        dacc2d_a.GetZaxis().SetTitle('acc. unc.')
        dacc2d_a.GetXaxis().SetTitleOffset(1.0)
        dacc2d_a.GetYaxis().SetTitleOffset(0.8)
        dacc2d_a.GetZaxis().SetTitleOffset(0.6)
        dacc2d_a.GetZaxis().SetRangeUser(-0.01,0.2)
        dacc2d_a.Draw("colzTEXT")
        dacc2d_a.GetXaxis().SetNdivisions(505)
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right   
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right  
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.23, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.4, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " (#sqrt{s} = 13 TeV)")
#        c.SaveAs("YY_plots/dacc2d_a_"+shortname+".png")
#        c.SaveAs("YY_plots/dacc2d_a_"+shortname+".pdf")
        del c
        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        acc2d_b.GetXaxis().SetTitle(X_Label+'(gen.)')
        acc2d_b.GetYaxis().SetTitle(Y_Label+'(gen.)')
        acc2d_b.GetZaxis().SetTitle('acc.')
        acc2d_b.GetXaxis().SetTitleOffset(1.0)
        acc2d_b.GetYaxis().SetTitleOffset(0.8)
        acc2d_b.GetZaxis().SetTitleOffset(0.6)
        acc2d_b.GetZaxis().SetRangeUser(0.7,1.0)
        acc2d_b.GetXaxis().SetNdivisions(505)
        acc2d_b.Draw("colzTEXT")
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right   
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right  
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.23, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.4, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " (#sqrt{s} = 13 TeV)")
#        c.SaveAs("YY_plots/acc2d_b_"+shortname+".png")
#        c.SaveAs("YY_plots/acc2d_b_"+shortname+".pdf")
        del c
        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        dacc2d_b.GetXaxis().SetTitle(X_Label+'(gen.)')
        dacc2d_b.GetYaxis().SetTitle(Y_Label+'(gen.)')
        dacc2d_b.GetZaxis().SetTitle('acc. unc.')
        dacc2d_b.GetXaxis().SetTitleOffset(1.0)
        dacc2d_b.GetYaxis().SetTitleOffset(0.8)
        dacc2d_b.GetZaxis().SetTitleOffset(0.6)
        dacc2d_b.GetZaxis().SetRangeUser(-0.01,0.2)
        dacc2d_b.GetXaxis().SetNdivisions(505)
        dacc2d_b.Draw("colzTEXT")
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right   
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right  
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.23, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.4, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " (#sqrt{s} = 13 TeV)")
#        c.SaveAs("YY_plots/dacc2d_b_"+shortname+".png")
#        c.SaveAs("YY_plots/dacc2d_b_"+shortname+".pdf")
        del c
        del acc2d_b
        del acc2d_a
        del dacc2d_b
        del dacc2d_a
        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        eff2d_a.GetXaxis().SetTitle(X_Label+'(gen.)')
        eff2d_a.GetYaxis().SetTitle(Y_Label+'(gen.)')
        eff2d_a.GetZaxis().SetTitle('reco. eff.')
        eff2d_a.GetXaxis().SetTitleOffset(1.0)
        eff2d_a.GetYaxis().SetTitleOffset(0.8)
        eff2d_a.GetZaxis().SetTitleOffset(0.6)
        eff2d_a.GetZaxis().SetRangeUser(0.3,1.0) 
        eff2d_a.Draw("colzTEXT")
        eff2d_a.GetXaxis().SetNdivisions(505)
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right   
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right  
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.23, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.4, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " (#sqrt{s} = 13 TeV)")
        c.SaveAs("YY_plots/eff2d_a_"+shortname+".png")
        c.SaveAs("YY_plots/eff2d_a_"+shortname+".pdf")
        del c

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        deff2d_a.GetXaxis().SetTitle(X_Label+'(gen.)')
        deff2d_a.GetYaxis().SetTitle(Y_Label+'(gen.)')
        deff2d_a.GetZaxis().SetTitle('reco. eff. unc.')
        deff2d_a.GetXaxis().SetTitleOffset(1.0)
        deff2d_a.GetYaxis().SetTitleOffset(0.8)
        deff2d_a.GetZaxis().SetTitleOffset(0.6)
        deff2d_a.GetZaxis().SetRangeUser(-0.01,0.2)
        deff2d_a.Draw("colzTEXT")
        deff2d_a.GetXaxis().SetNdivisions(505)
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right   
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right  
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.23, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.4, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " (#sqrt{s} = 13 TeV)")
        c.SaveAs("YY_plots/deff2d_a_"+shortname+".png")
        c.SaveAs("YY_plots/deff2d_a_"+shortname+".pdf")
        del c

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        eff2d_b.GetXaxis().SetTitle(X_Label+'(gen.)')
        eff2d_b.GetYaxis().SetTitle(Y_Label+'(gen.)')
        eff2d_b.GetZaxis().SetTitle('reco. eff.')
        eff2d_b.GetXaxis().SetTitleOffset(1.0)
        eff2d_b.GetYaxis().SetTitleOffset(0.8)
        eff2d_b.GetZaxis().SetTitleOffset(0.6)
        eff2d_b.GetZaxis().SetRangeUser(0.3,1.0)
        eff2d_b.Draw("colzTEXT")
        eff2d_b.GetXaxis().SetNdivisions(505)
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right   
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right  
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.23, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.4, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " (#sqrt{s} = 13 TeV)")
        c.SaveAs("YY_plots/eff2d_b_"+shortname+".png")
        c.SaveAs("YY_plots/eff2d_b_"+shortname+".pdf")
        del c

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        deff2d_b.GetXaxis().SetTitle(X_Label+'(gen.)')
        deff2d_b.GetYaxis().SetTitle(Y_Label+'(gen.)')
        deff2d_b.GetZaxis().SetTitle('reco. eff. unc.')
        deff2d_b.GetXaxis().SetTitleOffset(1.0)
        deff2d_b.GetYaxis().SetTitleOffset(0.8)
        deff2d_b.GetZaxis().SetTitleOffset(0.6)
        deff2d_b.GetZaxis().SetRangeUser(-0.01,0.2)
        deff2d_b.Draw("colzTEXT")
        deff2d_b.GetXaxis().SetNdivisions(505)
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right   
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right  
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.23, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.4, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " (#sqrt{s} = 13 TeV)")
        c.SaveAs("YY_plots/deff2d_b_"+shortname+".png")
        c.SaveAs("YY_plots/deff2d_b_"+shortname+".pdf")
        del c
        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        eff2d_avg.GetXaxis().SetTitle(X_Label+'(gen.)')
        eff2d_avg.GetYaxis().SetTitle(Y_Label+'(gen.)')
        eff2d_avg.GetZaxis().SetTitle('reco. eff.')
        eff2d_avg.GetXaxis().SetTitleOffset(1.0)
        eff2d_avg.GetYaxis().SetTitleOffset(0.8)
        eff2d_avg.GetZaxis().SetTitleOffset(0.6)
        eff2d_avg.GetZaxis().SetRangeUser(0.3,1.0)
        eff2d_avg.Draw("colzTEXT")
        eff2d_avg.GetXaxis().SetNdivisions(505)
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right   
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right  
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.23, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.4, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " (#sqrt{s} = 13 TeV)")
        c.SaveAs("YY_plots/eff2d_avg_"+shortname+".png")
        c.SaveAs("YY_plots/eff2d_avg_"+shortname+".pdf")
        del c 
        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        deff2d_avg.GetXaxis().SetTitle(X_Label+'(gen.)')
        deff2d_avg.GetYaxis().SetTitle(Y_Label+'(gen.)')
        deff2d_avg.GetZaxis().SetTitle('reco. eff. unc.')
        deff2d_avg.GetXaxis().SetTitleOffset(1.0)
        deff2d_avg.GetYaxis().SetTitleOffset(0.8)
        deff2d_avg.GetZaxis().SetTitleOffset(0.6)
        deff2d_avg.GetZaxis().SetRangeUser(-0.01,0.2)
        deff2d_avg.Draw("colzTEXT")
        deff2d_avg.GetXaxis().SetNdivisions(505)
        latex2 = TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right   
        latex2.SetTextSize(0.5*c.GetTopMargin())
        latex2.SetTextFont(62)
        latex2.SetTextAlign(11) # align right  
        latex2.DrawLatex(0.18, 0.92, "CMS")
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(52)
        latex2.SetTextAlign(11)
        latex2.DrawLatex(0.23, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.4, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " (#sqrt{s} = 13 TeV)")
        c.SaveAs("YY_plots/deff2d_avg_"+shortname+".png")
        c.SaveAs("YY_plots/deff2d_avg_"+shortname+".pdf")
        del c       
        del eff2d_b
        del eff2d_a
        del deff2d_b
        del deff2d_a
        del eff2d_avg
        del deff2d_avg
