import math

class Rastrigin:
    MIN_VALUE = -5.12
    MAX_VALUE = 5.12
    def __init__(self):
        pass
    def fitness(self, vector):
        z = 0
        for dimension in range(len(vector)):
            z += ((vector[dimension])**2)-(10 * (math.cos((2*(math.pi)*vector[dimension]))))
        return (10 * len(vector)) + z
