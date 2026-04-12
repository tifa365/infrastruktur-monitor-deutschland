# Infrastruktur-Monitor Deutschland

Erfassung und Visualisierung von Schließungen öffentlicher Infrastruktur in Deutschland – mit Fokus auf kommunale Einrichtungen, die aufgrund von Haushaltsproblemen geschlossen oder gefährdet sind.

## Status

🚧 **In Entwicklung** – aktuell als Mockup

## Demo

Öffne `index.html` im Browser – keine Installation nötig.

## Entwicklung

- `python3 -m http.server 8000` startet einen lokalen Server
- `uv run scripts/sync_geodata.py sync` ergänzt OSM-Koordinaten und Kartenlinks
- `uv run scripts/sync_geodata.py check` prüft, ob alle Einträge `lat`, `lon` und OSM-Links haben

## Dateien

```
├── data/schwimmbaeder.js   # Gerenderte Datengrundlage inkl. OSM-Koordinaten
├── index.html              # Mockup (lauffähig im Browser)
├── scripts/sync_geodata.py # Geocoding- und Prüfskript
├── schwimmbaeder.md        # Datentabelle mit Quellen
├── quellen.md              # Übersichtsartikel & Recherchequellen
└── README.md
```

## Daten

### Schwimmbäder

| Status | Anzahl |
|--------|--------|
| 🔴 Geschlossen | 29 |
| 🟡 Gefährdet | 10 |

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
