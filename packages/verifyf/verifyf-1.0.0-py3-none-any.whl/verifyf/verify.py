from scipy.spatial.distance import cdist
import numpy as np

def distance_cal(embedding_check, know_embedding):
    distances = cdist(embedding_check, know_embedding, 'cosine')
    return distances

def verify(embedding_check, know_embedding, threshsold=0.5):
    distances = distance_cal([embedding_check], know_embedding)
    distances = np.array(distances)
    mask = distances < threshsold
    if True in mask:
        return "True"
    else:
        return "False"