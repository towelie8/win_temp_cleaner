PS M:\workspace> cd .\win_temp_cleaner
PS M:\workspace\win_temp_cleaner> python main.py

╔═══════════════════════════════════════════════════════════════════╗
║     Windows Temporäre Dateien Scanner & Cleaner                   ║
║     Version 1.0                                                   ║
╚═══════════════════════════════════════════════════════════════════╝

======================================================================
STARTE SCAN DER TEMPORÄREN DATEIEN
======================================================================

Scanne: Windows Temp...
  > Größe: 5.75 MB
  > Dateien: 36

Scanne: User Temp...
  > Größe: 3.38 GB
  > Dateien: 2224

Scanne: Windows Update Cache...
  > Größe: 776.82 KB
  > Dateien: 2

Scanne: Prefetch...
  > Größe: 2.84 MB
  > Dateien: 149

Scanne: Chrome Cache...
  > Größe: 0.00 B
  > Dateien: 0

Scanne: Edge Cache...
  > Größe: 18.69 MB
  > Dateien: 10

Scanne: Firefox Cache...
  > Größe: 229.87 MB
  > Dateien: 3263

Scanne: Windows Explorer Thumbnails...
  > Größe: 7.04 MB
  > Dateien: 32

Scanne: IE Cache...
  > Größe: 326.50 KB
  > Dateien: 87

======================================================================
SCAN ABGESCHLOSSEN
Gesamt: 3.64 GB in 5803 Dateien
======================================================================

Erstelle Markdown-Report...
Report erstellt: M:\workspace\win_temp_cleaner\temp_scan_report_20251114_124948.md

Möchtest du jetzt Dateien löschen? (ja/nein): ja

======================================================================
INTERAKTIVE BEREINIGUNG
======================================================================

Folgende Orte können bereinigt werden:

1. User Temp
   Größe: 3.38 GB, Dateien: 2224
   Pfad: C:\Users\towelie\AppData\Local\Temp

2. Firefox Cache
   Größe: 229.87 MB, Dateien: 3263
   Pfad: C:\Users\towelie\AppData\Local\Mozilla\Firefox\Profiles

3. Edge Cache
   Größe: 18.69 MB, Dateien: 10
   Pfad: C:\Users\towelie\AppData\Local\Microsoft\Edge\User Data\Default\Cache

4. Windows Explorer Thumbnails
   Größe: 7.04 MB, Dateien: 32
   Pfad: C:\Users\towelie\AppData\Local\Microsoft\Windows\Explorer

5. Windows Temp
   Größe: 5.75 MB, Dateien: 36
   Pfad: C:\Windows\Temp

6. Prefetch
   Größe: 2.84 MB, Dateien: 149
   Pfad: C:\Windows\Prefetch

7. Windows Update Cache
   Größe: 776.82 KB, Dateien: 2
   Pfad: C:\Windows\SoftwareDistribution\Download

8. IE Cache
   Größe: 326.50 KB, Dateien: 87
   Pfad: C:\Users\towelie\AppData\Local\Microsoft\Windows\INetCache

9. Chrome Cache
   Größe: 0.00 B, Dateien: 0
   Pfad: C:\Users\towelie\AppData\Local\Google\Chrome\User Data\Default\Cache


Optionen:
  a - Alle löschen
  1,2,3 - Spezifische Nummern löschen (kommagetrennt)
  q - Abbrechen

Deine Wahl: a

WARNUNG: Du bist dabei 3.64 GB zu löschen!
Betroffene Orte: User Temp, Firefox Cache, Edge Cache, Windows Explorer Thumbnails, Windows Temp, Prefetch, Windows Update Cache, IE Cache, Chrome Cache

Wirklich löschen? (ja/nein): ja

Lösche Dateien...

Bearbeite: User Temp...
  ✓ 2205 Dateien gelöscht (3.36 GB freigegeben)
19 Dateien konnten nicht gelöscht werden

Bearbeite: Firefox Cache...
  ✓ 3258 Dateien gelöscht (184.66 MB freigegeben)
5 Dateien konnten nicht gelöscht werden

Bearbeite: Edge Cache...
  ✓ 4 Dateien gelöscht (351.01 KB freigegeben)
6 Dateien konnten nicht gelöscht werden

Bearbeite: Windows Explorer Thumbnails...
  ✓ 31 Dateien gelöscht (7.03 MB freigegeben)
1 Dateien konnten nicht gelöscht werden

Bearbeite: Windows Temp...
  ✓ 28 Dateien gelöscht (5.01 MB freigegeben)
8 Dateien konnten nicht gelöscht werden

Bearbeite: Prefetch...
  ✓ 149 Dateien gelöscht (2.67 MB freigegeben)
1 Dateien konnten nicht gelöscht werden

Bearbeite: Windows Update Cache...
  ✓ 2 Dateien gelöscht (776.82 KB freigegeben)

Bearbeite: IE Cache...
  ✓ 87 Dateien gelöscht (326.50 KB freigegeben)

Bearbeite: Chrome Cache...
  ✓ 0 Dateien gelöscht (0.00 B freigegeben)

======================================================================
BEREINIGUNG ABGESCHLOSSEN
======================================================================

Fertig! Report gespeichert unter: M:\workspace\win_temp_cleaner\temp_scan_report_20251114_124948.md
PS M:\workspace\win_temp_cleaner>