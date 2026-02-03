import math

def norm_vector(vector):
    mag = math.sqrt(vector[0]**2 + vector[1]**2)
    if mag == 0:
        return [0.0, 0.0]
    return [vector[0]/mag, vector[1]/mag]

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
