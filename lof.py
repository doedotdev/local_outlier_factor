from itertools import combinations
import math
from json import dumps
from collections import OrderedDict


def get_manhattan_distance(point_a, point_b):
    return abs(point_a['x'] - point_b['x']) + abs(point_a['y'] - point_b['y'])


def get_euclidean_distance(point_a, point_b):
    return math.sqrt((point_a['x'] - point_b['x']) ** 2 + abs(point_a['y'] - point_b['y']) ** 2)


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
        self.initial_check_data(coordinates, k)
        self.k = k
        self.coordinates = coordinates
        self.distance_formula = self.initial_check_distance_formula(distance_formula)

        # run it
        self.write_initial_distance_calculations()
        self.calculate_final_lof()

    def write_initial_distance_calculations(self):
        for combo in combinations(self.coordinates, 2):
            distance = self.get_distance(self.coordinates[combo[0]], self.coordinates[combo[1]])
            self.write_distance(combo[0], combo[1], distance)
            self.write_distance(combo[1], combo[0], distance)

    def initial_check_data(self, coordinates, k):
        if k >= len(coordinates):
            print(self.CONST_ERROR + 'K value is greater than or equal to number of given coordinates')
            exit()
        else:
            pass

    def initial_check_distance_formula(self, distance_formula):
        if distance_formula in self.CONST_DISTANCE_FORMULAS:
            return distance_formula
        else:
            return self.CONST_MANHATTAN


    def print_all_data(self, tab=4):
        print('===All Data For Each Coordinate===')
        print(dumps(self.coordinates, indent=tab))

    def print_all_lof(self):
        print('===All Local Outlier Factors for Each Coordinate===')
        for coordinate in self.coordinates:
            print(coordinate + ': ' + str(self.coordinates[coordinate][self.LOF_KEY]))

    def print_lof_sorted_filtered(self, reverse_order=False, filter_value_greater_than=None,
                                  filter_value_less_than=None):
        print('===Local Outlier Factor Distances Sorted and Filtered===')

        if (filter_value_less_than is not None and filter_value_greater_than is not None) and \
                filter_value_greater_than > filter_value_less_than:
            print(self.CONST_ERROR + 'Cannot filter for values greater than ' + filter_value_greater_than +
                  ' and less than ' + filter_value_less_than)

        if filter_value_less_than is None:
            filter_value_less_than = math.inf

        if filter_value_greater_than is None:
            filter_value_greater_than = -math.inf

        local_reachability_distances = []
        for coordinate in self.coordinates:
            coordinate_value = self.coordinates[coordinate][self.LOF_KEY]
            if filter_value_greater_than < coordinate_value < filter_value_less_than:
                local_reachability_distances.append((coordinate, coordinate_value))

        local_reachability_distances.sort(key=lambda tup: tup[1], reverse=reverse_order)
        for coordinate in local_reachability_distances:
            print(coordinate[0] + ': ' + str(coordinate[1]))

    def calculate_final_lof(self):
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
        return max(self.get_k_nearest_value(coordinate_one),
                   self.get_distance(self.coordinates[coordinate_one], self.coordinates[coordinate_two]))

    def get_local_reachability_distance(self, coordinate):
        neighbors = self.coordinates[coordinate][self.DIST_KEY]
        reach_distance_sum = 0
        for neighbor in neighbors:
            reach_distance_sum = reach_distance_sum + self.get_reach_distance(neighbor, coordinate)

        l_r_d = len(self.coordinates[coordinate][self.DIST_KEY]) / reach_distance_sum

        self.coordinates[coordinate][self.LRD_KEY] = l_r_d

        return l_r_d

    def get_k_nearest_value(self, coordinate):
        k_nearest_neighbor = list(self.coordinates[coordinate][self.DIST_KEY].keys())[self.k - 1]
        return self.coordinates[coordinate][self.DIST_KEY][k_nearest_neighbor]

    def write_distance(self, key_1, key_2, distance):
        if self.DIST_KEY in self.coordinates[key_1]:
            if len(self.coordinates[key_1][self.DIST_KEY]) == self.k:
                if distance > list(self.coordinates[key_1][self.DIST_KEY].values())[0]:
                    return
                else:
                    # TODO
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


