from sklearn.impute import KNNImputer
import random
import copy
import pandas as pd
import torch

def augment(D_0):
    """
    Augments the input data by imputing missing values using K-nearest neighbors.

    Parameters:
    D_0 (numpy.ndarray): The input data with missing values.

    Returns:
    pd.DataFrame: A DataFrame with missing values imputed using K-nearest neighbors.
    """
    imputer = KNNImputer(n_neighbors=5)
    df = copy.deepcopy(D_0)
    df = pd.DataFrame(df)
    imputer.fit(df)
    D_A = imputer.transform(df)
    D_A = pd.DataFrame(D_A)
    return D_A

def mask(D_0, missing_type, missing_severity):
    """
    Creates a binary mask to simulate missing data in the input.

    Parameters:
    D_0 (numpy.ndarray): The input data.
    missing_type (str): The type of missing data ("MCAR" for Missing Completely At Random or "other").
    missing_severity (float): The severity of missing data as a probability or length.

    Returns:
    torch.Tensor: A binary mask with the same shape as D_0, where True indicates missing values.
    """
    m = D_0.shape[0]
    n = D_0.shape[1]
    if missing_type == "MCAR":
        corruption_mask = torch.FloatTensor(m, n).uniform_() > missing_severity
    else:
        length = missing_severity
        corruption_mask = torch.full((m, n), True)
        for i in range(int(m / 288)):
            for j in range(n):
                number = random.randint(288 * i + 1, 288 * (i + 1) - length - 1)
                corruption_mask[number:number+length, j] = False
    return corruption_mask

def corrupt(corruption_mask, D_A):
    """
    Applies the given binary mask to corrupt a DataFrame by setting missing values to -1.

    Parameters:
    corruption_mask (torch.Tensor): A binary mask where True indicates missing values.
    D_A (pd.DataFrame): The DataFrame to be corrupted.

    Returns:
    pd.DataFrame: The corrupted DataFrame with missing values set to -1.
    """
    mask = torch.tensor(corruption_mask.values)
    D_C = copy.deepcopy(D_A)
    D_C[mask.numpy() == False] = -1
    return D_C
