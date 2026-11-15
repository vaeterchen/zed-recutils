# GNU Recutils for Zed

This extension recognizes `.rec` files as **GNU Recutils**. It highlights field
names, descriptor fields such as `%rec` and `%type`, colons, values, comment
lines, and both forms of line continuation. Colors depend on your Zed theme.
Values are treated as text. The extension does not validate Recutils rules
such as `%type` or `%key`.

## Install locally

1. Clone this repository.
2. In Zed, run **zed: install dev extension** from the command palette and
   select the cloned folder containing `extension.toml`. Zed fetches the
   grammar revision specified in the manifest and builds the parser as
   WebAssembly.
3. Open `examples/contacts.rec`. The status bar should show **GNU Recutils**.

## Regenerate and test the parser

To regenerate the parser, use Node.js (tested with version 22) and Tree-sitter
CLI **0.25.10**. The tests also require a C compiler because Tree-sitter
builds the parser as a native library.

```sh
cd tree-sitter-recutils
tree-sitter generate --abi 14
cd ..
python3 test.py
```

Use `test.py --tree-sitter /path/to/tree-sitter` to specify a different CLI
location. To test grammar changes in Zed, run `python3 prepare.py` to point
the manifest at a local grammar checkout.

The corpus tests cover descriptors, repeated and empty fields, Unicode values,
comments, and line continuations. The remaining tests verify the highlight
ranges from Zed's query, Windows line endings, a file without a trailing
newline, and error detection for a standalone continuation line. Blank lines
are recognized as separators. The syntax tree provides fields and comments in
file order for highlighting.

## Project files

| Path | Contents |
| --- | --- |
| `extension.toml` | Zed manifest with the public grammar pinned to a commit |
| `languages/recutils/` | File association, comment prefix, and highlight query |
| `tree-sitter-recutils/grammar.js` | Tree-sitter grammar |
| `tree-sitter-recutils/src/` | Generated C parser and headers |
| `tree-sitter-recutils/test/corpus/` | Expected syntax trees |
| `prepare.py`, `test.py` | Local installation setup and test runner |
| `examples/contacts.rec` | Sample database for Zed |

## References

- [Zed Language Extensions](https://zed.dev/docs/extensions/languages)
- [Developing Zed Extensions](https://zed.dev/docs/extensions/developing-extensions)
- [Zed 1.28.1 Extension Builder](https://github.com/zed-industries/zed/blob/v1.28.1/crates/extension/src/extension_builder.rs)
- [GNU Recutils Rec Format](https://www.gnu.org/software/recutils/manual/html_node/The-Rec-Format.html)
