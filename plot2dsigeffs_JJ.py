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
    parser.add_option('',   '--obsName',dest='OBSNAME',    type='string',default='',   help='Name of the observalbe, supported: "inclusive", "pT", "eta", "Njets"')
    parser.add_option('',   '--obsBins',dest='OBSBINS',    type='string',default='',   help='Bin boundaries for the diff. measurement separated by "|", e.g. as "|0|50|100|", use the defalut if empty string')
    parser.add_option('',   '--Mix', action='store_true', dest='MIX', default=False, help='plot Mix of SPS(80%) and DPS(20%), default is False')
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
    
if (not os.path.exists("JJ_plots")):
    os.system("mkdir JJ_plots")
        
from ROOT import *
from tdrStyle import *
setTDRStyle()

ROOT.gStyle.SetPaintTextFormat("1.2f")
#ROOT.gStyle.SetPalette(55)
ROOT.gStyle.SetNumberContours(99)

obsName = opt.OBSNAME
if (obsName=='pT2mu_rapidity2mu'):
    X_Label = 'p_{T} (J/#Psi)'
    Y_Label = 'rapidity (J/#Psi)'


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
                        
#_temp = __import__('inputs_sig_JJ'+obsName, globals(), locals(), ['acc_a_eta','dacc_a_eta','acc_b_eta','dacc_b_eta','acc_a_etapt','dacc_a_etapt','acc_b_etapt','dacc_b_etapt'], -1)
_temp = __import__('inputs_sig_JJ'+obsName+'_inc', globals(), locals(), ['acc_a_eta','dacc_a_eta','acc_b_eta','dacc_b_eta','acc_a_etapt','dacc_a_etapt','acc_b_etapt','dacc_b_etapt'], -1)
acc_a_eta = _temp.acc_a_eta
acc_b_eta = _temp.acc_b_eta
dacc_a_eta = _temp.dacc_a_eta
dacc_b_eta = _temp.dacc_b_eta
acc_a_etapt = _temp.acc_a_etapt
acc_b_etapt = _temp.acc_b_etapt
dacc_a_etapt = _temp.dacc_a_etapt
dacc_b_etapt = _temp.dacc_b_etapt
fStates = ['4mu']
channel = '4mu'
a_bins_pt = array('d',[float(obs_bins_pt[i]) for i in range(len(obs_bins_pt))])
a_bins_y = array('d',[float(obs_bins_y[i]) for i in range(len(obs_bins_y))])
print a_bins_pt
print a_bins_y
##Mixing SPS(80%) and DPS(20%)
##
if opt.MIX:
    acc_a_Mix_eta ={}
    dacc_a_Mix_eta ={}
    acc_b_Mix_eta ={}
    dacc_b_Mix_eta ={}
    acc_a_Mix_etapt ={}
    dacc_a_Mix_etapt ={}
    acc_b_Mix_etapt ={}
    dacc_b_Mix_etapt ={}
    for x in range(0,len(obs_bins_pt)-1):
        for y in range(0,len(obs_bins_y)-1):
            a = acc_a_eta['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            b = acc_a_eta['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            da = dacc_a_eta['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            db = dacc_a_eta['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            if (b>-1):
                c = (a*0.8)+(b*0.2)
                dc = (da*0.8)+(db*0.2)
            else:
                c = (a*1.0)
                dc = (da*1.0)
            acc_a_Mix_eta['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = c
            dacc_a_Mix_eta['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = dc
 
            a = acc_b_eta['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            b = acc_b_eta['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] 
            da = dacc_b_eta['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            db = dacc_b_eta['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            if (b>-1):
                c = (a*0.8)+(b*0.2)
                dc = (da*0.8)+(db*0.2)
            else:
                c = (a*1.0)
                dc = (da*1.0)
            acc_b_Mix_eta['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = c
            dacc_b_Mix_eta['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = dc

            a = acc_a_etapt['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            b = acc_a_etapt['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            da = dacc_a_etapt['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            db = dacc_a_etapt['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            if (b>-1):
                c = (a*0.8)+(b*0.2)
                dc = (da*0.8)+(db*0.2)
            else:
                c = (a*1.0)
                dc = (da*1.0)
            acc_a_Mix_etapt['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = c
            dacc_a_Mix_etapt['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = dc

            a = acc_b_etapt['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            b = acc_b_etapt['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            da = dacc_b_etapt['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            db = dacc_b_etapt['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            if (b>-1):
                c = (a*0.8)+(b*0.2)
                dc = (da*0.8)+(db*0.2)
            else:
                c = (a*1.0)
                dc = (da*1.0)
            acc_b_Mix_etapt['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = c
            dacc_b_Mix_etapt['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = dc
##
List = []
for long, short in sample_shortnames.iteritems():
    List.append(long)
i_sample = -1
print List
for Sample in List:
    i_sample = i_sample+1
    shortname = sample_shortnames[Sample]
    for fState in fStates:
        acc2d_a_eta = TH2D("acc2d_a_eta", "acc2d_a_eta", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        dacc2d_a_eta = TH2D("dacc2d_a_eta", "dacc2d_a_eta", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        acc2d_b_eta = TH2D("acc2d_b_eta", "acc2d_b_eta", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        dacc2d_b_eta = TH2D("dacc2d_b_eta", "dacc2d_b_eta", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)

        acc2d_a_Mix_eta = TH2D("acc2d_a_Mix_eta", "acc2d_a_Mix_eta", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        acc2d_b_Mix_eta = TH2D("acc2d_b_Mix_eta", "acc2d_b_Mix_eta", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        dacc2d_a_Mix_eta = TH2D("dacc2d_a_Mix_eta", "dacc2d_a_Mix_eta", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        dacc2d_b_Mix_eta = TH2D("dacc2d_b_Mix_eta", "dacc2d_b_Mix_eta", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)

        acc2d_a_Mix_etapt = TH2D("acc2d_a_Mix_etapt", "acc2d_a_Mix_etapt", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        acc2d_b_Mix_etapt = TH2D("acc2d_b_Mix_etapt", "acc2d_b_Mix_etapt", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        dacc2d_a_Mix_etapt = TH2D("dacc2d_a_Mix_etapt", "dacc2d_a_Mix_etapt", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        dacc2d_b_Mix_etapt = TH2D("dacc2d_b_Mix_etapt", "dacc2d_b_Mix_etapt", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)

        acc2d_a_etapt = TH2D("acc2d_a_etapt", "acc2d_a_etapt", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        dacc2d_a_etapt = TH2D("dacc2d_a_etapt", "dacc2d_a_etapt", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        acc2d_b_etapt = TH2D("acc2d_b_etapt", "acc2d_b_etapt", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        dacc2d_b_etapt = TH2D("dacc2d_b_etapt", "dacc2d_b_etapt", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)


        for x in range(0,len(obs_bins_pt)-1):
            for y in range(0,len(obs_bins_y)-1):
                processBin = shortname+'_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)
                bin = acc2d_a_eta.GetBin(x+1,y+1)
                acc2d_a_eta.SetBinContent(bin,acc_a_eta[processBin])
                dacc2d_a_eta.SetBinContent(bin,dacc_a_eta[processBin])
                acc2d_a_etapt.SetBinContent(bin,acc_a_etapt[processBin])
                dacc2d_a_etapt.SetBinContent(bin,dacc_a_etapt[processBin])
                if opt.MIX:
                    acc2d_a_Mix_eta.SetBinContent(bin,acc_a_Mix_eta['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    acc2d_a_Mix_etapt.SetBinContent(bin,acc_a_Mix_etapt['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    dacc2d_a_Mix_eta.SetBinContent(bin,dacc_a_Mix_eta['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    dacc2d_a_Mix_etapt.SetBinContent(bin,dacc_a_Mix_etapt['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                bin = acc2d_b_eta.GetBin(x+1,y+1)
                acc2d_b_eta.SetBinContent(bin,acc_b_eta[processBin])
                dacc2d_b_eta.SetBinContent(bin,dacc_b_eta[processBin])
                acc2d_b_etapt.SetBinContent(bin,acc_b_etapt[processBin])
                dacc2d_b_etapt.SetBinContent(bin,dacc_b_etapt[processBin])
                if opt.MIX:
                    acc2d_b_Mix_eta.SetBinContent(bin,acc_b_Mix_eta['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    acc2d_b_Mix_etapt.SetBinContent(bin,acc_b_Mix_etapt['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    dacc2d_b_Mix_eta.SetBinContent(bin,dacc_b_Mix_eta['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    dacc2d_b_Mix_etapt.SetBinContent(bin,dacc_b_Mix_etapt['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        acc2d_a_eta.GetXaxis().SetTitle(X_Label+'(gen.)')
        acc2d_a_eta.GetYaxis().SetTitle(Y_Label+'(gen.)')
        acc2d_a_eta.GetZaxis().SetTitle('acc.')
        acc2d_a_eta.GetXaxis().SetTitleOffset(1.0)
        acc2d_a_eta.GetYaxis().SetTitleOffset(0.8)
        acc2d_a_eta.GetZaxis().SetTitleOffset(0.6)
        acc2d_a_eta.GetZaxis().SetRangeUser(0.4,1.0) 
        acc2d_a_eta.Draw("colzTEXT")
        acc2d_a_eta.GetXaxis().SetNdivisions(505)
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
        latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
        c.SaveAs("JJ_plots/acc2d_a_eta_"+shortname+".png")
        c.SaveAs("JJ_plots/acc2d_a_eta_"+shortname+".pdf")
        del c
        if opt.MIX:
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            acc2d_a_Mix_eta.GetXaxis().SetTitle(X_Label+'(gen.)')
            acc2d_a_Mix_eta.GetYaxis().SetTitle(Y_Label+'(gen.)')
            acc2d_a_Mix_eta.GetZaxis().SetTitle('acc.')
            acc2d_a_Mix_eta.GetXaxis().SetTitleOffset(1.0)
            acc2d_a_Mix_eta.GetYaxis().SetTitleOffset(0.8)
            acc2d_a_Mix_eta.GetZaxis().SetTitleOffset(0.6)
            acc2d_a_Mix_eta.GetZaxis().SetRangeUser(0.4,1.0)
            acc2d_a_Mix_eta.Draw("colzTEXT")
            acc2d_a_Mix_eta.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,"Mix_JJto4mu_SPS_DPS")
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/acc2d_a_Mix_JJto4mu_SPS_DPS_eta.png")
            c.SaveAs("JJ_plots/acc2d_a_Mix_JJto4mu_SPS_DPS_eta.pdf")
            del c

            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            dacc2d_a_Mix_eta.GetXaxis().SetTitle(X_Label+'(gen.)')
            dacc2d_a_Mix_eta.GetYaxis().SetTitle(Y_Label+'(gen.)')
            dacc2d_a_Mix_eta.GetZaxis().SetTitle('acc. unc.')
            dacc2d_a_Mix_eta.GetXaxis().SetTitleOffset(1.0)
            dacc2d_a_Mix_eta.GetYaxis().SetTitleOffset(0.8)
            dacc2d_a_Mix_eta.GetZaxis().SetTitleOffset(0.6)
            dacc2d_a_Mix_eta.GetZaxis().SetRangeUser(0,0.4)
            dacc2d_a_Mix_eta.Draw("colzTEXT")
            dacc2d_a_Mix_eta.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,"Mix_JJto4mu_SPS_DPS")
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/dacc2d_a_Mix_JJto4mu_SPS_DPS_eta.png")
            c.SaveAs("JJ_plots/dacc2d_a_Mix_JJto4mu_SPS_DPS_eta.pdf")
            del c

            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            acc2d_a_Mix_etapt.GetXaxis().SetTitle(X_Label+'(gen.)')
            acc2d_a_Mix_etapt.GetYaxis().SetTitle(Y_Label+'(gen.)')
            acc2d_a_Mix_etapt.GetZaxis().SetTitle('acc.')
            acc2d_a_Mix_etapt.GetXaxis().SetTitleOffset(1.0)
            acc2d_a_Mix_etapt.GetYaxis().SetTitleOffset(0.8)
            acc2d_a_Mix_etapt.GetZaxis().SetTitleOffset(0.6)
            acc2d_a_Mix_etapt.GetZaxis().SetRangeUser(0,1.0)
            acc2d_a_Mix_etapt.Draw("colzTEXT")
            acc2d_a_Mix_etapt.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,"Mix_JJto4mu_SPS_DPS")
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/acc2d_a_Mix_JJto4mu_SPS_DPS_etapt.png")
            c.SaveAs("JJ_plots/acc2d_a_Mix_JJto4mu_SPS_DPS_etapt.pdf")
            del c

            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            dacc2d_a_Mix_etapt.GetXaxis().SetTitle(X_Label+'(gen.)')
            dacc2d_a_Mix_etapt.GetYaxis().SetTitle(Y_Label+'(gen.)')
            dacc2d_a_Mix_etapt.GetZaxis().SetTitle('acc. unc.')
            dacc2d_a_Mix_etapt.GetXaxis().SetTitleOffset(1.0)
            dacc2d_a_Mix_etapt.GetYaxis().SetTitleOffset(0.8)
            dacc2d_a_Mix_etapt.GetZaxis().SetTitleOffset(0.6)
            dacc2d_a_Mix_etapt.GetZaxis().SetRangeUser(0,0.4)
            dacc2d_a_Mix_etapt.Draw("colzTEXT")
            dacc2d_a_Mix_etapt.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,"Mix_JJto4mu_SPS_DPS")
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/dacc2d_a_Mix_JJto4mu_SPS_DPS_etapt.png")
            c.SaveAs("JJ_plots/dacc2d_a_Mix_JJto4mu_SPS_DPS_etapt.pdf")
            del c

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        acc2d_a_etapt.GetXaxis().SetTitle(X_Label+'(gen.)')
        acc2d_a_etapt.GetYaxis().SetTitle(Y_Label+'(gen.)')
        acc2d_a_etapt.GetZaxis().SetTitle('acc.')
        acc2d_a_etapt.GetXaxis().SetTitleOffset(1.0)
        acc2d_a_etapt.GetYaxis().SetTitleOffset(0.8)
        acc2d_a_etapt.GetZaxis().SetTitleOffset(0.6)
        acc2d_a_etapt.GetZaxis().SetRangeUser(0,1.0)
        acc2d_a_etapt.Draw("colzTEXT")
        acc2d_a_etapt.GetXaxis().SetNdivisions(505)
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
        latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
        c.SaveAs("JJ_plots/acc2d_a_etapt_"+shortname+".png")
        c.SaveAs("JJ_plots/acc2d_a_etapt_"+shortname+".pdf")
        del c
        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        dacc2d_a_eta.GetXaxis().SetTitle(X_Label+'(gen.)')
        dacc2d_a_eta.GetYaxis().SetTitle(Y_Label+'(gen.)')
        dacc2d_a_eta.GetZaxis().SetTitle('acc. unc.')
        dacc2d_a_eta.GetXaxis().SetTitleOffset(1.0)
        dacc2d_a_eta.GetYaxis().SetTitleOffset(0.8)
        dacc2d_a_eta.GetZaxis().SetTitleOffset(0.6)
        dacc2d_a_eta.GetZaxis().SetRangeUser(-0.01,0.1)
        dacc2d_a_eta.Draw("colzTEXT")
        dacc2d_a_eta.GetXaxis().SetNdivisions(505)
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
        latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
        c.SaveAs("JJ_plots/dacc2d_a_eta_"+shortname+".png")
        c.SaveAs("JJ_plots/dacc2d_a_eta_"+shortname+".pdf")
        del c

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        dacc2d_a_etapt.GetXaxis().SetTitle(X_Label+'(gen.)')
        dacc2d_a_etapt.GetYaxis().SetTitle(Y_Label+'(gen.)')
        dacc2d_a_etapt.GetZaxis().SetTitle('acc. unc.')
        dacc2d_a_etapt.GetXaxis().SetTitleOffset(1.0)
        dacc2d_a_etapt.GetYaxis().SetTitleOffset(0.8)
        dacc2d_a_etapt.GetZaxis().SetTitleOffset(0.6)
        dacc2d_a_etapt.GetZaxis().SetRangeUser(-0.01,0.3)
        dacc2d_a_etapt.Draw("colzTEXT")
        dacc2d_a_etapt.GetXaxis().SetNdivisions(505)
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
        latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
        c.SaveAs("JJ_plots/dacc2d_a_etapt_"+shortname+".png")
        c.SaveAs("JJ_plots/dacc2d_a_etapt_"+shortname+".pdf")
        del c

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        acc2d_b_eta.GetXaxis().SetTitle(X_Label+'(gen.)')
        acc2d_b_eta.GetYaxis().SetTitle(Y_Label+'(gen.)')
        acc2d_b_eta.GetZaxis().SetTitle('acc.')
        acc2d_b_eta.GetXaxis().SetTitleOffset(1.0)
        acc2d_b_eta.GetYaxis().SetTitleOffset(0.8)
        acc2d_b_eta.GetZaxis().SetTitleOffset(0.6)
        acc2d_b_eta.GetZaxis().SetRangeUser(0.4,1.0)
        acc2d_b_eta.GetXaxis().SetNdivisions(505)
        acc2d_b_eta.Draw("colzTEXT")
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
        latex2.DrawLatex(0.40, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, "#sqrt{s} = 13 TeV")
        c.SaveAs("JJ_plots/acc2d_b_eta_"+shortname+".png")
        c.SaveAs("JJ_plots/acc2d_b_eta_"+shortname+".pdf")
        del c
        if opt.MIX:
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            acc2d_b_Mix_eta.GetXaxis().SetTitle(X_Label+'(gen.)')
            acc2d_b_Mix_eta.GetYaxis().SetTitle(Y_Label+'(gen.)')
            acc2d_b_Mix_eta.GetZaxis().SetTitle('acc.')
            acc2d_b_Mix_eta.GetXaxis().SetTitleOffset(1.0)
            acc2d_b_Mix_eta.GetYaxis().SetTitleOffset(0.8)
            acc2d_b_Mix_eta.GetZaxis().SetTitleOffset(0.6)
            acc2d_b_Mix_eta.GetZaxis().SetRangeUser(0.4,1.0)
            acc2d_b_Mix_eta.GetXaxis().SetNdivisions(505)
            acc2d_b_Mix_eta.Draw("colzTEXT")
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
            latex2.DrawLatex(0.40, 0.92,"Mix_JJto4mu_SPS_DPS")
            latex2.DrawLatex(0.72, 0.92, "#sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/acc2d_b_Mix_JJto4mu_SPS_DPS_eta.png")
            c.SaveAs("JJ_plots/acc2d_b_Mix_JJto4mu_SPS_DPS_eta.pdf")
            del c

            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            dacc2d_b_Mix_eta.GetXaxis().SetTitle(X_Label+'(gen.)')
            dacc2d_b_Mix_eta.GetYaxis().SetTitle(Y_Label+'(gen.)')
            dacc2d_b_Mix_eta.GetZaxis().SetTitle('acc. unc.')
            dacc2d_b_Mix_eta.GetXaxis().SetTitleOffset(1.0)
            dacc2d_b_Mix_eta.GetYaxis().SetTitleOffset(0.8)
            dacc2d_b_Mix_eta.GetZaxis().SetTitleOffset(0.6)
            dacc2d_b_Mix_eta.GetZaxis().SetRangeUser(0,0.4)
            dacc2d_b_Mix_eta.GetXaxis().SetNdivisions(505)
            dacc2d_b_Mix_eta.Draw("colzTEXT")
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
            latex2.DrawLatex(0.40, 0.92,"Mix_JJto4mu_SPS_DPS")
            latex2.DrawLatex(0.72, 0.92, "#sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/dacc2d_b_Mix_JJto4mu_SPS_DPS_eta.png")
            c.SaveAs("JJ_plots/dacc2d_b_Mix_JJto4mu_SPS_DPS_eta.pdf")
            del c

            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            acc2d_b_Mix_etapt.GetXaxis().SetTitle(X_Label+'(gen.)')
            acc2d_b_Mix_etapt.GetYaxis().SetTitle(Y_Label+'(gen.)')
            acc2d_b_Mix_etapt.GetZaxis().SetTitle('acc.')
            acc2d_b_Mix_etapt.GetXaxis().SetTitleOffset(1.0)
            acc2d_b_Mix_etapt.GetYaxis().SetTitleOffset(0.8)
            acc2d_b_Mix_etapt.GetZaxis().SetTitleOffset(0.6)
            acc2d_b_Mix_etapt.GetZaxis().SetRangeUser(0,1.0)
            acc2d_b_Mix_etapt.GetXaxis().SetNdivisions(505)
            acc2d_b_Mix_etapt.Draw("colzTEXT")
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
            latex2.DrawLatex(0.40, 0.92,"Mix_JJto4mu_SPS_DPS")
            latex2.DrawLatex(0.72, 0.92, "#sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/acc2d_b_Mix_JJto4mu_SPS_DPS_etapt.png")
            c.SaveAs("JJ_plots/acc2d_b_Mix_JJto4mu_SPS_DPS_etapt.pdf")
            del c
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            dacc2d_b_Mix_etapt.GetXaxis().SetTitle(X_Label+'(gen.)')
            dacc2d_b_Mix_etapt.GetYaxis().SetTitle(Y_Label+'(gen.)')
            dacc2d_b_Mix_etapt.GetZaxis().SetTitle('acc. unc.')
            dacc2d_b_Mix_etapt.GetXaxis().SetTitleOffset(1.0)
            dacc2d_b_Mix_etapt.GetYaxis().SetTitleOffset(0.8)
            dacc2d_b_Mix_etapt.GetZaxis().SetTitleOffset(0.6)
            dacc2d_b_Mix_etapt.GetZaxis().SetRangeUser(0,0.4)
            dacc2d_b_Mix_etapt.GetXaxis().SetNdivisions(505)
            dacc2d_b_Mix_etapt.Draw("colzTEXT")
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
            latex2.DrawLatex(0.40, 0.92,"Mix_JJto4mu_SPS_DPS")
            latex2.DrawLatex(0.72, 0.92, "#sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/dacc2d_b_Mix_JJto4mu_SPS_DPS_etapt.png")
            c.SaveAs("JJ_plots/dacc2d_b_Mix_JJto4mu_SPS_DPS_etapt.pdf")
            del c


        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        acc2d_b_etapt.GetXaxis().SetTitle(X_Label+'(gen.)')
        acc2d_b_etapt.GetYaxis().SetTitle(Y_Label+'(gen.)')
        acc2d_b_etapt.GetZaxis().SetTitle('acc.')
        acc2d_b_etapt.GetXaxis().SetTitleOffset(1.0)
        acc2d_b_etapt.GetYaxis().SetTitleOffset(0.8)
        acc2d_b_etapt.GetZaxis().SetTitleOffset(0.6)
        acc2d_b_etapt.GetZaxis().SetRangeUser(0,1.0)
        acc2d_b_etapt.GetXaxis().SetNdivisions(505)
        acc2d_b_etapt.Draw("colzTEXT")
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
        latex2.DrawLatex(0.40, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, "#sqrt{s} = 13 TeV")
        c.SaveAs("JJ_plots/acc2d_b_etapt_"+shortname+".png")
        c.SaveAs("JJ_plots/acc2d_b_etapt_"+shortname+".pdf")
        del c


        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        dacc2d_b_eta.GetXaxis().SetTitle(X_Label+'(gen.)')
        dacc2d_b_eta.GetYaxis().SetTitle(Y_Label+'(gen.)')
        dacc2d_b_eta.GetZaxis().SetTitle('acc. unc.')
        dacc2d_b_eta.GetXaxis().SetTitleOffset(1.0)
        dacc2d_b_eta.GetYaxis().SetTitleOffset(0.8)
        dacc2d_b_eta.GetZaxis().SetTitleOffset(0.6)
        dacc2d_b_eta.GetZaxis().SetRangeUser(-0.01,0.1)
        dacc2d_b_eta.GetXaxis().SetNdivisions(505)
        dacc2d_b_eta.Draw("colzTEXT")
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
        latex2.DrawLatex(0.40, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, "#sqrt{s} = 13 TeV")
        c.SaveAs("JJ_plots/dacc2d_b_eta_"+shortname+".png")
        c.SaveAs("JJ_plots/dacc2d_b_eta_"+shortname+".pdf")
        del c

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        dacc2d_b_etapt.GetXaxis().SetTitle(X_Label+'(gen.)')
        dacc2d_b_etapt.GetYaxis().SetTitle(Y_Label+'(gen.)')
        dacc2d_b_etapt.GetZaxis().SetTitle('acc. unc.')
        dacc2d_b_etapt.GetXaxis().SetTitleOffset(1.0)
        dacc2d_b_etapt.GetYaxis().SetTitleOffset(0.8)
        dacc2d_b_etapt.GetZaxis().SetTitleOffset(0.6)
        dacc2d_b_etapt.GetZaxis().SetRangeUser(-0.01,0.3)
        dacc2d_b_etapt.GetXaxis().SetNdivisions(505)
        dacc2d_b_etapt.Draw("colzTEXT")
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
        latex2.DrawLatex(0.40, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, "#sqrt{s} = 13 TeV")
        c.SaveAs("JJ_plots/dacc2d_b_etapt_"+shortname+".png")
        c.SaveAs("JJ_plots/dacc2d_b_etapt_"+shortname+".pdf")
        #Saving histogram in root file
        f = TFile ("JJ_plots/acc_hist_"+shortname+".root","RECREATE")
        f.cd()
        acc2d_b_eta.Write()
        acc2d_a_eta.Write()
        dacc2d_b_eta.Write()
        dacc2d_a_eta.Write()
        acc2d_b_etapt.Write()
        acc2d_a_etapt.Write()
        dacc2d_b_etapt.Write()
        dacc2d_a_etapt.Write()
        f.Close()
        if opt.MIX:
            fa = TFile ("JJ_plots/acc_hist_Mix_SPS_DPS.root","RECREATE")  
            fa.cd()
            acc2d_b_Mix_eta.Write()
            acc2d_b_Mix_etapt.Write()
            acc2d_a_Mix_eta.Write()
            acc2d_a_Mix_etapt.Write()
            dacc2d_b_Mix_eta.Write()
            dacc2d_b_Mix_etapt.Write()
            dacc2d_a_Mix_eta.Write()
            dacc2d_a_Mix_etapt.Write()
            fa.Close()
            del acc2d_b_Mix_eta
            del acc2d_b_Mix_etapt
            del dacc2d_b_Mix_eta
            del dacc2d_b_Mix_etapt
            del acc2d_a_Mix_eta
            del acc2d_a_Mix_etapt
            del dacc2d_a_Mix_eta
            del dacc2d_a_Mix_etapt
        del acc2d_a_eta
        del acc2d_b_eta
        del dacc2d_b_eta
        del dacc2d_a_eta
        del acc2d_b_etapt
        del acc2d_a_etapt
        del dacc2d_b_etapt
        del dacc2d_a_etapt
