import csv
import tempfile
import unittest
import zipfile
from pathlib import Path
from audit_variables import blocks, catalog, profile, source_text


class AuditTests(unittest.TestCase):
    def test_zip_reader(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'source.zip'
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr('data.csv', 'id,value\n1,2\n')
            with source_text(path) as f:
                self.assertEqual(f.read(), 'id,value\n1,2\n')

    def test_blocks_and_selection(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'fixture.cdb'
            p.write_text('R00001.00    [PUBID]    Survey Year: 1997\n  PRIMARY VARIABLE\n\n ID\n'
                         'R98602.00    [TRANS_MATHPIPE]    Survey Year: HSTR\n  PRIMARY VARIABLE\n\n MATH PIPELINE\n')
            self.assertEqual(len(list(blocks(p))), 2)
            selected, _ = catalog(p)
            self.assertEqual(len(selected), 2)
            self.assertEqual(selected[1]['wave'], 'HSTR')

    def test_profile_keeps_special_codes_separate(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            core, data = root/'core.csv', root/'raw.csv'
            core.write_text('PUBID_1997,IS_BLACK_FEMALE\n1,1\n2,1\n3,0\n')
            data.write_text('R0000100,R9864600\n1,-7\n2,100\n3,900\n')
            refs = [{'reference':'R00001.00','question':'PUBID'},
                    {'reference':'R98646.00','question':'TRANS_TOT_ADV_MATH'}]
            result = profile(data, refs, core)[1]
            self.assertEqual(result['denominator'], 2)
            self.assertEqual(result['negative_code_counts'], {'-7':1})
            self.assertEqual(result['nonnegative_count_not_validity'], 1)

    def test_missing_focal_id_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            core, data = root/'core.csv', root/'raw.csv'
            core.write_text('PUBID_1997,IS_BLACK_FEMALE\n1,1\n2,1\n')
            data.write_text('R0000100\n1\n')
            with self.assertRaises(ValueError):
                profile(data, [{'reference':'R00001.00','question':'PUBID'}], core)


if __name__ == '__main__':
    unittest.main()
