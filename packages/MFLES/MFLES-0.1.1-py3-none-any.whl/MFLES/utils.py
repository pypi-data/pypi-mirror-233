import numpy as np
from numba import jit, njit, vectorize

def cap_outliers(series, outlier_cap=3):
    mean = np.mean(series)
    std = np.std(series)
    series = series.clip(min=mean - outlier_cap * std,
                         max=mean + outlier_cap * std)
    return series

@njit
def set_fourier(period):
    if period < 10:
        fourier = 5
    elif period < 70:
        fourier = 10
    else:
        fourier = 15
    return fourier

@njit
def calc_trend_strength(resids, deseasonalized):
    return max(0, 1-(np.var(resids)/np.var(deseasonalized)))

@njit
def calc_seas_strength(resids, detrended):
    return max(0, 1-(np.var(resids)/np.var(detrended)))

@njit
def calc_rsq(y, fitted):
    try:
        mean_y = np.mean(y)
        ssres = 0
        sstot = 0
        for vals in zip(y, fitted):
            sstot += (vals[0] - mean_y) ** 2
            ssres += (vals[0] - vals[1]) ** 2
        return 1 - (ssres / sstot)
    except:
        return 0

@njit
def calc_cov(y, mult=1):
    if mult:
        # source http://medcraveonline.com/MOJPB/MOJPB-06-00200.pdf
        return np.sqrt(np.exp(np.log(10)*(np.std(y)**2) - 1))
    else:
        return np.std(y) / np.mean(y)


@njit
def fastsin(x):
    return np.sin(2* np.pi * x)


@njit
def fastcos(x):
    return np.cos(2 * np.pi * x)

@njit
def calc_mse(actual, fitted):
    mse = np.zeros(len(actual))
    for i, val in enumerate(zip(actual, fitted)):
        mse[i] = (val[0] - val[1])**2
    return np.mean(mse)

@njit
def calc_mae(actual, fitted):
    mae = np.zeros(len(actual))
    for i, val in enumerate(zip(actual, fitted)):
        mae[i] = np.abs(val[0] - val[1])
    return np.mean(mae)

@njit
def calc_mape(actual, fitted):
    mape = np.zeros(len(actual))
    for i, val in enumerate(zip(actual, fitted)):
        mape[i] = np.abs(val[0] - val[1]) / val[0]
    return np.mean(mape)

@njit
def calc_smape(actual, fitted):
    smape = np.zeros(len(actual))
    for i, val in enumerate(zip(actual, fitted)):
        smape[i] = np.abs(val[0] - val[1]) / (np.abs(val[0] + val[1]) / 2)
    return np.mean(smape)


def cross_validation(y, test_size, n_splits, model_obj, **kwargs):
    mses = []
    maes = []
    mapes = []
    smapes = []
    residuals = []
    for split in range(1, 1+ n_splits):
        train_y = y[:(-split) * test_size]
        test_y = y[len(train_y): len(train_y) + test_size]
        model_obj.fit(train_y, **kwargs)
        prediction = model_obj.predict(test_size)
        mses.append(calc_mse(test_y, prediction))
        maes.append(calc_mae(test_y, prediction))
        mapes.append(calc_mape(test_y, prediction))
        smapes.append(calc_smape(test_y, prediction))
        # mases.append(calc_mase(test_y, prediction, train_y, kwargs['seasonal_period']))
        residuals.append(test_y - prediction)
    return {'mses': mses,
            'maes': maes,
            'mapes': mapes,
            'smapes': smapes,
            # 'mases': mases,
            'residuals': residuals}

