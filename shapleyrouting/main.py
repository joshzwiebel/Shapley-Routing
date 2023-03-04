import itertools
import numpy as np


def shapley_value(players, game):
    """
    Compute the Shapley value of a game.
    """
    n = len(players)
    shapley = {}
    for player in players:
        shapley[player] = 0
    for k in range(1, n):
        for coalition in itertools.combinations(players, k):
            # Compute the value of the game for the coalition.
            value = game(coalition)
            # Compute the number of permutations of the coalition.
            num_perms = np.math.factorial(k)
            # Compute the Shapley value for each player in the coalition.
            for player in coalition:
                shapley[player] += value / num_perms
    return shapley


def game(coalition):
    return 5 if 'A' in coalition else 1


print(shapley_value(['A', 'B', 'C'], game))


def SHAPO(num, Distances):
    shapo = [0.0] * num
    for i in range(1, num + 1):
        shapo[i - 1] += 1.0 / i * Distances[0][i]
        shapo[i - 1] += 1.0 / (num - i + 1) * Distances[i][0]
        for q in range(i + 1, num + 1):
            shapo[i - 1] -= 1.0 / (q * (q - 1)) * Distances[0][q]
            shapo[i - 1] += 1.0 / ((q - i) * (q - i + 1)) * Distances[i][q]
        for p in range(1, i):
            shapo[i - 1] += 1.0 / ((i - p) * (i - p + 1)) * Distances[p][i]
            shapo[i - 1] -= 1.0 / ((num - p) * (num - p + 1)) * Distances[p][0]
            for q in range(i + 1, num + 1):
                shapo[i - 1] -= (
                    2.0
                    / ((q - p) * (q - p + 1) * (q - p - 1))
                    * Distances[p][q]
                )
    return shapo


num = 2
Distances = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]

print(SHAPO(num, Distances))
