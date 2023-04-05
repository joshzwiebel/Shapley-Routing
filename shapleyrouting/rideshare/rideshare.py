import numpy as np
from numpy.typing import NDArray


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
        shapo = np.array([0.0] * num)
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

    def APPROO1(self, num, Distances):
        """
        Compute 2D approximation for Shapley values.

        This algorithm is designed based on the Appro-O(1) algorithm for
        Shapley value approximation by Dan C. Popescu and Philip Kilby.

        The approximation equation is as follows for a given location k:

        .. math::
            \\phi^{(1)}_k=s_{kk}-Sc(S_{1,k},...,S_{k-1,k},S_{k+1,k},...,S_{n,k})

        This equation uses the equations for shared distance between two
        locations, i and j, with respect to starting location.

        .. math::
            s_{ij} = d_{0i}+d_{0j}-d_{ij}

        It also uses the Shared Contribution function. Please note in the
        equation below that the vector y is equivalent to the input
        vector x sorted in descending order.

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
        SharedDistances = np.array(
            [
                [
                    max(Distances[0][i] + Distances[0][j] - Distances[i][j], 0)
                    for j in range(len(Distances[0]))
                ]
                for i in range(len(Distances))
            ]
        )

        appro = np.array([])
        for k in range(1, len(Distances)):
            # Sort input vector in descending order
            x = [SharedDistances[n][k] for n in range(num)]
            x.sort(reverse=True)

            # Determine shared contribution for given k
            Sc = 0
            for i in range(1, len(x) + 1):
                Sc += x[i - 1] / (i * (i + 1))

            # Get approximate Shapley value
            np.append(appro, SharedDistances[k][k] - Sc)
        return appro

    def cost_samples(
        self,
        subsets: NDArray[np.bool_],
        costs: NDArray[np.float64],
    ):
        """
        Compute Shapley values for ride sharing given cost samples.

        This algorithm is designed based on the cost sharing algorithm based on
        cost samples, written by Eric Balkanski, Umar Syed, and Sergei
        Vassilvitskii.

        Given a set of :math:`m` samples,
        :math:`(S_1, C(S_1)), (S_2, C(S_2)), ..., (S_m, C(S_m))`, from
        distribution :math:`\\mathcal{D}`, where :math:`S_i` represents a
        subset of players and :math:`C(S_i)` represents the cost of the subset
        of players, the approximate share of the player :math:`i`, denoted by
        :math:`\\tilde{\\Phi^\\mathcal{D}_i}` is given by:

        .. math::
            \\tilde{\\phi^\\mathcal{D}_i} =
            \\frac{1}{m} \\sum\\limits_{S_j : i \\in S_j} \\frac{C(S_j)}{|S_j|}

        Parameters
        ----------
        subsets : numpy.ndarray
            2D boolean array of size ``mxn``, where ``m`` is the number of
            subsets of players and n is the number of players. Each boolean
            entry indicates whether or not the player was included in that
            subset.

        costs : numpy.ndarray
            1D array of length ``m`` indicating the total costs incurred by
            each subset.

        Examples
        --------
        >>> import numpy as np
        >>> subsets = np.array([
        ...     [True, False, False],
        ...     [False, True, True],
        ...     [True, True, False],
        ... ], dtype=bool)
        >>> costs = np.array([10, 5, 8], dtype=np.float64)
        >>> cost_samples(subsets, costs)
        array([4.66666667, 2.16666667, 0.83333333])
        """
        if subsets.shape[0] != costs.shape[0]:
            raise ValueError('Number of costs much match number of subsets')

        num_players = np.sum(subsets, axis=1)
        shapley_all = costs / num_players
        shapley_players = np.matmul(shapley_all, subsets) / costs.shape[0]

        return shapley_players

    def fit(self):
        # Use approximation if there are over 10 players
        if self.num_players < 10:
            self.shap_values = self.SHAPO(self.num_players, self.distances)
        else:
            self.shap_values = self.APPROO1(self.num_players, self.distances)
        return self.shap_values
