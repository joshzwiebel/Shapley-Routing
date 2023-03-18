import numpy as np
from shapleyrouting.rideshare import RideShare


def test_cost_samples():
    rng = np.random.default_rng()
    num_players = 3
    distances = rng.integers(
        low=0,
        high=10,
        size=(num_players + 1, num_players + 1),
    )
    rs = RideShare(num_players, distances)

    subsets = np.array([
        [True, False, False],
        [False, True, True],
        [True, True, False],
    ], dtype=bool)
    costs = np.array([12, 6, 18], dtype=np.float64)
    shapley_values = rs.cost_samples(subsets, costs)

    assert np.allclose(shapley_values, np.array([7, 4, 1]))
