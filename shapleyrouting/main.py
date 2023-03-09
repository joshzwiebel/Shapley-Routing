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


def APPROO1(num, Distances):
    """
    Compute 2D approximation for Shapley values.

    This algorithm is designed based on the Appro-O(1) algorithm for Shapley
    value approximation by Dan C. Popescu and Philip Kilby.

    The approximation equation is as follows for a given location k:

    .. math::
        \\phi^{(1)}_k = s_{kk}-Sc(S_{1,k},...,S_{k-1,k},S_{k+1,k},...,S_{n,k})

    This equation uses the equations for shared distance between two locations,
    i and j, with respect to starting location.

    .. math::
        s_{ij} = d_{0i}+d_{0j}-d_{ij}

    It also uses the Shared Contribution function. Please note in the equation
    below that the vector y is equivalent to the input vector x sorted
    in descending order.

    .. math::
        Sc(x_1,x_2,...,x_k)=\\sum\\limits_{i=1}^{k} \\frac{y_i}{i(i+1)}

    Parameters
    ----------
    num : int
        Number of players.

    Distances : list
        2D list of distances.

    Returns
    -------
    appro : list
        List of approximated shapley values.

    Examples
    --------
    >>> num = 9
    >>> Distances = [
        [0, 2, 9, 7, 7, 7, 6, 7, 1, 7],
        [2, 0, 5, 9, 9, 8, 9, 1, 7, 6],
        [9, 5, 0, 9, 6, 5, 7, 4, 7, 1],
        [7, 9, 9, 0, 1, 2, 8, 7, 1, 5],
        [7, 9, 6, 1, 0, 5, 5, 5, 8, 8],
        [7, 8, 5, 2, 5, 0, 1, 8, 2, 5],
        [6, 9, 7, 8, 5, 1, 0, 1, 6, 1],
        [7, 1, 4, 7, 5, 8, 1, 0, 1, 2],
        [1, 7, 7, 1, 8, 2, 6, 1, 0, 4],
        [7, 6, 1, 5, 8, 5, 1, 2, 4, 0]
        ]
    >>> APPROO1(num, Distances)
    [-1.3249999999999993,
    5.001190476190477,
    2.994047619047622,
    3.05952380952381,
    2.8861111111111093,
    2.2075396825396822,
    2.908333333333333,
    -3.362698412698413,
    2.4940476190476204]
    """
    # Compute matrix of shared distances
    SharedDistances = [
        [
            Distances[0][i] + Distances[0][j] - Distances[i][j]
            for j in range(len(Distances[0]))
        ]
        for i in range(len(Distances))
    ]

    appro = []
    for k in range(1, len(Distances)):
        # Sort input vector in descending order
        x = [SharedDistances[n][k] for n in range(num)]
        x.sort(reverse=True)

        # Determine shared contribution for given k
        Sc = 0
        for i in range(1, len(x) + 1):
            Sc += x[i - 1] / (i * (i + 1))

        # Get approximate Shapley value
        appro.append(SharedDistances[k][k] - Sc)
    return appro


if __name__ == '__main__':
    players = ['A', 'B', 'C']
    print(shapley_value(players, lambda x: 5 if 'A' in x else 1))

    num = 2
    Distances = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]

    print(SHAPO(num, Distances))
