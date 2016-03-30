import yaml


class Experiment:
    def __init__(self, list_of_blocks, id, sex, age):
        self.name = str(id) + sex + str(age)
        self.list_of_blocks = list_of_blocks

    def prepare(self):
        elements_list = []
        for element in self.list_of_blocks:
            elements_list.append(element.prepare())
        info = {
            "name": self.name,
            "list_of_blocks": elements_list
        }
        return info

    def randomize(self):
        for block in self.list_of_blocks:
            block.randomize_block()

    def save(self):
        info = self.prepare()
        with open(self.name + ".yaml", 'w') as save_file:
            save_file.write(yaml.dump(info))
