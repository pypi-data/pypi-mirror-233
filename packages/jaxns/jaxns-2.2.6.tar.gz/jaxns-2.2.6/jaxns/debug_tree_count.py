import numpy as np


def count_intervals(S, X):
    if not S:
        return np.zeros(len(X), dtype=int)

    a, b = np.array(list(zip(*S)))
    X = np.array(X)

    # Sort a and b for searchsorted
    a = np.sort(a)
    b = np.sort(b)

    # Count the number of 'a' values that are strictly less than x
    count_a = np.searchsorted(a, X, side='left')
    c = []
    for x in X:
        c.append(np.sum(a < x))

    print(count_a)
    print(c)

    # Count the number of 'b' values that are greater than or equal to x
    count_b = len(b) - np.searchsorted(b, X, side='left')
    c = []
    for x in X:
        c.append(np.sum(b >= x))

    print(count_b)
    print(c)

    return np.minimum(count_a, count_b)

def count_intervals(S, X):
    if not S:
        return np.zeros(len(X), dtype=int)

    a, b = np.array(list(zip(*S)))
    X = np.array(X)

    # Count the number of 'a' values that are less than or equal to x
    count_leq_a = np.searchsorted(a, X, side='right')

    # Count the number of 'b' values that are strictly greater than x
    count_gt_b = len(b) - np.searchsorted(b, X, side='left')

    return len(S) - count_leq_a - count_gt_b


def count_intervals_naive(S, X):
    counts = []

    for x in X:
        count = sum(1 for a, b in S if a < x <= b)
        counts.append(count)

    return counts


def test_basic():
    S = {(1, 5), (2, 6), (4, 8)}
    X = [3, 6, 7]
    assert np.array_equal(count_intervals(S, X), count_intervals_naive(S, X))


def test_empty_intervals():
    S = set()
    X = [3, 6, 7]
    assert np.array_equal(count_intervals(S, X), count_intervals_naive(S, X))


def test_empty_values():
    S = {(1, 5), (2, 6), (4, 8)}
    X = []
    assert np.array_equal(count_intervals(S, X), count_intervals_naive(S, X))


def test_single_interval():
    S = {(1, 5)}
    X = [0, 1, 3, 5, 6]
    assert np.array_equal(count_intervals(S, X), count_intervals_naive(S, X))


def test_non_overlapping_intervals():
    S = {(1, 2), (2, 3), (3, 6), (2, 4), (4, 6), (4, 5)}
    X = [1,2,3,4,5,6]
    assert np.array_equal(count_intervals(S, X), count_intervals_naive(S, X))


def test_overlapping_intervals():
    S = {(1, 4), (3, 6), (5, 8)}
    X = [1, 3, 5, 6, 8]
    assert np.array_equal(count_intervals(S, X), count_intervals_naive(S, X))


def test_consecutive_values():
    S = {(1, 3), (2, 4), (3, 5)}
    X = [3]
    assert np.array_equal(count_intervals(S, X), count_intervals_naive(S, X))


def test_no_valid_intervals():
    S = {(1, 2), (3, 4), (5, 6)}
    X = [7, 8, 9]
    assert np.array_equal(count_intervals(S, X), count_intervals_naive(S, X))


def test_interval_edges():
    S = {(1, 5)}
    X = [1, 5]
    assert np.array_equal(count_intervals(S, X), count_intervals_naive(S, X))
