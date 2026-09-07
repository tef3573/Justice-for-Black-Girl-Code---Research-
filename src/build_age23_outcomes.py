"""Build age-23 attainment, employment-access, and earnings outcomes."""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
import zipfile
from collections import Counter
from datetime import date
from pathlib import Path


HEADER = re.compile(r'^([A-Z]\d{5}\.\d{2})\s+\[([^]]+)\]\s+Survey Year:\s+(\S+)')
MISSING = {-1: "refusal", -2: "dont_know", -3: "invalid_skip",
           -4: "valid_skip", -5: "noninterview"}
YEARS = range(2002, 2009)


def codebook_catalog(path: Path):
    catalog = {}
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            match = HEADER.match(line)
            if match:
                ref, question, wave = match.groups()
                catalog[(question, wave)] = ref.replace(".", "")
    return catalog


def choose(catalog, year, *questions):
    for question in questions:
        ref = catalog.get((question, str(year)))
        if ref:
            return ref
    raise KeyError(f"No codebook reference for {year}: {questions}")


def variable_map(catalog):
    result = {}
    for year in YEARS:
        result[year] = {
            "hgc": choose(catalog, year, "CV_HGC_EVER_EDT", "CV_HGC_EVER"),
            "degree": choose(catalog, year, "CV_HIGHEST_DEGREE_EVER_EDT", "CV_HIGHEST_DEGREE_EVER"),
            "enrollment": choose(catalog, year, "CV_ENROLLSTAT_EDT", "CV_ENROLLSTAT"),
            "interview_month": choose(catalog, year, "CV_INTERVIEW_DATE~M", "CV_INTERVIEW_DATE_M"),
            "interview_year": choose(catalog, year, "CV_INTERVIEW_DATE~Y", "CV_INTERVIEW_DATE_Y"),
            "wage_receipt": choose(catalog, year, "YINC-1400"),
            "wage_receipt_dk": catalog.get(("YINC-1500", str(year))),
            "wage_receipt_rf": choose(catalog, year, "YINC-1600"),
            "wage_amount": choose(catalog, year, "YINC-1700"),
            "wage_bracket": choose(catalog, year, "YINC-1800"),
            "self_receipt": choose(catalog, year, "YINC-2000"),
            "self_amount": choose(catalog, year, "YINC-2100"),
            "self_bracket": choose(catalog, year, "YINC-2200"),
            "weekly_status": [catalog[(f"EMP_STATUS_{year}.{week:02}", "XRND")]
                              for week in range(1, 53)],
        }
    return result


def integer(raw):
    if raw is None or raw == "":
        return None
    return int(raw)


def observed(raw, allow_negative=False):
    value = integer(raw)
    if value is None or value in MISSING:
        return None
    if value < 0 and not allow_negative:
        return None
    return value


def attainment(hgc_raw, degree_raw, enrollment_raw):
    hgc = observed(hgc_raw)
    degree = observed(degree_raw)
    enrollment = observed(enrollment_raw)
    if hgc == 95:
        hgc = None
    labels = {
        1: (1, "high_school_equivalent_GED"),
        2: (1, "high_school_diploma"),
        3: (3, "associate_degree"),
        4: (4, "bachelors_degree"),
        5: (5, "graduate_or_professional_degree"),
        6: (5, "graduate_or_professional_degree"),
        7: (5, "graduate_or_professional_degree"),
    }
    if degree in (0, 1, 2) and hgc is not None and hgc >= 13:
        level, label = 2, "some_college_no_degree"
    elif degree in labels:
        level, label = labels[degree]
    elif degree == 0 and hgc is not None:
        if hgc >= 13:
            level, label = 2, "some_college_no_degree"
        else:
            level, label = 0, "no_high_school_credential"
    else:
        level, label = None, None
    enrolled_postsecondary = None if enrollment is None else int(enrollment in (9, 10, 11))
    return hgc, degree, enrollment, level, label, enrolled_postsecondary


def weekly_class(value):
    if value is None or value in MISSING or value in (0, 3):
        return "unknown"
    if value == 4:
        return "unemployed"
    if value in (1, 5):
        return "not_in_labor_force"
    if value == 2:
        return "indeterminate_not_working"
    if value == 6:
        return "active_military"
    if value >= 9701:
        return "employed"
    return "unknown"


