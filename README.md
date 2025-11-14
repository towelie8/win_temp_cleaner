# Windows Temporary Files Cleaner

Ein Scanner und Cleaner für Windows 10/11 Temporärdateien. Dieses Tool scannt und löscht temporäre Dateien, die sich über Zeit ansammeln und deine Festplatte zumüllen sowie deinen PC verlangsamen.

## Warum?

Windows speichert automatisch Temporärdateien an vielen Orten:
- **Browser-Cache** (Chrome, Firefox, Edge)
- **Windows Update-Cache**
- **Prefetch-Dateien**
- **Benutzer-Temp-Ordner**
- **Thumbnail-Datenbanken**
- Und weitere Systemcaches

Diese Dateien können sich über Wochen und Monate zu **mehreren Gigabyte** ansammeln und:
- Wertvollen Speicherplatz auf deiner Festplatte verschwenden
- Die Systemleistung verlangsamen
- Unnötige Schreibvorgänge verursachen und die Festplatte abnutzen
- FPS (z.B. in CS2 negativ beeinflussen)

## Funktionen

**Vollständiger Scan** - Scannt 9+ Systemlokationen auf temporäre Dateien
**Detaillierte Reports** - Erstellt aussagekräftige Markdown-Reports mit Statistiken
**Sicherheit zuerst** - Interaktive Bestätigung vor dem Löschen
**Selective Cleanup** - Wähle aus, welche Orte gelöscht werden sollen
**Fehlerbehandlung** - Robuste Handhabung von Zugriffsfehlern
**Einsehbarer Quellcode** - Absolut sicher, trotzdem ist die Nutzung auf eigene Gefahr


## Quickstart

### Voraussetzungen
- Python 3.7 oder höher
- Windows 10 oder Windows 11
- Administrator-Rechte (empfohlen für vollständigen Zugriff)

### Installation & Ausführung

```bash
# Clone oder Download des Repositories
cd win_temp_cleaner

# Script ausführen
python main.py
```

## Schritte nach dem Start

Das Tool durchläuft 3 einfache Schritte:

### Scan durchführen
Das Tool scannt automatisch alle bekannten Temp-Locations und zeigt:
- Größe jedes Temp-Ordners
- Anzahl der Dateien
- Warnungen bei Zugriffsproblemen

### Report generieren

Es wird ein detaillierter Markdown-Report erstellt (`temp_scan_report_YYYYMMDD_HHMMSS.md`), der:
- Zusammenfassung des gesamten Speicherverbrauchs
- Detaillierte Aufschlüsselung pro Ort
- Empfehlungen zur Bereinigung
- Fehlerdetails (bei Bedarf)

### Beispiel-Report
> example\example_scan_report.md

### Interaktive Bereinigung
Du kannst dann wählen, ob und welche Temp-Dateien gelöscht werden sollen:
```
Optionen:
  a         - Alle Orte löschen
  1,2,3     - Spezifische Nummern löschen (kommagetrennt)
  q         - Abbrechen
```

## Gescannte Lokationen

Das Tool scannt diese Windows-Verzeichnisse:

| Ort | Pfad |
|-----|------|
| Windows Temp | `C:\Windows\Temp` |
| User Temp | `C:\Users\[User]\AppData\Local\Temp` |
| Windows Update Cache | `C:\Windows\SoftwareDistribution\Download` |
| Prefetch | `C:\Windows\Prefetch` |
| Chrome Cache | `C:\Users\[User]\AppData\Local\Google\Chrome\User Data\Default\Cache` |
| Edge Cache | `C:\Users\[User]\AppData\Local\Microsoft\Edge\User Data\Default\Cache` |
| Firefox Cache | `C:\Users\[User]\AppData\Local\Mozilla\Firefox\Profiles` |
| Windows Explorer Thumbnails | `C:\Users\[User]\AppData\Local\Microsoft\Windows\Explorer` |
| Internet Explorer Cache | `C:\Users\[User]\AppData\Local\Microsoft\Windows\INetCache` |

## Sicherheitshinweise

- **Bestätigung erforderlich**: Das Tool fordert dich auf, jede Löschung zu bestätigen
- **Sichere Dateien**: Es werden nur bekannte temporäre Dateien gelöscht, keine Systemdateien
- **Fehlerbehandlung**: Dateien, die nicht gelöscht werden können (z.B. wegen Zugriffsrechten), werden übersprungen
- **Reports speichern**: Der Scan-Report wird immer gespeichert, auch wenn du keine Dateien löschst
- **Admin-Rechte empfohlen**: Für vollständigen Zugriff solltest du das Script mit Administrator-Rechten ausführen

## Typische Ergebnisse

Nach dem Cleanup kannst du normalerweise erwarten:
- **Speicherfreigabe**: 100 MB bis mehrere GB (abhängig vom System und der Nutzung)
- **Schnellerer PC**: Weniger Disk-I/O und mehr verfügbarer RAM
- **Bessere SSD-Lebensdauer**: Reduzierte Schreibvorgänge

## Beispiel-Report

Der erstellte Report enthält:
```
# Windows Temporäre Dateien - Scan Report

**Erstellt am:** 13.11.2025 um 16:35:22
**Benutzer:** deinbenutzername

## Zusammenfassung
- **Gesamtgröße:** 2.45 GB
- **Anzahl Dateien:** 15,342
- **Gescannte Orte:** 9

## Detaillierte Ergebnisse
...
```

## Technische Details

- **Sprache**: Python 3
- **Abhängigkeiten**: Nur Python Standard Library (keine externen Pakete erforderlich)
- **Plattform**: Windows 10/11 nur
- **Größe**: Minimal (~14 KB)

## FAQ

**F:** *Ist es sicher, alle Temp-Dateien zu löschen?* 

**A:** *Ja, temporäre Dateien sind per Definition nicht essentiell. Windows erstellt sie bei Bedarf neu.*

**F:** *Brauche ich Administrator-Rechte?*
**A:** *Empfohlen, damit das Tool auf alle Verzeichnisse zugreifen kann. Ohne Admin-Rechte können einige Dateien übersprungen werden.*

**F:** *Kann ich das Tool regelmäßig ausführen?*
**A:** *Ja! Es ist völlig sicher, es regelmäßig (z.B. monatlich) auszuführen.*

**F:** *Was passiert mit meinen persönlichen Daten?*
**A:** *Das Tool löscht nur bekannte Windows-Temp-Verzeichnisse. Deine Dateien, Dokumente und Einstellungen bleiben unberührt.*

## Lizenz

Dieses Projekt ist frei nutzbar. Über die Erwähnung oder Stern in GitHub würde ich mich sehr freuen.

---

**Hinweis:** Dieses Tool wurde für Windows 10/11 entwickelt. Führe es mit Administrator-Rechten aus für beste Ergebnisse.

