import copy
import random

from matrix import Matrix
from parameters import FIGURES, FRAME_CHANGES_PAIRS, BRIGHTNESS_CHANGES_PAIRS, ROTATION_CHANGES_PAIRS
from figure import Figure


class Trial:
    def __init__(self, time, per, rel, feedb, wait, exp, tip, tip_time):
        self.type = 'trial'
        self.time = time
        self.per = per
        self.rel = rel
        self.feedb = feedb
        self.wait = wait
        self.exp = exp
        self.figures_list_len = per[0] * per[1]
        self.figures = FIGURES
        random.shuffle(self.figures)
        self.list_of_changes = []
        self.tip = tip
        self.tip_time = tip_time

        self.matrix_list = None
        self.matrix_a = None
        self.matrix_b = None
        self.matrix_c = None
        self.matrix_d1 = None
        self.matrix_d2 = None
        self.matrix_d3 = None
        self.matrix_d4 = None
        self.matrix_d5 = None
        self.matrix_d6 = None

        self.create_all_matrix()

    def create_all_matrix(self):
        self.create_matrix_a()
        self.create_matrix_b()
        self.create_matrix_c()
        self.create_matrix_d6()
        self.create_matrix_d1()
        self.create_matrix_d2()
        self.create_matrix_d3()
        self.create_matrix_d4()
        self.create_matrix_d5()

        self.matrix_list = [self.matrix_d1, self.matrix_d2, self.matrix_d3,
                            self.matrix_d4, self.matrix_d5, self.matrix_d6]
        self.shuffle_all_matrix()

        random.shuffle(self.matrix_list)
        self.matrix_list = [self.matrix_a.return_figure_list(), self.matrix_b.return_figure_list(),
                            self.matrix_c.return_figure_list()] + [x.return_figure_list() for x in self.matrix_list]

    def shuffle_all_matrix(self):
        new_figures_positions = list(range(self.figures_list_len))
        for i in range(0, len(new_figures_positions)-1):
            pick = random.randint(i+1, len(new_figures_positions)-1)
            new_figures_positions[i], new_figures_positions[pick] = new_figures_positions[pick], new_figures_positions[i]
        for matrix in self.matrix_list:
            matrix.change_figures_positions(new_figures_positions)

    def create_matrix_a(self):
        matrix_frame_changes_pairs = copy.deepcopy(FRAME_CHANGES_PAIRS)
        matrix_brightness_changes_pairs = copy.deepcopy(BRIGHTNESS_CHANGES_PAIRS)
        matrix_rotation_changes_pairs = copy.deepcopy(ROTATION_CHANGES_PAIRS)
        figures_list = []
        for name in self.figures[:self.figures_list_len]:
            figure_frame = random.choice(matrix_frame_changes_pairs)
            matrix_frame_changes_pairs = [x for x in matrix_frame_changes_pairs if x[1] != figure_frame[1]]

            figure_brightness = random.choice(matrix_brightness_changes_pairs)
            matrix_brightness_changes_pairs = [x for x in matrix_brightness_changes_pairs if
                                               x[1] != figure_brightness[1]]

            figure_rotation = random.choice(matrix_rotation_changes_pairs)
            matrix_rotation_changes_pairs = [x for x in matrix_rotation_changes_pairs if x[1] != figure_rotation[1]]

            figures_list += [Figure([name, figure_rotation, figure_brightness, figure_frame])]

        self.figures = self.figures[self.figures_list_len:]
        self.matrix_a = Matrix(figures_list)
        self.matrix_a.name = "A"

    def create_matrix_b(self):
        self.matrix_b = copy.deepcopy(self.matrix_a)
        self.matrix_b.change_figures_b(self.rel)
        for figure in self.matrix_b.figures_list:
            self.list_of_changes.append(figure.elements_changed)
        self.matrix_b.shuffle_matrix()
        # random.shuffle(self.list_of_changes)
        self.matrix_b.name = "B"

    def create_matrix_c(self):
        matrix_frame_changes_pairs = copy.deepcopy(FRAME_CHANGES_PAIRS)
        matrix_brightness_changes_pairs = copy.deepcopy(BRIGHTNESS_CHANGES_PAIRS)
        matrix_rotation_changes_pairs = copy.deepcopy(ROTATION_CHANGES_PAIRS)
        figures_list_c = []
        for idx, name in enumerate(self.figures[:self.figures_list_len]):
            a_frame_possible_change = self.matrix_a.figures_list[idx].frame_possible_change
            figure_frame_changes_pairs = [x for x in matrix_frame_changes_pairs if x[1] == a_frame_possible_change]
            c_figure_frame = random.choice(figure_frame_changes_pairs)

            a_brightness_possible_change = self.matrix_a.figures_list[idx].brightness_possible_change
            figure_brightness_changes_pairs = [x for x in matrix_brightness_changes_pairs if
                                               x[1] == a_brightness_possible_change]
            c_figure_brightness = random.choice(figure_brightness_changes_pairs)

            a_rotation_possible_change = self.matrix_a.figures_list[idx].rotation_possible_change
            figure_rotation_changes_pairs = [x for x in matrix_rotation_changes_pairs if
                                             x[1] == a_rotation_possible_change]
            c_figure_rotation = random.choice(figure_rotation_changes_pairs)

            figures_list_c += [Figure([name, c_figure_rotation, c_figure_brightness, c_figure_frame])]

        self.figures = self.figures[self.figures_list_len:]
        self.matrix_c = Matrix(figures_list_c)
        self.matrix_c.name = "C"

    def create_matrix_d1(self):
        self.matrix_d1 = copy.deepcopy(self.matrix_d6)
        self.matrix_d1.change_figures_d1(self.list_of_changes)

    def create_matrix_d2(self):
        self.matrix_d2 = copy.deepcopy(self.matrix_d6)
        list_of_changes = copy.deepcopy(self.list_of_changes)
        self.matrix_d2.change_figures_d2(list_of_changes)

    def create_matrix_d3(self):
        self.matrix_d3 = copy.deepcopy(self.matrix_d6)
        list_of_changes = copy.deepcopy(self.list_of_changes)
        self.matrix_d3.change_figures_d3(list_of_changes)

    def create_matrix_d4(self):
        self.matrix_d4 = copy.deepcopy(self.matrix_d6)
        list_of_changes = copy.deepcopy(self.list_of_changes)
        self.matrix_d4.change_figures_d4(list_of_changes)

    def create_matrix_d5(self):
        self.matrix_d5 = copy.deepcopy(self.matrix_d6)
        list_of_changes = copy.deepcopy(self.list_of_changes)
        self.matrix_d5.change_figures_d5(list_of_changes)

    def create_matrix_d6(self):
        self.matrix_d6 = copy.deepcopy(self.matrix_c)
        self.matrix_d6.name = "D6"

    def prepare(self):
        trial_info = {
            "type": self.type,
            "time": self.time,
            # "per": self.per,
            "rel": self.rel,
            "feedb": self.feedb,
            "wait": self.wait,
            "exp": self.exp,
            "matrix_info": self.matrix_list,
            "tip": self.tip,
            "tip_time": self.tip_time
        }
        return trial_info