def employment(month_raw, year_raw, weekly_raw):
    month, interview_year = observed(month_raw), observed(year_raw)
    classes = [weekly_class(integer(v)) for v in weekly_raw]
    known = [v for v in classes if v != "unknown"]
    counts = Counter(known)
    midpoint = None
    if month and interview_year:
        week = min(date(interview_year, month, 15).isocalendar().week, 52)
        midpoint = classes[week - 1]
        if midpoint == "unknown":
            midpoint = None
    denominator = len(known)
    proportions = {name: (counts[name] / denominator if denominator else None)
                   for name in ("employed", "unemployed", "not_in_labor_force",
                                "active_military", "indeterminate_not_working")}
    return midpoint, week if month and interview_year else None, denominator, proportions


def routed_component(receipt_raw, amount_raw, bracket_raw, dk_raw=None, rf_raw=None,
                     allow_negative=False):
    receipt = integer(receipt_raw)
    amount = observed(amount_raw, allow_negative=allow_negative)
    bracket = observed(bracket_raw)
    routed = receipt
    if receipt == -2 and dk_raw is not None and integer(dk_raw) in (0, 1):
        routed = integer(dk_raw)
    if receipt == -1 and rf_raw is not None and integer(rf_raw) in (0, 1):
        routed = integer(rf_raw)
    if routed == 0:
        return 0, 0, "routed_zero", bracket
    if routed == 1:
        if amount is not None:
            return amount, int(amount > 0), "exact_amount", bracket
        if bracket is not None:
            return None, 1, "bracket_only", bracket
        return None, 1, "positive_amount_missing", None
    return None, None, MISSING.get(receipt, "unresolved"), bracket


def earnings(values, cpi, survey_year):
    wage = routed_component(values["wage_receipt"], values["wage_amount"],
                            values["wage_bracket"], values.get("wage_receipt_dk"),
                            values["wage_receipt_rf"])
    self_emp = routed_component(values["self_receipt"], values["self_amount"],
                                values["self_bracket"], allow_negative=True)
    exact_total = None
    if wage[0] is not None and self_emp[0] is not None:
        exact_total = wage[0] + self_emp[0]
    positive = 1 if 1 in (wage[1], self_emp[1]) else (
        0 if wage[1] == 0 and self_emp[1] == 0 else None)
    income_year = survey_year - 1
    factor = cpi[2025] / cpi[income_year]
    real_total = None if exact_total is None else round(exact_total * factor, 2)
    log_positive = math.log(real_total) if real_total is not None and real_total > 0 else None
    return wage, self_emp, exact_total, positive, income_year, factor, real_total, log_positive


def source_text(path):
    if path.suffix.lower() == ".zip":
        archive = zipfile.ZipFile(path)
        member = next(n for n in archive.namelist() if n.endswith(".csv"))
        raw = archive.open(member)
        return archive, io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
    return None, path.open(encoding="utf-8-sig", newline="")


