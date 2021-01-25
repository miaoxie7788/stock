import unittest

from ta_strategy.eval import eval_increase


class TestEvaluate(unittest.TestCase):

    def test_eval_increase(self):
        y = [5.5, 5.35, 5.4, 5.55, 5.7]
        is_increase, significance, max_increase = eval_increase(y)

        # print(is_increase, significance, max_increase)
        self.assertEqual(is_increase, True)


if __name__ == '__main__':
    unittest.main()
