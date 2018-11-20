from itertools import combinations
from math import sqrt, inf
from json import dumps
from collections import OrderedDict
from itertools import islice
from csv import reader


def get_manhattan_distance(point_a, point_b):
    return abs(point_a['x'] - point_b['x']) + abs(point_a['y'] - point_b['y'])


def get_euclidean_distance(point_a, point_b):
    return sqrt((point_a['x'] - point_b['x']) ** 2 + abs(point_a['y'] - point_b['y']) ** 2)


class LOF:
    # Distance Formulas
    CONST_MANHATTAN = 'Manhattan'
    CONST_EUCLIDEAN = 'Euclidean'
    CONST_DISTANCE_FORMULAS = [CONST_MANHATTAN, CONST_EUCLIDEAN]

    # Ordered Dict Keys
    LOF_KEY = 'local_outlier_factor'
    LRD_KEY = 'local_reachability_distance'
    DIST_KEY = 'k_nearest_nodes_distances'

    # Formatting Constants
    CONST_ERROR = 'Error: '

    def __init__(self, coordinates, distance_formula, k):

        # set up
        self.coordinates = self.get_coordinates_by_format(coordinates)
        self.initial_check_data(k)
        self.k = k
        self.distance_formula = self.initial_check_distance_formula(distance_formula)

        # run it
        self.write_initial_distance_calculations()
        self.calculate_lof()

    def get_coordinates_by_format(self, coordinates):
        if isinstance(coordinates, OrderedDict):
            return coordinates
        elif isinstance(coordinates, str):
            # do normal
            coordinates_to_return = OrderedDict([])
            with open(coordinates, newline='') as csv_file:
                file = reader(csv_file, delimiter=',', quotechar='|')
                for i, coord in enumerate(file):
                    key = str('coord_' + str(i) + '_x_' + coord[0] + '_y_' + coord[1])
                    coordinates_to_return[key] = OrderedDict([
                        ('x', int(coord[0])),
                        ('y', int(coord[1]))
                    ])
            return coordinates_to_return

        elif isinstance(coordinates, list) and isinstance(coordinates[0], tuple):
            coordinates_to_return = OrderedDict([])
            for i, coord in enumerate(coordinates):
                key = str('coord_' + str(i) + '_x_' + str(coord[0]) + '_y_' + str(coord[1]))
                coordinates_to_return[key] = OrderedDict([
                    ('x', int(coord[0])),
                    ('y', int(coord[1]))
                ])
            return coordinates_to_return

        elif isinstance(coordinates, list) and isinstance(coordinates[0], list) and len(coordinates) == 2 and len(
                coordinates[0]) == len(coordinates[1]):
            coordinates_to_return = OrderedDict([])
            for i, coord in enumerate(coordinates[0]):
                key = str('coord_' + str(i) + '_x_' + str(coord) + '_y_' + str(coordinates[1][i]))
                coordinates_to_return[key] = OrderedDict([
                    ('x', int(coord)),
                    ('y', int(coordinates[1][i]))
                ])
            return coordinates_to_return

        else:
            print(self.CONST_ERROR + 'Invalid coordinates data type')
            exit()

    def write_initial_distance_calculations(self):
        for combo in combinations(self.coordinates, 2):
            distance = self.get_distance(self.coordinates[combo[0]], self.coordinates[combo[1]])
            self.write_distance(combo[0], combo[1], distance)
            self.write_distance(combo[1], combo[0], distance)

    def initial_check_data(self, k):
        if k >= len(self.coordinates):
            print(self.CONST_ERROR + 'K value is greater than or equal to number of given coordinates')
            exit()
        else:
            pass

    def initial_check_distance_formula(self, distance_formula):
        if distance_formula in self.CONST_DISTANCE_FORMULAS:
            return distance_formula
        else:
            return self.CONST_MANHATTAN

    def calculate_lof(self):
        for coordinate in self.coordinates:
            neighbors = self.coordinates[coordinate][self.DIST_KEY]
            k_nearest_set_count = len(self.coordinates[coordinate][self.DIST_KEY])
            reach_distances_sum = 0
            for neighbor in neighbors:
                reach_distances_sum += self.get_reach_distance(neighbor, coordinate)

            l_r_d_sum = 0
            for neighbor in neighbors:
                l_r_d_sum += self.get_local_reachability_distance(neighbor)

            self.coordinates[coordinate][self.LOF_KEY] = (reach_distances_sum * l_r_d_sum) / k_nearest_set_count ** 2

    def get_reach_distance(self, coordinate_one, coordinate_two):
        k_nearest_neighbor = list(self.coordinates[coordinate_one][self.DIST_KEY].keys())[self.k - 1]
        k_nearest_neighbor_value = self.coordinates[coordinate_one][self.DIST_KEY][k_nearest_neighbor]

        return max(k_nearest_neighbor_value,
                   self.get_distance(self.coordinates[coordinate_one], self.coordinates[coordinate_two]))

    def get_local_reachability_distance(self, coordinate):
        neighbors = self.coordinates[coordinate][self.DIST_KEY]
        reach_distance_sum = 0
        for neighbor in neighbors:
            reach_distance_sum = reach_distance_sum + self.get_reach_distance(neighbor, coordinate)

        l_r_d = len(self.coordinates[coordinate][self.DIST_KEY]) / reach_distance_sum

        self.coordinates[coordinate][self.LRD_KEY] = l_r_d

        return l_r_d

    def write_distance(self, key_1, key_2, distance):
        if self.DIST_KEY in self.coordinates[key_1]:
            if len(self.coordinates[key_1][self.DIST_KEY]) == self.k:
                if distance > list(self.coordinates[key_1][self.DIST_KEY].values())[0]:
                    return
                else:
                    self.coordinates[key_1][self.DIST_KEY][key_2] = distance
                    temp_ordered_dict_sorted = OrderedDict(
                        sorted(self.coordinates[key_1][self.DIST_KEY].items(), key=lambda x: x[1]))
                    self.coordinates[key_1][self.DIST_KEY] = OrderedDict(
                        islice(temp_ordered_dict_sorted.items(), self.k))
                    return
            else:
                if key_2 in self.coordinates[key_1][self.DIST_KEY]:
                    self.coordinates[key_1][self.DIST_KEY][key_2] = distance
                    self.coordinates[key_1][self.DIST_KEY] = \
                        OrderedDict(sorted(self.coordinates[key_1][self.DIST_KEY].items(), key=lambda x: x[1]))
                else:
                    self.coordinates[key_1][self.DIST_KEY][key_2] = distance
                    self.coordinates[key_1][self.DIST_KEY] = \
                        OrderedDict(sorted(self.coordinates[key_1][self.DIST_KEY].items(), key=lambda x: x[1]))
        else:
            self.coordinates[key_1][self.DIST_KEY] = {}
            self.write_distance(key_1, key_2, distance)

    def get_unique_pairs(self):
        return combinations(self.coordinates, 2)

    def get_distance(self, point_a, point_b):
        if self.distance_formula == self.CONST_MANHATTAN:
            return get_manhattan_distance(point_a, point_b)
        elif self.distance_formula == self.CONST_EUCLIDEAN:
            return get_euclidean_distance(point_a, point_b)

    def print_all_data(self, tab=4):
        print('===All Data For Each Coordinate===')
        print(dumps(self.coordinates, indent=tab))

    def get_all_data(self):
        return self.coordinates

    def print_all_lof(self):
        print('===All Local Outlier Factors for Each Coordinate===')
        for coordinate in self.coordinates:
            print(coordinate + ': ' + str(self.coordinates[coordinate][self.LOF_KEY]))

    def get_all_lof(self):
        lofs = []
        for coordinate in self.coordinates:
            lofs.append((coordinate, self.coordinates[coordinate][self.LOF_KEY]))
        return lofs

    def print_lof_sorted_filtered(self, reverse_order=False, filter_value_greater_than=None,
                                  filter_value_less_than=None):
        print('===Local Outlier Factor Distances Sorted and Filtered===')
        for coordinate in self.get_lof_sorted_filtered(reverse_order, filter_value_greater_than, filter_value_less_than):
            print(coordinate[0] + ': ' + str(coordinate[1]))

    def get_lof_sorted_filtered(self, reverse_order=False, filter_value_greater_than=None,
                                filter_value_less_than=None):
        if (filter_value_less_than is not None and filter_value_greater_than is not None) and \
                filter_value_greater_than > filter_value_less_than:
            print(self.CONST_ERROR + 'Cannot filter for values greater than ' + filter_value_greater_than +
                  ' and less than ' + filter_value_less_than)
            return []

        if filter_value_less_than is None:
            filter_value_less_than = inf

        if filter_value_greater_than is None:
            filter_value_greater_than = -inf

        local_outlier_factors = []
        for coordinate in self.coordinates:
            coordinate_value = self.coordinates[coordinate][self.LOF_KEY]
            if filter_value_greater_than < coordinate_value < filter_value_less_than:
                local_outlier_factors.append((coordinate, coordinate_value))

        local_outlier_factors.sort(key=lambda tup: tup[1], reverse=reverse_order)

        lofs = []
        for coordinate in local_outlier_factors:
            lofs.append((coordinate[0], coordinate[1]))

        return lofs