def build(panel_path, source_path, codebook_path, cpi_path, output_path, validation_path):
    with panel_path.open(encoding="utf-8-sig", newline="") as handle:
        panel = [r for r in csv.DictReader(handle) if int(r["age"]) == 23]
    by_id = {int(r["respondent_id"]): r for r in panel}
    if len(by_id) != len(panel):
        raise ValueError("Age-23 panel must have one row per respondent")
    mappings = variable_map(codebook_catalog(codebook_path))
    cpi_doc = json.loads(cpi_path.read_text())
    cpi = {int(k): float(v) for k, v in cpi_doc["annual_average"].items()}
    archive, handle = source_text(source_path)
    try:
        reader = csv.reader(handle)
        positions = {ref: i for i, ref in enumerate(next(reader))}
        id_pos = positions["R0000100"]
        results = []
        for raw in reader:
            pid = int(raw[id_pos])
            p = by_id.get(pid)
            if not p:
                continue
            year = int(p["survey_year"])
            refs = mappings[year]
            get = lambda name: raw[positions[refs[name]]] if refs.get(name) else None
            hgc, degree, enroll, att_level, att_label, enrolled = attainment(
                get("hgc"), get("degree"), get("enrollment"))
            weekly = [raw[positions[ref]] for ref in refs["weekly_status"]]
            emp, emp_week, weeks_known, props = employment(
                get("interview_month"), get("interview_year"), weekly)
            income_values = {name: get(name) for name in (
                "wage_receipt", "wage_receipt_dk", "wage_receipt_rf", "wage_amount",
                "wage_bracket", "self_receipt", "self_amount", "self_bracket")}
            wage, self_emp, total, positive, income_year, factor, real, logged = earnings(
                income_values, cpi, year)
            results.append({
                "respondent_id": pid, "age": 23, "survey_year": year,
                "survey_round": p["survey_round"],
                "race_ethnicity_group": p["race_ethnicity_group"],
                "race_gender_group": p["race_gender_group"],
                "highest_grade_completed": hgc, "highest_degree_code": degree,
                "enrollment_status_code": enroll, "attainment_level": att_level,
                "attainment_category": att_label, "enrolled_postsecondary": enrolled,
                "employment_status": emp, "employment_proxy_week": emp_week,
                "employment_weeks_known": weeks_known,
                "proportion_year_employed": props["employed"],
                "proportion_year_unemployed": props["unemployed"],
                "proportion_year_not_in_labor_force": props["not_in_labor_force"],
                "proportion_year_active_military": props["active_military"],
                "proportion_year_indeterminate_not_working": props["indeterminate_not_working"],
                "wage_salary_nominal": wage[0], "wage_salary_positive": wage[1],
                "wage_salary_status": wage[2], "wage_salary_bracket": wage[3],
                "self_employment_nominal": self_emp[0], "self_employment_positive": self_emp[1],
                "self_employment_status": self_emp[2], "self_employment_bracket": self_emp[3],
                "labor_earnings_nominal": total, "positive_labor_earnings": positive,
                "earnings_reference_year": income_year,
                "cpi_u_to_2025_factor": round(factor, 8),
                "labor_earnings_2025_dollars": real,
                "log_positive_labor_earnings_2025": logged,
            })
    finally:
        handle.close()
        if archive:
            archive.close()
    if len(results) != len(panel):
        raise ValueError(f"Expected {len(panel)} age-23 respondents; extracted {len(results)}")
    results.sort(key=lambda r: r["respondent_id"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]))
        writer.writeheader(); writer.writerows(results)
    summary = {
        "age23_panel_respondents": len(panel),
        "output_respondents": len(results),
        "attainment_observed": sum(r["attainment_category"] is not None for r in results),
        "employment_status_observed": sum(r["employment_status"] is not None for r in results),
        "positive_earnings_status_observed": sum(r["positive_labor_earnings"] is not None for r in results),
        "exact_labor_earnings_observed": sum(r["labor_earnings_nominal"] is not None for r in results),
        "attainment_counts": dict(Counter(str(r["attainment_category"]) for r in results)),
        "employment_counts": dict(Counter(str(r["employment_status"]) for r in results)),
        "wage_status_counts": dict(Counter(r["wage_salary_status"] for r in results)),
        "self_employment_status_counts": dict(Counter(r["self_employment_status"] for r in results)),
        "earnings_price_basis": "2025 CPI-U annual average",
        "earnings_reference_period": "previous calendar year (survey year minus one)",
        "employment_definition": "weekly status for week containing 15th of interview month; active military separated from civilian employment; proxy for interview-date status",
        "source_topcoding": "NLSY97 source topcoded/truncated values retained; individual topcode flags unavailable",
        "validation": "PASS",
    }
    validation_path.parent.mkdir(parents=True, exist_ok=True)
    validation_path.write_text(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--panel", type=Path, default=Path("data/interim/nlsy97_comparison_age15_23.csv"))
    p.add_argument("--source", type=Path, default=Path("data/raw/nlsy97_all_1997-2023.zip"))
    p.add_argument("--codebook", type=Path, default=Path("data/raw/nlsy97_all_1997-2023/nlsy97_all_1997-2023.cdb"))
    p.add_argument("--cpi", type=Path, default=Path("config/cpi_u_annual.json"))
    p.add_argument("--output", type=Path, default=Path("data/processed/age23_outcomes.csv"))
    p.add_argument("--validation", type=Path, default=Path("outputs/tables/age23_outcomes_validation.json"))
    a = p.parse_args()
    print(json.dumps(build(a.panel, a.source, a.codebook, a.cpi, a.output, a.validation), indent=2))
