import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *
import os,sys
sys.path.append('./SPS_DPS_JHU_resutls')
obsName = "pT2mu_rapidity2mu"
_temp = __import__('inputs_sig_JJ'+obsName, globals(), locals(), ['acc_a_eta','dacc_a_eta','acc_b_eta','dacc_b_eta','acc_a_etapt','dacc_a_etapt','acc_b_etapt','dacc_b_etapt'], -1)
acc_a_eta = _temp.acc_a_eta
acc_b_eta = _temp.acc_b_eta
dacc_a_eta = _temp.dacc_a_eta
dacc_b_eta = _temp.dacc_b_eta
acc_a_etapt = _temp.acc_a_etapt
acc_b_etapt = _temp.acc_b_etapt
dacc_a_etapt = _temp.dacc_a_etapt
dacc_b_etapt = _temp.dacc_b_etapt
_temp = __import__('inputs_sig_JJ'+obsName+'_test', globals(), locals(), ['acc_a_eta','dacc_a_eta','acc_b_eta','dacc_b_eta','acc_a_etapt','dacc_a_etapt','acc_b_etapt','dacc_b_etapt'], -1)
acc_a_eta_test = _temp.acc_a_eta
acc_b_eta_test = _temp.acc_b_eta
dacc_a_eta_test = _temp.dacc_a_eta
dacc_b_eta_test = _temp.dacc_b_eta
acc_a_etapt_test = _temp.acc_a_etapt
acc_b_etapt_test = _temp.acc_b_etapt
dacc_a_etapt_test = _temp.dacc_a_etapt
dacc_b_etapt_test = _temp.dacc_b_etapt

acc_a_eta.update(acc_a_eta_test)
acc_b_eta.update(acc_b_eta_test)
dacc_a_eta.update(dacc_a_eta_test)
dacc_b_eta.update(dacc_b_eta_test)
acc_a_etapt.update(acc_a_etapt_test)
acc_b_etapt.update(acc_b_etapt_test)
dacc_a_etapt.update(dacc_a_etapt_test)
dacc_b_etapt.update(dacc_b_etapt_test)

with open('inputs_sig_JJ'+obsName+'_final.py', 'w') as f:
    f.write('acc_a_eta = '+str(acc_a_eta)+' \n')
    f.write('dacc_a_eta = '+str(dacc_a_eta)+' \n')
    f.write('acc_b_eta = '+str(acc_b_eta)+' \n')
    f.write('dacc_b_eta = '+str(dacc_b_eta)+' \n')
    f.write('acc_a_etapt = '+str(acc_a_etapt)+' \n')
    f.write('dacc_a_etapt = '+str(dacc_a_etapt)+' \n')
    f.write('acc_b_etapt = '+str(acc_b_etapt)+' \n')
    f.write('dacc_b_etapt = '+str(dacc_b_etapt)+' \n')
