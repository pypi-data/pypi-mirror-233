import numpy as np
from scipy.stats import norm, binom
from scipy.special import expit
from scipy.optimize import brentq
from statsmodels.regression.linear_model import OLS, WLS
from statsmodels.stats.weightstats import _zconfint_generic, _zstat_generic
from sklearn.linear_model import LogisticRegression
from .utils import (
    dataframe_decorator,
    linfty_dkw,
    linfty_binom,
    form_discrete_distribution,
)
import pdb


def _rectified_mean(rectifier, imputed_mean):
    """Computes a rectified mean.

    Rectified mean is the sum of the rectifier and the imputed mean.

    Args:
        rectifier (float or ndarray): Rectifier value.
        imputed_mean (float or ndarray): Imputed mean.

    Returns:
        float or ndarray: Rectified mean.

    """
    return imputed_mean + rectifier


def _rectified_ci(
    rectifier,
    rectifier_std,
    imputed_mean,
    imputed_std,
    alpha,
    alternative="two-sided",
):
    """Computes a rectified confidence interval.

    Args:
        rectifier (float or ndarray): Rectifier value.
        rectifier_std (float or ndarray): Rectifier standard deviation.
        imputed_mean (float or ndarray): Imputed mean.
        imputed_std (float or ndarray): Imputed standard deviation.
        alpha (float): Error level; the confidence interval will target a coverage of 1 - alpha. Must be in (0, 1).
        alternative (str): Alternative hypothesis, either 'two-sided', 'larger' or 'smaller'.

    Returns:
        tuple: Lower and upper bounds of the confidence interval.
    """
    rectified_point_estimate = imputed_mean + rectifier
    rectified_std = np.sqrt(imputed_std**2 + rectifier_std**2)
    return _zconfint_generic(
        rectified_point_estimate, rectified_std, alpha, alternative
    )


def _rectified_p_value(
    rectifier,
    rectifier_std,
    imputed_mean,
    imputed_std,
    null=0,
    alternative="two-sided",
):
    """Computes a rectified p-value.

    Args:
        rectifier (float or ndarray): Rectifier value.
        rectifier_std (float or ndarray): Rectifier standard deviation.
        imputed_mean (float or ndarray): Imputed mean.
        imputed_std (float or ndarray): Imputed standard deviation.
        null (float): Value of the null hypothesis to be tested.
        alternative (str): Alternative hypothesis, either 'two-sided', 'larger' or 'smaller'.

    Returns:
        float or ndarray: P-value.
    """
    rectified_point_estimate = imputed_mean + rectifier
    rectified_std = np.maximum(
        np.sqrt(imputed_std**2 + rectifier_std**2), 1e-16
    )
    return _zstat_generic(
        rectified_point_estimate, 0, rectified_std, alternative, null
    )[1]


"""
    MEAN ESTIMATION

"""


def ppi_mean_pointestimate(Y, Yhat, Yhat_unlabeled):
    """Computes the prediction-powered point estimate of the mean.

    Args:
        Y (ndarray): Gold-standard labels.
        Yhat (ndarray): Predictions corresponding to the gold-standard labels.
        Yhat_unlabeled (ndarray): Predictions corresponding to the unlabeled data.

    Returns:
        float or ndarray: Prediction-powered point estimate of the mean.
    """
    return _rectified_mean((Y - Yhat).mean(), Yhat_unlabeled.mean())


def ppi_mean_ci(Y, Yhat, Yhat_unlabeled, alpha=0.1, alternative="two-sided"):
    """Computes the prediction-powered confidence interval for the mean.

    Args:
        Y (ndarray): Gold-standard labels.
        Yhat (ndarray): Predictions corresponding to the gold-standard labels.
        Yhat_unlabeled (ndarray): Predictions corresponding to the unlabeled data.
        alpha (float): Error level; the confidence interval will target a coverage of 1 - alpha. Must be in (0, 1).
        alternative (str): Alternative hypothesis, either 'two-sided', 'larger' or 'smaller'.

    Returns:
        tuple: Lower and upper bounds of the prediction-powered confidence interval for the mean.
    """
    n = Y.shape[0]
    N = Yhat_unlabeled.shape[0]
    return _rectified_ci(
        (Y - Yhat).mean(),
        (Y - Yhat).std() / np.sqrt(n),
        Yhat_unlabeled.mean(),
        Yhat_unlabeled.std() / np.sqrt(N),
        alpha,
        alternative,
    )


