# mini-carver

Kleines Forensik-Tool zum **File Carving**: extrahiert JPG/PNG/PDF durch Suche nach Header/Trailer.
Kein Dateisystem-Parsing, sondern einfache heuristische Suche – dafür gut nachvollziehbar.

## Features
- erkennt `jpg`, `png`, `pdf` über Header/Trailer
- schreibt Funde nach `recovered/`
- loggt Offsets und Dateigrößen in die Konsole

## Installation
(nur Standardbibliothek)
```bash
python3 --version
```

## Nutzung
```bash
# Beispiel
python3 carver.py usb.img -o recovered
```

## Hinweise
- Für PNG wird der `IEND`-Trailer heuristisch verlängert (+8 Bytes), damit der Chunk sauber endet.
- Das Tool ist ein Lernprojekt und ersetzt keine professionellen Carver wie `foremost`.

## TODO
- CSV/JSON-Log
- Mehr Formate (ZIP, GIF)
- Exakteres PNG-Parsing (Chunk-basiert)
