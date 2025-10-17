import numpy as np

def get_predicted_class(prediction_array):
    """
    Returns the index of the highest probability (predicted class) from a prediction array.
    """
    return int(np.argmax(prediction_array))