def ppi_mean_pval(Y, Yhat, Yhat_unlabeled, null=0, alternative="two-sided"):
    """Computes the prediction-powered p-value for the mean.

    Args:
        Y (ndarray): Gold-standard labels.
        Yhat (ndarray): Predictions corresponding to the gold-standard labels.
        Yhat_unlabeled (ndarray): Predictions corresponding to the unlabeled data.
        null (float): Value of the null hypothesis to be tested.
        alternative (str): Alternative hypothesis, either 'two-sided', 'larger' or 'smaller'.

    Returns:
        float or ndarray: Prediction-powered p-value for the mean.
    """
    n = Y.shape[0]
    N = Yhat_unlabeled.shape[0]
    return _rectified_p_value(
        (Y - Yhat).mean(),
        (Y - Yhat).std() / np.sqrt(n),
        Yhat_unlabeled.mean(),
        Yhat_unlabeled.std() / np.sqrt(N),
        null,
        alternative,
    )


"""
    QUANTILE ESTIMATION

"""


def _compute_cdf(Y, grid):
    """Computes the empirical CDF of the data.

    Args:
        Y (ndarray): Data.
        grid (ndarray): Grid of values to compute the CDF at.

    Returns:
        tuple: Empirical CDF and its standard deviation at the specified grid points.
    """
    indicators = (Y[:, None] <= grid[None, :]).astype(float)
    return indicators.mean(axis=0), indicators.std(axis=0)


def _compute_cdf_diff(Y, Yhat, grid):
    """Computes the difference between the empirical CDFs of the data and the predictions.

    Args:
        Y (ndarray): Data.
        Yhat (ndarray): Predictions.
        grid (ndarray): Grid of values to compute the CDF at.

    Returns:
        tuple: Difference between the empirical CDFs of the data and the predictions and its standard deviation at the specified grid points.
    """
    indicators_Y = (Y[:, None] <= grid[None, :]).astype(float)
    indicators_Yhat = (Yhat[:, None] <= grid[None, :]).astype(float)
    return (indicators_Y - indicators_Yhat).mean(axis=0), (
        indicators_Y - indicators_Yhat
    ).std(axis=0)


def _rectified_cdf(Y, Yhat, Yhat_unlabeled, grid):
    """Computes the rectified CDF of the data.

    Args:
        Y (ndarray): Gold-standard labels.
        Yhat (ndarray): Predictions corresponding to the gold-standard labels.
        Yhat_unlabeled (ndarray): Predictions corresponding to the unlabeled data.
        grid (ndarray): Grid of values to compute the CDF at.

    Returns:
        ndarray: Rectified CDF of the data at the specified grid points.
    """
    cdf_Yhat_unlabeled, _ = _compute_cdf(Yhat_unlabeled, grid)
    cdf_rectifier, _ = _compute_cdf_diff(Y, Yhat, grid)
    return cdf_Yhat_unlabeled + cdf_rectifier


