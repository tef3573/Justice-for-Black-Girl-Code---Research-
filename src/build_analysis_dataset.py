"""Build and audit the age-23 analysis dataset."""

from collections import Counter, defaultdict


_CIVILIAN_EMPLOYMENT_STATUSES = {"employed", "unemployed", "not_in_labor_force"}
_AUDITED_FIELDS = (
    "socioeconomic_risk_index",
    "transcript_collected",
    "math_pipeline_level",
    "science_pipeline_level",
    "attainment_level",
    "employment_status",
    "positive_labor_earnings",
    "labor_earnings_2025_dollars",
)


def _text(value):
    return "" if value is None else str(value).strip()


def _present(value):
    return int(bool(_text(value)))


def _demographic_mismatch(left, right):
    for key in ("race_ethnicity_group", "race_gender_group"):
        lv = _text(left.get(key))
        rv = _text(right.get(key))
        if lv and rv and lv != rv:
            return True
    return False


def eligible_flags(row):
    employment_status = _text(row.get("employment_status"))
    positive_earnings = _text(row.get("positive_labor_earnings"))
    exact_earnings = _present(row.get("labor_earnings_2025_dollars"))
    return {
        "has_socioeconomic_risk_index": _present(row.get("socioeconomic_risk_index")),
        "has_transcript": int(_text(row.get("transcript_collected")) == "1"),
        "eligible_attainment_complete_case": _present(row.get("attainment_level")),
        "eligible_employment_complete_case": int(employment_status in _CIVILIAN_EMPLOYMENT_STATUSES),
        "eligible_earnings_part1_complete_case": int(positive_earnings in {"0", "1"}),
        "eligible_earnings_part2_complete_case": int(positive_earnings == "1" and exact_earnings == 1),
    }


def merge(outcome_rows, socioeconomic_by_id, stem_by_id):
    merged_rows = []
    seen = set()
    for row in outcome_rows:
        respondent_id = _text(row.get("respondent_id"))
        if not respondent_id or respondent_id in seen:
            raise ValueError("Invalid or duplicate respondent_id")
        if _text(row.get("age")) != "23":
            raise ValueError("Outcome rows must be age 23")
        seen.add(respondent_id)

        merged = dict(row)
        for source in (socioeconomic_by_id.get(respondent_id), stem_by_id.get(respondent_id)):
            if not source:
                continue
            if _demographic_mismatch(merged, source):
                raise ValueError("Demographic mismatch across merge inputs")
            for key, value in source.items():
                if key not in {"respondent_id", "race_ethnicity_group", "race_gender_group"}:
                    merged[key] = value

        merged["socioeconomic_match"] = int(respondent_id in socioeconomic_by_id)
        merged["stem_match"] = int(respondent_id in stem_by_id)
        merged.update(eligible_flags(merged))
        merged_rows.append(merged)
    return merged_rows


def missingness_tables(rows):
    group_counts = defaultdict(Counter)
    pattern_counts = Counter()

    for row in rows:
        group = _text(row.get("race_gender_group")) or _text(row.get("race_ethnicity_group")) or "unknown"
        group_counts[group]["respondents"] += 1

        missing_fields = []
        for field in _AUDITED_FIELDS:
            value = _text(row.get(field))
            missing = value == ""
            if field == "labor_earnings_2025_dollars" and _text(row.get("positive_labor_earnings")) != "1":
                missing = False
            if missing:
                group_counts[group][f"missing_{field}"] += 1
                missing_fields.append(field)

        pattern = "complete_on_audited_fields" if not missing_fields else "missing:" + ",".join(missing_fields)
        pattern_counts[pattern] += 1

    groups = [
        {"group": group, **dict(sorted(counts.items()))}
        for group, counts in sorted(group_counts.items())
    ]
    patterns = [
        {"missingness_pattern": pattern, "respondents": count}
        for pattern, count in sorted(pattern_counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    return groups, patterns
