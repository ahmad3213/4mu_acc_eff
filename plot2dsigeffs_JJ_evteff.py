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
    parser.add_option('',   '--symmetrize', action='store_true', dest='SYMMETRIZE', default=False, help='symmetrized to be independent of the ordering of the candidates, default is False') 
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
if (obsName=='pT2mu_pT2mu'):
    X_Label = 'p_{T} (J/#Psi)_{1}'
    Y_Label = 'p_{T} (J/#Psi)_{2}'


obs_bins_PT_a = opt.OBSBINS.split("_")[0]
obs_bins_PT_b = opt.OBSBINS.split("_")[1]
obs_bins_pt_a = obs_bins_PT_a.split("|")
obs_bins_pt_b = obs_bins_PT_b.split("|")
if (not (obs_bins_pt_a[0] == '' and obs_bins_pt_a[len(obs_bins_pt_a)-1]=='')):
    print 'BINS OPTION MUST START AND END WITH A |'
obs_bins_pt_a.pop()
obs_bins_pt_a.pop(0)
if (not (obs_bins_pt_b[0] == '' and obs_bins_pt_b[len(obs_bins_pt_b)-1]=='')):
    print 'BINS OPTION MUST START AND END WITH A |'
obs_bins_pt_b.pop()
obs_bins_pt_b.pop(0)

#if float(obs_bins[len(obs_bins)-1])>199:
#    obs_bins[len(obs_bins)-1]='250'
#    obs_bins[len(obs_bins)-1]='4'
                        
