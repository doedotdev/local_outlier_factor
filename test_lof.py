from unittest import TestCase
import lof
from collections import OrderedDict


class TestLOF(TestCase):
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

    def test(self):
        test_lof = lof.LOF(self.coords, lof.LOF.CONST_MANHATTAN, 2)
        test_lof.print_all_lof()
        pass

    def test_manhattan_distance(self):
        assert(lof.get_manhattan_distance(self.coords['a'], self.coords['b']) == 1)
        assert(lof.get_manhattan_distance(self.coords['a'], self.coords['c']) == 2)
        assert(lof.get_manhattan_distance(self.coords['a'], self.coords['d']) == 3)
        assert(lof.get_manhattan_distance(self.coords['a'], self.coords['a']) == 0)

    def test_euclidean_distance(self):
        assert(lof.get_euclidean_distance(self.coords['a'], self.coords['b']) == 1)
        assert(round(lof.get_euclidean_distance(self.coords['a'], self.coords['c']), 3) == 1.414)
        assert(lof.get_euclidean_distance(self.coords['a'], self.coords['d']) == 3)
        assert(lof.get_euclidean_distance(self.coords['a'], self.coords['a']) == 0)

    def test_get_unique_pairs(self):
        test_lof = lof.LOF(self.coords, lof.LOF.CONST_MANHATTAN, 2)
        test_lof.get_unique_pairs()
        pairs = []
        for pair in test_lof.get_unique_pairs():
            pairs.append(pair)
            print(pair)

        assert(len(pairs) == 6)
        assert(pairs[0] == ('a', 'b'))
        assert(pairs[1] == ('a', 'c'))
        assert(pairs[2] == ('a', 'd'))
        assert(pairs[3] == ('b', 'c'))
        assert(pairs[4] == ('b', 'd'))
        assert(pairs[5] == ('c', 'd'))

    def test_get_all_lof(self):
        test_lof = lof.LOF(self.coords, lof.LOF.CONST_MANHATTAN, 2)
        lofs = test_lof.get_all_lof()
        assert(len(lofs) == 4)
        assert(lofs[0] == ('a', 0.8749999999999999))
        assert(lofs[1] == ('b', 1.3333333333333333))
        assert(lofs[2] == ('c', 0.8749999999999999))
        assert(lofs[3] == ('d', 2.0))

    def test_print_all_lof(self):
        test_lof = lof.LOF(self.coords, lof.LOF.CONST_MANHATTAN, 2)
        print(test_lof.print_all_lof())

    def test_print_lof_sorted_filtered_ascending(self):
        test_lof = lof.LOF(self.coords, lof.LOF.CONST_MANHATTAN, 2)
        print(test_lof.print_all_lof())

    def test_get_lof_sorted_filtered_ascending(self):
        test_lof = lof.LOF(self.coords, lof.LOF.CONST_MANHATTAN, 2)
        lofs = test_lof.get_lof_sorted_filtered(False)
        assert(len(lofs) == 4)
        assert(lofs[0] == ('a', 0.8749999999999999))
        assert(lofs[2] == ('b', 1.3333333333333333))
        assert(lofs[1] == ('c', 0.8749999999999999))
        assert(lofs[3] == ('d', 2.0))

    def test_get_lof_sorted_filtered_descending(self):
        test_lof = lof.LOF(self.coords, lof.LOF.CONST_MANHATTAN, 2)
        lofs = test_lof.get_lof_sorted_filtered(True)
        assert(len(lofs) == 4)
        assert(lofs[2] == ('a', 0.8749999999999999))
        assert(lofs[1] == ('b', 1.3333333333333333))
        assert(lofs[3] == ('c', 0.8749999999999999))
        assert(lofs[0] == ('d', 2.0))

    def test_get_lof_sorted_filtered_ascending_filtered(self):
        test_lof = lof.LOF(self.coords, lof.LOF.CONST_MANHATTAN, 2)
        lofs = test_lof.get_lof_sorted_filtered(False, 1, 2)
        assert(len(lofs) == 1)
        assert(lofs[0] == ('b', 1.3333333333333333))

    def test_get_lof_sorted_filtered_descending_filtered(self):
        test_lof = lof.LOF(self.coords, lof.LOF.CONST_MANHATTAN, 2)
        lofs = test_lof.get_lof_sorted_filtered(True, 1, 2)
        assert(len(lofs) == 1)
        assert(lofs[0] == ('b', 1.3333333333333333))

    def test_get_lof_sorted_filtered_ascending_filtered_range(self):
        test_lof = lof.LOF(self.coords, lof.LOF.CONST_MANHATTAN, 2)
        lofs = test_lof.get_lof_sorted_filtered(False, 0, 2)
        assert(len(lofs) == 3)
        assert(lofs[0] == ('a', 0.8749999999999999))
        assert(lofs[2] == ('b', 1.3333333333333333))
        assert(lofs[1] == ('c', 0.8749999999999999))

    def test_get_lof_sorted_filtered_descending_filtered_range(self):
        test_lof = lof.LOF(self.coords, lof.LOF.CONST_MANHATTAN, 2)
        lofs = test_lof.get_lof_sorted_filtered(True, 0, 2)
        assert(len(lofs) == 3)
        assert(lofs[1] == ('a', 0.8749999999999999))
        assert(lofs[0] == ('b', 1.3333333333333333))
        assert(lofs[2] == ('c', 0.8749999999999999))

    def test_init_with_coords_input_as_ordered_dict(self):
        coords_as_ordered_dict = OrderedDict([
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

        test_lof = lof.LOF(coords_as_ordered_dict, lof.LOF.CONST_MANHATTAN, 2)
        lofs = test_lof.get_all_lof()
        assert(len(lofs) == 4)
        assert(lofs[0] == ('a', 0.8749999999999999))
        assert(lofs[1] == ('b', 1.3333333333333333))
        assert(lofs[2] == ('c', 0.8749999999999999))
        assert(lofs[3] == ('d', 2.0))

    def test_init_with_coords_input_as_x_and_y_array(self):
        x = [0, 0, 1, 3]
        y = [0, 1, 1, 0]
        coords_as_x_and_y_array = [x, y]

        test_lof = lof.LOF(coords_as_x_and_y_array, lof.LOF.CONST_MANHATTAN, 2)
        lofs = test_lof.get_all_lof()
        assert(len(lofs) == 4)
        assert(lofs[0] == ('coord_0_x_0_y_0', 0.8749999999999999))
        assert(lofs[1] == ('coord_1_x_0_y_1', 1.3333333333333333))
        assert(lofs[2] == ('coord_2_x_1_y_1', 0.8749999999999999))
        assert(lofs[3] == ('coord_3_x_3_y_0', 2.0))

    def test_init_with_coords_input_as_array_of_tuples(self):
        coords_as_array_of_tuples = [(0, 0), (0, 1), (1, 1), (3, 0)]

        test_lof = lof.LOF(coords_as_array_of_tuples, lof.LOF.CONST_MANHATTAN, 2)
        lofs = test_lof.get_all_lof()
        assert(len(lofs) == 4)
        assert(lofs[0] == ('coord_0_x_0_y_0', 0.8749999999999999))
        assert(lofs[1] == ('coord_1_x_0_y_1', 1.3333333333333333))
        assert(lofs[2] == ('coord_2_x_1_y_1', 0.8749999999999999))
        assert(lofs[3] == ('coord_3_x_3_y_0', 2.0))

    def test_init_with_coords_input_from_csv_file_name(self):

        test_lof = lof.LOF('test.csv', lof.LOF.CONST_MANHATTAN, 2)
        lofs = test_lof.get_all_lof()
        assert(len(lofs) == 4)
        assert(lofs[0] == ('coord_0_x_0_y_0', 0.8749999999999999))
        assert(lofs[1] == ('coord_1_x_0_y_1', 1.3333333333333333))
        assert(lofs[2] == ('coord_2_x_1_y_1', 0.8749999999999999))
        assert(lofs[3] == ('coord_3_x_3_y_0', 2.0))


#
# coords_as_array_of_tuples = [(0, 0), (0, 1), (1, 1), (3, 0)]
# lof3 = LOF(coords_as_array_of_tuples, LOF.CONST_MANHATTAN, 2)
#
# coords_from_csv_file_name = 'test_copy.csv'
# lof4 = LOF(coords_from_csv_file_name, LOF.CONST_MANHATTAN, 2)
#
# # lof = LOF(coords, LOF.CONST_MANHATTAN, 2)
# # # lof.print_all_data()
# # # # lof.print_all_data(10)
# # lof.print_all_lof()
# # # # lof.print_lof_sorted_filtered(True)






