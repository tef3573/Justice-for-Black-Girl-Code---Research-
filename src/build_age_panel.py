"""Build an observed-age cohort scaffold; no outcome imputation or estimation."""
import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def construct(rows, age_fields):
    ids = set()
    focal = []
    candidates = []
    missing = Counter()
    reversals = []
    valid_count = 0
    fields = sorted(age_fields, key=lambda x: int(x.rsplit('_', 1)[1]))
    if not fields:
        raise ValueError('No interview-age fields')
    for row in rows:
        pid = int(row['PUBID_1997'])
        if pid <= 0 or pid in ids:
            raise ValueError('Invalid or duplicate respondent ID')
        ids.add(pid)
        sex, race = int(row['KEY_SEX_1997']), int(row['KEY_RACE_ETHNICITY_1997'])
        if sex not in (1, 2) or race not in (1, 2, 3, 4):
            raise ValueError('Unexpected baseline demographic code')
        flag = int(sex == 2 and race == 1)
        if int(row['IS_BLACK_FEMALE']) != flag:
            raise ValueError('Focal flag disagrees with source demographics')
        if not flag:
            continue
        focal.append(pid)
        previous = None
        for round_no, field in enumerate(fields, 1):
            value = row[field].strip()
            if not value or int(value) < 0:
                missing[value or 'blank'] += 1
                continue
            age = int(value)
            if not 0 <= age <= 100:
                raise ValueError('Implausible age')
            valid_count += 1
            year = int(field.rsplit('_', 1)[1])
            if previous is not None and age < previous:
                reversals.append({'respondent_id': pid, 'survey_round': round_no,
                                  'previous_age': previous, 'age': age})
            previous = age
            if 15 <= age <= 23:
                candidates.append({'respondent_id': pid, 'age': age,
                    'survey_round': round_no, 'survey_year': year,
                    'source_age_variable': field, 'baseline_sex': sex,
                    'baseline_race_ethnicity': race})
    grouped = defaultdict(list)
    for record in candidates:
        grouped[record['respondent_id'], record['age']].append(record)
    panel, duplicates = [], []
    for key, records in sorted(grouped.items()):
        kept = max(records, key=lambda r: r['survey_round'])
        panel.append(kept)
        for dropped in records:
            if dropped is not kept:
                duplicates.append({'respondent_id': key[0], 'age': key[1],
                    'dropped_round': dropped['survey_round'],
                    'retained_round': kept['survey_round']})
    by_id = defaultdict(list)
    for record in panel:
        by_id[record['respondent_id']].append(record['age'])
    coverage = []
    for pid in sorted(focal):
        ages = sorted(by_id[pid])
        absent = sorted(set(range(15, 24)) - set(ages))
        coverage.append({'respondent_id': pid, 'observed_ages': len(ages),
            'first_age': min(ages) if ages else '', 'last_age': max(ages) if ages else '',
            'missing_ages': ';'.join(map(str, absent)),
            'internal_gap_count': sum(min(ages) < a < max(ages) for a in absent) if ages else 0,
            'complete_age_coverage': int(len(ages) == 9)})
    return panel, duplicates, coverage, reversals, {
        'source_respondents': len(ids), 'focal_respondents': len(focal),
        'focal_round_slots': len(focal) * len(fields),
        'valid_age_observations_all_ages': valid_count,
        'missing_age_codes_all_rounds': dict(sorted(missing.items())),
        'eligible_observations_before_deduplication': len(candidates),
        'duplicate_age_records_removed': len(duplicates),
        'panel_observations': len(panel), 'panel_respondents': sum(bool(a) for a in by_id.values()),
        'complete_age_trajectories': sum(r['complete_age_coverage'] for r in coverage),
        'age_reversals': len(reversals)}


def build(source, output, reports):
    with source.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fields = [x for x in reader.fieldnames if x.startswith('CV_AGE_INT_DATE_')]
        panel, duplicates, coverage, reversals, summary = construct(list(reader), fields)
    if not panel:
        raise ValueError('Empty panel')
    # Validate before writing. Source age reversals are preserved as audit flags.
    assert len({(r['respondent_id'], r['age']) for r in panel}) == len(panel)
    assert all(15 <= r['age'] <= 23 and r['baseline_sex'] == 2 and r['baseline_race_ethnicity'] == 1 for r in panel)
    assert summary['eligible_observations_before_deduplication'] - len(duplicates) == len(panel)
    summary['source_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
    summary['validation'] = 'PASS (review source age reversal flags)' if reversals else 'PASS'
    write_csv(output / 'nlsy97_black_female_age15_23.csv', list(panel[0]), panel)
    write_csv(output / 'day2_respondent_coverage.csv', list(coverage[0]), coverage)
    write_csv(output / 'day2_duplicate_audit.csv', ['respondent_id', 'age', 'dropped_round', 'retained_round'], duplicates)
    write_csv(output / 'day2_age_reversals.csv', ['respondent_id', 'survey_round', 'previous_age', 'age'], reversals)
    age_counts = Counter(r['age'] for r in panel)
    age_rows = [{'age': a, 'observed_respondents': age_counts[a],
                 'not_observed_of_initial_focal': len(coverage)-age_counts[a]} for a in range(15,24)]
    write_csv(reports / 'day2_age_coverage.csv', list(age_rows[0]), age_rows)
    flow = [{'stage': k, 'count': summary[k]} for k in ('source_respondents', 'focal_respondents',
        'focal_round_slots', 'valid_age_observations_all_ages', 'eligible_observations_before_deduplication',
        'duplicate_age_records_removed', 'panel_observations', 'panel_respondents')]
    write_csv(reports / 'day2_sample_flow.csv', ['stage', 'count'], flow)
    histogram = Counter(r['observed_ages'] for r in coverage)
    write_csv(reports / 'day2_trajectory_coverage.csv', ['observed_ages', 'respondents'],
              [{'observed_ages': n, 'respondents': histogram[n]} for n in range(10)])
    reports.mkdir(parents=True, exist_ok=True)
    (reports / 'day2_validation.json').write_text(json.dumps(summary, indent=2) + '\n')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path('data/interim/nlsy97_core_cohort.csv'))
    parser.add_argument('--output', type=Path, default=Path('data/interim'))
    parser.add_argument('--reports', type=Path, default=Path('outputs/tables'))
    args = parser.parse_args()
    print(json.dumps(build(args.source, args.output, args.reports), indent=2))