def ppi_quantile_pointestimate(Y, Yhat, Yhat_unlabeled, q, exact_grid=False):
    """Computes the prediction-powered point estimate of the quantile.

    Args:
        Y (ndarray): Gold-standard labels.
        Yhat (ndarray): Predictions corresponding to the gold-standard labels.
        Yhat_unlabeled (ndarray): Predictions corresponding to the unlabeled data.
        q (float): Quantile to estimate.
        exact_grid (bool): Whether to compute the exact solution (True) or an approximate solution based on a linearly spaced grid of 5000 values (False).

    Returns:
        float: Prediction-powered point estimate of the quantile.
    """
    assert len(Y.shape) == 1
    grid = np.concatenate([Y, Yhat, Yhat_unlabeled], axis=0)
    if exact_grid:
        grid = np.sort(grid)
    else:
        grid = np.linspace(grid.min(), grid.max(), 5000)
    rectified_cdf = _rectified_cdf(Y, Yhat, Yhat_unlabeled, grid)
    minimizers = np.argmin(np.abs(rectified_cdf - q))
    minimizer = (
        minimizers
        if isinstance(minimizers, (int, np.int64))
        else minimizers[0]
    )
    return grid[
        minimizer
    ]  # Find the intersection of the rectified CDF and the quantile


def ppi_quantile_ci(Y, Yhat, Yhat_unlabeled, q, alpha=0.1, exact_grid=False):
    """Computes the prediction-powered confidence interval for the quantile.

    Args:
        Y (ndarray): Gold-standard labels.
        Yhat (ndarray): Predictions corresponding to the gold-standard labels.
        Yhat_unlabeled (ndarray): Predictions corresponding to the unlabeled data.
        q (float): Quantile to estimate. Must be in the range (0, 1).
        alpha (float): Error level; the confidence interval will target a coverage of 1 - alpha. Must be in the range (0, 1).
        exact_grid (bool): Whether to use the exact grid of values or a linearly spaced grid of 5000 values.

    Returns:
        tuple: Lower and upper bounds of the prediction-powered confidence interval for the quantile.
    """
    n = Y.shape[0]
    N = Yhat_unlabeled.shape[0]
    grid = np.concatenate([Y, Yhat, Yhat_unlabeled], axis=0)
    if exact_grid:
        grid = np.sort(grid)
    else:
        grid = np.linspace(grid.min(), grid.max(), 5000)
    cdf_Yhat_unlabeled, cdf_Yhat_unlabeled_std = _compute_cdf(
        Yhat_unlabeled, grid
    )
    cdf_rectifier, cdf_rectifier_std = _compute_cdf_diff(Y, Yhat, grid)
    # Calculate rectified p-value for null that the rectified cdf is equal to q
    rectified_p_value = _rectified_p_value(
        cdf_rectifier,
        cdf_rectifier_std / np.sqrt(n),
        cdf_Yhat_unlabeled,
        cdf_Yhat_unlabeled_std / np.sqrt(N),
        null=q,
        alternative="two-sided",
    )
    # Return the min and max values of the grid where p > alpha
    return grid[rectified_p_value > alpha][[0, -1]]


"""
    ORDINARY LEAST SQUARES

"""


def _ols(X, Y, return_se=False):
    """Computes the ordinary least squares coefficients.

    Args:
        X (ndarray): Covariates.
        Y (ndarray): Labels.
        return_se (bool): Whether to return the standard errors of the coefficients.

    Returns:
        theta (ndarray): Ordinary least squares estimate of the coefficients.
        se (ndarray): If return_se==True, return the standard errors of the coefficients.
    """
    regression = OLS(Y, exog=X).fit()
    theta = regression.params
    if return_se:
        return theta, regression.HC0_se
    else:
        return theta


def ppi_ols_pointestimate(X, Y, Yhat, X_unlabeled, Yhat_unlabeled):
    """Computes the prediction-powered point estimate of the OLS coefficients.

    Args:
        X (ndarray): Covariates corresponding to the gold-standard labels.
        Y (ndarray): Gold-standard labels.
        Yhat (ndarray): Predictions corresponding to the gold-standard labels.
        X_unlabeled (ndarray): Covariates corresponding to the unlabeled data.
        Yhat_unlabeled (ndarray): Predictions corresponding to the unlabeled data.

    Returns:
        theta_pp (ndarray): Prediction-powered point estimate of the OLS coefficients.
    """
    imputed_theta = _ols(X_unlabeled, Yhat_unlabeled)
    rectifier = _ols(X, Y - Yhat)
    theta_pp = imputed_theta + rectifier
    return theta_pp


