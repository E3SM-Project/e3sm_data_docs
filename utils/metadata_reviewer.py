#!/usr/bin/env python
"""
Cross-check CMIP6-Metadata JSON files against the ESGF links published in the
E3SM Data Docs simulation tables.

For every variant described by a CMIP6-Metadata JSON file, this script tries
to find a matching ESGF link in one of the `simulation_table.rst` pages in
the E3SM Data Docs repo. It then reports, as three Markdown tables:

  1. Variants on CMIP6 Metadata, but not on E3SM Data Docs
  2. Variants not on CMIP6 Metadata, but on E3SM Data Docs
  3. Variants on both CMIP6 Metadata and E3SM Data Docs

NOTE on institution_id / activity_id:
The ESGF search links embedded in the data-docs tables only ever encode
`source_id`, `experiment_id`, and `variant_label` (as query parameters, or as
a URL-encoded JSON blob in an `activeFacets` parameter). They do not encode
`institution_id` or `activity_id`. Because of that, a Variant's *identity*
(used for matching/hashing/equality) is based only on
(source_id, experiment_id, variant_label). When a variant is discovered only
from a data-docs link (i.e. it has no corresponding CMIP6-Metadata JSON),
its institution_id/activity_id fields are set to "N/A" rather than guessed.

NOTE on experiment_id casing:
E3SM Data Docs and CMIP6-Metadata don't always agree on the casing of
experiment_id (e.g. `piClim-histghg` vs `piClim-histGHG`). Matching therefore
ignores case, but CMIP6-Metadata is treated as the source of truth: when a
CMIP6-Metadata variant is matched to a data-docs link, the variant's
displayed experiment_id keeps CMIP6-Metadata's original casing. Only
variants found *exclusively* in data-docs (no CMIP6-Metadata counterpart)
display data-docs' casing, since there's no CMIP6-Metadata value to prefer.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urlparse, parse_qs

# Set these parameters before running the script:
CMIP6_METADATA_REPO = "/home/ac.forsyth2/ez/CMIP6-Metadata"
DATA_DOCS_REPO = "/home/ac.forsyth2/ez/e3sm_data_docs/"

# Fields that are not derivable from an ESGF link alone.
UNKNOWN = "N/A"


class Variant(object):
    def __init__(
        self,
        institution_id: str = "",
        source_id: str = "",
        activity_id: str = "",
        experiment_id: str = "",
        variant_label: str = "",
        e3sm_data_docs_page: str = "",
        e3sm_data_docs_link: str = "",
    ):
        self.institution_id: str = institution_id
        self.source_id: str = source_id
        self.activity_id: str = activity_id
        self.experiment_id: str = experiment_id
        self.variant_label: str = variant_label
        self.e3sm_data_docs_page: str = e3sm_data_docs_page
        self.e3sm_data_docs_link: str = e3sm_data_docs_link

    def _key(self) -> Tuple[str, str, str]:
        # institution_id / activity_id are deliberately excluded from the
        # identity key -- see module docstring. experiment_id is lower-cased
        # for the purposes of matching/hashing/equality only -- the
        # *displayed* experiment_id (self.experiment_id) keeps its original
        # casing; see the module docstring's note on experiment_id casing.
        return (self.source_id, self.experiment_id.lower(), self.variant_label)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Variant):
            return NotImplemented
        return self._key() == other._key()

    def __hash__(self) -> int:
        return hash(self._key())

    def __repr__(self) -> str:
        return (
            f"Variant(institution_id={self.institution_id!r}, "
            f"source_id={self.source_id!r}, activity_id={self.activity_id!r}, "
            f"experiment_id={self.experiment_id!r}, "
            f"variant_label={self.variant_label!r}, "
            f"e3sm_data_docs_page={self.e3sm_data_docs_page!r})"
        )


# CMIP6-Metadata JSON files are named "<experiment_id>_<variant_label>.json",
# e.g. "1pctCO2_r1i1p1f1.json".
FILENAME_RE = re.compile(r"^(?P<experiment_id>.+)_(?P<variant_label>r\d+i\d+p\d+f\d+)$")


def create_variant_from_json(json_path: str) -> Variant:
    with open(json_path) as f:
        metadata: Dict = json.load(f)

    # "#..." keys are just documentation/notes embedded in the CMIP6-Metadata
    # JSON files -- ignore them.
    metadata = {k: v for k, v in metadata.items() if not k.startswith("#")}

    # variant_label isn't a top-level JSON field, but it's encoded in the
    # filename ("<experiment_id>_<variant_label>.json") and can also be
    # reconstructed from the realization/initialization/physics/forcing
    # index fields. Prefer the filename (it's the more direct source and
    # doesn't assume the index fields are always present/well-formed), but
    # cross-check against the indices when they're available and warn on a
    # mismatch rather than silently picking one.
    stem = Path(json_path).stem
    filename_match = FILENAME_RE.match(stem)
    variant_label = filename_match.group("variant_label") if filename_match else None

    if all(
        k in metadata
        for k in (
            "realization_index",
            "initialization_index",
            "physics_index",
            "forcing_index",
        )
    ):
        variant_label_from_indices = (
            f"r{metadata['realization_index']}"
            f"i{metadata['initialization_index']}"
            f"p{metadata['physics_index']}"
            f"f{metadata['forcing_index']}"
        )
        if variant_label is None:
            variant_label = variant_label_from_indices
        elif variant_label != variant_label_from_indices:
            print(
                f"WARNING: {json_path}: variant_label from filename "
                f"({variant_label!r}) disagrees with variant_label computed "
                f"from index fields ({variant_label_from_indices!r}); using "
                f"the filename's value."
            )

    if variant_label is None:
        raise ValueError(
            f"{json_path}: could not determine variant_label from the "
            f"filename or from index fields."
        )

    return Variant(
        institution_id=metadata.get("institution_id", ""),
        source_id=metadata.get("source_id", ""),
        activity_id=metadata.get("activity_id", ""),
        experiment_id=metadata.get("experiment_id", ""),
        variant_label=variant_label,
        e3sm_data_docs_page="",
    )


def find_all_variants_from_cmip6_metadata() -> Set[Variant]:
    variants_from_cmip6_metadata: Set[Variant] = set()
    for json_path in Path(CMIP6_METADATA_REPO).glob("*/*.json"):
        variants_from_cmip6_metadata.add(create_variant_from_json(str(json_path)))
    return variants_from_cmip6_metadata


# Matches an ESGF search link labeled "CMIP" in an RST hyperlink, e.g.:
#   `CMIP <https://esgf-node.llnl.gov/search/cmip6/?source_id=...>`_
CMIP_LINK_RE = re.compile(r"`CMIP\s*<([^>]+)>`_")

# A new list-table row: "   * - <first column>"
ROW_START_RE = re.compile(r"^\s*\*\s*-\s?(.*)$")
# A continuation column of the current row: "     - <column>"
COL_CONT_RE = re.compile(r"^\s*-\s?(.*)$")


def _parse_esgf_url(url: str) -> Optional[Tuple[str, str, str]]:
    """Extract (source_id, experiment_id, variant_label) from an ESGF link.

    Two URL flavors are supported:
      - Simple query params, e.g. esgf-node.llnl.gov/search/cmip6/?source_id=...
      - A URL-encoded JSON blob in an `activeFacets` param, e.g. aims2.llnl.gov
    """
    query = parse_qs(urlparse(url).query)

    if "activeFacets" in query:
        try:
            facets = json.loads(query["activeFacets"][0])
        except (json.JSONDecodeError, IndexError):
            return None
        source_id = facets.get("source_id")
        experiment_id = facets.get("experiment_id")
        variant_label = facets.get("variant_label")
    else:
        source_id = query.get("source_id", [None])[0]
        experiment_id = query.get("experiment_id", [None])[0]
        variant_label = query.get("variant_label", [None])[0]

    if not (source_id and experiment_id and variant_label):
        return None

    return source_id, experiment_id, variant_label


def _parse_list_table_rows(rst_path: str) -> List[List[str]]:
    """Parse a Sphinx `.. list-table::` into a list of rows of column text."""
    rows: List[List[str]] = []
    current_row: Optional[List[str]] = None

    with open(rst_path) as f:
        for line in f:
            row_match = ROW_START_RE.match(line)
            if row_match:
                if current_row is not None:
                    rows.append(current_row)
                current_row = [row_match.group(1).strip()]
                continue

            if current_row is not None:
                col_match = COL_CONT_RE.match(line)
                if col_match:
                    current_row.append(col_match.group(1).strip())
                    continue

    if current_row is not None:
        rows.append(current_row)

    return rows


def collect_links_from_table(rst_path: str) -> List[Variant]:
    variants: List[Variant] = []

    rows = _parse_list_table_rows(rst_path)
    if not rows:
        return variants

    # `:header-rows: 1` -- the first row is the header; use it to find the
    # "ESGF Links" column index rather than assuming a fixed position.
    header = rows[0]
    esgf_col_idx = next(
        (i for i, col in enumerate(header) if "ESGF Links" in col), None
    )
    if esgf_col_idx is None:
        return variants

    for row in rows[1:]:
        if esgf_col_idx >= len(row):
            continue
        esgf_cell = row[esgf_col_idx]

        match = CMIP_LINK_RE.search(esgf_cell)
        if not match:
            continue

        parsed = _parse_esgf_url(match.group(1))
        if parsed is None:
            continue

        source_id, experiment_id, variant_label = parsed

        simulation_name = row[0] if row else ""
        url = _data_docs_url(rst_path)
        e3sm_data_docs_link = (
            f"[{simulation_name}]({url})" if simulation_name and url else ""
        )

        variants.append(
            Variant(
                institution_id=UNKNOWN,
                source_id=source_id,
                activity_id=UNKNOWN,
                experiment_id=experiment_id,
                variant_label=variant_label,
                e3sm_data_docs_page=rst_path,
                e3sm_data_docs_link=e3sm_data_docs_link,
            )
        )

    return variants


def process_links_in_data_docs(variants_from_cmip6_metadata: Set[Variant]) -> Set[Variant]:
    variants_not_in_cmip6_metadata: Set[Variant] = set()

    # Lookup by identity key so we can mutate the *actual* objects that live
    # in `variants_from_cmip6_metadata` when we find a matching link. Since
    # `_key()` lower-cases experiment_id, this matches regardless of casing
    # differences between CMIP6-Metadata and data-docs, and because we only
    # ever update e3sm_data_docs_page/e3sm_data_docs_link on `match` (never
    # experiment_id itself), CMIP6-Metadata's original casing is preserved.
    lookup: Dict[Tuple[str, str, str], Variant] = {
        v._key(): v for v in variants_from_cmip6_metadata
    }

    simulation_table_paths = Path(DATA_DOCS_REPO).glob(
        "docs/source/*/*/simulation_data/simulation_table.rst"
    )
    for simulation_table_page in simulation_table_paths:
        variants_in_this_table = collect_links_from_table(str(simulation_table_page))
        for variant in variants_in_this_table:
            match = lookup.get(variant._key())
            if match is not None:
                match.e3sm_data_docs_page = variant.e3sm_data_docs_page
                match.e3sm_data_docs_link = variant.e3sm_data_docs_link
            else:
                variants_not_in_cmip6_metadata.add(variant)

    return variants_not_in_cmip6_metadata


def find_variants_not_on_data_docs(variants_from_cmip6_metadata: Set[Variant]) -> Set[Variant]:
    variants_not_on_data_docs: Set[Variant] = set()
    for variant in variants_from_cmip6_metadata:
        if variant.e3sm_data_docs_page == "":
            variants_not_on_data_docs.add(variant)
    return variants_not_on_data_docs


# Matches a variant_label's r/i/p/f indices, e.g. "r6i1p1f1" ->
# ("6", "1", "1", "1"). Used only for sorting -- the variant_label string
# itself is never rewritten/reformatted (e.g. never zero-padded).
VARIANT_LABEL_INDICES_RE = re.compile(
    r"^r(?P<r>\d+)i(?P<i>\d+)p(?P<p>\d+)f(?P<f>\d+)$"
)


def _variant_label_sort_key(variant_label: str) -> Tuple[int, int, int, int]:
    """Sort key for a variant_label that orders r/i/p/f as integers (so
    r6i1p1f1 sorts before r25i1p1f1), instead of lexicographically as
    strings (which would put r25... before r6...).

    Falls back to a key of all -1s (sorting before any real index) for
    labels that don't match the expected "rXiYpZfW" pattern, so malformed
    labels don't crash the sort.
    """
    match = VARIANT_LABEL_INDICES_RE.match(variant_label)
    if not match:
        return (-1, -1, -1, -1)
    return (
        int(match.group("r")),
        int(match.group("i")),
        int(match.group("p")),
        int(match.group("f")),
    )


def _sort_key(
    variant: Variant,
) -> Tuple[str, str, str, str, Tuple[int, int, int, int]]:
    return (
        variant.institution_id,
        variant.source_id,
        variant.activity_id,
        variant.experiment_id,
        _variant_label_sort_key(variant.variant_label),
    )


# The E3SM Data Docs repo's `docs/source/**/*.rst` pages are built to
# `docs/source/**/*.html` under this base URL, e.g.
#   docs/source/v3/CoupledSystem/simulation_data/simulation_table.rst  ->
#   https://docs.e3sm.org/e3sm_data_docs/_build/html/v3/CoupledSystem/simulation_data/simulation_table.html
DATA_DOCS_BASE_URL = "https://docs.e3sm.org/e3sm_data_docs/_build/html"
DOCS_SOURCE_MARKER = "docs/source/"


def _data_docs_relative_path(page_path: str) -> Optional[str]:
    """e.g. '.../docs/source/v3/CoupledSystem/.../simulation_table.rst' ->
    'v3/CoupledSystem/.../simulation_table.rst'"""
    idx = page_path.find(DOCS_SOURCE_MARKER)
    if idx == -1:
        return None
    return page_path[idx + len(DOCS_SOURCE_MARKER) :]


def _data_docs_url(page_path: str) -> Optional[str]:
    relative = _data_docs_relative_path(page_path)
    if relative is None:
        return None
    relative_html = re.sub(r"\.rst$", ".html", relative)
    return f"{DATA_DOCS_BASE_URL}/{relative_html}"


def _make_markdown_table(title: str, variants: Set[Variant]) -> str:
    lines = [
        f"### {title}",
        "",
        "| Institution ID | Source ID | Activity ID | Experiment ID | Variant Label | Can be found on... |",
        "|---|---|---|---|---|---|",
    ]
    for v in sorted(variants, key=_sort_key):
        lines.append(
            f"| {v.institution_id} | {v.source_id} | {v.activity_id} | "
            f"{v.experiment_id} | {v.variant_label} | {v.e3sm_data_docs_link} |"
        )
    lines.append("")
    return "\n".join(lines)


def main():
    variants_from_cmip6_metadata: Set[Variant] = find_all_variants_from_cmip6_metadata()

    variants_not_in_cmip6_metadata: Set[Variant] = process_links_in_data_docs(
        variants_from_cmip6_metadata
    )
    variants_not_on_data_docs: Set[Variant] = find_variants_not_on_data_docs(
        variants_from_cmip6_metadata
    )
    variants_on_both: Set[Variant] = variants_from_cmip6_metadata - variants_not_on_data_docs

    report = "\n".join(
        [
            _make_markdown_table(
                "Variants on CMIP6 Metadata, but not on E3SM Data Docs",
                variants_not_on_data_docs,
            ),
            _make_markdown_table(
                "Variants not on CMIP6 Metadata, but on E3SM Data Docs",
                variants_not_in_cmip6_metadata,
            ),
            _make_markdown_table(
                "Variants on both CMIP6 Metadata and E3SM Data Docs",
                variants_on_both,
            ),
        ]
    )
    output_path = Path("metadata_review.md")
    output_path.write_text(report)
    print(f"Wrote report to {output_path.resolve()}")


if __name__ == "__main__":
    main()
