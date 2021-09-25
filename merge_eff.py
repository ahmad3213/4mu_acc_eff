import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
from array import array
from math import *
from decimal import *
import os,sys
sys.path.append('./SPS_DPS_JHU_resutls')
obsName = "pT2mu_rapidity2mu"
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
_temp = __import__('inputs_sig_JJ'+obsName+'_eff_test', globals(), locals(), ['recoeff_a','drecoeff_a','recoeff_b','drecoeff_b','recoeff_id_a','drecoeff_id_a','recoeff_id_b','drecoeff_id_b','recoeff_id_vtx_a','drecoeff_id_vtx_a','recoeff_id_vtx_b','drecoeff_id_vtx_b'], -1)
recoeff_a_test = _temp.recoeff_a
drecoeff_a_test = _temp.drecoeff_a
recoeff_b_test = _temp.recoeff_b
drecoeff_b_test = _temp.drecoeff_b
recoeff_id_a_test = _temp.recoeff_id_a
drecoeff_id_a_test = _temp.drecoeff_id_a
recoeff_id_b_test = _temp.recoeff_id_b
drecoeff_id_b_test = _temp.drecoeff_id_b
recoeff_id_vtx_a_test = _temp.recoeff_id_vtx_a
drecoeff_id_vtx_a_test = _temp.drecoeff_id_vtx_a
recoeff_id_vtx_b_test = _temp.recoeff_id_vtx_b
drecoeff_id_vtx_b_test = _temp.drecoeff_id_vtx_b


recoeff_a.update(recoeff_a_test)
drecoeff_a.update(drecoeff_a_test)
recoeff_b.update(recoeff_b_test)
drecoeff_b.update(drecoeff_b_test)
recoeff_id_a.update(recoeff_id_a_test)
drecoeff_id_a.update(drecoeff_id_a_test)
recoeff_id_b.update(recoeff_id_b_test)
drecoeff_id_b.update(drecoeff_id_b_test)
recoeff_id_vtx_a.update(recoeff_id_vtx_a_test)
drecoeff_id_vtx_a.update(drecoeff_id_vtx_a_test)
recoeff_id_vtx_b.update(recoeff_id_vtx_b_test)
drecoeff_id_vtx_b.update(drecoeff_id_vtx_b_test)


with open('inputs_sig_JJ'+obsName+'_eff_final.py', 'w') as f:
     f.write('recoeff_a = '+str(recoeff_a)+' \n')
     f.write('drecoeff_a = '+str(drecoeff_a)+' \n')
     f.write('recoeff_b = '+str(recoeff_b)+' \n')
     f.write('drecoeff_b = '+str(drecoeff_b)+' \n')
     f.write('recoeff_id_a = '+str(recoeff_id_a)+' \n')
     f.write('drecoeff_id_a = '+str(drecoeff_id_a)+' \n')
     f.write('recoeff_id_b = '+str(recoeff_id_b)+' \n')
     f.write('drecoeff_id_b = '+str(drecoeff_id_b)+' \n')
     f.write('recoeff_id_vtx_a = '+str(recoeff_id_vtx_a)+' \n')
     f.write('drecoeff_id_vtx_a = '+str(drecoeff_id_vtx_a)+' \n')
     f.write('recoeff_id_vtx_b = '+str(recoeff_id_vtx_b)+' \n')
     f.write('drecoeff_id_vtx_b = '+str(drecoeff_id_vtx_b)+' \n')


