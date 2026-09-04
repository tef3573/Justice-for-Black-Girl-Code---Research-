"""Create a small demographic and interview-age extract from the NLSY97 archive."""

from __future__ import annotations

import argparse
import csv
import io
import zipfile
from pathlib import Path


CORE_EXACT_NAMES = {
    "PUBID_1997",
    "KEY_SEX_1997",
    "KEY_BDATE_M_1997",
    "KEY_BDATE_Y_1997",
    "CV_SAMPLE_TYPE_1997",
    "KEY_RACE_ETHNICITY_1997",
}
CORE_PREFIXES = ("CV_AGE_INT_DATE_",)


def _quoted_value(line: str) -> str | None:
    stripped = line.strip()
    if not stripped.startswith(("'", '"')):
        return None
    quote = stripped[0]
    end = stripped.rfind(quote)
    if end == 0:
        return None
    return stripped[1:end]

"""Read reference-number and question-name vectors from the official R file."""
def read_metadata(archive: zipfile.ZipFile, member: str) -> tuple[list[str], list[str]]:
    references: list[str] = []
    question_names: list[str] = []
    target: list[str] | None = None

    with archive.open(member) as raw:
        for line in io.TextIOWrapper(raw, encoding="utf-8", errors="replace"):
            stripped = line.strip()
            if stripped.startswith("names(new_data) <- c("):
                target = references
            elif stripped.startswith("names(data) <- c("):
                target = question_names
            elif target is not None and stripped.startswith(")"):
                target = None
            elif target is not None:
                value = _quoted_value(line)
                if value is not None:
                    target.append(value)
                if stripped.endswith(")"):
                    target = None

    if not references or not question_names:
        raise ValueError("Could not locate both metadata vectors in the official R file.")
    if len(references) != len(question_names):
        raise ValueError(
            f"Metadata vectors differ in length: {len(references)} references and "
            f"{len(question_names)} question names."
        )
    return references, question_names

def wanted(name: str) -> bool:
    return name in CORE_EXACT_NAMES or name.startswith(CORE_PREFIXES)

"""Stream the full archive and retain only cohort-defining variables."""
def build_core_extract(source: Path, destination: Path) -> dict[str, int]:
    with zipfile.ZipFile(source) as archive:
        names = archive.namelist()
        r_member = next(name for name in names if name.endswith(".R"))
        csv_member = next(name for name in names if name.endswith(".csv"))
        references, question_names = read_metadata(archive, r_member)

        selected_metadata = [
            (reference, qname)
            for reference, qname in zip(references, question_names)
            if wanted(qname)
        ]
        if len(selected_metadata) < 7:
            raise ValueError(f"Only {len(selected_metadata)} core variables were found.")

        destination.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(csv_member) as raw_input, destination.open(
            "w", encoding="utf-8", newline=""
        ) as output:
            reader = csv.reader(io.TextIOWrapper(raw_input, encoding="utf-8-sig", newline=""))
            writer = csv.writer(output)
            source_header = next(reader)
            source_positions = {reference: index for index, reference in enumerate(source_header)}
            missing_references = [
                reference for reference, _ in selected_metadata if reference not in source_positions
            ]
            if missing_references:
                raise ValueError(
                    "Selected metadata references missing from CSV: "
                    + ", ".join(missing_references[:10])
                )
            selected = [
                (source_positions[reference], reference, qname)
                for reference, qname in selected_metadata
            ]

            writer.writerow([qname for _, _, qname in selected] + ["IS_BLACK_FEMALE"])
            row_count = 0
            black_female_count = 0
            qname_to_output = {qname: position for position, (_, _, qname) in enumerate(selected)}
            sex_position = qname_to_output["KEY_SEX_1997"]
            race_position = qname_to_output["KEY_RACE_ETHNICITY_1997"]

            for row in reader:
                values = [row[index] for index, _, _ in selected]
                is_black_female = values[sex_position] == "2" and values[race_position] == "1"
                writer.writerow(values + [int(is_black_female)])
                row_count += 1
                black_female_count += int(is_black_female)

    return {
        "rows": row_count,
        "selected_variables": len(selected),
        "black_female_respondents": black_female_count,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("data/raw/nlsy97_all_1997-2023.zip"),
    )
    parser.add_argument(
        "--destination",
        type=Path,
        default=Path("data/interim/nlsy97_core_cohort.csv"),
    )
    args = parser.parse_args()
    result = build_core_extract(args.source, args.destination)
    print(
        "Created core cohort extract: "
        f"{result['rows']:,} respondents, "
        f"{result['selected_variables']} source variables, "
        f"{result['black_female_respondents']:,} Black female respondents."
    )
    
if __name__ == "__main__":
    main()