def ppi_ols_ci(X, Y, Yhat, X_unlabeled, Yhat_unlabeled, alpha=0.1):
    """Computes the prediction-powered confidence interval for the OLS coefficients.

    Args:
        X (ndarray): Covariates corresponding to the gold-standard labels.
        Y (ndarray): Gold-standard labels.
        Yhat (ndarray): Predictions corresponding to the gold-standard labels.
        X_unlabeled (ndarray): Covariates corresponding to the unlabeled data.
        Yhat_unlabeled (ndarray): Predictions corresponding to the unlabeled data.
        alpha (float): Error level; the confidence interval will target a coverage of 1 - alpha. Must be in the range (0, 1).

    Returns:
        tuple: Lower and upper bounds of the prediction-powered confidence interval for the OLS coefficients.
    """
    n = Y.shape[0]
    N = Yhat_unlabeled.shape[0]
    imputed_theta, imputed_se = _ols(
        X_unlabeled, Yhat_unlabeled, return_se=True
    )
    rectifier, rectifier_se = _ols(X, Y - Yhat, return_se=True)
    return _rectified_ci(
        imputed_theta,
        imputed_se,
        rectifier,
        rectifier_se,
        alpha,
        alternative="two-sided",
    )


"""
    LOGISTIC REGRESSION

"""


# Todo: Numba accel
def ppi_logistic_pointestimate(
    X, Y, Yhat, X_unlabeled, Yhat_unlabeled, step_size=1e-3, grad_tol=5e-16
):
    """Computes the prediction-powered point estimate of the logistic regression coefficients.

    Args:
        X (ndarray): Covariates corresponding to the gold-standard labels.
        Y (ndarray): Gold-standard labels.
        Yhat (ndarray): Predictions corresponding to the gold-standard labels.
        X_unlabeled (ndarray): Covariates corresponding to the unlabeled data.
        Yhat_unlabeled (ndarray): Predictions corresponding to the unlabeled data.

    Returns:
        theta_pp (ndarray): Prediction-powered point estimate of the logistic regression coefficients.
    """
    n = Y.shape[0]
    d = X.shape[1]
    N = Yhat_unlabeled.shape[0]
    rectifier = 1 / n * X.T @ (Yhat - Y)
    theta = (
        LogisticRegression(
            penalty="none",
            solver="lbfgs",
            max_iter=10000,
            tol=1e-15,
            fit_intercept=False,
        )
        .fit(X, Y)
        .coef_.squeeze()
    )
    mu_theta = expit(X_unlabeled @ theta)
    grad = grad_tol * np.ones(d) + 1  # Initialize to enter while loop
    while np.linalg.norm(grad) > grad_tol:
        mu_theta = expit(X_unlabeled @ theta)
        grad = 1 / N * X_unlabeled.T @ (mu_theta - Yhat_unlabeled) + rectifier
        theta -= step_size * grad
    return theta

