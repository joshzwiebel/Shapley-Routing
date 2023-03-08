import numpy as np


class RideShare:
    def __init__(self, num_players, distances):
        self.num_players = num_players
        self.distances = np.array(distances)
        # assert that the number of players is equal to
        # the number of rows in the distance matrix
        assert self.num_players + 1 == len(self.distances)

    def SHAPO(self, num, Distances):
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
                shapo[i - 1] -= (
                    1.0 / ((num - p) * (num - p + 1)) * Distances[p][0]
                )
                for q in range(i + 1, num + 1):
                    shapo[i - 1] -= (
                        2.0
                        / ((q - p) * (q - p + 1) * (q - p - 1))
                        * Distances[p][q]
                    )
        return shapo

    def fit(self):
        self.shap_values = self.SHAPO(self.num_players, self.distances)
        return self.shap_values
