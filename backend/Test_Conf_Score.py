import numpy as np


def calculate_score(class_probability, threshold = 0.5):
    m = None
    n = None
    if class_probability <= threshold:
        m = - 1 / threshold
        n = 1
    else:
        m = 1 / (1-threshold)
        n = - threshold * m
    confidence = m*class_probability+n
    return confidence

test = np.array([0.05, 0, 1, 0.13, 0.8])
print(calculate_score(test, 0.13))