def ppi_logistic_ci(
    X,
    Y,
    Yhat,
    X_unlabeled,
    Yhat_unlabeled,
    alpha=0.1,
    step_size=1e-3,  # Optimizer step size
    grad_tol=5e-16,  # Optimizer grad tol
    alternative='two-sided'
):
    """Computes the prediction-powered confidence interval for the logistic regression coefficients.

    Args:
        X (ndarray): Covariates corresponding to the gold-standard labels.
        Y (ndarray): Gold-standard labels.
        Yhat (ndarray): Predictions corresponding to the gold-standard labels.
        X_unlabeled (ndarray): Covariates corresponding to the unlabeled data.
        Yhat_unlabeled (ndarray): Predictions corresponding to the unlabeled data.
        alpha (float): Error level; the confidence interval will target a coverage of 1 - alpha. Must be in the range (0, 1).
        step_size (float): Step size to use in the optimizer.
        grad_tol (float): Gradient tolerance to use in the optimizer.
        alternative (str): Alternative hypothesis, either 'two-sided', 'larger' or 'smaller'.

    Returns:
        tuple: Lower and upper bounds of the prediction-powered confidence interval for the logistic regression coefficients.
    """
    n = Y.shape[0]
    d = X.shape[1]
    N = Yhat_unlabeled.shape[0]

    ppi_pointest = ppi_logistic_pointestimate(
        X,
        Y,
        Yhat,
        X_unlabeled,
        Yhat_unlabeled,
        step_size=step_size,
        grad_tol=grad_tol,
    )

    mu_til = expit(X_unlabeled@ppi_pointest)

    Hessian = np.zeros((d,d))
    grads_til = np.zeros(X_unlabeled.shape)
    for i in range(N):
        Hessian += 1/N * mu_til[i] * (1-mu_til[i]) * np.outer(X_unlabeled[i], X_unlabeled[i])
        grads_til[i,:] = X_unlabeled[i,:]*(mu_til[i] - Yhat_unlabeled[i])

    inv_Hessian = np.linalg.inv(Hessian)
    var_unlabeled = np.cov(grads_til.T)

    pred_error = Yhat - Y
    grad_diff = np.diag(pred_error) @ X
    var = np.cov(grad_diff.T)

    Sigma_hat = inv_Hessian @ (n/N * var_unlabeled + var) @ inv_Hessian

    return _zconfint_generic(ppi_pointest, np.sqrt(np.diag(Sigma_hat)/n), alpha=alpha, alternative=alternative)


"""
    ORDINARY LEAST SQUARES UNDER COVARIATE SHIFT

"""


def _wls(X, Y, w, return_se=False):
    """Computes the weighted least squares estimate of the coefficients.

    Args:
        X (ndarray): Covariates.
        Y (ndarray): Labels.
        w (ndarray): Weights.
        return_se (bool): Whether to return the standard errors.

    Returns:
        theta (ndarray): Weighted least squares estimate of the coefficients.
        se (ndarray): If return_se==True, returns the standard errors of the coefficients.
    """
    regression = WLS(Y, exog=X, weights=w).fit()
    theta = regression.params
    if return_se:
        return theta, regression.HC0_se
    else:
        return theta


def ppi_ols_covshift_pointestimate(X, Y, Yhat, X_unlabeled, Yhat_unlabeled, w):
    """Computes the prediction-powered point estimate for the ordinary least squares coefficients under covariate shift.

    Args:
        X (ndarray): Covariates corresponding to the gold-standard labels.
        Y (ndarray): Gold-standard labels.
        Yhat (ndarray): Predictions corresponding to the gold-standard labels.
        X_unlabeled (ndarray): Covariates corresponding to the unlabeled data.
        Yhat_unlabeled (ndarray): Predictions corresponding to the unlabeled data.

    Returns:
        theta_pp (ndarray): Prediction-powered point estimate for the ordinary least squares coefficients under covariate shift.
    """
    imputed_theta = _wls(X_unlabeled, Yhat_unlabeled)
    rectifier = _wls(X, Y - Yhat, w)
    theta_pp = imputed_theta + rectifier
    return theta_pp


