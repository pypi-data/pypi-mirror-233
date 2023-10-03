# load model with lowest validation lost
from math import sqrt
# from models.layers import *
import numpy as np
import os
import pandas as pd
import scipy.sparse as sp
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm
import math
from torch_geometric.nn import ChebConv

def model_test(test_iter, device, args, model_saved_path):
    """
    Test a Spatio-Temporal Convolutional Autoencoder (STConvAE) model on a given test dataset.

    Args:
        test_iter (iterable): An iterable providing test data batches.
        device (torch.device): The device on which to perform testing (e.g., 'cuda' or 'cpu').
        args (argparse.Namespace): Command-line arguments containing model parameters.
        model_saved_path (str): Path to the saved model checkpoint.

    Returns:
        torch.Tensor: Complete predictions made by the model on the test data.
    """

    best_model = STConvAE(device, num_nodes, channels, num_layers, kernel_size, K, n_his, kernel_size_de, stride, padding, normalization = 'sym', bias = True).to(device)
    best_model.load_state_dict(torch.load(model_save_path))

    best_model.eval()
    cost = 0
    missing_count = 0
    predicted = []
    ground_truth = []

    i = 1

    for x, y in tqdm(test_iter, desc = 'Batch', position = 0):
        # get model predictions and compute loss
        y_pred = best_model(x.to(device), edge_index, edge_weight)
        if i == 1:
            y_pred_complete = y_pred
        else:
            y_pred_complete = torch.cat((y_pred_complete, y_pred), 0)
        i+=1

    print(y_pred_complete.shape)
    return y_pred_complete


def test_error(y_pred_complete, y_test, x_test):
    """
    Calculate and print the test error metrics (RMSE and MAE) of a Spatio-Temporal Graph Convolutional Autoencoder (STGCN-DAE).

    Args:
        y_pred_complete (torch.Tensor): Complete predictions made by the model on the test data.
        y_test (torch.Tensor): Ground truth values for the test data.
        x_test (torch.Tensor): Mask indicating missing values in the test data.
    """

    pred = y_pred_complete[x_test.cpu().numpy()==-1]
    ground_truth = y_test[x_test.cpu().numpy()==-1]
    print("Test RMSE of STGCN-DAE is: "+ str(sqrt(torch.mean((pred-ground_truth)**2))))
    print("Test MAE is of STGCN-DAE is: "+ str(torch.mean(abs(pred-ground_truth))))