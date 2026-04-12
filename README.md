# Infrastruktur-Monitor Deutschland

Erfassung und Visualisierung von Schließungen öffentlicher Infrastruktur in Deutschland – mit Fokus auf kommunale Einrichtungen, die aufgrund von Haushaltsproblemen geschlossen oder gefährdet sind.

## Status

🚧 **In Entwicklung** – aktuell als Mockup

## Demo

Öffne `index.html` im Browser – keine Installation nötig.

## Entwicklung

- `python3 -m http.server 8000` startet einen lokalen Server
- `uv run scripts/update_last_updated.py` setzt `data/meta.js` auf das heutige Datum
- `uv run scripts/sync_geodata.py sync` ergänzt OSM-Koordinaten und Kartenlinks
- `uv run scripts/sync_geodata.py check` prüft, ob alle Einträge `lat`, `lon` und OSM-Links haben
- `uv run scripts/check_history.py` erzwingt einen Eintrag in `status_history.md`, wenn bestehende Fälle relevant neu bewertet werden

## Dateien

```
├── data/meta.js            # Letztes Update für die Oberfläche
├── data/schwimmbaeder.js   # Gerenderte Datengrundlage inkl. OSM-Koordinaten
├── index.html              # Mockup (lauffähig im Browser)
├── scripts/check_history.py       # Prüft, ob relevante Umklassifizierungen im Verlauf dokumentiert sind
├── scripts/update_last_updated.py # Aktualisiert das sichtbare Letzte-Update-Datum
├── scripts/sync_geodata.py # Geocoding- und Prüfskript
├── status_history.md       # Verlauf für Umklassifizierungen und spätere Neubewertungen
├── schwimmbaeder.md        # Datentabelle mit Quellen
├── quellen.md              # Übersichtsartikel & Recherchequellen
└── README.md
```

## Daten

### Schwimmbäder

| Status | Anzahl |
|--------|--------|
| 🔴 Geschlossen | 25 |
| 🟡 Gefährdet | 11 |

**Kriterium:** Öffentliche Bäder mit Finanzen/Haushaltslage als Schließungsgrund.

→ Vollständige Liste: [schwimmbaeder.md](schwimmbaeder.md)

## Geplante Kategorien

- Schwimmbäder ✓
- Bibliotheken
- Jugendeinrichtungen
- Sportanlagen
- Kultureinrichtungen

## Datenquellen

- Lokale Pressemeldungen
- Offizielle Mitteilungen der Kommunen
- Ratsunterlagen / Amtsblätter
- Betreiberwebseiten

## Tech-Stack (Mockup)

- React 18 (via CDN)
- Tailwind CSS (via CDN)
- Keine Build-Tools nötig

## Lizenz

CC BY 4.0
