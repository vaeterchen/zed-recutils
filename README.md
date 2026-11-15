# GNU Recutils für Zed

Die Extension erkennt `.rec`-Dateien als **GNU Recutils**. Sie hebt Feldnamen,
Deskriptorfelder wie `%rec` und `%type`, Doppelpunkte, Werte, Kommentarzeilen und
die beiden Arten von Zeilenfortsetzungen hervor. Die konkreten Farben hängen vom
Zed-Theme ab. Werte bleiben Text. Die Extension prüft keine Recutils-Regeln wie
`%type` oder `%key`.

## Lokal installieren

1. Dieses Repository klonen.
2. In Zed **zed: install dev extension** aufrufen und den geklonten
   Ordner mit `extension.toml` auswählen. Zed lädt den im Manifest
   referenzierten Grammatik-Commit und baut den Parser als WebAssembly.
3. `examples/contacts.rec` öffnen. In der Statusleiste sollte
   **GNU Recutils** erscheinen.

## Parser neu erzeugen und testen

Für die Regenerierung werden Node.js (getestet mit 22) und Tree-sitter CLI
**0.25.10** verwendet. Für die Tests brauchst du außerdem einen C-Compiler,
da die CLI den Parser dafür als native Bibliothek baut.

```sh
cd tree-sitter-recutils
tree-sitter generate --abi 14
cd ..
python3 test.py
```

`test.py --tree-sitter /pfad/zur/tree-sitter` akzeptiert einen alternativen
Pfad zur CLI. Für einen lokalen Grammatiktest mit Zed kann `python3 prepare.py`
das Manifest auf einen lokalen Grammatik-Checkout umstellen.

Die Korpustests prüfen Deskriptoren, wiederholte und leere Felder, Unicode-Werte,
Kommentare und Zeilenfortsetzungen. Ein weiterer Test prüft die Bereiche der
Original-Zed-Query, Windows-Zeilenenden, ein Dateiende ohne Zeilenumbruch und die
Fehlererkennung bei einer alleinstehenden Fortsetzungszeile. Leerzeilen
werden als Trennzeichen erkannt. Für die Hervorhebung liefert der Baum Felder
und Kommentare in Dateireihenfolge.

## Projektdateien

| Datei oder Ordner | Inhalt |
| --- | --- |
| `extension.toml` | Zed-Manifest mit der öffentlichen, auf einen Commit festgelegten Grammatik |
| `languages/recutils/` | Dateizuordnung, Kommentarpräfix und Highlighting-Query |
| `tree-sitter-recutils/grammar.js` | Tree-sitter-Grammatik |
| `tree-sitter-recutils/src/` | Generierter C-Parser und Header |
| `tree-sitter-recutils/test/corpus/` | Erwartete Syntaxbäume |
| `prepare.py`, `test.py` | Lokale Installation vorbereiten und Tests ausführen |
| `examples/contacts.rec` | Beispieldatenbank für Zed |

## Referenzen

- [Zed: Language Extensions](https://zed.dev/docs/extensions/languages)
- [Zed: Developing Extensions](https://zed.dev/docs/extensions/developing-extensions)
- [Zed 1.28.1: Extension-Builder](https://github.com/zed-industries/zed/blob/v1.28.1/crates/extension/src/extension_builder.rs)
- [GNU Recutils: The Rec Format](https://www.gnu.org/software/recutils/manual/html_node/The-Rec-Format.html)
