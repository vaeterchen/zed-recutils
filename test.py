"""Run the corpus and check Zed's actual highlight query with Tree-sitter."""

import argparse
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GRAMMAR = ROOT / "tree-sitter-recutils"
QUERY = ROOT / "languages" / "recutils" / "highlights.scm"
CAPTURE = re.compile(
    r"capture:\s+\d+ - ([\w.]+), start: \((\d+), (\d+)\), end: \((\d+), (\d+)\)"
)


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--tree-sitter", default="tree-sitter")
    executable = args.parse_args().tree_sitter
    if Path(executable).is_file():
        executable = str(Path(executable).resolve())

    def run(*arguments, **options):
        return subprocess.run([executable, *map(str, arguments)], cwd=GRAMMAR,
                              text=True, **options)

    run("test", check=True)
    run("parse", "--quiet", ROOT / "examples" / "contacts.rec", check=True)

    with tempfile.TemporaryDirectory() as directory:
        sample = Path(directory) / "edge.rec"
        sample.write_bytes(
            b"# x\r\n%rec: T\r\n\r\nN: a#b\r\n+ c\\\r\n"
            b"# value\r\nEmpty:"
        )
        run("parse", "--quiet", sample, check=True)
        output = run("query", "--captures", QUERY, sample,
                     check=True, capture_output=True).stdout
        actual = CAPTURE.findall(output)
        expected = [
            ("comment", "0", "0", "0", "3"),
            ("keyword", "1", "0", "1", "4"),
            ("punctuation.delimiter", "1", "4", "1", "5"),
            ("string", "1", "5", "1", "7"),
            ("property", "3", "0", "3", "1"),
            ("punctuation.delimiter", "3", "1", "3", "2"),
            ("string", "3", "2", "3", "6"),
            ("string.escape", "3", "6", "4", "1"),
            ("string", "4", "1", "4", "3"),
            ("string.escape", "4", "3", "5", "0"),
            ("string", "5", "0", "5", "7"),
            ("property", "6", "0", "6", "5"),
            ("punctuation.delimiter", "6", "5", "6", "6"),
        ]
        if actual != expected:
            raise SystemExit(f"Unexpected highlight ranges:\n{output}")

        sample.write_bytes(b"+ stray continuation\nOK: yes\n")
        result = run("parse", sample, capture_output=True)
        if result.returncode != 1 or "(ERROR" not in result.stdout:
            raise SystemExit(f"Expected a syntax error:\n{result.stdout}")
    print("Highlight ranges, CRLF, end of file, and error detection: OK")


if __name__ == "__main__":
    main()
