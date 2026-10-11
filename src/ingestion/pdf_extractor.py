
from pathlib import Path
import json
import fitz  # PyMuPDF

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "text"


def extract_pdf(pdf_path: Path, company: str, year: str):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"{company}_{year}.jsonl"
    extracted_pages = 0

    with fitz.open(pdf_path) as pdf:
        with output_file.open("w", encoding="utf-8") as file:
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()

                record = {
                    "company": company,
                    "report_year": year,
                    "source_pdf": pdf_path.name,
                    "page_number": page_number,
                    "text": text,
                }

                file.write(json.dumps(record, ensure_ascii=False) + "\n")

                if text:
                    extracted_pages += 1

    print(f"Company: {company}")
    print(f"Pages with text: {extracted_pages}")
    print(f"Output: {output_file}")


def main():
    reports = [
        (RAW_DIR / "infosys" / "FY2025-26.pdf", "Infosys", "2025-26"),
        (RAW_DIR / "tcs" / "FY2025-26.pdf", "TCS", "2025-26"),
    ]

    for pdf_path, company, year in reports:
        if not pdf_path.exists():
            print(f"PDF not found: {pdf_path}")
            continue

        try:
            extract_pdf(pdf_path, company, year)
        except Exception as error:
            print(f"Failed to process {pdf_path.name}: {error}")


if __name__ == "__main__":
    main()
    