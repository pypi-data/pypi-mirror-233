

PVplr-stGNN is a Python3 package developed by the SDLE Research Center at Case Western Reserve University in Cleveland OH. This repository contains the full source PVplr-stGNN package. The package contains the PV-stGAE for missingness data detection and imputation and PV-DynGNN for Photovolatics (PV) PLR estimation.

# Features
 -  Data Preparation for stGNN Training.
 	- Transform raw data files into the current formats used for stGNN training and inference
 -  stGNN for missing data imputation
	- Based on input adjancecy matrix (A) and node features (X)
 -  stGNN for long-term PV degradation (PLR) Estimation
 
#  Setup
1. Install it at bash
```bash
$ pip install PVplr-stGNN
```
2.	Import it in python
```python
from PVplr_stGNN.DataPreprocessing import *
from PVplr_stGNN.DataAugmentation import *
from PVplr_stGNN.Layers import *

``` 
#  Two examples
***Create the adjacency matrix based on the location file***
```python
location = pd.read_csv('.../location.csv',index_col=0)
A = adjacency_matrix(location, epsilon = 0.5)
``` 
***Output will be the adjacency matrix using epsilon = 0.5***

***Model Training***
```python
model = STConvAE(device, num_nodes, channels, num_layers, kernel_size, K, n_his, kernel_size_de, stride, padding, normalization = 'sym', bias = True)
``` 
***Output will be initialized stGAE model for imputation***

#  A demo of training and testing st-GAE imputation model
Google colab link: https://colab.research.google.com/drive/1tQkbJRXEEQJFE0z3HhHlyJ9LK6jtLmqp#scrollTo=hy0rm7D1tCyw

## Prerequisites
Our code is based on Python3 (>= 3.8). The major libraries are listed as follows:
* NumPy (>= 1.22.3)
* Pandas (>= 1.4.2)
* Torch (>= 1.10.0)
* PyG (PyTorch Geometric) (>= 2.0.4)
* Scikit-learn (>= 1.0.2)

Photovoltaic (PV) power stations have become an integral component to a sustainable energy pro-
duction landscape. Accurately estimating and predicting performance of PV systems is critical to
their feasibility as a power generation technology and as a financial asset. Among the major domain
problems is to understand the PV Performance Loss Rate (PLR) for large fleets of PV systems.
The integration of the global PV market with real time data-loggers has enabled large scale PV
data analytical pipelines for power forecasting and long-term reliability assessment of PV fleets.
Nevertheless, such analysis heavily depends on the quality of PV data. One of the most challenging
problem in PV data quality is about how to impute missing data. 
We have developed two spatio-temporal graph-based deep learning techniques that address two major PV challenges: (1) missing PV data imputation, and (2) diversity of degradation patterns from PV data to support “end-to-end” long-term PV performance degradation analysis. Specifically, for (1) We propose a Spatio-Temporal Denoising Graph Autoencoder (STD-GAE) to impute missing PV Power Data. STD-GAE exploits temporal correlation, spatial coherence, and value dependencies from domain knowledge to recover missing data. For (2), we outline a novel Spatio-temporal Dynamic Graph Neural Network (st-DynGNN) that adopts a paralleled graph autoencoder architecture to extract different aging and fluctuation terms simultaneously. 

Yangxin Fan, Xuanji Yu, Raymond Wieser, David Meakin, Avishai Shaton, Jean-Nicolas
Jaubert, Robert Flottemesch, Michael Howell, Jennifer Braid, et al. Spatio-temporal denoising
graph autoencoders with data augmentation for photovoltaic data imputation. Proceedings of the ACM on Management of Data, 1(1):1–19, 2023.

William C Oltjen, Fan, Yangxin, Jiqi Liu, Liangyi Huang, Xuanji Yu, Mengjie Li, Hubert
Seigneur, Xusheng Xiao, Kristopher O Davis, Laura S Bruckman, et al. Fairification, quality
assessment, and missingness pattern discovery for spatiotemporal photovoltaic data. In 2022.
IEEE 49th Photovoltaics Specialists Conference (PVSC), pages 0796–0801. IEEE, 2022.

## License:
This work is legally bound by the following software license: BSD-3-Clause 1
Please see the LICENSE.txt file, in the root of this repository, for further details.

## Funding Acknowledgements:
This work is supported by the U.S. Department of Energy’s Office of Energy Efficiency and Renewable Energy (EERE) under Solar Energy Technologies Office (SETO) Agreement Number DE-EE0009353.

