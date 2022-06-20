import unittest
import worldle


class TestInputBox(unittest.TestCase, worldle.InputBox):
    def test_calculate_distance(self):
        input_box1 = worldle.InputBox(400, 40, 140, 32)
        input_box2 = worldle.InputBox(400, 80, 140, 32)
        input_box1.text = 'Bulgaria'
        input_box2.text = 'Macedonia'
        worldle.CORRECT_COUNTRY = 'Bulgaria'
        self.assertEqual(worldle.calculate_distance(input_box1), "BINGO! You won the game!")
