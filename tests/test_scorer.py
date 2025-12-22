import unittest
import sys
import os

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scorer import get_change_score, calculate_raw_score, normalize_to_1_10_scale, determine_risk_level_and_action

class TestScorer(unittest.TestCase):
    
    def test_get_change_score(self):
        self.assertEqual(get_change_score('endpoint-removed'), 25)
        self.assertEqual(get_change_score('parameter-optional-added'), 0)
        self.assertEqual(get_change_score('unknown-change'), 0)

    def test_calculate_raw_score(self):
        diffs = [
            {'type': 'endpoint-removed'},
            {'type': 'parameter-required-added'}
        ]
        # 25 + 15 = 40
        self.assertEqual(calculate_raw_score(diffs), 40)

    def test_normalize_score(self):
        # New max score is 30.
        # 40 / 30 * 10 = 13.33 -> Clamped to 10
        self.assertEqual(normalize_to_1_10_scale(40), 10)
        
        # Max score check
        self.assertEqual(normalize_to_1_10_scale(30), 10)
        self.assertEqual(normalize_to_1_10_scale(500), 10) # cap at 10

        # Small score: 5 / 30 * 10 = 1.66 -> 1.7
        # 5 points (e.g. deprecated w/ timeline)
        self.assertEqual(normalize_to_1_10_scale(5), 1.7)

    def test_risk_level(self):
        info_low = determine_risk_level_and_action(2.0)
        self.assertEqual(info_low['risk_level'], 'LOW')
        
        info_med = determine_risk_level_and_action(5.0)
        self.assertEqual(info_med['risk_level'], 'MEDIUM')
        
        info_high = determine_risk_level_and_action(8.0)
        self.assertEqual(info_high['risk_level'], 'HIGH')

if __name__ == '__main__':
    unittest.main()
