"""Day 3: codebook-linked candidate audit. Does not recode or fit models."""
import argparse
import csv
import hashlib
import json
import re
import io
import zipfile
from contextlib import contextmanager
from collections import Counter
from pathlib import Path

HEADER = re.compile(r'^([A-Z]\d{5}\.\d{2})\s+\[([^]]+)\]\s+Survey Year:\s+(\S+)')
STEMS = {
    'STEM coursework': {'TRANS_MATHPIPE', 'TRANS_SCI_PIPE', 'TRANS_PHYS_SCI_PIPE',
        'TRANS_TOT_MATH', 'TRANS_TOT_ADV_MATH', 'TRANS_TOT_LIFE_PHYS_SCI'},
    'Achievement (not quality)': {'TRANS_CRD_GPA_MATH', 'TRANS_CRD_GPA_LP_SCI', 'TRANS_GPA'},
    'Socioeconomic context': {'CV_INCOME_GROSS_YR', 'CV_HH_POV_RATIO', 'CV_HGC_BIO_MOM',
        'CV_HGC_BIO_DAD', 'CV_HGC_RES_MOM', 'CV_HGC_RES_DAD', 'CV_HH_SIZE', 'CV_HH_INCOME_SOURCE'},
    'Attainment': {'CV_HGC_EVER', 'CV_HIGHEST_DEGREE_EVER', 'CV_ENROLLSTAT'},
    'Employment (job-specific hours)': {'CV_HRS_PER_WEEK.01'},
    'Earnings': {'YINC-1400', 'YINC-1500', 'YINC-1600', 'YINC-1700'},
    'Timing and design': {'PUBID', 'CV_INTERVIEW_CMONTH', 'CV_INTERVIEW_DATE_M',
        'CV_INTERVIEW_DATE_Y', 'CV_INTERVIEW_DATE~M', 'CV_INTERVIEW_DATE~Y',
        'SAMPLING_WEIGHT', 'TRANS_STATUS', 'TRANS_PROBFLAG'},
}


def blocks(path):
    current, body = None, []
    with path.open(encoding='utf-8', errors='replace') as f:
        for line_no, line in enumerate(f, 1):
            match = HEADER.match(line)
            if match:
                if current:
                    yield current, ''.join(body)
                current = dict(zip(('reference', 'question', 'wave'), match.groups()))
                current['codebook_line'] = line_no
                body = [line]
            elif current:
                body.append(line)
        if current:
            yield current, ''.join(body)


def catalog(path):
    selected, discovery = [], []
    for meta, body in blocks(path):
        name, wave = meta['question'], meta['wave']
        group = next((g for g, names in STEMS.items() if name in names), None)
        if group and (wave == 'HSTR' or (wave.isdigit() and 1997 <= int(wave) <= 2009)):
            selected.append({**meta, 'construct': group, 'codebook_entry': body,
                'status': 'candidate; timing, eligibility and coding review required'})
        # Discovery candidates are not automatically selected or approved.
        label = ' '.join(body.splitlines()[2:7])
        if re.search(r'MATH|SCIENCE|TUTOR|COUNSEL|TRANSCRIPT.*WEIGHT|TRANSCRIPT.*RECEIV|WKS.*WORK|HRS.*WORK', label, re.I):
            if wave in ('1997', 'HSTR'):
                discovery.append({**meta, 'label_excerpt': label.strip()})
    return selected, discovery


@contextmanager
def source_text(data):
    if data.suffix.lower() == '.zip':
        with zipfile.ZipFile(data) as archive:
            member = next(n for n in archive.namelist() if n.endswith('.csv'))
            with archive.open(member) as raw:
                with io.TextIOWrapper(raw, encoding='utf-8-sig', newline='') as f:
                    yield f
    else:
        with data.open(newline='', encoding='utf-8-sig') as f:
            yield f


def profile(data, candidates, core):
    with core.open(newline='') as f:
        focal = {int(r['PUBID_1997']) for r in csv.DictReader(f) if r['IS_BLACK_FEMALE'] == '1'}
    counts = {r['reference']: Counter() for r in candidates}
    normalize = lambda ref: ref.replace('.', '')
    id_ref = next(r['reference'] for r in candidates if r['question'] == 'PUBID')
    seen = set()
    with source_text(data) as f:
        reader = csv.reader(f)
        positions = {normalize(ref): i for i, ref in enumerate(next(reader))}
        columns = [(r['reference'], positions[normalize(r['reference'])]) for r in candidates]
        id_pos = positions[normalize(id_ref)]
        for row in reader:
            pid = int(row[id_pos])
            if pid not in focal:
                continue
            if pid in seen:
                raise ValueError('Duplicate focal respondent in source')
            seen.add(pid)
            for ref, pos in columns:
                counts[ref][row[pos]] += 1
    if seen != focal:
        raise ValueError('Source does not cover all focal IDs')
    result = []
    for r in candidates:
        values = counts[r['reference']]
        nonnegative = sum(n for v, n in values.items() if v and float(v) >= 0)
        result.append({k: v for k, v in r.items() if k != 'codebook_entry'} | {
            'denominator': len(focal), 'nonnegative_count_not_validity': nonnegative,
            'negative_code_counts': {v: n for v, n in sorted(values.items()) if v and float(v) < 0},
            'blank_count': values.get('', 0)})
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--codebook', type=Path, required=True)
    p.add_argument('--data', type=Path)
    p.add_argument('--core', type=Path, default=Path('data/interim/nlsy97_core_cohort.csv'))
    p.add_argument('--output', type=Path, default=Path('data/interim/day3'))
    p.add_argument('--crosswalk', type=Path)
    args = p.parse_args()
    selected, discovery = catalog(args.codebook)
    if args.crosswalk:
        args.crosswalk.parent.mkdir(parents=True, exist_ok=True)
        args.crosswalk.write_text(json.dumps([{k: v for k, v in r.items() if k != 'codebook_entry'}
                                             for r in selected], indent=2) + '\n')
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'candidate_codebook.json').write_text(json.dumps(selected, indent=2))
    (args.output / 'discovery.json').write_text(json.dumps(discovery, indent=2))
    if args.data:
        profiles = profile(args.data, selected, args.core)
        (args.output / 'candidate_profiles.json').write_text(json.dumps(profiles, indent=2))
    manifest = {'selected_candidates': len(selected), 'by_construct': dict(Counter(r['construct'] for r in selected)),
        'codebook_sha256': hashlib.sha256(args.codebook.read_bytes()).hexdigest(),
        'scope': 'Metadata audit and optional raw availability profiles; no cleaning, imputation or model estimation'}
    (args.output / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))
    for r in selected:
        if r['wave'] in ('1997', 'HSTR'):
            print(r['reference'], r['question'], r['wave'], r['construct'])
