# GNU Recutils für Zed

Die Extension erkennt `.rec`-Dateien als **GNU Recutils**. Sie hebt Feldnamen,
Deskriptorfelder wie `%rec` und `%type`, Doppelpunkte, Werte, Kommentarzeilen und
die beiden Arten von Zeilenfortsetzungen hervor. Die konkreten Farben hängen vom
Zed-Theme ab. Werte bleiben Text. Die Extension prüft keine Recutils-Regeln wie
`%type` oder `%key`.

## Lokal installieren

1. Das ZIP in einen Ordner entpacken, den du behalten möchtest. Du brauchst Zed,
   Git und Python 3. Der C-Parser liegt bereits bei.
2. Im entpackten Ordner `zed-recutils` ausführen:

   ```sh
   python3 prepare.py
   ```

   Unter Windows funktioniert alternativ `py -3 prepare.py`. Das Skript legt in
   `tree-sitter-recutils/` ein lokales Git-Repository an und trägt dessen
   `file://`-Adresse und Commit-SHA in `extension.toml` ein. Dafür ist kein
   GitHub-Konto oder Git-Remote nötig.
3. In Zed über die Befehlspalette **zed: install dev extension** aufrufen und
   den Ordner `zed-recutils` auswählen, in dem `extension.toml` liegt. Zed
   baut die Grammatik als WebAssembly. Beim ersten Build lädt Zed bei Bedarf
   das WASI SDK. Alternativ kann `WASI_SDK_PATH` auf ein vorhandenes SDK
   zeigen, dessen Unterordner `bin` den Compiler enthält.
4. `examples/contacts.rec` in Zed öffnen. In der Statusleiste sollte
   **GNU Recutils** erscheinen. Die Beispieldatei enthält alle
   Hervorhebungsarten.

Die Extension enthält ausschließlich Sprachkonfiguration, Grammatik und Query.
Für sie ist daher kein Rust-Build nötig. Tree-sitter CLI und Node.js brauchst
du nur für die Entwicklung beziehungsweise die Tests.

Wenn du den Ordner verschiebst, deinstalliere die Dev-Extension in Zed, entferne
das von Zed erzeugte Verzeichnis `grammars/` im Projektordner und führe die
Schritte 2–4 am neuen Ort erneut aus. So wird der Git-Checkout mit der neuen
lokalen Adresse angelegt. Bei einem Installationsfehler zeigt **zed: open log**
die Build-Meldung.

## Parser neu erzeugen und testen

Für die Regenerierung werden Node.js (getestet mit 22) und Tree-sitter CLI
**0.25.10** verwendet. Für die Tests brauchst du außerdem einen C-Compiler,
da die CLI den Parser dafür als native Bibliothek baut.

```sh
cd tree-sitter-recutils
tree-sitter generate --abi 14
cd ..
python3 test.py
python3 prepare.py
```

`test.py --tree-sitter /pfad/zur/tree-sitter` akzeptiert einen alternativen
Pfad zur CLI. Nach einer Änderung Zeds **zed: rebuild dev extension** verwenden
oder die Dev-Extension erneut installieren.

Die Korpustests prüfen Deskriptoren, wiederholte und leere Felder, Unicode-Werte,
Kommentare und Zeilenfortsetzungen. Ein weiterer Test prüft die Bereiche der
Original-Zed-Query, Windows-Zeilenenden, ein Dateiende ohne Zeilenumbruch und die
Fehlererkennung bei einer alleinstehenden Fortsetzungszeile. Leerzeilen
werden als Trennzeichen erkannt. Für die Hervorhebung liefert der Baum Felder
und Kommentare in Dateireihenfolge.

## Projektdateien

| Datei oder Ordner | Inhalt |
| --- | --- |
| `extension.toml` | Zed-Manifest mit Platzhaltern für die lokale Grammatik |
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
