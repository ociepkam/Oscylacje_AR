import yaml


class Instruction:
    def __init__(self, file_path, instruction_type, time):
        with open(file_path, 'r') as instruction_file:
            self.instruction = yaml.load(instruction_file)
        self.instruction_type = instruction_type
        self.time = time
        self.type = "instruction"

    def prepare(self):
        instruction_info = {
            "type": self.type,
            "time": self.time,
            "instruction_type": self.instruction_type,
            "path": self.instruction
        }
        return instruction_info
