import itertools
import numpy as np


def shapley_value(players, game):
    """
    Compute the Shapley value of a game.

    .. math::
        \\varphi_m(v) = \\frac{1}{p} \\sum\\limits_s
        \\frac{v(S \\cup \\{m\\}) - v(S)}{\\binom{p - 1}{k(S))}},
        \\:\\:\\:\\: m = 1, 2, 3, ..., p

    Parameters
    ----------
    players : list
        List of players of game.

    game : Callable
        Function that takes coalition as parameter and returns score.

    Returns
    -------
    shapley : dict
        Shapley values by players.

    Examples
    --------
    >>> players = ['A', 'B', 'C']
    >>> game = lambda coalition: 5 if 'A' in coalition else 1
    >>> shapley_value(players, game)
    {'A': 10.0, 'B': 4.0, 'C': 4.0}
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


def SHAPO(num, Distances):
    """
    Compute ride sharing Shapley values.

    Parameters
    ----------
    num : int
        Number of players.

    Distances : list
        2D list of distances.

    Returns
    -------
    shapo : list
        List of shapley values.

    Examples
    --------
    >>> num = 2
    >>> Distances = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
    >>> SHAPO(num, Distances)
    [2.0, 4.0]
    """
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


if __name__ == '__main__':
    players = ['A', 'B', 'C']
    print(shapley_value(players, lambda x: 5 if 'A' in x else 1))

    num = 2
    Distances = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]

    print(SHAPO(num, Distances))
