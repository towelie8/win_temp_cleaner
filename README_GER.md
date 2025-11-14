# Windows Temporary Files Cleaner

Ein umfassender Scanner und Cleaner für Windows 10/11 Temporärdateien. **Version 2.0 Extended** scannt über **50 Locations** und kann **60-300 GB** an versteckten temporären Dateien finden und löschen!

## Neu in Version 0.8.1

- **50+ Scan-Locations** (vorher nur 9)
- **Intelligente Prioritätssortierung** (Kritisch → Hoch → Mittel → Niedrig)
- **Kategorie-basierte Organisation** (System, Browser, Gaming, Development, etc.)
- **Prozess-Erkennung** (verhindert Löschen wenn Apps laufen)
- **Service-Management** (stoppt/startet Services sicher)
- **Erweiterte Reports** mit Größenanalyse und Empfehlungen
- **Modulare Architektur** für einfache Erweiterung

## Warum?

Windows speichert automatisch Temporärdateien an **dutzenden versteckten Orten**:

### System-Caches (oft 20-100 GB)
- **Windows.old** (15-30 GB) - Alte Windows-Installation
- **Windows Error Reports** (5-50 GB) - Crash-Dumps
- **CBS Logs** (bis 20 GB) - Windows Update Logs
- **Defender Scan History** (10-20 GB) - Defender Cache
- **ETL Diagnostic Logs** (10-50 GB) - Telemetrie-Daten
- **Delivery Optimization** (1-20 GB) - P2P Update Cache

### Application-Caches (oft 10-50 GB)
- **Browser-Caches** (Chrome, Firefox, Edge)
- **Discord, Teams, Slack, Spotify** - Chat/Media Caches
- **GPU Shader Caches** (NVIDIA, AMD, Intel)
- **Development Tools** (npm, pip, Visual Studio)

### Und viele mehr!

Diese Dateien können sich zu **mehreren hundert Gigabyte** ansammeln und:
- Wertvollen Speicherplatz verschwenden
- Die Systemleistung verlangsamen
- SSD-Lebensdauer durch unnötige Schreibvorgänge reduzieren
- FPS in Spielen negativ beeinflussen

## Features

### Vollständiger Scan
- Scannt **50+ kritische Locations**
- Findet versteckte Temp-Dateien die andere Tools übersehen
- Zeigt detaillierte Größen- und Dateianzahl-Statistiken

### Intelligente Priorisierung
- 🔴 **Kritisch**: Große Dateien mit spezieller Behandlung
- 🟠 **Hoch**: Große, sicher löschbare Dateien  
- 🟡 **Mittel**: Moderate Größe
- 🟢 **Niedrig**: Klein oder bedingt löschbar
- ⚫ **Nur Anzeige**: NIEMALS löschen (z.B. Windows Installer)

### Sicherheit First
- Interaktive Bestätigung vor dem Löschen
- Prozess-Erkennung (verhindert Löschen wenn App läuft)
- Service-Management (stoppt/startet Services sicher)
- Admin-Rechte-Prüfung
- Detaillierte Fehlerbehandlung
- Mehrfache Bestätigungen bei kritischen Locations

### Detaillierte Reports
- Markdown-Reports mit vollständiger Statistik
- Sortierung nach Priorität und Kategorie
- Warnungen bei kritischen Locations
- Empfehlungen für optimale Bereinigung

### Selective Cleanup
- Wähle spezifische Locations zum Löschen
- Lösche nur hohe Priorität
- Oder alle sicheren Locations auf einmal

## Quickstart

### Voraussetzungen
- Python 3.7 oder höher
- Windows 10 oder Windows 11
- Administrator-Rechte (empfohlen für vollständigen Zugriff)

### Installation & Ausführung

```bash
# Clone Repository
git clone https://github.com/towelie8/win_temp_cleaner
cd win_temp_cleaner

# Auf dev-Branch wechseln für Version 2.0
git checkout dev

# Script mit Admin-Rechten ausführen
python main.py
```

## Verwendung

### 1. Scan durchführen
```bash
python main.py
```

Das Tool scannt automatisch alle 50+ Locations und zeigt:
- Gefundene Größe pro Location
- Anzahl der Dateien
- Prioritätseinstufung
- Warnungen bei kritischen Locations

### 2. Report generieren

Ein detaillierter Markdown-Report wird automatisch erstellt:
```
temp_scan_report_YYYYMMDD_HHMMSS.md
```

Der Report enthält:
- Zusammenfassung der gesamten Speichernutzung
- Aufschlüsselung nach Priorität
- Aufschlüsselung nach Kategorie
- Top 10 größte Locations
- Detaillierte Empfehlungen

### 3. Interaktive Bereinigung

Wähle aus verschiedenen Optionen:
```
Optionen:
  a       - Alle SICHEREN Locations löschen
  h       - Nur HOHE Priorität löschen
  1,2,3   - Spezifische Nummern löschen (kommagetrennt)
  q       - Abbrechen
```

## Gescannte Locations

