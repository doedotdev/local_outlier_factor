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


