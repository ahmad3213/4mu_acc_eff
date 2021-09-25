import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *
import os,sys
sys.path.append('./SPS_DPS_JHU_resutls')
obsName = "pT2mu_pT2mu"
_temp = __import__('inputs_sig_JJ'+obsName+'_evteff', globals(), locals(), ['recoeff_evt','drecoeff_evt'], -1)
recoeff_evt = _temp.recoeff_evt
drecoeff_evt = _temp.drecoeff_evt
recoeff_trg_evt = _temp.recoeff_trg_evt
drecoeff_trg_evt = _temp.drecoeff_trg_evt

_temp = __import__('inputs_sig_JJ'+obsName+'_evteff_test', globals(), locals(), ['recoeff_evt','drecoeff_evt'], -1)
recoeff_evt_test = _temp.recoeff_evt
drecoeff_evt_test = _temp.drecoeff_evt
recoeff_trg_evt_test = _temp.recoeff_trg_evt
drecoeff_trg_evt_test = _temp.drecoeff_trg_evt

recoeff_evt.update(recoeff_evt_test)
drecoeff_evt.update(drecoeff_evt_test)
recoeff_trg_evt.update(recoeff_trg_evt_test)
drecoeff_trg_evt.update(drecoeff_trg_evt_test)
with open('inputs_sig_JJ'+obsName+'_evteff_final.py', 'w') as f:
     f.write('recoeff_trg_evt = '+str(recoeff_trg_evt)+' \n')
     f.write('drecoeff_trg_evt = '+str(drecoeff_trg_evt)+' \n')
     f.write('recoeff_evt = '+str(recoeff_evt)+' \n')
     f.write('drecoeff_evt = '+str(drecoeff_evt)+' \n')



