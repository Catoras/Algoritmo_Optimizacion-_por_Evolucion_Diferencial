class Quartic:
    MIN_VALUE = -1.28
    MAX_VALUE = 1.28
    def __init__(self):
        pass
    def fitness(self, vector):
        z = 0
        i = 1
        for dimension in range(len(vector)):
            z += (i) * ((vector[dimension])**4)
            i += 1
        return z
