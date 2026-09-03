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


if __name__ == "__main__":
    main()
