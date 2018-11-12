from itertools import combinations
from math import sqrt
from json import dumps
from collections import OrderedDict


class LOF:
    CONST_MANHATTAN = 'Manhattan'

    def __init__(self, coordinates, distance_formula, k):
        self.distance_formula = distance_formula
        self.coordinates = coordinates
        self.k = k

        # get all unique pairs
        self.combos = combinations(self.coordinates, 2)

        # get distance between all
        for combo in self.combos:
            distance = self.get_manhattan_distance(self.coordinates[combo[0]], self.coordinates[combo[1]])
            self.write_distance(combo[0], combo[1], distance)
            self.write_distance(combo[1], combo[0], distance)

        print()

        for coord_key in self.coordinates:
            self.write_k_nearest_set(coord_key)
            self.write_k_nearest_neighbor(coord_key)

        for coord_key in self.coordinates:
            self.get_local_reachability_distance(coord_key)

        for coord_key in self.coordinates:


        print(dumps(self.coordinates, indent=4))


        # TODO: we actually dont need to store an item if it is over the kth item distance away
        # we can discard it and not have to sort though it.
        # TODO: we can actiually instantiate an array of length k and just populate that as items come in
        # and sort it in place

    def calculate_final_lof(self, coord):
    #     [LRD(b) + LRD(c)] * [reachDist(b < - a) + reachDist(c < - a)]
    #
    # LOF(a) = ----------------------------------------------------------
    # kNearestSetCount(a) * kNearestSetCount(a)



    def get_reach_distance(self, coord_one, coord_two):
        return max(self.coordinates[coord_one]['k_nearest_value'],
                   self.get_manhattan_distance(self.coordinates[coord_one], self.coordinates[coord_two]))

    def get_local_reachability_distance(self, coord):
        neighbors = self.coordinates[coord]['distances']
        print(neighbors)
        reach_distance_sum = 0
        for neighbor in neighbors:
            print(neighbor)
            reach_distance_sum = reach_distance_sum + self.get_reach_distance(neighbor, coord)

        self.coordinates[coord]['local_reachability_distance'] = \
            len(self.coordinates[coord]['distances'])/reach_distance_sum

    def write_k_nearest_neighbor(self, coord):
        # write neighbor and value
        k_nearest_neighbor = list(self.coordinates[coord]['distances'].keys())[self.k-1]
        k_nearest_value = self.coordinates[coord]['distances'][k_nearest_neighbor]
        self.coordinates[coord]['k_nearest_neighbor'] = k_nearest_neighbor
        self.coordinates[coord]['k_nearest_value'] = k_nearest_value


    def write_k_nearest_set(self, coord):
        return

    def write_distance(self, key_1, key_2, distance):
        if 'distances' in self.coordinates[key_1]:
            if len(self.coordinates[key_1]['distances']) == self.k:
                # print('could already be full')
                if distance > list(self.coordinates[key_1]['distances'].values())[0]:
                    # print('no need to insert')
                    return
                else:
                    # print('insert and pop uneeded off')
                    return
            else:
                # normal insert
                if key_2 in self.coordinates[key_1]['distances']:
                    print('if key is already in, update it')
                    self.coordinates[key_1]['distances'][key_2] = distance
                    self.coordinates[key_1]['distances'] = \
                        OrderedDict(sorted(self.coordinates[key_1]['distances'].items(), key=lambda x: x[1]))
                else:
                    # print('key doesnt exist, sort it in')
                    self.coordinates[key_1]['distances'][key_2] = distance
                    self.coordinates[key_1]['distances'] = \
                        OrderedDict(sorted(self.coordinates[key_1]['distances'].items(), key=lambda x: x[1]))
        else:
            self.coordinates[key_1]['distances'] = {}
            self.write_distance(key_1, key_2, distance)

    def get_unique_pairs(self):
        return combinations(self.coordinates, 2)

    def get_manhattan_distance(self, point_a, point_b):
        return abs(point_a['x'] - point_b['x']) + abs(point_a['y'] - point_b['y'])

    def get_euclidean_distance(self, point_a, point_b):
        return sqrt((point_a[x] - point_b[x]) ** 2 + abs(point_a[y] - point_b[y]) ** 2)


data = [(1, 5), (2, 6), (3, 7), (4, 8), (123, 321)]

# coords = {
#     "a": {
#         "x": 0,
#         "y": 0
#     },
#     "b": {
#         "x": 1,
#         "y": 2,
#     },
#     "c": {
#         "x": 3,
#         "y": 4,
#     },
#     "d": {
#         "x": 5,
#         "y": 6,
#     }
# }

# coords = OrderedDict([
#     ('a', {'x': 0, 'y': 0}),
#     ('b', {'x': 1, 'y': 2}),
#     ('c', {'x': 3, 'y': 4}),
#     ('d', {'x': 5, 'y': 6})
# ])

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
])

# temp = coords['a']
# print(dumps(temp, indent=4))
# temp = OrderedDict(sorted(temp.items(), key=lambda x: x[1]))

# print(dumps(temp, indent=4))
#
# print(sorted(coords.items(), key=lambda x: x[1].items()))
#
# temp = OrderedDict([
#     ('a', 4),
#     ('b', 2),
#     ('c', 3)
# ])

# # sort ordered dict by values
# print(sorted(temp.items(), key=lambda x: x[1]))
#
# # sort ordered dict by keys
# print(sorted(temp.items(), key=lambda x: x[0]))

lof = LOF(coords, 'hello', 2)
