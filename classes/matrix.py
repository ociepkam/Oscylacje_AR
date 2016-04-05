import random
import copy
from parameters import PARAMETERS, PARAMETERS_DICT


class Matrix:
    def __init__(self, figure_list):
        self.figures_list = figure_list
        self.name = None

    def __str__(self):
        a = self.name
        for x in self.figures_list:
            a += "\n"
            a += x.__str__()
        return a

    def return_figure_list(self):
        parameters = []
        for figure in self.figures_list:
            parameters += [figure.return_parameters()]
        all_informations = {'name': self.name, 'parameters': parameters}
        return all_informations

    def shuffle_matrix(self):
        for i in range(0, len(self.figures_list) - 1):
            pick = random.randint(i + 1, len(self.figures_list) - 1)
            self.figures_list[i], self.figures_list[pick] = self.figures_list[pick], self.figures_list[i]

    def change_figures_positions(self, new_positions):
        new_figures_list = []
        for idx in new_positions:
            new_figures_list.append(self.figures_list[idx])
        self.figures_list = new_figures_list

    def change_figures_b(self, number_of_figures_to_change):
        figures_position = range(len(self.figures_list))
        random.shuffle(figures_position)
        figures_position = figures_position[:number_of_figures_to_change]
        list_of_parameters_to_change = [2]
        for i in range(number_of_figures_to_change - 1):
            list_of_parameters_to_change += [random.choice(range(1, 4))]

        for i in range(number_of_figures_to_change):
            self.figures_list[figures_position[i]].change_parameters(list_of_parameters_to_change[i])

    def change_figures_d1(self, list_of_changes):
        for idx in range(len(self.figures_list)):
            for parameter in list_of_changes[idx]:
                self.figures_list[idx].change_parameter(parameter[0])
        self.name = "D1"

    def change_figures_d2(self, list_of_changes):
        changes_2_or_shorter = [x for x in list_of_changes if 0 < len(x) <= 2]
        figure_parameters = random.choice(changes_2_or_shorter)
        parameter_to_change = random.choice(figure_parameters)

        possible_new_parameters = copy.deepcopy(PARAMETERS)
        for parameter, _ in figure_parameters:
            possible_new_parameters.remove(parameter)

        new_parameter = random.choice(possible_new_parameters)
        change_lvl = random.choice(range(len(PARAMETERS_DICT[new_parameter]) - 1)) + 1

        for idx_f, figure in enumerate(list_of_changes):
            if figure == figure_parameters:
                for idx_p, parameter in enumerate(figure):
                    if parameter == parameter_to_change:
                        figure[idx_p] = [new_parameter, change_lvl]
                        list_of_changes[idx_f] = figure
                        self.change_figures_d1(list_of_changes)
        self.name = "D2"

    def change_figures_d3(self, list_of_changes):
        changes_2_or_1 = [x for x in list_of_changes if len(x) >= 2]
        figure_parameters = random.choice(changes_2_or_1)
        parameter_to_remove = random.choice(figure_parameters)

        for idx_f, figure in enumerate(list_of_changes):
            if figure == figure_parameters:
                for idx_p, parameter in enumerate(figure):
                    if parameter == parameter_to_remove:
                        del figure[idx_p]
                        list_of_changes[idx_f] = figure
                        self.change_figures_d1(list_of_changes)
        self.name = "D3"

    def change_figures_d4(self, list_of_changes):
        changes_2_or_1 = [x for x in list_of_changes if 2 <= len(x) <= 3]
        figure_elements_to_change = random.choice(changes_2_or_1)
        for idx, figure in enumerate(list_of_changes):
            if figure == figure_elements_to_change:
                for name, _ in figure_elements_to_change:
                    self.figures_list[idx].change_parameter(name)
                break
        self.name = "D4"

    def change_figures_d5(self, list_of_changes):
        changes_2_or_1 = [x for x in list_of_changes if 0 < len(x) <= 2]
        figure_elements_to_change = random.choice(changes_2_or_1)
        figure_element_to_change = random.choice(figure_elements_to_change)
        for idx, figure in enumerate(list_of_changes):
            if figure == figure_elements_to_change:
                for name, _ in figure:
                    if name == figure_element_to_change[0]:
                        self.figures_list[idx].change_parameter(name)
                        break
                break

        self.name = "D5"