### 🔴 Kritische Priorität (Spezielle Behandlung)
| Location | Typische Größe | Beschreibung |
|----------|---------------|--------------|
| Windows.old | 15-30 GB | Vorherige Windows-Installation |
| $Windows.~BT | 3-20 GB | Windows Upgrade-Dateien |
| CBS Logs | 0.1-20 GB | Update-/Component-Logs |
| WER Reports | 1-10 GB | Windows Error Reports |
| Memory Dumps | 1-64 GB | BSOD Crash Dumps |
| Defender Scan History | 10-20 GB | Defender Cache Files |
| ETL Diagnostic Logs | 10-50 GB | Telemetrie-Daten |

### 🟠 Hohe Priorität (Große, sichere Dateien)
- Delivery Optimization Cache (1-20 GB)
- Adobe Temp Files (0.5-100 GB)
- Application Crash Dumps (1-5 GB)
- Live Kernel Reports (0.5-2 GB)

### 🟡 Mittlere Priorität (Moderate Größe)
- Browser Caches (Chrome, Firefox, Edge)
- Discord, Teams, Slack, Spotify Caches
- GPU Shader Caches (NVIDIA, AMD, Intel, DirectX)
- Development Tool Caches (npm, pip, NuGet)
- Windows Update Cache

### 🟢 Niedrige Priorität (Klein)
- Windows Explorer Thumbnails
- Icon Cache
- Font Cache
- Recent Documents
- Notification Cache

### ⚫ Nur Anzeige (NIEMALS LÖSCHEN)
-  Windows Installer Cache (C:\Windows\Installer)
-  WinSxS Component Store (nur via DISM)

## Sicherheitshinweise

### Was ist sicher?
Alle Locations mit grünem Häkchen im Report
Locations mit Priorität "Hoch" oder "Mittel"
Temporäre Caches und Browser-Daten

### Was ist NICHT sicher?
 **Windows Installer Cache** - Bricht Updates/Deinstallation
 **WinSxS direkt löschen** - Nur über DISM-Tools!

### Empfohlene Vorgehensweise
1. **Backup wichtiger Daten** vor großen Bereinigungen
2. **Als Administrator ausführen** für vollständigen Zugriff
3. **Report lesen** vor dem Löschen
4. **Bei Windows.old**: Nur löschen wenn >30 Tage seit Upgrade
5. **Apps schließen** vor Bereinigung ihrer Caches

## Typische Ergebnisse

Nach einer vollständigen Bereinigung kannst du erwarten:

- **Speicherfreigabe**: 60 MB - 300+ GB (abhängig vom Systemalter)
- **Schnellerer PC**: Weniger Disk-I/O, mehr verfügbarer Cache
- **Bessere SSD-Lebensdauer**: Reduzierte Schreibvorgänge
- **Verbesserte FPS**: Durch freigegebenen GPU-Shader-Cache-Speicher

### Beispiel: 2 Jahre altes Gaming-System
```
Scan-Ergebnis:
- Windows.old: 28 GB
- CBS Logs: 12 GB
- WER Reports: 8 GB
- Defender History: 15 GB
- GPU Shader Caches: 6 GB
- Browser Caches: 4 GB
- Discord/Teams: 3 GB
----------------------------
Gesamt freigegeben: 76 GB
```

## Dokumentation

- **README.md** (diese Datei) - Benutzer-Dokumentation
- **README_DEV.md** - Entwickler-Dokumentation und Architektur
- **config.py** - Alle Location-Definitionen
- **utils.py** - Utility-Funktionen
- **main.py** - Hauptanwendung

## Development

### Projekt-Struktur
```
win_temp_cleaner/
├── main.py           # Hauptanwendung
├── config.py         # 50+ Location-Definitionen
├── utils.py          # Prozess-/Service-Management
├── README.md         # Benutzer-Doku
├── README_DEV.md     # Entwickler-Doku
└── .gitignore
```

### Neue Location hinzufügen
Siehe **README_DEV.md** für Details zum Hinzufügen neuer Locations.

## ❓ FAQ

**F: Ist es sicher, alle Temp-Dateien zu löschen?**  
**A:** Ja, alle als "safe_delete=True" markierten Locations sind sicher. Windows erstellt temporäre Dateien bei Bedarf neu.

**F: Warum finde ich mehr Dateien als Tool XYZ?**  
**A:** Wir scannen 50+ Locations inkl. versteckter System-Caches, die viele Tools übersehen (z.B. ETL Logs, Defender History, CBS Logs).

**F: Brauche ich Administrator-Rechte?**  
**A:** Empfohlen! Ohne Admin-Rechte können System-Temp-Ordner nicht gescannt werden (~30% der Locations).

**F: Kann ich das Tool regelmäßig ausführen?**  
**A:** Ja! Völlig sicher, monatlich oder bei Speicherknappheit ausführen.

**F: Was passiert mit meinen persönlichen Daten?**  
**A:** Das Tool löscht NUR temporäre System- und Cache-Dateien. Dokumente, Fotos, Downloads bleiben unberührt.

**F: Kann das Tool mein System beschädigen?**  
**A:** Nein, wenn du die Warnungen beachtest. Wir löschen NIEMALS kritische System-Ordner wie Windows Installer oder WinSxS direkt.

## Lizenz

MIT License - Siehe LICENSE Datei

## Autor

**GitHub:** [@towelie8](https://github.com/towelie8)

## Stern geben!

Wenn dir dieses Tool geholfen hat, Speicherplatz freizugeben, gib dem Repository einen Stern auf GitHub! ⭐
