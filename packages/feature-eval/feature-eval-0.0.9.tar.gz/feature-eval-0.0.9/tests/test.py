import numpy as np  
from scipy.stats import entropy  
  
def mutual_info(x, y):  
    """  
    计算两个变量的互信息  
    """  
    px = np.histogram(x, bins=30, density=True)[0]  
    py = np.histogram(y.flatten(), bins=30, density=True)[0]  
    pxy = np.histogram2d(x, y.flatten(), bins=(30, 30), density=True)[0]  
    px_py = px.reshape(-1, 1) * py  
    nzs = pxy > 0  
    mi = np.sum(pxy[nzs] * np.log(pxy[nzs] / (px_py[nzs])))  
    return mi  
  
def mrmr(X, y, m):  
    """  
    使用mRMR算法选择特征  
    """  
    n_features = X.shape[1]  
    I = np.zeros((n_features, 1))  
    for i in range(n_features):  
        I[i] = mutual_info(X[:, i], y)  
    S = []  
    while len(S) < m:  
        max_idx = np.argmax(I)  
        S.append(max_idx)  
        I[:] -= I[max_idx] * mutual_info(X[:, max_idx], X[:, S])  
        I[max_idx] = 0  
    return S

# 生成随机数据  
np.random.seed(0)  
X = np.random.randn(100, 10)  
y = np.random.randint(0, 2, 100)  
  
# 使用mRMR算法选择3个特征  
S = mrmr(X, y, 3)  
print("Selected features:", S)