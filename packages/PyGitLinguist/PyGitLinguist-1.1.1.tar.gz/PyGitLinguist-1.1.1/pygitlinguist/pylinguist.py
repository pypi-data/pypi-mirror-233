import json
import os
import mimetypes
import argparse
from linguist.blob import Blob
from linguist.language import Language
from lang_detect import Linguist

HELP_TEXT = """
Linguist
Detect language type and determine language breakdown for code files in a directory.

Usage: pylinguist.py <path>
       pylinguist.py <path> [--breakdown] [--json]
       pylinguist.py [--breakdown] [--json]

Options:
  -b, --breakdown   Analyze code files in the directory and display detailed usage statistics
  -j, --json         Output results as JSON
  -h, --help         Display this help message and exit
"""


def analyze_directory(path, breakdown=False, json_output=False):
    results = {}

    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type and mime_type.startswith("text"):

                    blob = Blob(file_path, '')

                    linguist = Linguist()
                    language = linguist.detect(blob)

                    language = language.name

                    if language in results:
                        results[language]["files"].append(file_path)
                    else:
                        results[language] = {"size": 0, "files": [file_path]}

                    results[language]["size"] += blob.loc
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    print(results)
    return results


def analyze_file(path, breakdown, json_output):
    results = {}
    try:
        mime_type, _ = mimetypes.guess_type(path)
        if mime_type and mime_type.startswith("text"):

            blob = Blob(path, '')

            linguist = Linguist()
            language = linguist.detect(blob)
            if language in results:
                results[language.name]["files"].append(path)
            else:
                results[language.name] = {"size": 0, "files": [path]}
            results[language.name]["size"] += blob.loc
    except Exception as e:
        print(f"Error processing {path}: {e}")
    print(results)
    return results


def main():
    parser = argparse.ArgumentParser(description="Linguist - Detect programming languages in code files.")
    parser.add_argument("path", nargs="?", default=".", help="Path to the directory containing code files")
    parser.add_argument("-b", "--breakdown", action="store_true", help="Analyze code files in the directory and display detailed usage statistics")
    parser.add_argument("-j", "--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    if os.path.isdir(args.path):
        analyze_directory(args.path, args.breakdown, args.json)
    elif os.path.isfile(args.path):
        analyze_file(args.path, args.breakdown, args.json)
    else:
        print(HELP_TEXT)


if __name__ == "__main__":
    # analyze_file('lang_detect.py')
    analyze_directory('linguist/strategy')