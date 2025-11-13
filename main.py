#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows Temporäre Dateien Scanner und Cleaner
Scannt verschiedene Temp-Ordner, erstellt Statistiken und löscht nach Bestätigung
Author: https://github.com/towelie8
"""

import datetime
import getpass
import os
from typing import List, Tuple


class TempFileCleaner:
    def __init__(self):
        self.username = getpass.getuser()
        self.scan_results = {}
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Definiere die zu scannenden Pfade
        self.temp_locations = {
            "Windows Temp": r"C:\Windows\Temp",
            "User Temp": rf"C:\Users\{self.username}\AppData\Local\Temp",
            "Windows Update Cache": r"C:\Windows\SoftwareDistribution\Download",
            "Prefetch": r"C:\Windows\Prefetch",
            "Chrome Cache": rf"C:\Users\{self.username}\AppData\Local\Google\Chrome\User Data\Default\Cache",
            "Edge Cache": rf"C:\Users\{self.username}\AppData\Local\Microsoft\Edge\User Data\Default\Cache",
            "Firefox Cache": rf"C:\Users\{self.username}\AppData\Local\Mozilla\Firefox\Profiles",
            "Windows Explorer Thumbnails": rf"C:\Users\{self.username}\AppData\Local\Microsoft\Windows\Explorer",
            "IE Cache": rf"C:\Users\{self.username}\AppData\Local\Microsoft\Windows\INetCache",
        }

    def get_dir_size(self, path: str) -> Tuple[int, int, List[str]]:
        """
        Berechnet die Größe eines Verzeichnisses
        Returns: (Größe in Bytes, Anzahl Dateien, Liste von Fehlern)
        """
        total_size = 0
        file_count = 0
        errors = []

        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(file_path)
                        file_count += 1
                    except (OSError, PermissionError) as e:
                        errors.append(f"Fehler bei {file_path}: {str(e)}")
        except (OSError, PermissionError) as e:
            errors.append(f"Fehler beim Zugriff auf {path}: {str(e)}")

        return total_size, file_count, errors

    def format_size(self, bytes_size: int) -> str:
        """Formatiert Bytes in lesbare Größe"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} PB"

    def scan_all_locations(self):
        """Scannt alle definierten Temp-Ordner"""
        print("=" * 70)
        print("STARTE SCAN DER TEMPORÄREN DATEIEN")
        print("=" * 70)
        print()

        total_size_all = 0
        total_files_all = 0

        for location_name, path in self.temp_locations.items():
            print(f"Scanne: {location_name}...")

            if not os.path.exists(path):
                self.scan_results[location_name] = {
                    'path': path,
                    'exists': False,
                    'size': 0,
                    'files': 0,
                    'errors': [f"Pfad existiert nicht: {path}"]
                }
                print(f"  ! Pfad existiert nicht\n")
                continue

            size, files, errors = self.get_dir_size(path)
            self.scan_results[location_name] = {
                'path': path,
                'exists': True,
                'size': size,
                'files': files,
                'errors': errors
            }

            total_size_all += size
            total_files_all += files

            print(f"  > Größe: {self.format_size(size)}")
            print(f"  > Dateien: {files}")
            if errors:
                print(f"  ! {len(errors)} Fehler aufgetreten")
            print()

        self.scan_results['_total'] = {
            'size': total_size_all,
            'files': total_files_all
        }

        print("=" * 70)
        print(f"SCAN ABGESCHLOSSEN")
        print(f"Gesamt: {self.format_size(total_size_all)} in {total_files_all} Dateien")
        print("=" * 70)
        print()

    def create_markdown_report(self) -> str:
        """Erstellt einen Markdown-Report der Scan-Ergebnisse"""
        report_filename = f"temp_scan_report_{self.timestamp}.md"
        report_path = os.path.join(os.getcwd(), report_filename)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Windows Temporäre Dateien - Scan Report\n\n")
            f.write(f"**Erstellt am:** {datetime.datetime.now().strftime('%d.%m.%Y um %H:%M:%S')}\n\n")
            f.write(f"**Benutzer:** {self.username}\n\n")
            f.write("---\n\n")

            # Zusammenfassung
            f.write("## Zusammenfassung\n\n")
            total = self.scan_results.get('_total', {})
            f.write(f"- **Gesamtgröße:** {self.format_size(total.get('size', 0))}\n")
            f.write(f"- **Anzahl Dateien:** {total.get('files', 0):,}\n")
            f.write(f"- **Gescannte Orte:** {len([k for k in self.scan_results.keys() if k != '_total'])}\n\n")
            f.write("---\n\n")

            # Detaillierte Ergebnisse
            f.write("## Detaillierte Ergebnisse\n\n")

            # Sortiere nach Größe (größte zuerst)
            sorted_results = sorted(
                [(k, v) for k, v in self.scan_results.items() if k != '_total'],
                key=lambda x: x[1].get('size', 0),
                reverse=True
            )

            for location_name, data in sorted_results:
                f.write(f"### {location_name}\n\n")
                f.write(f"**Pfad:** `{data['path']}`\n\n")

                if not data['exists']:
                    f.write("**Status:** Pfad existiert nicht\n\n")
                    continue

                f.write(f"- **Größe:** {self.format_size(data['size'])}\n")
                f.write(f"- **Dateien:** {data['files']:,}\n")

                if data['size'] > 0:
                    percentage = (data['size'] / total['size'] * 100) if total['size'] > 0 else 0
                    f.write(f"- **Anteil:** {percentage:.1f}% der Gesamtgröße\n")

                if data['errors']:
                    f.write(f"- **⚠ Warnungen:** {len(data['errors'])} Fehler beim Zugriff\n")

                f.write("\n")

            # Fehlerdetails (falls vorhanden)
            all_errors = []
            for location_name, data in self.scan_results.items():
                if location_name != '_total' and data.get('errors'):
                    all_errors.extend([(location_name, err) for err in data['errors']])

            if all_errors:
                f.write("---\n\n")
                f.write("## Fehlerdetails\n\n")
                f.write("<details>\n")
                f.write("<summary>Klicken zum Anzeigen der Fehler</summary>\n\n")
                for location, error in all_errors[:50]:  # Max 50 Fehler anzeigen
                    f.write(f"- **{location}:** {error}\n")
                if len(all_errors) > 50:
                    f.write(f"\n*...und {len(all_errors) - 50} weitere Fehler*\n")
                f.write("\n</details>\n\n")

            # Empfehlungen
            f.write("---\n\n")
            f.write("## Empfehlungen\n\n")

            large_locations = [(name, data) for name, data in sorted_results if
                               data.get('size', 0) > 1024 * 1024 * 100]  # > 100MB

            if large_locations:
                f.write("Die folgenden Orte belegen besonders viel Speicher:\n\n")
                for name, data in large_locations[:5]:
                    f.write(f"- **{name}:** {self.format_size(data['size'])} - kann sicher gelöscht werden\n")
            else:
                f.write("Keine ungewöhnlich großen temporären Dateien gefunden.\n")

            f.write("\n---\n\n")
            f.write("*Dieser Report wurde automatisch erstellt durch TempFileCleaner*\n")

        return report_path

    def delete_location(self, location_name: str) -> Tuple[bool, str]:
        """Löscht die Dateien an einem bestimmten Ort"""
        if location_name not in self.scan_results:
            return False, "Unbekannter Ort"

        data = self.scan_results[location_name]
        path = data['path']

        if not data['exists']:
            return False, "Pfad existiert nicht"

        deleted_files = 0
        deleted_size = 0
        errors = []

        try:
            for dirpath, dirnames, filenames in os.walk(path, topdown=False):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    try:
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        deleted_files += 1
                        deleted_size += file_size
                    except (OSError, PermissionError) as e:
                        errors.append(f"Konnte nicht löschen: {file_path} - {str(e)}")

                # Versuche leere Verzeichnisse zu löschen
                for dirname in dirnames:
                    dir_path = os.path.join(dirpath, dirname)
                    try:
                        if not os.listdir(dir_path):  # Nur wenn leer
                            os.rmdir(dir_path)
                    except (OSError, PermissionError):
                        pass  # Ignoriere Fehler bei Verzeichnissen

        except (OSError, PermissionError) as e:
            return False, f"Fehler beim Zugriff: {str(e)}"

        result_msg = f"✓ {deleted_files} Dateien gelöscht ({self.format_size(deleted_size)} freigegeben)"
        if errors:
            result_msg += f"\n{len(errors)} Dateien konnten nicht gelöscht werden"

        return True, result_msg

    def interactive_cleanup(self):
        """Interaktiver Cleanup-Prozess"""
        print("\n" + "=" * 70)
        print("INTERAKTIVE BEREINIGUNG")
        print("=" * 70)
        print()

        # Zeige Orte sortiert nach Größe
        sorted_results = sorted(
            [(k, v) for k, v in self.scan_results.items() if k != '_total' and v['exists']],
            key=lambda x: x[1].get('size', 0),
            reverse=True
        )

        print("Folgende Orte können bereinigt werden:\n")
        for i, (name, data) in enumerate(sorted_results, 1):
            print(f"{i}. {name}")
            print(f"   Größe: {self.format_size(data['size'])}, Dateien: {data['files']}")
            print(f"   Pfad: {data['path']}\n")

        print("\nOptionen:")
        print("  a - Alle löschen")
        print("  1,2,3 - Spezifische Nummern löschen (kommagetrennt)")
        print("  q - Abbrechen\n")

        choice = input("Deine Wahl: ").strip().lower()

        if choice == 'q':
            print("Abgebrochen.")
            return

        locations_to_delete = []

        if choice == 'a':
            locations_to_delete = [name for name, _ in sorted_results]
        else:
            try:
                indices = [int(x.strip()) for x in choice.split(',')]
                locations_to_delete = [sorted_results[i - 1][0] for i in indices if 1 <= i <= len(sorted_results)]
            except (ValueError, IndexError):
                print("Ungültige Eingabe!")
                return

        if not locations_to_delete:
            print("Keine Orte ausgewählt.")
            return

        # Finale Bestätigung
        total_size_to_delete = sum(
            self.scan_results[loc]['size'] for loc in locations_to_delete
        )

        print(f"\nWARNUNG: Du bist dabei {self.format_size(total_size_to_delete)} zu löschen!")
        print(f"Betroffene Orte: {', '.join(locations_to_delete)}")
        confirm = input("\nWirklich löschen? (ja/nein): ").strip().lower()

        if confirm not in ['ja', 'j', 'yes', 'y']:
            print("Abgebrochen.")
            return

        # Lösche die ausgewählten Orte
        print("\nLösche Dateien...\n")
        for location in locations_to_delete:
            print(f"Bearbeite: {location}...")
            success, message = self.delete_location(location)
            print(f"  {message}\n")

        print("=" * 70)
        print("BEREINIGUNG ABGESCHLOSSEN")
        print("=" * 70)


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     Windows Temporäre Dateien Scanner & Cleaner                   ║
║     Version 1.0                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    cleaner = TempFileCleaner()

    # Schritt 1: Scannen
    cleaner.scan_all_locations()

    # Schritt 2: Markdown-Report erstellen
    print("Erstelle Markdown-Report...")
    report_path = cleaner.create_markdown_report()
    print(f"Report erstellt: {report_path}\n")

    # Schritt 3: Interaktive Bereinigung anbieten
    proceed = input("Möchtest du jetzt Dateien löschen? (ja/nein): ").strip().lower()
    if proceed in ['ja', 'j', 'yes', 'y']:
        cleaner.interactive_cleanup()
    else:
        print("\nKeine Bereinigung durchgeführt. Du kannst den Report jederzeit einsehen.")

    print(f"\nFertig! Report gespeichert unter: {report_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgramm durch Benutzer abgebrochen.")
    except Exception as e:
        print(f"\nUnerwarteter Fehler: {e}")
        import traceback

        traceback.print_exc()