coords = OrderedDict([
    ('a', OrderedDict([
        ('x', 0),
        ('y', 0)
    ])),
    ('b', OrderedDict([
        ('x', 0),
        ('y', 1)
    ])),
    ('c', OrderedDict([
        ('x', 1),
        ('y', 1)
    ])),
    ('d', OrderedDict([
        ('x', 3),
        ('y', 0)
    ]))
    # ,
    # ('e', OrderedDict([
    #     ('x', 0),
    #     ('y', 0)
    # ])),
    # ('f', OrderedDict([
    #     ('x', 0),
    #     ('y', 1)
    # ])),
    # ('g', OrderedDict([
    #     ('x', 1),
    #     ('y', 1)
    # ])),
    # ('h', OrderedDict([
    #     ('x', 3),
    #     ('y', 0)
    # ])),
    # ('i', OrderedDict([
    #     ('x', 0),
    #     ('y', 0)
    # ])),
    # ('j', OrderedDict([
    #     ('x', 0),
    #     ('y', 1)
    # ])),
    # ('k', OrderedDict([
    #     ('x', 1),
    #     ('y', 1)
    # ])),
    # ('l', OrderedDict([
    #     ('x', 3),
    #     ('y', 0)
    # ])),
    # ('m', OrderedDict([
    #     ('x', 0),
    #     ('y', 0)
    # ])),
    # ('n', OrderedDict([
    #     ('x', 0),
    #     ('y', 1)
    # ])),
    # ('o', OrderedDict([
    #     ('x', 1),
    #     ('y', 1)
    # ])),
    # ('p', OrderedDict([
    #     ('x', 3),
    #     ('y', 0)
    # ])),
    # ('q', OrderedDict([
    #     ('x', 0),
    #     ('y', 0)
    # ])),
    # ('r', OrderedDict([
    #     ('x', 0),
    #     ('y', 1)
    # ])),
    # ('s', OrderedDict([
    #     ('x', 1),
    #     ('y', 1)
    # ])),
    # ('t', OrderedDict([
    #     ('x', 3),
    #     ('y', 0)
    # ])),
    # ('u', OrderedDict([
    #     ('x', 0),
    #     ('y', 0)
    # ])),
    # ('v', OrderedDict([
    #     ('x', 0),
    #     ('y', 1)
    # ])),
    # ('w', OrderedDict([
    #     ('x', 1),
    #     ('y', 1)
    # ])),
    # ('x', OrderedDict([
    #     ('x', 3),
    #     ('y', 0)
    # ])),
    # ('y', OrderedDict([
    #     ('x', 0),
    #     ('y', 0)
    # ])),
    # ('z', OrderedDict([
    #     ('x', 0),
    #     ('y', 1)
    # ])),
    # ('aa', OrderedDict([
    #     ('x', 1),
    #     ('y', 1)
    # ])),
    # ('ab', OrderedDict([
    #     ('x', 3),
    #     ('y', 0)
    # ])),
    # ('ac', OrderedDict([
    #     ('x', 0),
    #     ('y', 0)
    # ])),
    # ('ad', OrderedDict([
    #     ('x', 0),
    #     ('y', 1)
    # ])),
    # ('bc', OrderedDict([
    #     ('x', 1),
    #     ('y', 1)
    # ])),
    # ('bd', OrderedDict([
    #     ('x', 3),
    #     ('y', 0)
    # ])),
    # ('ca', OrderedDict([
    #     ('x', 0),
    #     ('y', 0)
    # ])),
    # ('cb', OrderedDict([
    #     ('x', 0),
    #     ('y', 1)
    # ])),
    # ('cc', OrderedDict([
    #     ('x', 1),
    #     ('y', 1)
    # ])),
    # ('cd', OrderedDict([
    #     ('x', 3),
    #     ('y', 0)
    # ])),
    # ('da', OrderedDict([
    #     ('x', 0),
    #     ('y', 0)
    # ])),
    # ('db', OrderedDict([
    #     ('x', 0),
    #     ('y', 1)
    # ])),
    # ('dc', OrderedDict([
    #     ('x', 1),
    #     ('y', 1)
    # ])),
    # ('dd', OrderedDict([
    #     ('x', 3),
    #     ('y', 0)
    # ])),
    # ('ea', OrderedDict([
    #     ('x', 0),
    #     ('y', 0)
    # ])),
    # ('eb', OrderedDict([
    #     ('x', 0),
    #     ('y', 1)
    # ])),
    # ('ec', OrderedDict([
    #     ('x', 1),
    #     ('y', 1)
    # ])),
    # ('ed', OrderedDict([
    #     ('x', 3),
    #     ('y', 0)
    # ])),
    # ('fa', OrderedDict([
    #     ('x', 0),
    #     ('y', 0)
    # ])),
    # ('fb', OrderedDict([
    #     ('x', 0),
    #     ('y', 1)
    # ])),
    # ('fc', OrderedDict([
    #     ('x', 1),
    #     ('y', 1)
    # ])),
    # ('fd', OrderedDict([
    #     ('x', 3),
    #     ('y', 0)
    # ])),
    # ('ga', OrderedDict([
    #     ('x', 0),
    #     ('y', 0)
    # ])),
    # ('gb', OrderedDict([
    #     ('x', 0),
    #     ('y', 1)
    # ])),
    # ('gc', OrderedDict([
    #     ('x', 1),
    #     ('y', 1)
    # ])),
    # ('gd', OrderedDict([
    #     ('x', 3),
    #     ('y', 0)
    # ]))
])

lof = LOF(coords, LOF.CONST_EUCLIDEAN, 2)
lof.print_all_data()
lof.print_all_data(10)
lof.print_all_lof()
lof.print_lof_sorted_filtered(True)
