import unittest
from unittest import mock

import character


class CharTests(unittest.TestCase):

    def setUp(self):
        char = {
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
        setattr(character, 'char', char)

    def test_roll(self):
        results = list(character.roll(5))
        self.assertEqual(5, len(results))

    @unittest.mock.patch('random.randint')
    def test_roll_implements_rule_of_six(self, rand):
        rand.side_effect = [6, 3]
        results = list(character.roll(1))
        self.assertEqual(results, [9])

    def test_can_roll_for_attribute(self):
        results = character.roll_stat('strength')
        self.assertEqual(5, len(list(results)))

    def test_can_roll_for_skills(self):
        results = character.roll_stat('pistols')
        self.assertEqual(6, len(list(results)))

    def test_can_roll_for_pool(self):
        results = character.roll_stat('combat')
        self.assertEqual(6, len(list(results)))

    def test_returns_empty_list_if_stat_not_found(self):
        results = character.roll_stat('definitely_not_there')
        self.assertEqual(0, len(list(results)))

    def test_can_read_in_character(self):
        char = character.read_character('data/tommy_talon.char')
        expected = {
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
        self.assertEqual(char, expected)


if __name__ == '__main__':
    unittest.main()
