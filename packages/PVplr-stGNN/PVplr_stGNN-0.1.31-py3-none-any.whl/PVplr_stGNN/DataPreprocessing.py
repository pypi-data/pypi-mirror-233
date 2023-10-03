import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
import os
import scipy.sparse as sp
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm
import math
from torch_geometric.nn import ChebConv

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)

    Parameters:
    lon1 (float): Longitude of the first point in decimal degrees.
    lat1 (float): Latitude of the first point in decimal degrees.
    lon2 (float): Longitude of the second point in decimal degrees.
    lat2 (float): Latitude of the second point in decimal degrees.

    Returns:
    float: The distance in kilometers between the two points.
    """

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def data_transform(data, corrupted_data, window, device):
    """
    Transform the data and corrupted_data into input and target tensors for training.

    Parameters:
    data (numpy.ndarray): The input data.
    corrupted_data (numpy.ndarray): The corrupted input data.
    window (int): The window size for data transformation.
    device: The PyTorch device to store the resulting tensors (e.g., 'cpu' or 'cuda').

    Returns:
    torch.Tensor: The transformed input data.
    torch.Tensor: The transformed target data.
    """

    num_nodes = data.shape[1]
    num_obs = int(len(data) / window)
    x = np.zeros([num_obs, window, num_nodes, 1])
    y = np.zeros([num_obs, window, num_nodes, 1])

    obs_idx = 0
    for i in range(num_obs):
        head = i * window
        tail = (i + 1) * window
        y[obs_idx, :, :, :] = data[head: tail].reshape(window, num_nodes, 1)
        x[obs_idx, :, :, :] = corrupted_data[head: tail].reshape(window, num_nodes, 1)
        # x[obs_idx, :, :, :] = data[head: tail].reshape(window, num_nodes, 1)
        obs_idx += 1

    return torch.Tensor(x).to(device), torch.Tensor(y).to(device)


def adjacency_matrix(location, epsilon):
    """
    Create an adjacency matrix based on geographical coordinates and a given epsilon threshold.

    Parameters:
    location (pd.DataFrame): A DataFrame containing geographical coordinates.
    epsilon (float): The threshold for determining the adjacency weight.

    Returns:
    pd.DataFrame: The adjacency matrix.
    """

    m = location.shape[0]
    distance = np.zeros(shape=(m,m))
    dist = []
    for i in range(m):
        for j in range(m):
            d = haversine(location.iloc[i][2], location.iloc[i][1], location.iloc[j][2], location.iloc[j][1])
            distance[i][j] = d
            dist.append(d)

    dist_std = np.std(dist)
    distance = pd.DataFrame(distance)

    # epsilon = 0, 0.25, 0.5, 0.75, 1
    sigma = dist_std
    W = np.zeros(shape=(m, m))

    for i in range(m):
        for j in range(m):
            if i == j:
                W[i][j] = 0
            else:
                # Compute distance between stations
                d_ij = distance.loc[i][j]

                # Compute weight w_ij
                w_ij = np.exp(-d_ij ** 2 / sigma ** 2)

                if w_ij >= epsilon:
                    W[i, j] = w_ij

    W = pd.DataFrame(W)
    return W