import numpy as np
from shapleyrouting.rideshare import RideShare
from time import time


def buildInput(num):
    b = np.random.randint(9, size=(num + 1, num + 1)) + 1
    Distances = (b + b.T) / 2
    np.fill_diagonal(Distances, 0)
    return Distances


def test_approximation_switch():
    max_players = 50
    min_players = 2
    faster_algorithm = np.empty(
        [100, max_players - min_players],
        dtype=np.chararray)
    for i in range(100):
        for num_players in range(min_players, max_players):
            Distances = buildInput(num_players)
            rs = RideShare(num_players, Distances)

            # time shapo
            st = time()
            rs.SHAPO(num_players, Distances)
            elapsedShapo = time() - st

            # time appro
            st = time()
            rs.APPROO1(num_players, Distances)
            elapsedAppro = time() - st

            winner = 'shapo' if elapsedAppro >= elapsedShapo else 'appro'
            faster_algorithm[i][num_players - min_players] = winner

    n_condition = -1
    average_faster_algorithm = np.empty(3, dtype=np.chararray)
    for n in range(len(faster_algorithm[0])):

        # tally faster algorithm for each iteration
        vals, counts = np.unique(
            np.array([item[n] for item in faster_algorithm]),
            return_counts=True)
        # find mode
        mode_value = counts.tolist().index(np.max(counts))

        # append and shift list
        average_faster_algorithm[0] = average_faster_algorithm[1]
        average_faster_algorithm[1] = average_faster_algorithm[2]
        average_faster_algorithm[2] = vals[mode_value]

        # look for 3 sequential occurrences of appro outperforming shapo
        if np.count_nonzero(average_faster_algorithm == 'appro') == 3:
            n_condition = n + min_players
            break

    print('Approximation should be used when n={}'.format(n_condition))
    assert n_condition >= 8 and n_condition <= 12
