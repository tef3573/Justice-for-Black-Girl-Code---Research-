import unittest
from build_age_panel import construct


def row(pid=1, **ages):
    return {'PUBID_1997': str(pid), 'KEY_SEX_1997': '2',
            'KEY_RACE_ETHNICITY_1997': '1', 'IS_BLACK_FEMALE': '1', **ages}


class PanelTests(unittest.TestCase):
    def test_boundaries_missing_and_duplicate(self):
        fields = [f'CV_AGE_INT_DATE_{y}' for y in range(1997, 2003)]
        r = row(**dict(zip(fields, ['14', '15', '15', '23', '24', '-5'])))
        panel, duplicates, coverage, reversals, summary = construct([r], fields)
        self.assertEqual([p['age'] for p in panel], [15, 23])
        self.assertEqual(panel[0]['survey_round'], 3)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(coverage[0]['internal_gap_count'], 7)
        self.assertEqual(summary['missing_age_codes_all_rounds'], {'-5': 1})
        self.assertFalse(reversals)

    def test_no_eligible_observation(self):
        fields = ['CV_AGE_INT_DATE_1997']
        result = construct([row(CV_AGE_INT_DATE_1997='14')], fields)
        self.assertEqual(result[4]['panel_respondents'], 0)
        self.assertEqual(result[2][0]['observed_ages'], 0)

    def test_duplicate_id_rejected(self):
        r = row(CV_AGE_INT_DATE_1997='15')
        with self.assertRaises(ValueError):
            construct([r, r], ['CV_AGE_INT_DATE_1997'])

    def test_flag_mismatch_rejected(self):
        r = row(CV_AGE_INT_DATE_1997='15')
        r['IS_BLACK_FEMALE'] = '0'
        with self.assertRaises(ValueError):
            construct([r], ['CV_AGE_INT_DATE_1997'])

    def test_reversal_flagged(self):
        r = row(CV_AGE_INT_DATE_1997='17', CV_AGE_INT_DATE_1998='16')
        self.assertEqual(len(construct([r], ['CV_AGE_INT_DATE_1997', 'CV_AGE_INT_DATE_1998'])[3]), 1)

    def test_nonfocal_excluded(self):
        r = row(CV_AGE_INT_DATE_1997='15')
        r.update(KEY_SEX_1997='1', IS_BLACK_FEMALE='0')
        self.assertEqual(construct([r], ['CV_AGE_INT_DATE_1997'])[4]['focal_respondents'], 0)


if __name__ == '__main__':
    unittest.main()
