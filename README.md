# LVK Generator aus LDT-Dateien

Dieses Mini-Projekt liest eine `.ldt`/EULUMDAT-Datei und erzeugt daraus automatisch:

- eine LVK-Grafik als PNG
- eine LVK-Grafik als PDF
- eine CSV-Tabelle mit den cd/klm-Werten

## Installation auf Windows

1. Python installieren: https://www.python.org/downloads/  
   Wichtig: Beim Installer **Add Python to PATH** aktivieren.

2. Ordner öffnen, in dem diese Dateien liegen.

3. Terminal/CMD öffnen und ausführen:

```bash
pip install -r requirements.txt
```

## Nutzung

```bash
python lvk_generator.py example_spotlight.ldt --out ausgabe
```

Danach liegen die Ergebnisse im Ordner `ausgabe`.

## Bestimmte C-Ebene ausgeben

```bash
python lvk_generator.py example_spotlight.ldt --out ausgabe --c-plane 0
```

Oder z. B.:

```bash
python lvk_generator.py example_spotlight.ldt --out ausgabe --c-plane 90
```

## Für die Präsentation beim Chef

Wichtig sagen: Das ist keine KI, die eine LVK schätzt. Die echten photometrischen Daten stehen in der LDT-Datei. Das Script liest diese Daten aus und erstellt automatisch die LVK-Darstellung.
