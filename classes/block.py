import random


class Block:
    def __init__(self, rand, list_of_experiment_elements):
        self.list_of_experiment_elements = list_of_experiment_elements
        self.rand = rand

        if self.rand:
            self.randomize_block()

    def randomize_block(self):
        block_trials = [x for x in self.list_of_experiment_elements if x.type == 'trial']
        experiment_elements_to_randomize = [x for x in block_trials if x.exp]
        random.shuffle(experiment_elements_to_randomize)
        i = 0

        for idx, element in enumerate(self.list_of_experiment_elements):
            if element.type == 'trial':
                if element.exp:
                    self.list_of_experiment_elements[idx] = experiment_elements_to_randomize[i]
                    i += 1

    def prepare(self):
        elements_list = []
        for element in self.list_of_experiment_elements:
            elements_list.append(element.prepare())

        block_info = {
            "rand": self.rand,
            "experiment_elements": elements_list
        }
        return block_info
