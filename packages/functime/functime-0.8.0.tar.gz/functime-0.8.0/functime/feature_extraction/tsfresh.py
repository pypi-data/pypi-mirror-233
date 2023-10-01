import math
from itertools import product
from typing import List, Mapping, Sequence, Union, Optional

import bottleneck as bn
import numpy as np
import polars as pl
from numpy.linalg import lstsq
from scipy.signal import find_peaks_cwt, ricker, welch
from scipy.spatial import KDTree
from polars.type_aliases import ClosedInterval

TIME_SERIES_T = Union[pl.Series, pl.Expr]
FLOAT_EXPR = Union[pl.Expr, float]
INT_EXPR = Union[pl.Expr, int]
LIST_EXPR = Union[pl.Expr, list]
BOOL_EXPR = Union[pl.Expr, bool]


def absolute_energy(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Compute the absolute energy of a time series.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float | Expr
    """
    return x.dot(x)


def absolute_maximum(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Compute the absolute maximum of a time series.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float | Expr
    """
    return x.abs().max()


def absolute_sum_of_changes(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Compute the absolute sum of changes of a time series.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float
    """
    return x.diff(n=1, null_behavior="drop").abs().sum()

def _phis(x: pl.Expr, m: int, N: int, rs: List[float]) -> List[float]:
    n = N - m + 1
    x_runs = [x.slice(i, m) for i in range(n)]
    max_dists = [(x_i - x_j).max() for x_i, x_j in product(x_runs, x_runs)]
    phis = []
    for r in rs:
        r_comparisons = [d.le(r) for d in max_dists]
        counts = [
            (pl.sum_horizontal(r_comparisons[i : i + n]) / n).log()
            for i in range(0, n**2, n)
        ]
        phis.append((1 / n) * pl.sum_horizontal(counts))
    return phis


def approximate_entropies(
    x: TIME_SERIES_T,
    filtering_levels: List[float],
    run_length: int = 2,
) -> List[float]:
    """
    Approximate sample entropies of a time series given multiple filtering levels.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    run_length : int, optional
        Length of compared run of data.
    filtering_levels : list of float, optional
        Filtering levels, must be positive

    Returns
    -------
    list of float
    """
    sigma = x.std()
    rs = [sigma * r for r in filtering_levels]
    N = x.count()
    phis_m = _phis(x, m=run_length, N=N, rs=rs)
    phis_m_plus_1 = _phis(x, m=run_length + 1, N=N, rs=rs)
    return [phis_m[i] - phis_m_plus_1[i] for i in range(len(phis_m))]


def augmented_dickey_fuller(x: pl.Series, n_lags: int) -> float:
    """
    Calculates the Augmented Dickey-Fuller (ADF) test statistic.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    n_lags : int
        The number of lags to include in the test.

    Returns
    -------
    float

    Notes
    -----
    The ADF test is a statistical test used to determine whether a time series is stationary or not.
    A stationary time series has constant statistical properties over time, such as constant mean and variance.

    References
    ----------
    1. Dickey, D. A., & Fuller, W. A. (1979). Distribution of the estimators for autoregressive time series with a unit root. Journal of the American statistical association, 74(366a), 427-431.
    2. MacKinnon, J. G. (1996). Numerical distribution functions for unit root and cointegration tests. Journal of applied econometrics, 11(6), 601-618.
    """

    x_diff = x.diff()
    k = x_diff.len()
    X = np.vstack(
        [
            x.slice(n_lags),
            np.asarray([x_diff.shift(i).slice(n_lags) for i in range(1, n_lags + 1)]),
            np.ones(k - n_lags),
        ]
    ).T
    y = x_diff.slice(n_lags).to_numpy(zero_copy_only=True)
    coeffs, resids, _, _ = lstsq(X, y, rcond=None)
    mse = bn.nansum(resids**2) / (k - X.shape[1])
    x_arr = np.asarray(x).T, np.asarray(x)
    cov = mse * np.linalg.inv(np.dot(x_arr.T, x))
    stderrs = np.sqrt(np.diag(cov))
    return coeffs[0] / stderrs[0]


def autocorrelation(x: TIME_SERIES_T, n_lags: int) -> FLOAT_EXPR:
    """
    Calculate the autocorrelation for a specified lag.

    The autocorrelation measures the linear dependence between a time-series and a lagged version of itself.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    n_lags : int
        The lag at which to calculate the autocorrelation. Must be a non-negative integer.

    Returns
    -------
    float | None | Expr
        Autocorrelation at the given lag. Returns None, if lag is less than 0.

    Notes
    -----
    - This function calculates the autocorrelation using https://en.wikipedia.org/wiki/Autocorrelation#Estimation
    - If `lag` is 0, the autocorrelation is always 1.0, as it represents the correlation of the timeseries with itself.
    """
    if n_lags < 0:
        return None

    if n_lags == 0:
        return pl.lit(1.0)

    return (
        x.shift(periods=-n_lags)
        .drop_nulls()
        .sub(x.mean())
        .dot(x.shift(periods=n_lags).drop_nulls().sub(x.mean()))
        .truediv((x.count() - n_lags).mul(x.var(ddof=0)))
    )


def autoregressive_coefficients(x: pl.Series, n_lags: int) -> List[float]:
    """
    Computes coefficients for an AR(`n_lags`) process.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    n_lags : int
        The number of lags in the autoregressive process.

    Returns
    -------
    list of float
    """
    X = np.vstack(
        [
            np.asarray([x.shift(i).slice(n_lags) for i in range(1, n_lags + 1)]),
            np.ones(x.len() - n_lags),
        ]
    ).T
    y = np.asarray(x.slice(n_lags))
    return lstsq(X, y, rcond=None)[0]


_BENFORD_DIST_SERIES = (1 + 1 / pl.int_range(1, 10, eager=True)).log10()


def benford_correlation(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Returns the correlation between the first digit distribution of the input time series and
    the Newcomb-Benford's Law distribution [1][2].

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float | Expr

    Notes
    -----
    The Newcomb-Benford distribution for d that is the leading digit of the number {1, 2, 3, 4, 5, 6, 7, 8, 9} is given by:

    .. math::

        P(d) = \\log_{10}\\left(1 + \\frac{1}{d}\\right)

    References
    ----------
    [1] Hill, T. P. (1995). A Statistical Derivation of the Significant-Digit Law. Statistical Science.
    [2] Hill, T. P. (1995). The significant-digit phenomenon. The American Mathematical Monthly.
    [3] Benford, F. (1938). The law of anomalous numbers. Proceedings of the American philosophical society.
    [4] Newcomb, S. (1881). Note on the frequency of use of the different digits in natural numbers. American Journal of
        mathematics.
    """
    y = x.cast(pl.Utf8).str.strip_chars_start("-0.")
    if isinstance(x, pl.Series):
        counts = (
            y.filter(y != "").str.slice(0, 1).cast(
                pl.UInt8
            ).append(pl.int_range(1, 10, eager=True, dtype=pl.UInt8))
            .value_counts()
            .sort(by=x.name)
            .get_column("counts")
        )
        return np.corrcoef(counts, _BENFORD_DIST_SERIES)[0,1]
    else:
        counts = y.filter(y != "").str.slice(0, 1).cast(
            pl.UInt8
        ).append(pl.int_range(1, 10, eager=False)).value_counts().sort().struct.field(
            "counts"
        ) - pl.lit(
            1, dtype = pl.UInt32
        )
        return pl.corr(counts, pl.lit(_BENFORD_DIST_SERIES))

def benford_correlation2(x: pl.Expr) -> pl.Expr:
    """
    Returns the correlation between the first digit distribution of the input time series and
    the Newcomb-Benford's Law distribution [1][2]. This version may hit some float point precision
    issues for some rare numbers.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    An expression for benford_correlation representing a float

    Notes
    -----
    The Newcomb-Benford distribution for d that is the leading digit of the number {1, 2, 3, 4, 5, 6, 7, 8, 9} is given by:

    .. math::

        P(d) = \\log_{10}\\left(1 + \\frac{1}{d}\\right)

    References
    ----------
    [1] Hill, T. P. (1995). A Statistical Derivation of the Significant-Digit Law. Statistical Science.
    [2] Hill, T. P. (1995). The significant-digit phenomenon. The American Mathematical Monthly.
    [3] Benford, F. (1938). The law of anomalous numbers. Proceedings of the American philosophical society.
    [4] Newcomb, S. (1881). Note on the frequency of use of the different digits in natural numbers. American Journal of
        mathematics.
    """
    counts = (
        # This part can be simplified once the log10(1000) precision issue is resolved.
        pl.when(x.abs() == 1000)
        .then(pl.lit(1))
        .otherwise(x.abs() / (pl.lit(10).pow((x.abs().log10()).floor())))
        .drop_nans()
        .drop_nulls()
        .cast(pl.UInt8)
        .append(pl.int_range(1, 10, eager=False))
        .value_counts()
        .sort()
        .struct.field("counts")
        - pl.lit(1)
    )
    return pl.corr(counts, pl.lit(_BENFORD_DIST_SERIES))


def binned_entropy(x: TIME_SERIES_T, bin_count: int = 10) -> FLOAT_EXPR:
    """
    Calculates the entropy of a binned histogram for a given time series.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    bin_count : int, optional
        The number of bins to use in the histogram. Default is 10.

    Returns
    -------
    float | Expr
    """
    if isinstance(x, pl.Series):
        hist, _ = np.histogram(x, bins=bin_count)
        probs = hist / len(x)
        probs[probs == 0] = 1.0
        return -np.sum(probs * np.log(probs))
    else:
        return (
            (x - x.min()).floordiv(pl.lit(1e-12) + (x.max() - x.min())/pl.lit(bin_count))
            .drop_nulls().value_counts()
            .sort()
            .struct.field("counts")
            .entropy().suffix("_binned_entropy")
        )


def c3(x: TIME_SERIES_T, n_lags: int) -> FLOAT_EXPR:
    """
    Measure of non-linearity in the time series using c3 statistics.

    This function calculates the value of

    .. math::

        \\frac{1}{n-2lag} \\sum_{i=1}^{n-2lag} x_{i + 2 \\cdot lag} \\cdot x_{i + lag} \\cdot x_{i}

    which is

    .. math::

        \\mathbb{E}[L^2(X) \\cdot L(X) \\cdot X]

    where :math:`\\mathbb{E}` is the mean and :math:`L` is the lag operator.
    It was proposed in [^1] as a measure of non linearity in the time series.


    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    n_lags : int
        The lag that should be used in the calculation of the feature.

    Returns
    -------
    float | Expr

    References
    ----------
    [1] Schreiber, T. and Schmitz, A. (1997). Discrimination power of measures for nonlinearity in a time series. PHYSICAL REVIEW E, VOLUME 55, NUMBER 5.

    """
    twice_lag = 2 * n_lags
    # Would potentially be faster if there is a pl.product_horizontal()
    return (x * x.shift(n_lags) * x.shift(twice_lag)).sum() / (
        x.count() - pl.lit(twice_lag)
    )


def change_quantiles(
    x: TIME_SERIES_T, q_low: float, q_high: float, is_abs: bool
) -> LIST_EXPR:
    """
    First fixes a corridor given by the quantiles ql and qh of the distribution of x.
    Then calculates the average, absolute value of consecutive changes of the series x inside this corridor.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        A single time-series.
    q_low : float
        The lower quantile of the corridor. Must be less than `qh`.
    q_high : float
        The upper quantile of the corridor. Must be greater than `ql`.
    is_abs : bool
        If True, takes absolute difference.

    Returns
    -------
    list of float | Expr
    """
    if q_high <= q_low:
        return 0.0

    # Use linear to conform to NumPy
    y = x.is_between(
        x.quantile(q_low, interpolation="linear"),
        x.quantile(q_high, interpolation="linear"),
    )
    expr = x.filter(pl.all_horizontal(y, y.shift_and_fill(False, period=-1))).diff()
    if is_abs:
        expr = expr.abs()

    return expr.implode()


def cid_ce(x: TIME_SERIES_T, normalize: bool = False) -> FLOAT_EXPR:
    """
    Computes estimate of time-series complexity[^1].

    A more complex time series has more peaks and valleys.
    This feature is calculated by:

    .. math::

        \\sqrt{ \\sum_{i=1}^{n-1} ( x_{i} - x_{i-1})^2 }

    Parameters
    ----------
    x : pl.Expr | pl.Series
        A single time-series.
    normalize : bool, optional
        If True, z-normalizes the time-series before computing the feature.
        Default is False.

    Returns
    -------
    float

    References
    ----------
    [1] Batista, Gustavo EAPA, et al (2014).
        CID: an efficient complexity-invariant distance for time series.
        Data Mining and Knowledge Discovery 28.3 (2014): 634-669.
    """
    if normalize:
        x = (x - x.mean()) / x.std()
    return ((x - x.shift(-1)) ** 2).sum() ** (0.5)


def count_above(x: TIME_SERIES_T, threshold: float = 0.0) -> FLOAT_EXPR:
    """
    Calculate the percentage of values above or equal to a threshold.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    threshold : float
        The threshold value for comparison.

    Returns
    -------
    float | Expr
    """
    # x.filter(x >= threshold).count().truediv(x.count()).mul(100)
    return (x >= threshold).sum().truediv(x.count()).mul(100)


def count_above_mean(x: TIME_SERIES_T) -> INT_EXPR:
    """
    Count the number of values that are above the mean.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    int | Expr
    """
    return (x > x.mean()).sum()


def count_below(x: TIME_SERIES_T, threshold: float = 0.0) -> FLOAT_EXPR:
    """
    Calculate the percentage of values below or equal to a threshold.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    threshold : float
        The threshold value for comparison.

    Returns
    -------
    float | Expr
    """
    # x.filter(x <= threshold).count().truediv(x.count()).mul(100)
    return (x <= threshold).sum().truediv(x.count()).mul(100)


def count_below_mean(x: TIME_SERIES_T) -> INT_EXPR:
    """
    Count the number of values that are below the mean.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    int | Expr
    """
    # x.filter(x < x.mean()).count()
    return (x < x.mean()).sum()


def cwt_coefficients(
    x: pl.Series, widths: Sequence[int] = (2, 5, 10, 20), n_coefficients: int = 14
) -> List[float]:
    """
    Calculates a Continuous wavelet transform for the Ricker wavelet.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    widths : Sequence[int], optional
        The widths of the Ricker wavelet to use for the CWT. Default is (2, 5, 10, 20).
    n_coefficients : int, optional
        The number of CWT coefficients to return. Default is 14.

    Returns
    -------
    list of float
    """
    convolution = np.empty((len(widths), x.len()), dtype=np.float32)
    for i, width in enumerate(widths):
        points = np.min([10 * width, x.len()])
        wavelet_x = np.conj(ricker(points, width)[::-1])
        convolution[i] = np.convolve(x.to_numpy(zero_copy_only=True), wavelet_x)
    coeffs = []
    for coeff_idx in range(min(n_coefficients, convolution.shape[1])):
        coeffs.extend(convolution[widths.index(), coeff_idx] for _ in widths)
    return coeffs


# def _energy_ratio_series(x, n_chunks):
#     n = len(x)
#     chunk_size = len(x) // n_chunks
#     y = x.pow(
#         2
#     )  # Vectorize better by squaring entire series at once, not for each chunk
#     energy = np.array([y.slice(i, chunk_size).sum() for i in range(0, n, chunk_size)])
#     full_energy = np.sum(
#         energy
#     )  # delay full energy computation until the end. Sum up partial sums
#     ratio: np.ndarray = energy / full_energy
#     return ratio.tolist()


# We calculate all 1,2,3,...,n_chunk indexed statistics at once
def energy_ratios(x: TIME_SERIES_T, n_chunks: int = 10) -> LIST_EXPR:
    """
    Calculates sum of squares over the whole series for `n_chunks` equally segmented parts of the time-series.

    Parameters
    ----------
    x : list of float
        The time-series to be segmented and analyzed.
    n_chunks : int, optional
        The number of equally segmented parts to divide the time-series into. Default is 10.

    Returns
    -------
    list of float | Expr
    """
    if isinstance(x, pl.Series):
        seg_sum = x.pow(2).reshape((n_chunks, -1)).list.sum()
        return (seg_sum / seg_sum.sum()).to_list()
    else:
        temp = x.pow(2).reshape((n_chunks, -1)).list.sum()
        return (temp/temp.sum()).implode().suffix("_energy_ratio")


def first_location_of_maximum(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Returns the first location of the maximum value of x.
    The position is calculated relatively to the length of x.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float | Expr
    """
    return x.arg_max() / x.count()


def first_location_of_minimum(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Returns the first location of the minimum value of x.
    The position is calculated relatively to the length of x.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float | Expr
    """
    return x.arg_min() / x.count()


def fourier_entropy(x: TIME_SERIES_T, n_bins: int = 10) -> float:
    """
    Calculate the Fourier entropy of a time series.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    n_bins : int, optional
        The number of bins to use for the entropy calculation. Default is 10.

    Returns
    -------
    float
    """
    if not isinstance(x, pl.Series):
        return NotImplemented

    _, pxx = welch(x, nperseg=min(x.len(), 256))
    return binned_entropy(pxx / bn.nanmax(pxx), n_bins)


def friedrich_coefficients(
    x: TIME_SERIES_T, polynomial_order: int = 3, n_quantiles: int = 30
) -> List[float]:
    """
    Calculate the Friedrich coefficients of a time series.

    Parameters
    ----------
    x : TIME_SERIES_T
        The time series to calculate the Friedrich coefficients of.
    polynomial_order : int, optional
        The order of the polynomial to fit to the quantile means. Default is 3.
    n_quantiles : int, optional
        The number of quantiles to use for the calculation. Default is 30.

    Returns
    -------
    list of float
    """
    X = (
        x.alias("signal")
        .to_frame()
        .with_columns(
            delta=x.diff().alias("delta"),
            quantile=x.qcut(q=n_quantiles, labels=[str(i) for i in range(n_quantiles)]),
        )
        .lazy()
    )
    X_means = (
        X.groupby("quantile")
        .agg([pl.all().mean()])
        .drop_nulls()
        .collect(streaming=True)
    )
    return np.polyfit(
        X_means.get_column("signal").to_numpy(zero_copy_only=True),
        X_means.get_column("delta").to_numpy(zero_copy_only=True),
        deg=polynomial_order,
    )


def has_duplicate(x: TIME_SERIES_T) -> BOOL_EXPR:
    """
    Check if the time-series contains any duplicate values.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    bool | Expr
    """
    return x.is_duplicated().any()


def _has_duplicate_of_value(x: TIME_SERIES_T, t: FLOAT_EXPR) -> BOOL_EXPR:
    """
    Check if a value exists as a duplicate.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    t : float | Expr
        The value to check for duplicates of.

    Returns
    -------
    bool
    """
    return x.filter(x == t).is_duplicated().any()


def has_duplicate_max(x: TIME_SERIES_T) -> BOOL_EXPR:
    """
    Check if the time-series contains any duplicate values equal to its maximum value.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    bool | Expr
    """
    return _has_duplicate_of_value(x, x.max())


def has_duplicate_min(x: TIME_SERIES_T) -> BOOL_EXPR:
    """
    Check if the time-series contains duplicate values equal to its minimum value.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    bool | Expr
    """
    return _has_duplicate_of_value(x, x.min())


def index_mass_quantile(x: TIME_SERIES_T, q: float) -> FLOAT_EXPR:
    """
    Calculates the relative index i of time series x where q% of the mass of x lies left of i.
    For example for q = 50% this feature calculator will return the mass center of the time series.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    q : float
        The quantile.

    Returns
    -------
    float | Expr
    """
    x_abs = x.abs()
    x_sum = x.sum()
    n = x.count()
    mass_center = x_abs.cumsum() / x_sum
    return ((mass_center >= q) + 1).arg_max() / n


def large_standard_deviation(x: TIME_SERIES_T, ratio: float = 0.25) -> BOOL_EXPR:
    """
    Checks if the time-series has a large standard deviation.

    True if:
    .. math::

        std(x) > r * (max(X)-min(X))

    As a heuristic, the standard deviation should be a forth of the range of the values.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    ratio : float
        The ratio of the interval to compare with.

    Returns
    -------
    bool | Expr
    """
    x_std = x.std()
    x_interval = x.max() - x.min()
    return x_std > (ratio * x_interval)


def last_location_of_maximum(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Returns the last location of the maximum value of x.
    The position is calculated relatively to the length of x.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float | Expr
    """
    return (x.count() - x.reverse().arg_max()) / x.count()


def last_location_of_minimum(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Returns the last location of the minimum value of x.
    The position is calculated relatively to the length of x.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float | Expr
    """
    return (x.count() - x.reverse().arg_min()) / x.count()


def lempel_ziv_complexity(x: pl.Series, n_bins: int) -> List[float]:
    """
    Calculate a complexity estimate based on the Lempel-Ziv compression algorithm.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    n_bins : int
        An integer specifying the number of bins to use for discretizing the time series.

    Returns
    -------
    list of float
    """
    complexities = []
    seq = x.search_sorted(
        element=np.linspace(x.min(), x.max(), n_bins + 1)[1:], side="left"
    ).to_numpy()
    sub_strs = set()
    n = x.len()
    ind, inc = 0, 1
    while not ind + inc > n:
        sub_str = seq[ind : ind + inc]
        if sub_str in sub_strs:
            inc += 1
        else:
            sub_strs.add(sub_str)
            ind += inc
            inc = 1
        complexities.append(len(sub_str) / n)
    return complexities


def linear_trend(x: TIME_SERIES_T) -> Mapping[str, float]:
    """
    Compute the slope, intercept, and RSS of the linear trend.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    Mapping | Expr
    """
    x_range = pl.int_range(1, x.count() + 1)
    beta = pl.cov(x, x_range) / x.var()
    alpha = x.mean() - beta * x_range.mean()
    resid = x - beta * x_range + alpha
    rss = resid.pow(2).sum()
    if isinstance(x, pl.Series):
        return {"slope": beta, "intercept": alpha, "rss": rss}
    else:
        return pl.Struct(
            beta.alias("slope"), alpha.alias("intercept"), rss.alias("rss")
        )


def _get_length_sequences_where(x: TIME_SERIES_T) -> LIST_EXPR:
    """
    Calculates the length of all sub-sequences where the series x is either True or 1.

    Parameters
    ----------
    x : pl.Expr
        A series containing only 1, True, 0 and False values.

    Returns
    -------
    pl.Expr
        A series with the length of all sub-sequences where the series is either True or False.
        If no ones or Trues contained, the list [0] is returned.
    """
    y = x.cast(pl.Int8).rle()
    return y.filter(x.struct[1] == 1).struct[0]


def longest_strike_above_mean(x: TIME_SERIES_T) -> INT_EXPR:
    """
    Returns the length of the longest consecutive subsequence in x that is greater than the mean of x.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    int | Expr
    """
    return _get_length_sequences_where(x > x.mean()).max().fill_null(0)


def longest_strike_below_mean(x: TIME_SERIES_T) -> INT_EXPR:
    """
    Returns the length of the longest consecutive subsequence in x that is smaller than the mean of x.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    int | Expr
    """
    return _get_length_sequences_where(x < x.mean()).max().fill_null(0)


def mean_abs_change(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Compute mean absolute change.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        A single time-series.

    Returns
    -------
    float | Expr
    """
    return x.diff(null_behavior="drop").abs().mean()


def mean_change(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Compute mean change.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        A single time-series.

    Returns
    -------
    float | Expr
    """
    return x.diff(null_behavior="drop").mean()


def mean_n_absolute_max(x: TIME_SERIES_T, n_maxima: int) -> FLOAT_EXPR:
    """
    Calculates the arithmetic mean of the n absolute maximum values of the time series.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    n_maxima : int
        The number of maxima to consider.

    Returns
    -------
    float | Expr
    """
    if n_maxima <= 0:
        raise ValueError("The number of maxima should be > 0.")
    return x.abs().top_k(n_maxima).mean().cast(pl.Float64)


def mean_second_derivative_central(x: pl.Series) -> float:
    """
    Returns the mean value of a central approximation of the second derivative.

    .. math::

    \\frac{1}{2(n-2)} \\sum_{i=1}^{n-1} 0.5 (x_{i+2} - 2 x_{i+1} + x_i)

    where n is the length of the time series x

    Parameters
    ----------
    x : pl.Series
        A time series to calculate the feature of.

    Returns
    -------
    float
    """
    return (x[-1] - x[-2] - x[1] + x[0]) / (2 * (len(x) - 2))


def number_crossings(x: TIME_SERIES_T, crossing_value: float = 0.0) -> FLOAT_EXPR:
    """
    Calculates the number of crossings of x on m, where m is the crossing value.

    A crossing is defined as two sequential values where the first value is lower than m and the next is greater, or vice-versa.
    If you set m to zero, you will get the number of zero crossings.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        A single time-series.
    crossing_value : float
        The crossing value. Defaults to 0.0.

    Returns
    -------
    float | Expr
    """
    return (
        x.gt(crossing_value).cast(pl.Int8).diff(null_behavior="drop").abs().eq(1).sum()
    )


def number_cwt_peaks(x: pl.Series, max_width: int = 5) -> float:
    """
    Number of different peaks in x.

    To estimate the numbers of peaks, x is smoothed by a ricker wavelet for widths ranging from 1 to n. This feature
    calculator returns the number of peaks that occur at enough width scales and with sufficiently high
    Signal-to-Noise-Ratio (SNR)

    Parameters
    ----------
    x : pl.Series
        A single time-series.

    max_width : int
        maximum width to consider


    Returns
    -------
    float
    """
    return len(
        find_peaks_cwt(
            vector=x.to_numpy(zero_copy_only=True),
            widths=np.array(list(range(1, max_width + 1))),
            wavelet=ricker,
        )
    )


def partial_autocorrelation(x: TIME_SERIES_T, n_lags: int) -> float:
    return NotImplemented


def percent_reocurring_points(x: TIME_SERIES_T) -> float:
    """
    Returns the percentage of non-unique data points in the time series. Non-unique data points are those that occur
    more than once in the time series.

    The percentage is calculated as follows:

        # of data points occurring more than once / # of all data points

    This means the ratio is normalized to the number of data points in the time series, in contrast to the
    `percent_reoccuring_values` function.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float
    """
    count = x.unique_counts()
    return count.filter(count > 1).sum() / x.count()


def percent_reoccuring_values(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Returns the percentage of values that are present in the time series more than once.

    The percentage is calculated as follows:

        len(different values occurring more than once) / len(different values)

    This means the percentage is normalized to the number of unique values in the time series, in contrast to the
    `percent_reocurring_points` function.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float | Expr
    """
    count = x.unique_counts()
    return (count > 1).sum() / count.count()


def number_peaks(x: TIME_SERIES_T, support: int) -> INT_EXPR:
    """
    Calculates the number of peaks of at least support n in the time series x. A peak of support n is defined as a
    subsequence of x where a value occurs, which is bigger than its n neighbours to the left and to the right.

    Hence in the sequence

    x = [3, 0, 0, 4, 0, 0, 13]

    4 is a peak of support 1 and 2 because in the subsequences

    [0, 4, 0]
    [0, 0, 4, 0, 0]

    4 is still the highest value. Here, 4 is not a peak of support 3 because 13 is the 3th neighbour to the right of 4
    and its bigger than 4.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    support : int
        Support of the peak

    Returns
    -------
    int | Expr
    """
    if isinstance(x, pl.Series):
        # Cheating by calling lazy... Series may or may not have a better implementation.
        frame = x.to_frame()
        return frame.select(number_peaks(pl.col(x.name), support)).item(0,0)
    else:
        return (
            pl.all_horizontal(
                ((x > x.shift(-i)) & (x > x.shift(i))).fill_null(False)
                for i in range(1, support+1)
            ).sum()
        )

def permutation_entropy(
    x: TIME_SERIES_T,
    tau: int = 1,
    n_dims: int = 3,
    base: float = math.e,
) -> FLOAT_EXPR:
    """
    Computes permutation entropy.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    tau : int
        The embedding time delay which controls the number of time periods between elements
        of each of the new column vectors.
    n_dims : int, > 1
        The embedding dimension which controls the length of each of the new column vectors
    base : float
        The base for log in the entropy computation

    Returns
    -------
    float | Expr
    """
    # This is kind of slow rn when tau > 1
    max_shift = -n_dims + 1
    if isinstance(x, pl.Series):
        # Complete this implementation by cheating (using exprs) for now.
        # There might be short cuts if we use eager. So improve this later.
        frame = x.to_frame()
        expr = permutation_entropy(pl.col(x.name), tau=tau, n_dims=n_dims)
        return frame.select(expr).item(0,0)
    else:
        return (
            (   # create list columns
                pl.concat_list(
                    x.take_every(tau), *(x.shift(-i).take_every(tau) for i in range(1, n_dims))
                ).filter(
                    x.shift(max_shift).take_every(tau).is_not_null()
                ).list.eval(
                    pl.element().arg_sort()
                )  # for each inner list, do an argsort
                .value_counts()  # groupby and count, but returns a struct
                .struct.field("counts")  # extract the field named "counts"
            )
            .entropy(normalize=True)
            .suffix("_permutation_entropy2")
        )

def range_count(x: TIME_SERIES_T, lower: float, upper: float, closed:ClosedInterval="left") -> INT_EXPR:
    """
    Computes values of input expression that is between lower (inclusive) and upper (exclusive).

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    lower : float
        The lower bound, inclusive
    upper : float
        The upper bound, exclusive

    Returns
    -------
    int | Expr
    """
    if upper < lower:
        raise ValueError("Upper must be greater than lower.")
    return x.is_between(lower_bound=lower, upper_bound=upper, closed=closed).sum()


def ratio_beyond_r_sigma(x: TIME_SERIES_T, ratio: float = 0.25) -> FLOAT_EXPR:
    """
    Returns the ratio of values in the series that is beyond r*std from mean on both sides.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.
    ratio : float
        The scaling factor for std

    Returns
    -------
    float | Expr
    """
    return (
        x.is_between(
            x.mean() - pl.lit(ratio) * x.std(),
            x.mean() + pl.lit(ratio) * x.std(),
            closed="both",
        )
        .is_not()  # check for deprecation
        .sum()
        / x.count()
    )


# Originally named `ratio_value_number_to_time_series_length` in tsfresh
def ratio_n_unique_to_length(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Calculate the ratio of the number of unique values to the length of the time-series.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float | Expr
    """
    return x.n_unique() / x.count()


def root_mean_square(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Calculate the root mean square.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float | Expr
    """
    return x.pow(2).mean().sqrt()


def _into_sequential_chunks(x: pl.Series, m: int) -> np.ndarray:
    name = x.name
    n_rows = len(x) - m + 1
    df = (
        x.to_frame()
        .select(
            pl.col(name), *(pl.col(name).shift(-i).suffix(str(i)) for i in range(1, m))
        )
        .slice(0, n_rows)
    )
    return df.to_numpy()


# Only works on series
def sample_entropy(x: TIME_SERIES_T, ratio: float = 0.2) -> FLOAT_EXPR:
    """
    Calculate the sample entropy of a time series.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        The input time series.
    ratio : float, optional
        The tolerance parameter. Default is 0.2.

    Returns
    -------
    float | Expr
    """
    # This is significantly faster than tsfresh
    if not isinstance(x, pl.Series):
        return NotImplemented

    threshold = ratio * x.std(ddof=0)
    m = 2
    mat = _into_sequential_chunks(x, m)
    tree = KDTree(mat)
    b = (
        np.sum(
            tree.query_ball_point(
                mat, r=threshold, p=np.inf, workers=-1, return_length=True
            )
        )
        - mat.shape[0]
    )
    mat = _into_sequential_chunks(x, m + 1)  #
    tree = KDTree(mat)
    a = (
        np.sum(
            tree.query_ball_point(
                mat, r=threshold, p=np.inf, workers=-1, return_length=True
            )
        )
        - mat.shape[0]
    )
    return np.log(b / a)  # -ln(a/b) = ln(b/a)

# Need to improve the input arguments depending on use cases.
def spkt_welch_density(x: TIME_SERIES_T, n_coeffs: Optional[int] = None) -> LIST_EXPR:
    '''
    This estimates the cross power spectral density of the time series x at different frequencies.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        The input time series.
    n_coeffs : Optional[int]
        The number of coefficients you want to take. If none, will take all, which will be a list
        as long as the input time series.
    '''
    if isinstance(x, pl.Series):
        if n_coeffs is None:
            last_idx = len(x)
        else:
            last_idx = n_coeffs
        _, pxx = welch(x, nperseg=min(len(x), 256))
        return pxx[: last_idx]
    else:
        return NotImplemented

# Originally named: `sum_of_reoccurring_data_points`
def sum_reocurring_points(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Returns the sum of all data points that are present in the time series more than once.

    For example, `sum_reocurring_points(pl.Series([2, 2, 2, 2, 1]))` returns 8, as 2 is a reoccurring value, so all 2's
    are summed up.

    This is in contrast to the `sum_reocurring_values` function, where each reoccuring value is only counted once.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float | Expr
    """
    return x.filter(~x.is_unique()).sum().cast(pl.Float64)


# Originally named: `sum_of_reoccurring_values`
def sum_reocurring_values(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Returns the sum of all values that are present in the time series more than once.

    For example, `sum_reocurring_values(pl.Series([2, 2, 2, 2, 1]))` returns 2, as 2 is a reoccurring value, so it is
    summed up with all other reoccuring values (there is none), so the result is 2.

    This is in contrast to the `sum_reocurring_points` function, where each reoccuring value is only counted as often
    as it is present in the data.

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time-series.

    Returns
    -------
    float | Expr
    """
    return x.filter(~x.is_unique()).unique().sum().cast(pl.Float64)


def symmetry_looking(x: TIME_SERIES_T, ratio: float = 0.25) -> BOOL_EXPR:
    """
    Check if the distribution of x looks symmetric.

    A distribution is considered symmetric if:

    .. math::

    | mean(X)-median(X) | < ratio * (max(X)-min(X))

    Parameters
    ----------
    x : polars.Series
        Input time-series.
    ratio : float
        Multiplier on distance between max and min.

    Returns
    -------
    bool | Expr
    """
    mean_median_difference = (x.mean() - x.median()).abs()
    max_min_difference = x.max() - x.min()
    return mean_median_difference < ratio * max_min_difference


def time_reversal_asymmetry_statistic(x: TIME_SERIES_T, n_lags: int) -> FLOAT_EXPR:
    """
    Returns the time reversal asymmetry statistic.

    This function calculates the value of:

    .. math::

        \\frac{1}{n-2lag} \\sum_{i=1}^{n-2lag} x_{i + 2 \\cdot lag}^2 \\cdot x_{i + lag} - x_{i + lag} \\cdot  x_{i}^2

    which is

    .. math::

        \\mathbb{E}[L^2(X)^2 \\cdot L(X) - L(X) \\cdot X^2]

    where :math:`\\mathbb{E}` is the mean and :math:`L` is the lag operator. It was proposed in [1] as a
    promising feature to extract from time series.

    Parameters
    ----------
    x : pl.Series
        Input time-series.
    n_lags : int
        The lag that should be used in the calculation of the feature.

    Returns
    -------
    float | Expr

    References
    ----------
    [1] Fulcher, B.D., Jones, N.S. (2014). Highly comparative feature-based time-series classification.
        Knowledge and Data Engineering, IEEE Transactions on 26, 3026–3037.
    """
    one_lag = x.shift(-n_lags)
    two_lag = x.shift(-2 * n_lags)
    return (one_lag * (two_lag.pow(2) - x.pow(2))).head(x.count() - 2 * n_lags).mean()


def variation_coefficient(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Calculate the coefficient of variation (CV).

    Parameters
    ----------
    x : pl.Expr | pl.Series
        Input time series.

    Returns
    -------
    float | Expr
    """
    return x.std() / x.mean()


def harmonic_mean(x: TIME_SERIES_T) -> FLOAT_EXPR:
    """
    Returns the harmonic mean of the expression
    """
    return x.count() / (pl.lit(1.0) / x).sum()


# FFT Features


def fft_coefficients(x: TIME_SERIES_T) -> Mapping[str, List[float]]:
    """
    Calculates Fourier coefficients and phase angles of the the 1-D discrete Fourier Transform.

    This function uses the `rustfft` Rust crate via pyo3-polars.
    """
    pass
