from classes.parameters import Trial_type
from gooey import Gooey, GooeyParser
from openpyxl import Workbook

__author__ = 'Michal Ociepka'


def save_to_xlsx(tab, filename):
    verification = "=IF(OR(B{0} = \"instruction\",AND(OR(B{0} = \"experiment\",B{0} = \"training\"),OR(D{0} = 2, D{0} = 3, D{0} = 4),OR(E{0} = 0, E{0} = 1, E{0} = 2))),1,0)"
    global_verification = "=SUM(J2: J500)"

    wb = Workbook()

    # grab the active worksheet
    ws = wb.active
    # time, per, rel, feedb, wait, exp, tip, tip_time
    # Data can be assigned directly to cells
    ws.append(
        ['BLOCK_NUMBER', 'TYPE', 'SHOW_TIME', 'RELATIONS', 'FEEDB', 'WAIT_TIME', 'TIP', 'TIP_TIME', '', global_verification])

    for idx, trial in enumerate(tab):
        if trial[1] == "instruction":
            trial_with_verification = trial[0:3] + ['', '', ''] + [trial[-1]] + ['', ''] + [verification.format(idx + 2)]
        else:
            trial_with_verification = trial + ['', verification.format(idx + 2)]
        ws.append(trial_with_verification)

    # Save the file
    wb.save(filename + ".xlsx")


@Gooey(language='english',  # Translations configurable via json
       default_size=(650, 600),  # starting size of the GUI
       required_cols=1,  # number of columns in the "Required" section
       optional_cols=3,  # number of columns in the "Optional" section
       )
def generate_trials_gui():
    # General information
    parser = GooeyParser(description='Create_general_experiment')
    parser.add_argument('Number_of_blocks', default=1, action='store', type=int, help='Number')
    parser.add_argument('Number_of_training_trials_in_blocks', default=4, action='store', type=int, help='Number')
    parser.add_argument('Number_of_experiment_trials_in_blocks', default=4, action='store', type=int, help='Number')
    parser.add_argument('File_name', default='experiment', type=str, help='Name of file with not personalized data')
    parser.add_argument('EEG_connected', default='1', choices=['1', '0'], help='Choice')

    parser.add_argument('--Instruction', widget='FileChooser', help='Choose instruction file')
    parser.add_argument('--Instruction_show_time', default=5, action='store', type=int, help='Number')

    # Information about training
    parser.add_argument('--Training_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_relations', default='2', choices=['2', '3', '4'], help='Choose number of relations')
    parser.add_argument('--Training_feedback', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_wait', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_tip', widget='FileChooser', help='Choose tip file')
    parser.add_argument('--Training_tip_time', default=4, action='store', type=int, help='Number')

    # Information about experiment
    parser.add_argument('--Experiment_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_relations', default='2', choices=['2', '3', '4'],
                        help='Choose number of relations')
    parser.add_argument('--Experiment_feedback', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_wait', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_tip', widget='FileChooser', help='Choose tip file')
    parser.add_argument('--Experiment_tip_time', default=4, action='store', type=int, help='Number')

    args = parser.parse_args()
    experiment = []

    name = args.Instruction.split('/')[-1]

    for idx in range(args.Number_of_blocks):
        instruction = [idx+1, Trial_type.instruction.value, args.Instruction_show_time, name]
        experiment.append(instruction)

        for _ in range(args.Number_of_training_trials_in_blocks):
            trial = [idx+1, Trial_type.training.value, args.Training_time, int(args.Training_relations), args.Training_feedback,
                     args.Training_wait, args.Training_tip, args.Training_tip_time]
            experiment.append(trial)
        for _ in range(args.Number_of_experiment_trials_in_blocks):
            trial = [idx+1, Trial_type.experiment.value, args.Experiment_time, int(args.Experiment_relations),
                     args.Experiment_feedback,
                     args.Experiment_wait, args.Experiment_tip, args.Experiment_tip_time]
            experiment.append(trial)

    save_to_xlsx(experiment, args.File_name)


def main():
    generate_trials_gui()


if __name__ == '__main__':
    main()