_temp = __import__('inputs_sig_JJ'+obsName+'_evteff', globals(), locals(), ['recoeff_evt','drecoeff_evt'], -1)
recoeff_evt = _temp.recoeff_evt
drecoeff_evt = _temp.drecoeff_evt
recoeff_trg_evt = _temp.recoeff_trg_evt
drecoeff_trg_evt = _temp.drecoeff_trg_evt
fStates = ['4mu']
channel = '4mu'
a_bins_pt_a = array('d',[float(obs_bins_pt_a[i]) for i in range(len(obs_bins_pt_a))])
a_bins_pt_b = array('d',[float(obs_bins_pt_b[i]) for i in range(len(obs_bins_pt_b))])
print a_bins_pt_a
print a_bins_pt_b
##Mixing SPS(80%) and DPS(20%)
if opt.MIX:
    recoeff_evt_Mix = {}
    drecoeff_evt_Mix = {} 
    recoeff_trg_evt_Mix = {}
    drecoeff_trg_evt_Mix = {}
    for x in range(0,len(a_bins_pt_a)-1):
        for y in range(0,len(a_bins_pt_b)-1):
            a = recoeff_trg_evt['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            b = recoeff_trg_evt['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            da = drecoeff_trg_evt['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            db = drecoeff_trg_evt['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            if (b>-1):
                c = (a*0.8)+(b*0.2)
                dc = (da*0.8)+(db*0.2)
            else:
                c = (a*1.0)
                dc = (da*1.0)
            recoeff_trg_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = c
            drecoeff_trg_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = dc

            a = recoeff_evt['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            b = recoeff_evt['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            da = drecoeff_evt['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            db = drecoeff_evt['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            if (b>-1):
                c = (a*0.8)+(b*0.2)
                dc = (da*0.8)+(db*0.2)
            else:
                c = (a*1.0)
                dc = (da*1.0)
            recoeff_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = c
            drecoeff_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = dc
List = []
for long, short in sample_shortnames.iteritems():
    List.append(long)
i_sample = -1
print List
for Sample in List:
    i_sample = i_sample+1
    shortname = sample_shortnames[Sample]
    for fState in fStates:
        recoeff2d_evt = TH2D("recoeff2d_evt", "recoeff2d_evt", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
        drecoeff2d_evt = TH2D("drecoeff2d_evt", "drecoeff2d_evt", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
        recoeff2d_trg = TH2D("recoeff2d_trg", "recoeff2d_trg", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
        drecoeff2d_trg = TH2D("drecoeff2d_trg", "drecoeff2d_trg", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
        if opt.SYMMETRIZE:
            recoeff2d_evt_sym = TH2D("recoeff2d_evt_sym", "recoeff2d_evt_sym", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
            drecoeff2d_evt_sym = TH2D("drecoeff2d_evt_sym", "drecoeff2d_evt_sym", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
            recoeff2d_trg_sym = TH2D("recoeff2d_trg_sym", "recoeff2d_trg_sym", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
            drecoeff2d_trg_sym = TH2D("drecoeff2d_trg_sym", "drecoeff2d_trg_sym", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)        
        if opt.MIX:
            recoeff2d_evt_Mix = TH2D("recoeff2d_evt_Mix", "recoeff2d_evt_Mix", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
            drecoeff2d_evt_Mix = TH2D("drecoeff2d_evt_Mix", "drecoeff2d_evt_Mix", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
            recoeff2d_trg_Mix = TH2D("recoeff2d_trg_Mix", "recoeff2d_trg_Mix", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
            drecoeff2d_trg_Mix = TH2D("drecoeff2d_trg_Mix", "drecoeff2d_trg_Mix", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
            if opt.SYMMETRIZE:
                recoeff2d_evt_sym_Mix = TH2D("recoeff2d_evt_sym_Mix", "recoeff2d_evt_sym_Mix", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
                drecoeff2d_evt_sym_Mix = TH2D("drecoeff2d_evt_sym_Mix", "drecoeff2d_evt_sym_Mix", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
                recoeff2d_trg_sym_Mix = TH2D("recoeff2d_trg_sym_Mix", "recoeff2d_trg_sym_Mix", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
                drecoeff2d_trg_sym_Mix = TH2D("drecoeff2d_trg_sym_Mix", "drecoeff2d_trg_sym_Mix", len(obs_bins_pt_a)-1, a_bins_pt_a, len(obs_bins_pt_b)-1, a_bins_pt_b)
        for x in range(0,len(obs_bins_pt_a)-1):
            for y in range(0,len(obs_bins_pt_b)-1):
                processBin = shortname+'_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)
                bin = recoeff2d_evt.GetBin(x+1,y+1)
                recoeff2d_evt.SetBinContent(bin,recoeff_evt[processBin])
                drecoeff2d_evt.SetBinContent(bin,drecoeff_evt[processBin])    
                recoeff2d_trg.SetBinContent(bin,recoeff_trg_evt[processBin])
                drecoeff2d_trg.SetBinContent(bin,drecoeff_trg_evt[processBin])
                if opt.MIX:
                    recoeff2d_evt_Mix.SetBinContent(bin,recoeff_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    drecoeff2d_evt_Mix.SetBinContent(bin,drecoeff_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])    
                    recoeff2d_trg_Mix.SetBinContent(bin,recoeff_trg_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    drecoeff2d_trg_Mix.SetBinContent(bin,drecoeff_trg_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                if opt.SYMMETRIZE:
                    recoeff2d_evt_sym.SetBinContent(bin,recoeff_evt[processBin])
                    drecoeff2d_evt_sym.SetBinContent(bin,drecoeff_evt[processBin])
                    recoeff2d_trg_sym.SetBinContent(bin,recoeff_trg_evt[processBin])
                    drecoeff2d_trg_sym.SetBinContent(bin,drecoeff_trg_evt[processBin])
                    if opt.MIX:
                        recoeff2d_evt_sym_Mix.SetBinContent(bin,recoeff_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                        drecoeff2d_evt_sym_Mix.SetBinContent(bin,drecoeff_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                        recoeff2d_trg_sym_Mix.SetBinContent(bin,recoeff_trg_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                        drecoeff2d_trg_sym_Mix.SetBinContent(bin,drecoeff_trg_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                if (x!=y and opt.SYMMETRIZE):
                    processBin_b = shortname+'_'+channel+'_'+opt.OBSNAME+'_genbin'+str(y)+'_genbin'+str(x)
                    avg_value = (recoeff_evt[processBin] + recoeff_evt[processBin_b])/2.0
                    recoeff2d_evt_sym.SetBinContent(bin,avg_value)
                    error = abs(recoeff_evt[processBin] - recoeff_evt[processBin_b])/(2.0*sqrt(2.0))
                    drecoeff2d_evt_sym.SetBinContent(bin,error)
                    avg_value = (recoeff_trg_evt[processBin] + recoeff_trg_evt[processBin_b])/2.0
                    recoeff2d_trg_sym.SetBinContent(bin,avg_value)
                    error = abs(recoeff_trg_evt[processBin] - recoeff_trg_evt[processBin_b])/(2.0*sqrt(2.0))
                    drecoeff2d_trg_sym.SetBinContent(bin,error)
                    if opt.MIX:
                        processBin_b = 'Mix_JJto4mu'+'_'+channel+'_'+opt.OBSNAME+'_genbin'+str(y)+'_genbin'+str(x)
                        avg_value = (recoeff_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] + recoeff_evt_Mix[processBin_b])/2.0
                        recoeff2d_evt_sym_Mix.SetBinContent(bin,avg_value)
                        error = abs(recoeff_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] - recoeff_evt_Mix[processBin_b])/(2.0*sqrt(2.0))
                        drecoeff2d_evt_sym_Mix.SetBinContent(bin,error)
                        avg_value = (recoeff_trg_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] + recoeff_trg_evt_Mix[processBin_b])/2.0
                        recoeff2d_trg_sym_Mix.SetBinContent(bin,avg_value)
                        error = abs(recoeff_trg_evt_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] - recoeff_trg_evt_Mix[processBin_b])/(2.0*sqrt(2.0))
                        drecoeff2d_trg_sym_Mix.SetBinContent(bin,error)

        c=TCanvas("c","c",1200,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        recoeff2d_evt.GetXaxis().SetTitle(X_Label+'(reco.)')
        recoeff2d_evt.GetYaxis().SetTitle(Y_Label+'(reco.)')
        recoeff2d_evt.GetZaxis().SetTitle('reco. eff.')
        recoeff2d_evt.GetXaxis().SetTitleOffset(1.3)
        recoeff2d_evt.GetYaxis().SetTitleOffset(0.8)
        recoeff2d_evt.GetZaxis().SetTitleOffset(1.3)
        recoeff2d_evt.GetZaxis().SetRangeUser(0,0.7) 
        recoeff2d_evt.Draw("colzTEXT")
        recoeff2d_evt.GetXaxis().SetNdivisions(505)
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
        latex2.DrawLatex(0.3, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.525, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
        c.SaveAs("JJ_plots/recoeff2d_evt_"+shortname+".png")
        c.SaveAs("JJ_plots/recoeff2d_evt_"+shortname+".pdf")
        del c
        if opt.MIX:

            c=TCanvas("c","c",1200,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            recoeff2d_evt_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            recoeff2d_evt_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            recoeff2d_evt_Mix.GetZaxis().SetTitle('reco. eff.')
            recoeff2d_evt_Mix.GetXaxis().SetTitleOffset(1.3)
            recoeff2d_evt_Mix.GetYaxis().SetTitleOffset(0.8)
            recoeff2d_evt_Mix.GetZaxis().SetTitleOffset(1.3)
            recoeff2d_evt_Mix.GetZaxis().SetRangeUser(0,0.7)
            recoeff2d_evt_Mix.Draw("colzTEXT")
            recoeff2d_evt_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.3, 0.92, "Preliminary")
            latex2.SetTextFont(42)
            latex2.SetTextSize(0.25*c.GetTopMargin())
            shortname_Mix = 'JJto4mu_SPS_DPS'
            latex2.DrawLatex(0.525, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV") 
            c.SaveAs("JJ_plots/recoeff2d_evt_Mix"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/recoeff2d_evt_Mix"+shortname_Mix+".pdf")            
            del c
        c=TCanvas("c","c",1200,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        recoeff2d_trg.GetXaxis().SetTitle(X_Label+'(reco.)')
        recoeff2d_trg.GetYaxis().SetTitle(Y_Label+'(reco.)')
        recoeff2d_trg.GetZaxis().SetTitle('trig. eff.')
        recoeff2d_trg.GetXaxis().SetTitleOffset(1.3)
        recoeff2d_trg.GetYaxis().SetTitleOffset(0.8)
        recoeff2d_trg.GetZaxis().SetTitleOffset(1.3)
        recoeff2d_trg.GetZaxis().SetRangeUser(0,0.7)
        recoeff2d_trg.Draw("colzTEXT")
        recoeff2d_trg.GetXaxis().SetNdivisions(505)
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
        latex2.DrawLatex(0.3, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.525, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
        c.SaveAs("JJ_plots/recoeff2d_trg_"+shortname+".png")
        c.SaveAs("JJ_plots/recoeff2d_trg_"+shortname+".pdf")
        del c
        if opt.MIX:
            c=TCanvas("c","c",1200,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            recoeff2d_trg_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            recoeff2d_trg_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            recoeff2d_trg_Mix.GetZaxis().SetTitle('trig. eff.')
            recoeff2d_trg_Mix.GetXaxis().SetTitleOffset(1.3)
            recoeff2d_trg_Mix.GetYaxis().SetTitleOffset(0.8)
            recoeff2d_trg_Mix.GetZaxis().SetTitleOffset(1.3)
            recoeff2d_trg_Mix.GetZaxis().SetRangeUser(0,0.7)
            recoeff2d_trg_Mix.Draw("colzTEXT")
            recoeff2d_trg_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.3, 0.92, "Preliminary")
            latex2.SetTextFont(42)
            latex2.SetTextSize(0.25*c.GetTopMargin())
            latex2.DrawLatex(0.525, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/recoeff2d_trg_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/recoeff2d_trg_Mix_"+shortname_Mix+".pdf")
        c=TCanvas("c","c",1200,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        drecoeff2d_evt.GetXaxis().SetTitle(X_Label+'(reco.)')
        drecoeff2d_evt.GetYaxis().SetTitle(Y_Label+'(reco.)')
        drecoeff2d_evt.GetZaxis().SetTitle('reco. eff. unc.')
        drecoeff2d_evt.GetXaxis().SetTitleOffset(1.3)
        drecoeff2d_evt.GetYaxis().SetTitleOffset(0.8)
        drecoeff2d_evt.GetZaxis().SetTitleOffset(1.3)
        drecoeff2d_evt.GetZaxis().SetRangeUser(0.,0.1)
        drecoeff2d_evt.Draw("colzTEXT")
        drecoeff2d_evt.GetXaxis().SetNdivisions(505)
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
        latex2.DrawLatex(0.3, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.525, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
        c.SaveAs("JJ_plots/drecoeff2d_evt_"+shortname+".png")
        c.SaveAs("JJ_plots/drecoeff2d_evt_"+shortname+".pdf")
        del c
        if opt.MIX:
            c=TCanvas("c","c",1200,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            drecoeff2d_evt_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            drecoeff2d_evt_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            drecoeff2d_evt_Mix.GetZaxis().SetTitle('reco. eff. unc.')
            drecoeff2d_evt_Mix.GetXaxis().SetTitleOffset(1.3)
            drecoeff2d_evt_Mix.GetYaxis().SetTitleOffset(0.8)
            drecoeff2d_evt_Mix.GetZaxis().SetTitleOffset(1.3)
            drecoeff2d_evt_Mix.GetZaxis().SetRangeUser(0.,0.1)
            drecoeff2d_evt_Mix.Draw("colzTEXT")
            drecoeff2d_evt_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.3, 0.92, "Preliminary")
            latex2.SetTextFont(42)
            latex2.SetTextSize(0.25*c.GetTopMargin())
            latex2.DrawLatex(0.525, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/drecoeff2d_evt_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/drecoeff2d_evt_Mix_"+shortname_Mix+".pdf")
            del c
        c=TCanvas("c","c",1200,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        drecoeff2d_trg.GetXaxis().SetTitle(X_Label+'(reco.)')
        drecoeff2d_trg.GetYaxis().SetTitle(Y_Label+'(reco.)')
        drecoeff2d_trg.GetZaxis().SetTitle('trig. eff. unc.')
        drecoeff2d_trg.GetXaxis().SetTitleOffset(1.3)
        drecoeff2d_trg.GetYaxis().SetTitleOffset(0.8)
        drecoeff2d_trg.GetZaxis().SetTitleOffset(1.3)
        drecoeff2d_trg.GetZaxis().SetRangeUser(0.,0.1)
        drecoeff2d_trg.Draw("colzTEXT")
        drecoeff2d_trg.GetXaxis().SetNdivisions(505)
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
        latex2.DrawLatex(0.3, 0.92, "Preliminary")
        latex2.SetTextFont(42)
        latex2.SetTextSize(0.25*c.GetTopMargin())
        latex2.DrawLatex(0.525, 0.92,shortname)
        latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
        c.SaveAs("JJ_plots/drecoeff2d_trg_"+shortname+".png")
        c.SaveAs("JJ_plots/drecoeff2d_trg_"+shortname+".pdf")
        del c
        if opt.MIX:
            c=TCanvas("c","c",1200,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            drecoeff2d_trg_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            drecoeff2d_trg_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            drecoeff2d_trg_Mix.GetZaxis().SetTitle('trig. eff. unc.')
            drecoeff2d_trg_Mix.GetXaxis().SetTitleOffset(1.3)
            drecoeff2d_trg_Mix.GetYaxis().SetTitleOffset(0.8)
            drecoeff2d_trg_Mix.GetZaxis().SetTitleOffset(1.3)
            drecoeff2d_trg_Mix.GetZaxis().SetRangeUser(0.,0.1)
            drecoeff2d_trg_Mix.Draw("colzTEXT")
            drecoeff2d_trg_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.3, 0.92, "Preliminary")
            latex2.SetTextFont(42)
            latex2.SetTextSize(0.25*c.GetTopMargin())
            latex2.DrawLatex(0.525, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/drecoeff2d_trg_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/drecoeff2d_trg_Mix_"+shortname_Mix+".pdf")
        if opt.SYMMETRIZE:
            c=TCanvas("c","c",1200,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            recoeff2d_evt_sym.GetXaxis().SetTitle(X_Label+'(reco.)')
            recoeff2d_evt_sym.GetYaxis().SetTitle(Y_Label+'(reco.)')
            recoeff2d_evt_sym.GetZaxis().SetTitle('reco. eff.')
            recoeff2d_evt_sym.GetXaxis().SetTitleOffset(1.3)
            recoeff2d_evt_sym.GetYaxis().SetTitleOffset(0.8)
            recoeff2d_evt_sym.GetZaxis().SetTitleOffset(1.3)
            recoeff2d_evt_sym.GetZaxis().SetRangeUser(0,0.7)
            recoeff2d_evt_sym.Draw("colzTEXT")
            recoeff2d_evt_sym.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.3, 0.92, "Preliminary")
            latex2.SetTextFont(42)
            latex2.SetTextSize(0.25*c.GetTopMargin())
            latex2.DrawLatex(0.525, 0.92,shortname)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/recoeff2d_evt_sym_"+shortname+".png")
            c.SaveAs("JJ_plots/recoeff2d_evt_sym_"+shortname+".pdf")
            del c
            if opt.MIX:
                c=TCanvas("c","c",1200,1200)
                c.cd()
                c.SetTopMargin(0.10)
                c.SetRightMargin(0.20)
                recoeff2d_evt_sym_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
                recoeff2d_evt_sym_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
                recoeff2d_evt_sym_Mix.GetZaxis().SetTitle('reco. eff.')
                recoeff2d_evt_sym_Mix.GetXaxis().SetTitleOffset(1.3)
                recoeff2d_evt_sym_Mix.GetYaxis().SetTitleOffset(0.8)
                recoeff2d_evt_sym_Mix.GetZaxis().SetTitleOffset(1.3)
                recoeff2d_evt_sym_Mix.GetZaxis().SetRangeUser(0,0.7)
                recoeff2d_evt_sym_Mix.Draw("colzTEXT")
                recoeff2d_evt_sym_Mix.GetXaxis().SetNdivisions(505)
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
                latex2.DrawLatex(0.3, 0.92, "Preliminary")
                latex2.SetTextFont(42)
                latex2.SetTextSize(0.25*c.GetTopMargin())
                latex2.DrawLatex(0.525, 0.92,shortname_Mix)
                latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
                c.SaveAs("JJ_plots/recoeff2d_evt_sym_Mix_"+shortname_Mix+".png")
                c.SaveAs("JJ_plots/recoeff2d_evt_sym_Mix_"+shortname_Mix+".pdf")
                del c
            c=TCanvas("c","c",1200,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            recoeff2d_trg_sym.GetXaxis().SetTitle(X_Label+'(reco.)')
            recoeff2d_trg_sym.GetYaxis().SetTitle(Y_Label+'(reco.)')
            recoeff2d_trg_sym.GetZaxis().SetTitle('trig. eff.')
            recoeff2d_trg_sym.GetXaxis().SetTitleOffset(1.3)
            recoeff2d_trg_sym.GetYaxis().SetTitleOffset(0.8)
            recoeff2d_trg_sym.GetZaxis().SetTitleOffset(1.3)
            recoeff2d_trg_sym.GetZaxis().SetRangeUser(0,0.7)
            recoeff2d_trg_sym.Draw("colzTEXT")
            recoeff2d_trg_sym.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.3, 0.92, "Preliminary")
            latex2.SetTextFont(42)
            latex2.SetTextSize(0.25*c.GetTopMargin())
            latex2.DrawLatex(0.525, 0.92,shortname)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/recoeff2d_trg_sym_"+shortname+".png")
            c.SaveAs("JJ_plots/recoeff2d_trg_sym_"+shortname+".pdf")
            del c
            if opt.MIX:
                c=TCanvas("c","c",1200,1200)
                c.cd()
                c.SetTopMargin(0.10)
                c.SetRightMargin(0.20)
                recoeff2d_trg_sym_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
                recoeff2d_trg_sym_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
                recoeff2d_trg_sym_Mix.GetZaxis().SetTitle('trig. eff.')
                recoeff2d_trg_sym_Mix.GetXaxis().SetTitleOffset(1.3)
                recoeff2d_trg_sym_Mix.GetYaxis().SetTitleOffset(0.8)
                recoeff2d_trg_sym_Mix.GetZaxis().SetTitleOffset(1.3)
                recoeff2d_trg_sym_Mix.GetZaxis().SetRangeUser(0,0.7)
                recoeff2d_trg_sym_Mix.Draw("colzTEXT")
                recoeff2d_trg_sym_Mix.GetXaxis().SetNdivisions(505)
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
                latex2.DrawLatex(0.3, 0.92, "Preliminary")
                latex2.SetTextFont(42)
                latex2.SetTextSize(0.25*c.GetTopMargin())
                latex2.DrawLatex(0.525, 0.92,shortname_Mix)
                latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
                c.SaveAs("JJ_plots/recoeff2d_trg_sym_Mix_"+shortname_Mix+".png")
                c.SaveAs("JJ_plots/recoeff2d_trg_sym_Mix_"+shortname_Mix+".pdf")
                del c
            c=TCanvas("c","c",1200,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            drecoeff2d_evt_sym.GetXaxis().SetTitle(X_Label+'(reco.)')
            drecoeff2d_evt_sym.GetYaxis().SetTitle(Y_Label+'(reco.)')
            drecoeff2d_evt_sym.GetZaxis().SetTitle('reco. eff. unc.')
            drecoeff2d_evt_sym.GetXaxis().SetTitleOffset(1.3)
            drecoeff2d_evt_sym.GetYaxis().SetTitleOffset(0.8)
            drecoeff2d_evt_sym.GetZaxis().SetTitleOffset(1.3)
            drecoeff2d_evt_sym.GetZaxis().SetRangeUser(0.,0.1)
            drecoeff2d_evt_sym.Draw("colzTEXT")
            drecoeff2d_evt_sym.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.3, 0.92, "Preliminary")
            latex2.SetTextFont(42)
            latex2.SetTextSize(0.25*c.GetTopMargin())
            latex2.DrawLatex(0.525, 0.92,shortname)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/drecoeff2d_evt_sym_"+shortname+".png")
            c.SaveAs("JJ_plots/drecoeff2d_evt_sym_"+shortname+".pdf")
            del c
            if opt.MIX:
                c=TCanvas("c","c",1200,1200)
                c.cd()
                c.SetTopMargin(0.10)
                c.SetRightMargin(0.20)
                drecoeff2d_evt_sym_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
                drecoeff2d_evt_sym_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
                drecoeff2d_evt_sym_Mix.GetZaxis().SetTitle('reco. eff. unc.')
                drecoeff2d_evt_sym_Mix.GetXaxis().SetTitleOffset(1.3)
                drecoeff2d_evt_sym_Mix.GetYaxis().SetTitleOffset(0.8)
                drecoeff2d_evt_sym_Mix.GetZaxis().SetTitleOffset(1.3)
                drecoeff2d_evt_sym_Mix.GetZaxis().SetRangeUser(0.,0.1)
                drecoeff2d_evt_sym_Mix.Draw("colzTEXT")
                drecoeff2d_evt_sym_Mix.GetXaxis().SetNdivisions(505)
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
                latex2.DrawLatex(0.3, 0.92, "Preliminary")
                latex2.SetTextFont(42)
                latex2.SetTextSize(0.25*c.GetTopMargin())
                latex2.DrawLatex(0.525, 0.92,shortname_Mix)
                latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
                c.SaveAs("JJ_plots/drecoeff2d_evt_sym_Mix_"+shortname_Mix+".png")
                c.SaveAs("JJ_plots/drecoeff2d_evt_sym_Mix_"+shortname_Mix+".pdf")
                del c
            c=TCanvas("c","c",1200,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            drecoeff2d_trg_sym.GetXaxis().SetTitle(X_Label+'(reco.)')
            drecoeff2d_trg_sym.GetYaxis().SetTitle(Y_Label+'(reco.)')
            drecoeff2d_trg_sym.GetZaxis().SetTitle('reco. eff. unc.')
            drecoeff2d_trg_sym.GetXaxis().SetTitleOffset(1.3)
            drecoeff2d_trg_sym.GetYaxis().SetTitleOffset(0.8)
            drecoeff2d_trg_sym.GetZaxis().SetTitleOffset(1.3)
            drecoeff2d_trg_sym.GetZaxis().SetRangeUser(0.,0.1)
            drecoeff2d_trg_sym.Draw("colzTEXT")
            drecoeff2d_trg_sym.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.3, 0.92, "Preliminary")
            latex2.SetTextFont(42)
            latex2.SetTextSize(0.25*c.GetTopMargin())
            latex2.DrawLatex(0.525, 0.92,shortname)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/drecoeff2d_trg_sym_"+shortname+".png")
            c.SaveAs("JJ_plots/drecoeff2d_trg_sym_"+shortname+".pdf")
            del c
            if opt.MIX:
                c=TCanvas("c","c",1200,1200)
                c.cd()
                c.SetTopMargin(0.10)
                c.SetRightMargin(0.20)
                drecoeff2d_trg_sym_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
                drecoeff2d_trg_sym_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
                drecoeff2d_trg_sym_Mix.GetZaxis().SetTitle('reco. eff. unc.')
                drecoeff2d_trg_sym_Mix.GetXaxis().SetTitleOffset(1.3)
                drecoeff2d_trg_sym_Mix.GetYaxis().SetTitleOffset(0.8)
                drecoeff2d_trg_sym_Mix.GetZaxis().SetTitleOffset(1.3)
                drecoeff2d_trg_sym_Mix.GetZaxis().SetRangeUser(0.,0.1)
                drecoeff2d_trg_sym_Mix.Draw("colzTEXT")
                drecoeff2d_trg_sym_Mix.GetXaxis().SetNdivisions(505)
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
                latex2.DrawLatex(0.3, 0.92, "Preliminary")
                latex2.SetTextFont(42)
                latex2.SetTextSize(0.25*c.GetTopMargin())
                latex2.DrawLatex(0.525, 0.92,shortname_Mix)
                latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
                c.SaveAs("JJ_plots/drecoeff2d_trg_sym_Mix_"+shortname_Mix+".png")
                c.SaveAs("JJ_plots/drecoeff2d_trg_sym_Mix_"+shortname_Mix+".pdf")
                del c

        #Saving histogram in root file
        f = TFile ("JJ_plots/evt_eff_hist_"+shortname+".root","RECREATE")
        f.cd()
        recoeff2d_evt.Write()
        drecoeff2d_evt.Write()
        recoeff2d_trg.Write()
        drecoeff2d_trg.Write()
        if opt.SYMMETRIZE:
            recoeff2d_evt_sym.Write()
            drecoeff2d_evt_sym.Write()
            recoeff2d_trg_sym.Write()
            drecoeff2d_trg_sym.Write()
        f.Close()
        del recoeff2d_evt
        del drecoeff2d_evt
        del recoeff2d_trg
        del drecoeff2d_trg
        if opt.MIX:
            fa = TFile ("JJ_plots/evt_eff_hist_Mix_"+shortname_Mix+".root","RECREATE")
            recoeff2d_evt_Mix.Write()
            drecoeff2d_evt_Mix.Write()
            recoeff2d_trg_Mix.Write()
            drecoeff2d_trg_Mix.Write()
            if opt.SYMMETRIZE:
                recoeff2d_evt_sym_Mix.Write()
                drecoeff2d_evt_sym_Mix.Write()
                recoeff2d_trg_sym_Mix.Write()
                drecoeff2d_trg_sym_Mix.Write()
            fa.Close()
            del recoeff2d_evt_Mix
            del drecoeff2d_evt_Mix
            del recoeff2d_trg_Mix
            del drecoeff2d_trg_Mix
            if opt.SYMMETRIZE:
                del recoeff2d_evt_sym_Mix
                del drecoeff2d_evt_sym_Mix
                del recoeff2d_trg_sym_Mix
                del drecoeff2d_trg_sym_Mix
