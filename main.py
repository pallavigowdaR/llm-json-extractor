import argparse
import json

from extractor.pipeline import extract


def main():
    parser = argparse.ArgumentParser(description="Structured JSON extractor")
    parser.add_argument("doc_type", choices=["invoice", "resume"])
    parser.add_argument("file", help="path to a .txt file")
    args = parser.parse_args()

    with open(args.file, encoding="utf-8") as f:
        text = f.read()

    if not text.strip():
        raise SystemExit(f"Error: {args.file} is empty. Add some text first.")

    result = extract(args.doc_type, text)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()