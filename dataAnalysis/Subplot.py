import matplotlib.pyplot as plt

class Subplot:
    def __init__(self, rows, columns):
        self.plt = plt
        self.rows = rows
        self.columns = columns
        self.index = 1

    def get_index(self):
        return self.index

    def increase_index(self):
        self.index += 1
