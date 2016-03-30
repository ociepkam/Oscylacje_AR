__author__ = 'Michal Ociepka'

from parameters import Instruction_type, Per
from trial import Trial
from instruction import Instruction
from block import Block
from experiment import Experiment


trial = Trial(0, Per.small, 2, 0, 0, 0)
trial2 = Trial(12, Per.small, 2, 1, 5, 1)
instrukcja = Instruction("instrukcja.yaml", Instruction_type.text, 3)
blok = Block(False, [instrukcja, trial, trial2])
eksperyment = Experiment([blok], "as", "K", 25)
print eksperyment.prepare()
eksperyment.save()

# print trial.matrix_a
# print trial.matrix_b
# print trial.matrix_c
# print trial.matrix_d1
# print trial.matrix_d2
# print trial.matrix_d3
# print trial.matrix_d3
# print trial.matrix_d4
# print trial.matrix_d5
# print trial.matrix_d6

#print trial.prepare_trial()




"""
TODO:
wskazowka tekstowa
"""
