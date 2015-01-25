import matplotlib.pyplot as plt
import bisect
import itertools

class PrecisionRecallData:

    def __init__(self, points): # TODO: document that
        if len(points) == 0:
            raise ValueError("A plot must have at least one point")
        self.__points = sorted(points, key=lambda x: x[0])
        self.__interpolated_points = self.__compute_interpolation(self.points)

    @property
    def points(self):
        return self.__points

    @property
    def interpolated_points(self):
        return self.__interpolated_points

    def __compute_interpolation(self, points):
        """
        Parameters:
            points (list of tuple of (int, int)): a list of points of (recall, precision)
        Returns:
            (list of tuple of (int, int)): the interpolated points. First point will always be (0, 1), and for a given recall value R, the associated precision will be the maximum precision encountered
            for recall values greater or equal than R.
        """

        # For a given recall value, only keep the greatest precision
        cleaned = []
        for k, g in itertools.groupby(points, lambda x: x[0]):
            cleaned.append(max(g, key=lambda x: x[1]))

        interpolated_points = [None] * len(cleaned)
        interpolated_points[-1] = cleaned[-1]

        for i in range(len(cleaned) - 2, -1, -1):
            interpolated_points[i] = (cleaned[i][0], cleaned[i][1] if cleaned[i][1] > interpolated_points[i+1][1] else interpolated_points[i+1][1])

        interpolated_points[0] = (0, 1)
        return interpolated_points
    
    def precision_for(self, recall_level):
        """
        Parameters:
        recall_level (int): a recall value between 0 and 1
        Returns:
        (int) the corresponding interpolated precision value
        """
        # Binary search
        i = bisect.bisect_right([p[0] for p in self.__interpolated_points], recall_level)
        if i > 0:
            return self.__interpolated_points[i - 1][1]
        return self.__interpolated_points[0][1]