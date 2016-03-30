class Instruction:
    def __init__(self, file_path, instruction_type, time):
        self.file_path = file_path
        self.instruction_type = instruction_type
        self.time = time
        self.type = "instruction"

    def prepare(self):
        instruction_info = {
            "type": self.type,
            "time": self.time,
            "instruction_type": self.instruction_type,
            "path": self.file_path
        }
        return instruction_info
