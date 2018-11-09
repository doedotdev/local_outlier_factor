from itertools import combinations
from math import sqrt
from json import dumps
from collections import OrderedDict
from operator import itemgetter


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



        # calculate each ones kth nearest

        print(dumps(self.coordinates, indent=4, sort_keys=True))

        for key, value in self.coordinates.items():
            print(key)
            sorted_list = []
            for sub_key, sub_value in self.coordinates[key]['distances'].items():
                print('-' + str(sub_key))
                print('-' + str(sub_value))

        # TODO: we actually dont need to store an item if it is over the kth item distance away
        # we can discard it and not have to sort though it.
        # TODO: we can actiually instantiate an array of length k and just populate that as items come in
        # and sort it in place

            #
            # "a": {
            #     "distances": {
            #         "b": 3,
            #         "c": 7,
            #         "d": 11
            #     },
            #     "distances": [
            #         "b": 3,
            #         "c": 7,
            #         "d": 11] ,
            #     "x": 0,
            #     "y": 0
            # }


            # self.coordinates[[combo[0]]['dists'][combo[1]]] = dist
            # self.coordinates[[combo[1]]['dists'][combo[0]]] = dist

        #unique_pairs = self.get_unique_pairs()

        #for pair in unique_pairs:

    def write_distance(self, key_1, key_2, distance):
        if 'distances' in self.coordinates[key_1]:
            print('Total Items in Dict: ' + str(len(self.coordinates[key_1]['distances'])))
            if len(self.coordinates[key_1]['distances']) == self.k:
                print('could already be full')
                print(self.coordinates[key_1]['distances'][self.coordinates[key_1]['distances'].keys()[0]])
                if distance > self.coordinates[key_1]['distances'][self.coordinates[key_1]['distances'].keys()[0]]:
                    return
                else:
                    return


            self.coordinates[key_1]['distances'][key_2] = distance
            print('before')
            print(self.coordinates[key_1]['distances'])
            print('after')
            self.coordinates[key_1]['distances'] = \
                dict(OrderedDict(sorted(self.coordinates[key_1]['distances'].items(),
                                        key=itemgetter(1),
                                        reverse=True)))
            print(self.coordinates[key_1]['distances'])
        else:
            self.coordinates[key_1]['distances'] = {}
            self.coordinates[key_1]['distances'][key_2] = distance


    def get_unique_pairs(self):
        return combinations(self.coordinates, 2)

    def get_manhattan_distance(self, point_a, point_b):
        return abs(point_a['x'] - point_b['x']) + abs(point_a['y'] - point_b['y'])

    def get_euclidean_distance(self, point_a, point_b):
        return sqrt((point_a[x] - point_b[x])**2 + abs(point_a[y] - point_b[y])**2)


data = [(1, 5), (2, 6), (3, 7), (4, 8), (123, 321)]


coords = {
    "a": {
        "x": 0,
        "y": 0
    },
    "b": {
        "x": 1,
        "y": 2,
    },
    "c": {
        "x": 3,
        "y": 4,
    },
    "d": {
        "x": 5,
        "y": 6,
    }
}

lof = LOF(coords, 'hello', 2)

# dicty =  {
#     "distances": {
#         "b": 3,
#         "c": 15,
#         "d": 11
#     }
# }
# temp_dict = dicty['distances']
# print(temp_dict)
#
# print(dict(OrderedDict(sorted(temp_dict.items(), key=itemgetter(1), reverse=False))))



# DIFFERENT WAYS TO REPRESENT DATA
# datax = [1, 2, 3, 4]
# datay = [5, 6, 7, 8]
# data = zip(datax, datay)
# print(list(data))
# print(abs(-4))