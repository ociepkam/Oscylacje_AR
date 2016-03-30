from classes.block import Block
from classes.experiment import Experiment
from classes.instruction import Instruction
from classes.parameters import Instruction_type, Per
from classes.trial import Trial

__author__ = 'Michal Ociepka'


trial = Trial(0, Per.small, 2, 0, 0, 0, "", -1)
trial2 = Trial(12, Per.small, 2, 1, 5, 1, "", -1)
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

# print trial.prepare_trial()
