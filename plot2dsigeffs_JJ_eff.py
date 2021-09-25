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
                        
_temp = __import__('inputs_sig_JJ'+obsName+'_eff', globals(), locals(), ['recoeff_a','drecoeff_a','recoeff_b','drecoeff_b','recoeff_id_a','drecoeff_id_a','recoeff_id_b','drecoeff_id_b','recoeff_id_vtx_a','drecoeff_id_vtx_a','recoeff_id_vtx_b','drecoeff_id_vtx_b'], -1)
recoeff_a = _temp.recoeff_a
drecoeff_a = _temp.drecoeff_a
recoeff_b = _temp.recoeff_b
drecoeff_b = _temp.drecoeff_b
recoeff_id_a = _temp.recoeff_id_a
drecoeff_id_a = _temp.drecoeff_id_a
recoeff_id_b = _temp.recoeff_id_b
drecoeff_id_b = _temp.drecoeff_id_b
recoeff_id_vtx_a = _temp.recoeff_id_vtx_a
drecoeff_id_vtx_a = _temp.drecoeff_id_vtx_a
recoeff_id_vtx_b = _temp.recoeff_id_vtx_b
drecoeff_id_vtx_b = _temp.drecoeff_id_vtx_b

fStates = ['4mu']
channel = '4mu'
a_bins_pt = array('d',[float(obs_bins_pt[i]) for i in range(len(obs_bins_pt))])
a_bins_y = array('d',[float(obs_bins_y[i]) for i in range(len(obs_bins_y))])
print a_bins_pt
print a_bins_y
##Mixing SPS(80%) and DPS(20%)
if opt.MIX:
    recoeff_a_Mix = {}
    recoeff_b_Mix = {}
    recoeff_id_a_Mix = {}
    recoeff_id_b_Mix = {}
    recoeff_id_vtx_a_Mix = {}
    recoeff_id_vtx_b_Mix = {}
    drecoeff_a_Mix = {}
    drecoeff_b_Mix = {}
    drecoeff_id_a_Mix = {}
    drecoeff_id_b_Mix = {}
    drecoeff_id_vtx_a_Mix = {}
    drecoeff_id_vtx_b_Mix = {}

    for x in range(0,len(obs_bins_pt)-1):
        for y in range(0,len(obs_bins_y)-1):
            a = recoeff_a['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            b = recoeff_a['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            da = drecoeff_a['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            db = drecoeff_a['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            if (b>-1):
                c = (a*0.8)+(b*0.2)
                dc = (da*0.8)+(db*0.2)
            else:
                c = (a*1.0)
                dc = (da*1.0)
            recoeff_a_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = c
            drecoeff_a_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = dc
            a = recoeff_b['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            b = recoeff_b['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            da = drecoeff_b['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            db = drecoeff_b['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            if (b>-1):
                c = (a*0.8)+(b*0.2)
                dc = (da*0.8)+(db*0.2)
            else:
                c = (a*1.0)
                dc = (da*1.0)
            recoeff_b_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = c
            drecoeff_b_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = dc
            a = recoeff_id_a['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            b = recoeff_id_a['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            da = drecoeff_id_a['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            db = drecoeff_id_a['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            if (b>-1):
                c = (a*0.8)+(b*0.2)
                dc = (da*0.8)+(db*0.2)
            else:
                c = (a*1.0)
                dc = (da*1.0)
            recoeff_id_a_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = c
            drecoeff_id_a_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = dc
            a = recoeff_id_b['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            b = recoeff_id_b['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            da = drecoeff_id_b['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            db = drecoeff_id_b['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]

            if (b>-1):
                c = (a*0.8)+(b*0.2)
                dc = (da*0.8)+(db*0.2)
            else:
                c = (a*1.0)
                dc = (da*1.0)
            recoeff_id_b_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = c
            drecoeff_id_b_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = dc

            a = recoeff_id_vtx_a['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            b = recoeff_id_vtx_a['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            da = drecoeff_id_vtx_a['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            db = drecoeff_id_vtx_a['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]

            if (b>-1):
                c = (a*0.8)+(b*0.2)
                dc = (da*0.8)+(db*0.2)
            else:
                c = (a*1.0)
                dc = (da*1.0)
            recoeff_id_vtx_a_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = c
            drecoeff_id_vtx_a_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = dc

            a = recoeff_id_vtx_b['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            b = recoeff_id_vtx_b['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            da = drecoeff_id_vtx_b['SPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]
            db = drecoeff_id_vtx_b['DPS_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]

            if (b>-1):
                c = (a*0.8)+(b*0.2)
                dc = (da*0.8)+(db*0.2)
            else:
                c = (a*1.0)
                dc = (da*1.0)
            recoeff_id_vtx_b_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = c
            drecoeff_id_vtx_b_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)] = dc
List = []
for long, short in sample_shortnames.iteritems():
    List.append(long)
i_sample = -1
print List
for Sample in List:
    i_sample = i_sample+1
    shortname = sample_shortnames[Sample]
    for fState in fStates:
        recoeff2d_a = TH2D("recoeff2d_a", "recoeff2d_a", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        drecoeff2d_a = TH2D("drecoeff2d_a", "drecoeff2d_a", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        
        recoeff2d_b = TH2D("recoeff2d_b", "recoeff2d_b", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        drecoeff2d_b = TH2D("drecoeff2d_b", "drecoeff2d_b", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        if opt.MIX:
            recoeff2d_a_Mix = TH2D("recoeff2d_a_Mix", "recoeff2d_a_Mix", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
            recoeff2d_b_Mix = TH2D("recoeff2d_b_Mix", "recoeff2d_b_Mix", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
            drecoeff2d_a_Mix = TH2D("drecoeff2d_a_Mix", "drecoeff2d_a_Mix", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
            drecoeff2d_b_Mix = TH2D("drecoeff2d_b_Mix", "drecoeff2d_b_Mix", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)

        recoeff2d_id_a = TH2D("recoeff2d_id_a", "recoeff2d_id_a", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        drecoeff2d_id_a = TH2D("drecoeff2d_id_a", "drecoeff2d_id_a", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)

        recoeff2d_id_b = TH2D("recoeff2d_id_b", "recoeff2d_id_b", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        drecoeff2d_id_b = TH2D("drecoeff2d_id_b", "drecoeff2d_id_b", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)

        if opt.MIX:
            recoeff2d_id_a_Mix = TH2D("recoeff2d_id_a_Mix", "recoeff2d_id_a_Mix", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
            recoeff2d_id_b_Mix = TH2D("recoeff2d_id_b_Mix", "recoeff2d_id_b_Mix", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)

            drecoeff2d_id_a_Mix = TH2D("drecoeff2d_id_a_Mix", "drecoeff2d_id_a_Mix", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
            drecoeff2d_id_b_Mix = TH2D("drecoeff2d_id_b_Mix", "drecoeff2d_id_b_Mix", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)

        recoeff2d_id_vtx_a = TH2D("recoeff2d_id_vtx_a", "recoeff2d_id_vtx_a", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        drecoeff2d_id_vtx_a = TH2D("drecoeff2d_id_vtx_a", "drecoeff2d_id_vtx_a", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)

        recoeff2d_id_vtx_b = TH2D("recoeff2d_id_vtx_b", "recoeff2d_id_vtx_b", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        drecoeff2d_id_vtx_b = TH2D("drecoeff2d_id_vtx_b", "drecoeff2d_id_vtx_b", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
        if opt.MIX:
            recoeff2d_id_vtx_a_Mix = TH2D("recoeff2d_id_vtx_a_Mix", "recoeff2d_id_vtx_a_Mix", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
            recoeff2d_id_vtx_b_Mix = TH2D("recoeff2d_id_vtx_b_Mix", "recoeff2d_id_vtx_b_Mix", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
            drecoeff2d_id_vtx_a_Mix = TH2D("drecoeff2d_id_vtx_a_Mix", "drecoeff2d_id_vtx_a_Mix", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)
            drecoeff2d_id_vtx_b_Mix = TH2D("drecoeff2d_id_vtx_b_Mix", "drecoeff2d_id_vtx_b_Mix", len(obs_bins_pt)-1, a_bins_pt, len(obs_bins_y)-1, a_bins_y)

        for x in range(0,len(obs_bins_pt)-1):
            for y in range(0,len(obs_bins_y)-1):
                processBin = shortname+'_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)
                bin = recoeff2d_a.GetBin(x+1,y+1)
                recoeff2d_a.SetBinContent(bin,recoeff_a[processBin])
                drecoeff2d_a.SetBinContent(bin,drecoeff_a[processBin])    
                recoeff2d_b.SetBinContent(bin,recoeff_b[processBin])
                drecoeff2d_b.SetBinContent(bin,drecoeff_b[processBin])
                if opt.MIX:
                    recoeff2d_a_Mix.SetBinContent(bin,recoeff_a_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    recoeff2d_b_Mix.SetBinContent(bin,recoeff_b_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    drecoeff2d_a_Mix.SetBinContent(bin,drecoeff_a_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    drecoeff2d_b_Mix.SetBinContent(bin,drecoeff_b_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                recoeff2d_id_a.SetBinContent(bin,recoeff_id_a[processBin])
                drecoeff2d_id_a.SetBinContent(bin,drecoeff_id_a[processBin])
                recoeff2d_id_b.SetBinContent(bin,recoeff_id_b[processBin])
                drecoeff2d_id_b.SetBinContent(bin,drecoeff_id_b[processBin])
                if opt.MIX:
                    recoeff2d_id_a_Mix.SetBinContent(bin,recoeff_id_a_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    recoeff2d_id_b_Mix.SetBinContent(bin,recoeff_id_b_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)]) 
                    drecoeff2d_id_a_Mix.SetBinContent(bin,drecoeff_id_a_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    drecoeff2d_id_b_Mix.SetBinContent(bin,drecoeff_id_b_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                recoeff2d_id_vtx_a.SetBinContent(bin,recoeff_id_vtx_a[processBin])
                drecoeff2d_id_vtx_a.SetBinContent(bin,drecoeff_id_vtx_a[processBin])
                recoeff2d_id_vtx_b.SetBinContent(bin,recoeff_id_vtx_b[processBin])
                drecoeff2d_id_vtx_b.SetBinContent(bin,drecoeff_id_vtx_b[processBin])
                if opt.MIX:
                    recoeff2d_id_vtx_a_Mix.SetBinContent(bin,recoeff_id_vtx_a_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    recoeff2d_id_vtx_b_Mix.SetBinContent(bin,recoeff_id_vtx_b_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])   
                    drecoeff2d_id_vtx_a_Mix.SetBinContent(bin,drecoeff_id_vtx_a_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
                    drecoeff2d_id_vtx_b_Mix.SetBinContent(bin,drecoeff_id_vtx_b_Mix['Mix_JJto4mu_'+channel+'_'+opt.OBSNAME+'_genbin'+str(x)+'_genbin'+str(y)])
        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        recoeff2d_a.GetXaxis().SetTitle(X_Label+'(reco.)')
        recoeff2d_a.GetYaxis().SetTitle(Y_Label+'(reco.)')
        recoeff2d_a.GetZaxis().SetTitle('reco. eff.')
        recoeff2d_a.GetXaxis().SetTitleOffset(1.0)
        recoeff2d_a.GetYaxis().SetTitleOffset(0.8)
        recoeff2d_a.GetZaxis().SetTitleOffset(0.6)
        recoeff2d_a.GetZaxis().SetRangeUser(0.,1.0) 
        recoeff2d_a.Draw("colzTEXT")
        recoeff2d_a.GetXaxis().SetNdivisions(505)
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
        c.SaveAs("JJ_plots/recoeff2d_a_"+shortname+".png")
        c.SaveAs("JJ_plots/recoeff2d_a_"+shortname+".pdf")
        del c
        if opt.MIX:
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            recoeff2d_a_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            recoeff2d_a_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            recoeff2d_a_Mix.GetZaxis().SetTitle('reco. eff.')
            recoeff2d_a_Mix.GetXaxis().SetTitleOffset(1.0)
            recoeff2d_a_Mix.GetYaxis().SetTitleOffset(0.8)
            recoeff2d_a_Mix.GetZaxis().SetTitleOffset(0.6)
            recoeff2d_a_Mix.GetZaxis().SetRangeUser(0.,1.0)
            recoeff2d_a_Mix.Draw("colzTEXT")
            recoeff2d_a_Mix.GetXaxis().SetNdivisions(505)
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
            shortname_Mix = 'JJto4mu_SPS_DPS'
            latex2.DrawLatex(0.4, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/recoeff2d_a_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/recoeff2d_a_Mix_"+shortname_Mix+".pdf")
            del c
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            drecoeff2d_a_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            drecoeff2d_a_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            drecoeff2d_a_Mix.GetZaxis().SetTitle('reco. eff. unc.')
            drecoeff2d_a_Mix.GetXaxis().SetTitleOffset(1.0)
            drecoeff2d_a_Mix.GetYaxis().SetTitleOffset(0.8)
            drecoeff2d_a_Mix.GetZaxis().SetTitleOffset(0.6)
            drecoeff2d_a_Mix.GetZaxis().SetRangeUser(0.,0.4)
            drecoeff2d_a_Mix.Draw("colzTEXT")
            recoeff2d_a_Mix.GetXaxis().SetNdivisions(505)
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
            shortname_Mix = 'JJto4mu_SPS_DPS'
            latex2.DrawLatex(0.4, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/drecoeff2d_a_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/drecoeff2d_a_Mix_"+shortname_Mix+".pdf")
            del c
        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        drecoeff2d_a.GetXaxis().SetTitle(X_Label+'(reco.)')
        drecoeff2d_a.GetYaxis().SetTitle(Y_Label+'(reco.)')
        drecoeff2d_a.GetZaxis().SetTitle('reco. eff. unc.')
        drecoeff2d_a.GetXaxis().SetTitleOffset(1.0)
        drecoeff2d_a.GetYaxis().SetTitleOffset(0.8)
        drecoeff2d_a.GetZaxis().SetTitleOffset(0.6)
        drecoeff2d_a.GetZaxis().SetRangeUser(0.,0.4)
        drecoeff2d_a.Draw("colzTEXT")
        drecoeff2d_a.GetXaxis().SetNdivisions(505)
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
        c.SaveAs("JJ_plots/drecoeff2d_a_"+shortname+".png")
        c.SaveAs("JJ_plots/drecoeff2d_a_"+shortname+".pdf")
        del c

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        recoeff2d_b.GetXaxis().SetTitle(X_Label+'(reco.)')
        recoeff2d_b.GetYaxis().SetTitle(Y_Label+'(reco.)')
        recoeff2d_b.GetZaxis().SetTitle('reco. eff.')
        recoeff2d_b.GetXaxis().SetTitleOffset(1.0)
        recoeff2d_b.GetYaxis().SetTitleOffset(0.8)
        recoeff2d_b.GetZaxis().SetTitleOffset(0.6)
        recoeff2d_b.GetZaxis().SetRangeUser(0.,1.0)
        recoeff2d_b.Draw("colzTEXT")
        recoeff2d_b.GetXaxis().SetNdivisions(505)
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
        c.SaveAs("JJ_plots/recoeff2d_b_"+shortname+".png")
        c.SaveAs("JJ_plots/recoeff2d_b_"+shortname+".pdf")
        del c
        if opt.MIX:
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            recoeff2d_b_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            recoeff2d_b_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            recoeff2d_b_Mix.GetZaxis().SetTitle('reco. eff.')
            recoeff2d_b_Mix.GetXaxis().SetTitleOffset(1.0)
            recoeff2d_b_Mix.GetYaxis().SetTitleOffset(0.8)
            recoeff2d_b_Mix.GetZaxis().SetTitleOffset(0.6)
            recoeff2d_b_Mix.GetZaxis().SetRangeUser(0.,1.0)
            recoeff2d_b_Mix.Draw("colzTEXT")
            recoeff2d_b_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/recoeff2d_b_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/recoeff2d_b_Mix_"+shortname_Mix+".pdf")
            del c
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            drecoeff2d_b_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            drecoeff2d_b_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            drecoeff2d_b_Mix.GetZaxis().SetTitle('dreco. eff. unc.')
            drecoeff2d_b_Mix.GetXaxis().SetTitleOffset(1.0)
            drecoeff2d_b_Mix.GetYaxis().SetTitleOffset(0.8)
            drecoeff2d_b_Mix.GetZaxis().SetTitleOffset(0.6)
            drecoeff2d_b_Mix.GetZaxis().SetRangeUser(0.,0.4)
            drecoeff2d_b_Mix.Draw("colzTEXT")
            drecoeff2d_b_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/drecoeff2d_b_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/drecoeff2d_b_Mix_"+shortname_Mix+".pdf")
            del c
        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        drecoeff2d_b.GetXaxis().SetTitle(X_Label+'(reco.)')
        drecoeff2d_b.GetYaxis().SetTitle(Y_Label+'(reco.)')
        drecoeff2d_b.GetZaxis().SetTitle('reco. eff. unc.')
        drecoeff2d_b.GetXaxis().SetTitleOffset(1.0)
        drecoeff2d_b.GetYaxis().SetTitleOffset(0.8)
        drecoeff2d_b.GetZaxis().SetTitleOffset(0.6)
        drecoeff2d_b.GetZaxis().SetRangeUser(0.,0.4)
        drecoeff2d_b.Draw("colzTEXT")
        drecoeff2d_b.GetXaxis().SetNdivisions(505)
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
        c.SaveAs("JJ_plots/drecoeff2d_b_"+shortname+".png")
        c.SaveAs("JJ_plots/drecoeff2d_b_"+shortname+".pdf")
        del c

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        recoeff2d_id_a.GetXaxis().SetTitle(X_Label+'(reco.)')
        recoeff2d_id_a.GetYaxis().SetTitle(Y_Label+'(reco.)')
        recoeff2d_id_a.GetZaxis().SetTitle('#mu soft id. eff.')
        recoeff2d_id_a.GetXaxis().SetTitleOffset(1.0)
        recoeff2d_id_a.GetYaxis().SetTitleOffset(0.8)
        recoeff2d_id_a.GetZaxis().SetTitleOffset(0.6)
        recoeff2d_id_a.GetZaxis().SetRangeUser(0.45,1.0)
        recoeff2d_id_a.Draw("colzTEXT")
        recoeff2d_id_a.GetXaxis().SetNdivisions(505)
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
        c.SaveAs("JJ_plots/recoeff2d_id_a_"+shortname+".png")
        c.SaveAs("JJ_plots/recoeff2d_id_a_"+shortname+".pdf")
        del c
        if opt.MIX:
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            recoeff2d_id_a_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            recoeff2d_id_a_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            recoeff2d_id_a_Mix.GetZaxis().SetTitle('#mu soft id. eff.')
            recoeff2d_id_a_Mix.GetXaxis().SetTitleOffset(1.0)
            recoeff2d_id_a_Mix.GetYaxis().SetTitleOffset(0.8)
            recoeff2d_id_a_Mix.GetZaxis().SetTitleOffset(0.6)
            recoeff2d_id_a_Mix.GetZaxis().SetRangeUser(0.6,1.0)
            recoeff2d_id_a_Mix.Draw("colzTEXT")
            recoeff2d_id_a_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/recoeff2d_id_a_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/recoeff2d_id_a_Mix_"+shortname_Mix+".pdf")
            del c
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            drecoeff2d_id_a_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            drecoeff2d_id_a_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            drecoeff2d_id_a_Mix.GetZaxis().SetTitle('#mu soft id. eff. unc')
            drecoeff2d_id_a_Mix.GetXaxis().SetTitleOffset(1.0)
            drecoeff2d_id_a_Mix.GetYaxis().SetTitleOffset(0.8)
            drecoeff2d_id_a_Mix.GetZaxis().SetTitleOffset(0.6)
            drecoeff2d_id_a_Mix.GetZaxis().SetRangeUser(0,0.4)
            drecoeff2d_id_a_Mix.Draw("colzTEXT")
            drecoeff2d_id_a_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/drecoeff2d_id_a_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/drecoeff2d_id_a_Mix_"+shortname_Mix+".pdf")
            del c
        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        drecoeff2d_id_a.GetXaxis().SetTitle(X_Label+'(reco.)')
        drecoeff2d_id_a.GetYaxis().SetTitle(Y_Label+'(reco.)')
        drecoeff2d_id_a.GetZaxis().SetTitle('#mu soft id. eff. unc.')
        drecoeff2d_id_a.GetXaxis().SetTitleOffset(1.0)
        drecoeff2d_id_a.GetYaxis().SetTitleOffset(0.8)
        drecoeff2d_id_a.GetZaxis().SetTitleOffset(0.6)
        drecoeff2d_id_a.GetZaxis().SetRangeUser(0.,0.4)
        drecoeff2d_id_a.Draw("colzTEXT")
        drecoeff2d_id_a.GetXaxis().SetNdivisions(505)
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
        c.SaveAs("JJ_plots/drecoeff2d_id_a_"+shortname+".png")
        c.SaveAs("JJ_plots/drecoeff2d_id_a_"+shortname+".pdf")
        del c

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        recoeff2d_id_b.GetXaxis().SetTitle(X_Label+'(reco.)')
        recoeff2d_id_b.GetYaxis().SetTitle(Y_Label+'(reco.)')
        recoeff2d_id_b.GetZaxis().SetTitle('#mu soft id. eff.')
        recoeff2d_id_b.GetXaxis().SetTitleOffset(1.0)
        recoeff2d_id_b.GetYaxis().SetTitleOffset(0.8)
        recoeff2d_id_b.GetZaxis().SetTitleOffset(0.6)
        recoeff2d_id_b.GetZaxis().SetRangeUser(0.45,1.0)
        recoeff2d_id_b.Draw("colzTEXT")
        recoeff2d_id_b.GetXaxis().SetNdivisions(505)
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
        c.SaveAs("JJ_plots/recoeff2d_id_b_"+shortname+".png")
        c.SaveAs("JJ_plots/recoeff2d_id_b_"+shortname+".pdf")
        del c


        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        drecoeff2d_id_b.GetXaxis().SetTitle(X_Label+'(reco.)')
        drecoeff2d_id_b.GetYaxis().SetTitle(Y_Label+'(reco.)')
        drecoeff2d_id_b.GetZaxis().SetTitle('#mu soft id. eff. unc.')
        drecoeff2d_id_b.GetXaxis().SetTitleOffset(1.0)
        drecoeff2d_id_b.GetYaxis().SetTitleOffset(0.8)
        drecoeff2d_id_b.GetZaxis().SetTitleOffset(0.6)
        drecoeff2d_id_b.GetZaxis().SetRangeUser(0.,0.4)
        drecoeff2d_id_b.Draw("colzTEXT")
        drecoeff2d_id_b.GetXaxis().SetNdivisions(505)
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
        c.SaveAs("JJ_plots/drecoeff2d_id_b_"+shortname+".png")
        c.SaveAs("JJ_plots/drecoeff2d_id_b_"+shortname+".pdf")
        del c
        if opt.MIX:
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            recoeff2d_id_b_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            recoeff2d_id_b_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            recoeff2d_id_b_Mix.GetZaxis().SetTitle('#mu soft id. eff.')
            recoeff2d_id_b_Mix.GetXaxis().SetTitleOffset(1.0)
            recoeff2d_id_b_Mix.GetYaxis().SetTitleOffset(0.8)
            recoeff2d_id_b_Mix.GetZaxis().SetTitleOffset(0.6)
            recoeff2d_id_b_Mix.GetZaxis().SetRangeUser(0.6,1.0)
            recoeff2d_id_b_Mix.Draw("colzTEXT")
            recoeff2d_id_b_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/recoeff2d_id_b_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/recoeff2d_id_b_Mix_"+shortname_Mix+".pdf")
            del c
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            drecoeff2d_id_b_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            drecoeff2d_id_b_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            drecoeff2d_id_b_Mix.GetZaxis().SetTitle('#mu soft id. eff. unc.')
            drecoeff2d_id_b_Mix.GetXaxis().SetTitleOffset(1.0)
            drecoeff2d_id_b_Mix.GetYaxis().SetTitleOffset(0.8)
            drecoeff2d_id_b_Mix.GetZaxis().SetTitleOffset(0.6)
            drecoeff2d_id_b_Mix.GetZaxis().SetRangeUser(0,0.4)
            drecoeff2d_id_b_Mix.Draw("colzTEXT")
            drecoeff2d_id_b_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/drecoeff2d_id_b_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/drecoeff2d_id_b_Mix_"+shortname_Mix+".pdf")
            del c
        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        recoeff2d_id_vtx_a.GetXaxis().SetTitle(X_Label+'(reco.)')
        recoeff2d_id_vtx_a.GetYaxis().SetTitle(Y_Label+'(reco.)')
        recoeff2d_id_vtx_a.GetZaxis().SetTitle('dimuon vertex cut eff.')
        recoeff2d_id_vtx_a.GetXaxis().SetTitleOffset(1.0)
        recoeff2d_id_vtx_a.GetYaxis().SetTitleOffset(0.8)
        recoeff2d_id_vtx_a.GetZaxis().SetTitleOffset(0.6)
        recoeff2d_id_vtx_a.GetZaxis().SetRangeUser(0.45,1.0)
        recoeff2d_id_vtx_a.Draw("colzTEXT")
        recoeff2d_id_vtx_a.GetXaxis().SetNdivisions(505)
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
        c.SaveAs("JJ_plots/recoeff2d_id_vtx_a_"+shortname+".png")
        c.SaveAs("JJ_plots/recoeff2d_id_vtx_a_"+shortname+".pdf")
        del c

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        drecoeff2d_id_vtx_a.GetXaxis().SetTitle(X_Label+'(reco.)')
        drecoeff2d_id_vtx_a.GetYaxis().SetTitle(Y_Label+'(reco.)')
        drecoeff2d_id_vtx_a.GetZaxis().SetTitle('dimuon vertex cut eff. unc.')
        drecoeff2d_id_vtx_a.GetXaxis().SetTitleOffset(1.0)
        drecoeff2d_id_vtx_a.GetYaxis().SetTitleOffset(0.8)
        drecoeff2d_id_vtx_a.GetZaxis().SetTitleOffset(0.6)
        drecoeff2d_id_vtx_a.GetZaxis().SetRangeUser(0.,0.4)
        drecoeff2d_id_vtx_a.Draw("colzTEXT")
        drecoeff2d_id_vtx_a.GetXaxis().SetNdivisions(505)
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
        c.SaveAs("JJ_plots/drecoeff2d_id_vtx_a_"+shortname+".png")
        c.SaveAs("JJ_plots/drecoeff2d_id_vtx_a_"+shortname+".pdf")
        del c
        if opt.MIX:
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            recoeff2d_id_vtx_a_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            recoeff2d_id_vtx_a_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            recoeff2d_id_vtx_a_Mix.GetZaxis().SetTitle('dimuon vertex cut eff.')
            recoeff2d_id_vtx_a_Mix.GetXaxis().SetTitleOffset(1.0)
            recoeff2d_id_vtx_a_Mix.GetYaxis().SetTitleOffset(0.8)
            recoeff2d_id_vtx_a_Mix.GetZaxis().SetTitleOffset(0.6)
            recoeff2d_id_vtx_a_Mix.GetZaxis().SetRangeUser(0.9,1.0)
            recoeff2d_id_vtx_a_Mix.Draw("colzTEXT")
            recoeff2d_id_vtx_a_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/recoeff2d_id_vtx_a_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/recoeff2d_id_vtx_a_Mix_"+shortname_Mix+".pdf")
            del c
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            drecoeff2d_id_vtx_a_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            drecoeff2d_id_vtx_a_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            drecoeff2d_id_vtx_a_Mix.GetZaxis().SetTitle('dimuon vertex cut eff. unc.')
            drecoeff2d_id_vtx_a_Mix.GetXaxis().SetTitleOffset(1.0)
            drecoeff2d_id_vtx_a_Mix.GetYaxis().SetTitleOffset(0.8)
            drecoeff2d_id_vtx_a_Mix.GetZaxis().SetTitleOffset(0.6)
            drecoeff2d_id_vtx_a_Mix.GetZaxis().SetRangeUser(0,0.4)
            drecoeff2d_id_vtx_a_Mix.Draw("colzTEXT")
            drecoeff2d_id_vtx_a_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/drecoeff2d_id_vtx_a_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/drecoeff2d_id_vtx_a_Mix_"+shortname_Mix+".pdf")
            del c

        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        recoeff2d_id_vtx_b.GetXaxis().SetTitle(X_Label+'(reco.)')
        recoeff2d_id_vtx_b.GetYaxis().SetTitle(Y_Label+'(reco.)')
        recoeff2d_id_vtx_b.GetZaxis().SetTitle('dimuon vertex cut eff.')
        recoeff2d_id_vtx_b.GetXaxis().SetTitleOffset(1.0)
        recoeff2d_id_vtx_b.GetYaxis().SetTitleOffset(0.8)
        recoeff2d_id_vtx_b.GetZaxis().SetTitleOffset(0.6)
        recoeff2d_id_vtx_b.GetZaxis().SetRangeUser(0.45,1.0)
        recoeff2d_id_vtx_b.Draw("colzTEXT")
        recoeff2d_id_vtx_b.GetXaxis().SetNdivisions(505)
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
        c.SaveAs("JJ_plots/recoeff2d_id_vtx_b_"+shortname+".png")
        c.SaveAs("JJ_plots/recoeff2d_id_vtx_b_"+shortname+".pdf")
        del c


        c=TCanvas("c","c",3000,1200)
        c.cd()
        c.SetTopMargin(0.10)
        c.SetRightMargin(0.20)
        drecoeff2d_id_vtx_b.GetXaxis().SetTitle(X_Label+'(reco.)')
        drecoeff2d_id_vtx_b.GetYaxis().SetTitle(Y_Label+'(reco.)')
        drecoeff2d_id_vtx_b.GetZaxis().SetTitle('dimuon vertex cut eff. unc.')
        drecoeff2d_id_vtx_b.GetXaxis().SetTitleOffset(1.0)
        drecoeff2d_id_vtx_b.GetYaxis().SetTitleOffset(0.8)
        drecoeff2d_id_vtx_b.GetZaxis().SetTitleOffset(0.6)
        drecoeff2d_id_vtx_b.GetZaxis().SetRangeUser(0.,0.4)
        drecoeff2d_id_vtx_b.Draw("colzTEXT")
        drecoeff2d_id_vtx_b.GetXaxis().SetNdivisions(505)
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
        c.SaveAs("JJ_plots/drecoeff2d_id_vtx_b_"+shortname+".png")
        c.SaveAs("JJ_plots/drecoeff2d_id_vtx_b_"+shortname+".pdf")
        del c
        if opt.MIX:
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            recoeff2d_id_vtx_b_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            recoeff2d_id_vtx_b_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            recoeff2d_id_vtx_b_Mix.GetZaxis().SetTitle('dimuon vertex cut eff.')
            recoeff2d_id_vtx_b_Mix.GetXaxis().SetTitleOffset(1.0)
            recoeff2d_id_vtx_b_Mix.GetYaxis().SetTitleOffset(0.8)
            recoeff2d_id_vtx_b_Mix.GetZaxis().SetTitleOffset(0.6)
            recoeff2d_id_vtx_b_Mix.GetZaxis().SetRangeUser(0.9,1.0)
            recoeff2d_id_vtx_b_Mix.Draw("colzTEXT")
            recoeff2d_id_vtx_b_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/recoeff2d_id_vtx_b_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/recoeff2d_id_vtx_b_Mix_"+shortname_Mix+".pdf")
            del c
            c=TCanvas("c","c",3000,1200)
            c.cd()
            c.SetTopMargin(0.10)
            c.SetRightMargin(0.20)
            drecoeff2d_id_vtx_b_Mix.GetXaxis().SetTitle(X_Label+'(reco.)')
            drecoeff2d_id_vtx_b_Mix.GetYaxis().SetTitle(Y_Label+'(reco.)')
            drecoeff2d_id_vtx_b_Mix.GetZaxis().SetTitle('dimuon vertex cut eff. unc.')
            drecoeff2d_id_vtx_b_Mix.GetXaxis().SetTitleOffset(1.0)
            drecoeff2d_id_vtx_b_Mix.GetYaxis().SetTitleOffset(0.8)
            drecoeff2d_id_vtx_b_Mix.GetZaxis().SetTitleOffset(0.6)
            drecoeff2d_id_vtx_b_Mix.GetZaxis().SetRangeUser(0.,0.4)
            drecoeff2d_id_vtx_b_Mix.Draw("colzTEXT")
            drecoeff2d_id_vtx_b_Mix.GetXaxis().SetNdivisions(505)
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
            latex2.DrawLatex(0.4, 0.92,shortname_Mix)
            latex2.DrawLatex(0.72, 0.92, " #sqrt{s} = 13 TeV")
            c.SaveAs("JJ_plots/drecoeff2d_id_vtx_b_Mix_"+shortname_Mix+".png")
            c.SaveAs("JJ_plots/drecoeff2d_id_vtx_b_Mix_"+shortname_Mix+".pdf")
            del c
        #Saving histogram in root file
        f = TFile ("JJ_plots/eff_hist_"+shortname+".root","RECREATE")
        f.cd()
        recoeff2d_a.Write()
        drecoeff2d_a.Write()
        recoeff2d_id_a.Write()
        drecoeff2d_id_a.Write()
        recoeff2d_id_vtx_a.Write()
        drecoeff2d_id_vtx_a.Write()
        recoeff2d_b.Write()
        drecoeff2d_b.Write()
        recoeff2d_id_b.Write()
        drecoeff2d_id_b.Write()
        recoeff2d_id_vtx_b.Write()
        drecoeff2d_id_vtx_b.Write()        
        f.Close()
        if opt.MIX:
            fa = TFile ("JJ_plots/eff_hist_Mix_"+shortname_Mix+".root","RECREATE")
            fa.cd()
            recoeff2d_a_Mix.Write()
            recoeff2d_id_a_Mix.Write()
            recoeff2d_id_vtx_a_Mix.Write()
            recoeff2d_b_Mix.Write()
            recoeff2d_id_b_Mix.Write()
            recoeff2d_id_vtx_b_Mix.Write()
            drecoeff2d_a_Mix.Write()
            drecoeff2d_id_a_Mix.Write()
            drecoeff2d_id_vtx_a_Mix.Write()
            drecoeff2d_b_Mix.Write()
            drecoeff2d_id_b_Mix.Write()
            drecoeff2d_id_vtx_b_Mix.Write()
            fa.Close()
            del recoeff2d_a_Mix
            del recoeff2d_id_a_Mix
            del recoeff2d_id_vtx_a_Mix
            del recoeff2d_b_Mix
            del recoeff2d_id_b_Mix
            del recoeff2d_id_vtx_b_Mix
            del drecoeff2d_a_Mix
            del drecoeff2d_id_a_Mix
            del drecoeff2d_id_vtx_a_Mix
            del drecoeff2d_b_Mix
            del drecoeff2d_id_b_Mix
            del drecoeff2d_id_vtx_b_Mix

        del recoeff2d_a
        del drecoeff2d_a
        del recoeff2d_id_a
        del drecoeff2d_id_a
        del recoeff2d_id_vtx_a
        del drecoeff2d_id_vtx_a
        del recoeff2d_b
        del drecoeff2d_b
        del recoeff2d_id_b
        del drecoeff2d_id_b
        del recoeff2d_id_vtx_b
        del drecoeff2d_id_vtx_b
