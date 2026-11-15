"""Prepare the local grammar repository and Zed manifest."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GRAMMAR = ROOT / "tree-sitter-recutils"


def git(*arguments):
    return subprocess.check_output(
        ["git", "-C", str(GRAMMAR), *arguments], text=True
    ).strip()


def main():
    if not (GRAMMAR / "src" / "parser.c").is_file():
        sys.exit("src/parser.c fehlt. Zuerst den Parser erzeugen (siehe README.md).")
    if not (GRAMMAR / ".git").exists():
        git("init", "--quiet")

    git("add", "--", "grammar.js", "tree-sitter.json", "src", "test")
    if subprocess.run(
        ["git", "-C", str(GRAMMAR), "diff", "--cached", "--quiet"], check=False
    ).returncode != 0:
        git("-c", "user.name=Recutils Grammar", "-c", "user.email=recutils@localhost",
            "-c", "commit.gpgsign=false", "commit", "--quiet", "-m",
            "Snapshot of the Recutils grammar")

    rev = git("rev-parse", "HEAD")
    manifest = ROOT / "extension.toml"
    source = manifest.read_text(encoding="utf-8")
    header, grammar_entry = source.split("[grammars.recutils]\n", maxsplit=1)
    grammar_entry = re.sub(r'^repository = ".*"$',
                           lambda _: f'repository = "{GRAMMAR.as_uri()}"',
                           grammar_entry, flags=re.MULTILINE)
    grammar_entry = re.sub(r'^rev = ".*"$', f'rev = "{rev}"',
                           grammar_entry, flags=re.MULTILINE)
    manifest.write_text(header + "[grammars.recutils]\n" + grammar_entry, encoding="utf-8")
    print(f"Zed-Extension vorbereitet: {ROOT}")


if __name__ == "__main__":
    main()
