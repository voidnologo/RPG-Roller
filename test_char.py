import unittest
from unittest import mock

from char import *  # noqa F403


class CharTests(unittest.TestCase):

    def setUp(self):
        self.char = {
            'attributes': {
                'strength': 5
            },
            'skills': {
                'pistols': 6
            },
            'pools': {
                'combat': 6
            },
            'meta': {
                'perception': 5,
                'physical_damage': 0,
                'stun_damage': 4
            }
        }

    def test_roll(self):
        results = list(roll(5))
        self.assertEqual(5, len(results))

    @unittest.mock.patch('random.randint')
    def test_roll_implements_rule_of_six(self, rand):
        rand.side_effect = [6, 3]
        results = list(roll(1))
        self.assertEqual(results, [9])

    def test_can_roll_for_attribute(self):
        results = roll_attribute('strength')
        self.assertEqual(5, len(list(results)))

    def test_can_roll_for_skills(self):
        results = roll_skill('pistols')
        self.assertEqual(6, len(list(results)))

    def test_can_roll_for_pool(self):
        results = roll_pool('combat')
        self.assertEqual(6, len(list(results)))



if __name__ == '__main__':
    unittest.main()
