# -*- coding: utf-8 -*-
from numba import jit, njit, vectorize
import numpy as np
from MFLES.utils import cap_outliers


@njit
def fsign(f):
    if f == 0:
        return 0
    elif f > 0:
        return 1.0
    else:
        return -1.0

@jit
def lasso_nb(X, y, alpha, tol=0.001, maxiter=10000):
    n, p = X.shape
    beta = np.zeros(p)
    R = y.copy()
    norm_cols_X = (X ** 2).sum(axis=0)
    resids = []
    prev_cost = 10e10
    for n_iter in range(maxiter):
        for ii in range(p):
            beta_ii = beta[ii]
            if beta_ii != 0.:
                R += X[:, ii] * beta_ii
            tmp = np.dot(X[:, ii], R)
            beta[ii] = fsign(tmp) * max(abs(tmp) - alpha, 0) / (.00001 + norm_cols_X[ii])
            if beta[ii] != 0.:
                R -= X[:, ii] * beta[ii]
        cost = (np.sum((y - X @ beta)**2) + alpha * np.sum(np.abs(beta))) / n
        resids.append(cost)
        if prev_cost - cost < tol:
            break
        else:
            prev_cost = cost
    return beta

# @jit
# def inv_rfft(f, c):
#     return np.fft.irfft(c * f)


# def linear_fourier(y, lamb, seasonal_period):
#     f = np.fft.rfft(y)
#     increment = .2
#     a = np.zeros(len(f))
#     for i in range(20 * lamb):
#         print(i)
#         round_mses = []
#         for coef in range(seasonal_period+1):
#             if a[coef] == 1:
#                 pass
#             else:
#                 c = a.copy()
#                 c[coef] = c[coef] + increment
#                 pred = inv_rfft(f, c)
#                 round_mses.append(np.mean((y[-len(pred):] - pred)**2))
#         idx = np.argmin(round_mses)
#         a[idx] = a[idx] + increment
#         pred = inv_rfft(f, a)
#         if not i % (5 * lamb):
#             increment /= 2
#     return np.fft.irfft(a * f)

@vectorize
def calc_slope(x1,y1,x2,y2):
    xd = x2-x1
    if xd == 0:
        slope = 0
    else:
        slope = (y2-y1) / (xd)
    return slope

@njit
def siegel_repeated_medians(x,y):
    # Siegel repeated medians regression
    n_total = x.size
    slopes = np.empty((n_total), dtype=y.dtype)
    ints = np.empty((n_total), dtype=y.dtype)
    slopes_sub = np.empty((n_total-1), dtype=y.dtype)
    for i in range(n_total):
        for j in range(n_total):            
            if i == j:
                continue
            slopes_sub[j] = calc_slope(x[i],y[i],x[j],y[j])
        slopes[i] = np.median(slopes_sub)
        ints[i] = y[i] - slopes[i]*x[i]
    trend = x * np.median(slopes) + np.median(ints)
    return trend

# @njit
# def get_smoother(resids, seasonal_period):
#     if seasonal_period is None:
#         len_check = int(.05 * len(resids))
#     else:
#         len_check = max(6, int(seasonal_period / 2))
#     mean_last = np.mean(resids[-len_check:-1])
#     mean_second_last = np.mean(resids[-len_check:-2])
#     std_last = np.std(resids[-len_check:-1])
#     std_second_last = np.std(resids[-len_check:-2])
#     smoother = 0
#     if resids[-1] > mean_last + 3 * std_last:
#         smoother = 1
#         resids = np.clip(resids,
#                          a_max=max(resids),
#                          a_min=mean_last - 2 * std_last)
#     if resids[-1] < mean_last - 3 * std_last:
#         smoother = 1
#         resids = np.clip(resids,
#                          a_max=mean_last + 2 * std_last,
#                          a_min=min(resids))
#     if resids[-2] > mean_second_last + 3 * std_second_last:
#         smoother = 1
#         resids = np.clip(resids,
#                          a_max=max(resids),
#                          a_min=mean_second_last - 2 * std_second_last)

#     if resids[-2] < mean_second_last - 3 * std_second_last:
#         smoother = 1
#         resids = np.clip(resids,
#                          a_max=mean_second_last + 2 * std_second_last,
#                          a_min=min(resids))
#     return smoother, resids

@njit
def ses(y, alpha):
    results = np.zeros(len(y))
    results[0] = y[0]
    for i in range(1, len(y)):
        results[i] = alpha * y[i] + (1 - alpha) * results[i - 1]
    return results

@njit
def ses_ensemble(y, min_alpha=.05, max_alpha=1, smooth=0, order=1):
    results = np.zeros(len(y))
    iters = np.arange(min_alpha, max_alpha, .05)
    if smooth:
        for alpha in iters:
            results += ses(y, alpha)
        results = results / len(iters)
    else:
        results[:order] = y[:order] #* len(iters)
        for i in range(1 + order, len(y)):
            # results[i] += alpha * y[i] + (1 - alpha) * y[i-1]
            results[i] += np.sum(y[i-order:i+1])/(order+1)

    return results #/ len(iters)

@njit
def fast_ols(x, y):
    """Simple OLS for two data sets."""
    M = x.size

    x_sum = 0.
    y_sum = 0.
    x_sq_sum = 0.
    x_y_sum = 0.

    for i in range(M):
        x_sum += x[i]
        y_sum += y[i]
        x_sq_sum += x[i] ** 2
        x_y_sum += x[i] * y[i]

    slope = (M * x_y_sum - x_sum * y_sum) / (M * x_sq_sum - x_sum**2)
    intercept = (y_sum - slope * x_sum) / M

    return slope * x + intercept

@njit
def median(y, seasonal_period):
    n = len(y)
    # return np.median(y) * np.ones(n)
    if seasonal_period is None:
        return np.median(y) * np.ones(n)
    else:
        medians = np.zeros(n)
        for i in range(int(n / seasonal_period)):
            left = i * seasonal_period
            right = (1 + i) * seasonal_period
            medians[left: right] = np.median(y[left: right])
        remainder = n % seasonal_period
        if remainder:
            medians[right:] = np.median(y[left + remainder: ])
        return medians

@jit
def ols(X, y):
    coefs = np.linalg.pinv(X.T.dot(X)).dot(X.T.dot(y))
    return  np.sum(coefs * X, axis=1)

@jit
def ridge(X, y, lam):
    eye = np.eye(X.shape[1])
    coefs = np.linalg.pinv(X.T.dot(X) + eye@lam).dot(X.T.dot(y))
    return  np.sum(coefs * X, axis=1)






