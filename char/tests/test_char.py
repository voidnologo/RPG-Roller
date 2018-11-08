from pathlib import Path
import unittest
from unittest import mock

import char.character


class CharTests(unittest.TestCase):

    def setUp(self):
        fpath = Path(__file__).resolve().parent.joinpath(Path('data', 'tommy_talon.char'))
        stats = char.character.read_character(fpath)
        setattr(char.character, 'stats', stats)

    def test_roll(self):
        results = list(char.character.roll(5))
        self.assertEqual(5, len(results))

    @unittest.mock.patch('random.randint')
    def test_roll_implements_rule_of_six(self, rand):
        rand.side_effect = [6, 3]
        results = list(char.character.roll(1))
        self.assertEqual(results, [9])

    def test_can_roll_for_attribute(self):
        results = char.character.roll_stat('strength')
        self.assertEqual(5, len(list(results)))

    def test_can_roll_for_skills(self):
        results = char.character.roll_stat('pistols')
        self.assertEqual(6, len(list(results)))

    def test_can_roll_for_pool(self):
        results = char.character.roll_stat('combat')
        self.assertEqual(6, len(list(results)))

    def test_returns_empty_list_if_stat_not_found(self):
        results = char.character.roll_stat('definitely_not_there')
        self.assertEqual(0, len(list(results)))

    # def test_can_read_in_character(self):
    #     fpath = Path(__file__).resolve().parent.joinpath(Path('data', 'tommy_talon.char'))
    #     stats = char.character.read_character(fpath)
    #     expected = {
    #         "attributes": {
    #             "strength": 5
    #         },
    #         "skills": {
    #             "pistols": 6
    #         },
    #         "pools": {
    #             "combat": 6,
    #             "initiative": {
    #                 "base": 2,
    #                 "rule_of_six": False,
    #                 "offset": 9
    #             }
    #         },
    #         "health": {
    #             "physical_damage": 0,
    #             "stun_damage": 4
    #         }
    #     }
    #     self.assertEqual(stats, expected)

    @unittest.mock.patch('random.randint')
    def test_initiative_adds_offset(self, rand):
        rand.side_effect = [3, 3]
        results = list(char.character.roll_stat('initiative'))
        self.assertEqual(1, len(results))
        self.assertEqual(15, results[0])

    @unittest.mock.patch('random.randint')
    def test_initiative_does_not_use_rule_of_six(self, rand):
        rand.side_effect = [6, 3]
        results = list(char.character.roll_stat('initiative'))
        self.assertEqual(1, len(results))
        self.assertEqual(18, results[0])


if __name__ == '__main__':
    unittest.main()
