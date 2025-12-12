import pandas as pd
from pathlib import Path
import json

# maps category to the list of merging systems defined
# by Murdock in murdockdata/At10.cod. Uses variant value (2nd value in pair).
MERGING_MAP = {
    "grandparents": [11, 12, 13],
    "grandchildren": [7],
    "niblings": [1, 2, 3, 4, 5, 8, 9],
    "aunts": [2, 3, 5, 7],
    "uncles": [1, 10, 6, 8],
}

# same as above but for rare systems defined by Murdock.
RARE_MAP = {
    "grandparents": [16, 17, 18, 19, 20, 21, 22],
    "grandchildren": [13, 14, 15, 16, 17, 18, 19, 20],
    "niblings": [19, 20, 21, 22, 23, 24, 25, 26],
    "aunts": [11, 12, 13, 14],
    "uncles": [13],
    "siblings": [37, 38, 39, 40, 41, 42, 43],
}

SEPARATE_TERM_MAP = {
    "grandparents": [4, 5, 6],
    "niblings": [2, 3, 4],
    "siblings": [10, 12]
}

SPEAKER_DIFFERENCE_MAP = {
    "grandparents": [16, 17, 18, 21, 22],
    "grandchildren": [10, 11, 12, 14, 15, 16, 17, 18, 19, 20],
    "uncles": [5, 10, 11, 12],
    "aunts": [10],
    "siblings": [2, 3, 4, 5, 13, 15, 18, 19, 20, 21, 22, 23, 24, 25, 26, 
                 27, 28, 29, 30, 31, 32, 34, 35, 37, 38, 39, 40, 41, 42, 43]
}

# maps category to corresponding variant header name in murdockdata/murdock_orig_codes.csv.
CATEGORY_TO_COLUMN_MAP = {
    "grandparents": "grandparents_variant",
    "grandchildren": "grandchildren_variant",
    "uncles": "uncles_variant",
    "aunts": "aunts_variant",
    "niblings": "nephewniece_variant",
    "siblings": "sibling_variant",
}

BASE_DIR = Path(".")
DIR_PATH = BASE_DIR / "2025_plots" / "nonoptimal_plots"

def generate_nonoptimal_languages_json(
    category_to_murdock_map: dict,
    category_to_column_name_map: dict,
    save_filename: str,
    base_dir: Path = Path(".")
):
    """
    Builds a JSON file mapping each kinship category to its corresponding languages
    based on Murdock variant indices.
    """

    d_murdock_file = base_dir / "murdockdata" / "murdock_orig_codes.csv"
    murdock_codes = pd.read_csv(d_murdock_file)

    all_languages = {}

    for category, variant_indices in category_to_murdock_map.items():
        col_name = category_to_column_name_map[category]

        murdock_codes[col_name] = pd.to_numeric(murdock_codes[col_name], errors="coerce")
        mask = murdock_codes[col_name].isin(variant_indices)

        category_languages = murdock_codes.loc[mask, "name"].dropna().tolist()
        all_languages[category] = category_languages

    # Write JSON file
    save_path = DIR_PATH / save_filename
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(all_languages, f, ensure_ascii=False, indent=2)

def main():
    generate_nonoptimal_languages_json(MERGING_MAP, CATEGORY_TO_COLUMN_MAP, "merging_languages.json")
    generate_nonoptimal_languages_json(RARE_MAP, CATEGORY_TO_COLUMN_MAP, "rare_languages.json")
    generate_nonoptimal_languages_json(SEPARATE_TERM_MAP, CATEGORY_TO_COLUMN_MAP, "separate_term_languages.json")
    generate_nonoptimal_languages_json(SPEAKER_DIFFERENCE_MAP, CATEGORY_TO_COLUMN_MAP, "speaker_difference_languages.json")

if __name__ == "__main__":
    main()