def ppi_ols_covshift_ci(X, Y, Yhat, X_unlabeled, Yhat_unlabeled, w, alpha=0.1):
    """Computes the prediction-powered confidence interval for the ordinary least squares coefficients under covariate shift.

    Args:
        X (ndarray): Covariates corresponding to the gold-standard labels.
        Y (ndarray): Gold-standard labels.
        Yhat (ndarray): Predictions corresponding to the gold-standard labels.
        X_unlabeled (ndarray): Covariates corresponding to the unlabeled data.
        Yhat_unlabeled (ndarray): Predictions corresponding to the unlabeled data.
        w (ndarray): Weights.
        alpha (float): Significance level.

    Returns:
        tuple: Lower and upper bounds of the prediction-powered confidence interval for the ordinary least squares coefficients under covariate shift.
    """
    n = Y.shape[0]
    N = Yhat_unlabeled.shape[0]
    imputed_theta, imputed_se = _ols(
        X_unlabeled, Yhat_unlabeled, return_se=True
    )
    rectifier, rectifier_se = _wls(X, Y - Yhat, w, return_se=True)
    return _rectified_ci(
        imputed_theta,
        imputed_se,
        rectifier,
        rectifier_se,
        alpha,
        alternative="two-sided",
    )


"""
    DISCRETE DISTRIBUTION ESTIMATION UNDER LABEL SHIFT ʕ·ᴥ·ʔ

"""


def ppi_distribution_label_shift_ci(
    Y, Yhat, Yhat_unlabeled, K, nu, alpha, delta, return_counts=True
):
    """Computes the prediction-powered confidence interval for nu^T f for a discrete distribution f, under label shift.

    Args:
        Y (ndarray): Gold-standard labels.
        Yhat (ndarray): Predictions corresponding to the gold-standard labels.
        Yhat_unlabeled (ndarray): Predictions corresponding to the unlabeled data.
        K (int): Number of classes.
        nu (ndarray): Vector nu. Coordinates must be bounded within [0, 1].
        alpha (float): Final error level; the confidence interval will target a coverage of 1 - alpha. Must be in (0, 1).
        delta (float): Error level of the intermediate confidence interval for the mean. Must be in (0, 1). If return_counts == False, then delta is set equal to alpha and ignored.
        return_counts (bool): Whether to return the number of samples in each class as opposed to the mean.

    Returns:
        tuple: Lower and upper bounds of the prediction-powered confidence interval for nu^T f for a discrete distribution f, under label shift.
    """
    if not return_counts:
        delta = alpha
    # Construct the confusion matrix
    n = Y.shape[0]
    N = Yhat_unlabeled.shape[0]

    # Construct column-normalized confusion matrix Ahat
    C = np.zeros((K, K)).astype(int)
    for j in range(K):
        for l in range(K):
            C[j, l] = np.bitwise_and(Yhat == j, Y == l).astype(int).sum()
    Ahat = C / C.sum(axis=0)

    # Invert Ahat
    Ahatinv = np.linalg.inv(Ahat)
    qfhat = form_discrete_distribution(Yhat_unlabeled, sorted_highlow=True)

    # Calculate the bound
    point_estimate = nu @ Ahatinv @ qfhat

    nmin = C.sum(axis=0).min()

    def invert_budget_split(budget_split):
        return np.sqrt(1 / (4 * nmin)) * (
            norm.ppf(1 - (budget_split * delta) / (2 * K**2))
            - norm.ppf((budget_split * delta) / (2 * K**2))
        ) - np.sqrt(2 / N * np.log(2 / ((1 - budget_split) * delta)))

    try:
        budget_split = brentq(invert_budget_split, 1e-9, 1 - 1e-9)
    except:
        budget_split = 0.999999
    epsilon1 = max(
        [
            linfty_binom(C.sum(axis=0)[k], K, budget_split * delta, Ahat[:, k])
            for k in range(K)
        ]
    )
    epsilon2 = linfty_dkw(N, K, (1 - budget_split) * delta)

    qyhat_lb = np.clip(point_estimate - epsilon1 - epsilon2, 0, 1)
    qyhat_ub = np.clip(point_estimate + epsilon1 + epsilon2, 0, 1)

    if return_counts:
        count_lb = int(binom.ppf((alpha - delta) / 2, N, qyhat_lb))
        count_ub = int(binom.ppf(1 - (alpha - delta) / 2, N, qyhat_ub))
        return count_lb, count_ub
    else:
        return qyhat_lb, qyhat_ub
