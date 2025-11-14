#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows Temporäre Dateien Scanner und Cleaner - Extended Version
Scannt 50+ Locations, erstellt Statistiken und löscht nach Bestätigung
Author: https://github.com/towelie8
Version: 2.0
"""

import datetime
import getpass
import os
import sys
from typing import List, Tuple, Dict, Optional

# Import configuration and utilities
from config import get_all_locations, get_safe_locations, Priority
from utils import (
    ProcessManager, ServiceManager, PermissionManager, FileOperations,
    DISMOperations, format_size, confirm_action
)


class TempFileCleanerExtended:
    """Extended temp file cleaner with support for 50+ locations"""
    
    def __init__(self):
        self.username = getpass.getuser()
        self.scan_results = {}
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.locations = get_all_locations()
        self.is_admin = PermissionManager.is_admin()
        
        # Statistics
        self.total_scanned = 0
        self.total_size = 0
        self.total_files = 0
        
    def print_header(self):
        """Print application header"""
        print("""
╔══════════════════════════════════════════════════════════════════════╗
║     Windows Temporäre Dateien Scanner & Cleaner                      ║
║     Extended Version 2.0                                             ║
║     Scannt 50+ Locations für maximale Speicherfreigabe              ║
╚══════════════════════════════════════════════════════════════════════╝
""")
        
        if not self.is_admin:
            print("⚠ WARNUNG: Nicht als Administrator gestartet!")
            print("  Einige Locations können nicht gescannt oder gelöscht werden.")
            print("  Für beste Ergebnisse als Administrator ausführen.\n")
    
    def expand_location_paths(self, location: dict) -> List[str]:
        """
        Expand location configuration to actual paths
        
        Args:
            location: Location configuration dictionary
            
        Returns:
            List of actual paths to scan
        """
        paths = []
        
        # Handle single path
        if 'path' in location:
            path = os.path.expandvars(location['path'])
            paths.append(path)
        
        # Handle multiple paths
        if 'paths' in location:
            for p in location['paths']:
                path = os.path.expandvars(p)
                paths.append(path)
        
        return paths
    
    def scan_location(self, location: dict) -> dict:
        """
        Scan a single location
        
        Args:
            location: Location configuration
            
        Returns:
            Scan result dictionary
        """
        name = location['name']
        paths = self.expand_location_paths(location)
        
        result = {
            'name': name,
            'category': location.get('category', 'unknown'),
            'priority': location.get('priority', Priority.LOW),
            'paths': paths,
            'exists': False,
            'size': 0,
            'files': 0,
            'errors': [],
            'safe_delete': location.get('safe_delete', False),
            'requires_admin': location.get('requires_admin', False),
            'description': location.get('description', ''),
            'warning': location.get('warning', ''),
            'method': location.get('method', 'simple_delete'),
            'service_to_stop': location.get('service_to_stop'),
            'process_check': location.get('process_check', []),
        }
        
        # Check if requires admin and we don't have it
        if location.get('requires_admin') and not self.is_admin:
            result['errors'].append("Benötigt Administrator-Rechte")
            return result
        
        # Scan all paths for this location
        total_size = 0
        total_files = 0
        all_errors = []
        found_any = False
        
        for path in paths:
            if os.path.exists(path):
                found_any = True
                size, files, errors = FileOperations.get_directory_size(path)
                total_size += size
                total_files += files
                all_errors.extend(errors)
        
        result['exists'] = found_any
        result['size'] = total_size
        result['files'] = total_files
        result['errors'] = all_errors
        
        return result
    
    def scan_all_locations(self):
        """Scan all configured locations"""
        print("=" * 70)
        print("STARTE ERWEITERTEN SCAN")
        print(f"Scanne {len(self.locations)} Locations...")
        print("=" * 70)
        print()
        
        for i, location in enumerate(self.locations, 1):
            name = location['name']
            print(f"[{i}/{len(self.locations)}] Scanne: {name}...", end='', flush=True)
            
            result = self.scan_location(location)
            self.scan_results[name] = result
            
            if result['exists']:
                print(f" ✓")
                print(f"    Größe: {format_size(result['size'])}, Dateien: {result['files']}")
                if result['errors'] and len(result['errors']) > 0:
                    print(f"    ⚠ {len(result['errors'])} Zugriffsfehler")
                
                self.total_size += result['size']
                self.total_files += result['files']
                self.total_scanned += 1
            else:
                print(f" ✗ (nicht gefunden)")
            
            if result['warning']:
                print(f"    ℹ {result['warning']}")
        
        print()
        print("=" * 70)
        print(f"SCAN ABGESCHLOSSEN")
        print(f"Gefunden: {self.total_scanned} Locations")
        print(f"Gesamt: {format_size(self.total_size)} in {self.total_files:,} Dateien")
        print("=" * 70)
        print()
    
    def create_markdown_report(self) -> str:
        """Create detailed markdown report"""
        report_filename = f"temp_scan_report_{self.timestamp}.md"
        report_path = os.path.join(os.getcwd(), report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Windows Temporäre Dateien - Extended Scan Report\n\n")
            f.write(f"**Erstellt am:** {datetime.datetime.now().strftime('%d.%m.%Y um %H:%M:%S')}\n")
            f.write(f"**Benutzer:** {self.username}\n")
            f.write(f"**Administrator-Rechte:** {'Ja' if self.is_admin else 'Nein'}\n\n")
            f.write("---\n\n")
            
            # Summary
            f.write("## Zusammenfassung\n\n")
            f.write(f"- **Gesamtgröße:** {format_size(self.total_size)}\n")
            f.write(f"- **Anzahl Dateien:** {self.total_files:,}\n")
            f.write(f"- **Gefundene Locations:** {self.total_scanned} von {len(self.locations)}\n")
            f.write(f"- **Löschbare Locations:** {len([r for r in self.scan_results.values() if r['safe_delete'] and r['exists']])}\n\n")
            f.write("---\n\n")
            
            # Priority breakdown
            f.write("## Nach Priorität\n\n")
            
            priority_groups = {
                Priority.CRITICAL: ("🔴 Kritisch (Hohe Priorität, spezielle Behandlung)", []),
                Priority.HIGH: ("🟠 Hoch (Große Dateien, sicher löschbar)", []),
                Priority.MEDIUM: ("🟡 Mittel (Moderate Größe)", []),
                Priority.LOW: ("🟢 Niedrig (Klein oder bedingt löschbar)", []),
                Priority.NEVER: ("⚫ Nur Anzeige (NIEMALS löschen)", []),
            }
            
            for result in self.scan_results.values():
                if result['exists']:
                    pri = result['priority']
                    if pri in priority_groups:
                        priority_groups[pri][1].append(result)
            
            for priority, (label, results) in sorted(priority_groups.items()):
                if not results:
                    continue
                    
                f.write(f"### {label}\n\n")
                
                # Sort by size within priority
                results.sort(key=lambda x: x['size'], reverse=True)
                
                for result in results:
                    f.write(f"#### {result['name']}\n\n")
                    f.write(f"- **Größe:** {format_size(result['size'])}\n")
                    f.write(f"- **Dateien:** {result['files']:,}\n")
                    f.write(f"- **Kategorie:** {result['category']}\n")
                    f.write(f"- **Sicher löschbar:** {'✅ Ja' if result['safe_delete'] else '❌ Nein'}\n")
                    
                    if result['requires_admin']:
                        f.write(f"- **Benötigt Admin:** Ja\n")
                    
                    if result['description']:
                        f.write(f"- **Beschreibung:** {result['description']}\n")
                    
                    if result['warning']:
                        f.write(f"- **⚠ Warnung:** {result['warning']}\n")
                    
                    # Show first path
                    if result['paths']:
                        f.write(f"- **Pfad:** `{result['paths'][0]}`\n")
                    
                    if len(result['errors']) > 0:
                        f.write(f"- **Fehler:** {len(result['errors'])} Zugriffsprobleme\n")
                    
                    f.write("\n")
                
                f.write("---\n\n")
            
            # Category breakdown
            f.write("## Nach Kategorie\n\n")
            
            categories = {}
            for result in self.scan_results.values():
                if not result['exists']:
                    continue
                cat = result['category']
                if cat not in categories:
                    categories[cat] = {'size': 0, 'files': 0, 'count': 0}
                categories[cat]['size'] += result['size']
                categories[cat]['files'] += result['files']
                categories[cat]['count'] += 1
            
            for cat, stats in sorted(categories.items(), key=lambda x: x[1]['size'], reverse=True):
                f.write(f"- **{cat}:** {format_size(stats['size'])} "
                       f"({stats['files']:,} Dateien in {stats['count']} Locations)\n")
            
            f.write("\n---\n\n")
            
            # Recommendations
            f.write("## Empfehlungen\n\n")
            
            # Top 10 largest
            largest = sorted(
                [r for r in self.scan_results.values() if r['exists'] and r['safe_delete']],
                key=lambda x: x['size'],
                reverse=True
            )[:10]
            
            if largest:
                f.write("### Top 10 größte löschbare Locations:\n\n")
                for i, result in enumerate(largest, 1):
                    f.write(f"{i}. **{result['name']}** - {format_size(result['size'])}\n")
                f.write("\n")
            
            # Critical warnings
            critical_locs = [r for r in self.scan_results.values() 
                           if r['exists'] and r['priority'] == Priority.CRITICAL]
            
            if critical_locs:
                f.write("### ⚠ Kritische Locations (Spezielle Behandlung erforderlich):\n\n")
                for result in critical_locs:
                    f.write(f"- **{result['name']}:** {format_size(result['size'])}\n")
                    if result['warning']:
                        f.write(f"  - *{result['warning']}*\n")
                f.write("\n")
            
            f.write("---\n\n")
            f.write("*Report generiert durch Windows Temp File Cleaner Extended v2.0*\n")
        
        return report_path
    
    def delete_location(self, location_name: str) -> Tuple[bool, str, int, int]:
        """
        Delete files at a specific location
        
        Returns:
            Tuple of (success, message, deleted_files, freed_bytes)
        """
        if location_name not in self.scan_results:
            return False, "Unbekannter Ort", 0, 0
        
        result = self.scan_results[location_name]
        
        if not result['exists']:
            return False, "Location existiert nicht", 0, 0
        
        if not result['safe_delete']:
            return False, "Location ist nicht sicher zu löschen!", 0, 0
        
        # Check admin requirements
        if result['requires_admin'] and not self.is_admin:
            return False, "Benötigt Administrator-Rechte", 0, 0
        
        # Check for running processes
        if result['process_check']:
            running = ProcessManager.get_running_processes(result['process_check'])
            if running:
                return False, f"Prozesse laufen noch: {', '.join(running)}", 0, 0
        
        # Stop service if required
        service_stopped = False
        if result['service_to_stop']:
            success, msg = ServiceManager.stop_service(result['service_to_stop'])
            if success:
                service_stopped = True
            else:
                return False, f"Service konnte nicht gestoppt werden: {msg}", 0, 0
        
        # Delete files
        total_deleted = 0
        total_freed = 0
        all_errors = []
        
        for path in result['paths']:
            if os.path.exists(path):
                deleted, freed, errors = FileOperations.delete_directory(path)
                total_deleted += deleted
                total_freed += freed
                all_errors.extend(errors)
        
        # Restart service if it was stopped
        if service_stopped:
            ServiceManager.start_service(result['service_to_stop'])
        
        # Build result message
        msg = f"✓ {total_deleted} Dateien gelöscht ({format_size(total_freed)} freigegeben)"
        if all_errors:
            msg += f"\n{len(all_errors)} Dateien konnten nicht gelöscht werden"
        
        return True, msg, total_deleted, total_freed
    
    def interactive_cleanup(self):
        """Interactive cleanup interface"""
        print("\n" + "=" * 70)
        print("INTERAKTIVE BEREINIGUNG")
        print("=" * 70)
        print()
        
        # Get deletable locations sorted by size
        deletable = sorted(
            [(name, r) for name, r in self.scan_results.items() 
             if r['exists'] and r['safe_delete']],
            key=lambda x: x[1]['size'],
            reverse=True
        )
        
        if not deletable:
            print("Keine löschbaren Locations gefunden.")
            return
        
        print(f"Gefunden: {len(deletable)} löschbare Locations\n")
        
        # Show by priority
        for priority in [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            priority_locs = [(n, r) for n, r in deletable if r['priority'] == priority]
            
            if not priority_locs:
                continue
            
            priority_names = {
                Priority.CRITICAL: "🔴 KRITISCH",
                Priority.HIGH: "🟠 HOCH",
                Priority.MEDIUM: "🟡 MITTEL",
                Priority.LOW: "🟢 NIEDRIG",
            }
            
            print(f"\n{priority_names.get(priority, 'UNKNOWN')}:")
            print("-" * 70)
            
            for name, result in priority_locs:
                idx = deletable.index((name, result)) + 1
                print(f"{idx:2d}. {name}")
                print(f"    Größe: {format_size(result['size'])}, Dateien: {result['files']}")
                print(f"    Pfad: {result['paths'][0]}")
                if result['warning']:
                    print(f"    ⚠ {result['warning']}")
                if result['process_check']:
                    print(f"    ⚙ Prüft Prozesse: {', '.join(result['process_check'])}")
                print()
        
        print("\nOptionen:")
        print("  a           - Alle SICHEREN Locations löschen")
        print("  h           - Nur HOHE Priorität löschen")
        print("  1,2,3       - Spezifische Nummern löschen (kommagetrennt)")
        print("  q           - Abbrechen")
        print()
        
        choice = input("Deine Wahl: ").strip().lower()
        
        if choice == 'q':
            print("Abgebrochen.")
            return
        
        locations_to_delete = []
        
        if choice == 'a':
            # All safe locations
            locations_to_delete = [name for name, _ in deletable]
        elif choice == 'h':
            # Only high priority
            locations_to_delete = [name for name, r in deletable 
                                  if r['priority'] in [Priority.HIGH, Priority.CRITICAL]]
        else:
            # Specific indices
            try:
                indices = [int(x.strip()) for x in choice.split(',')]
                locations_to_delete = [deletable[i-1][0] for i in indices 
                                      if 1 <= i <= len(deletable)]
            except (ValueError, IndexError):
                print("❌ Ungültige Eingabe!")
                return
        
        if not locations_to_delete:
            print("Keine Locations ausgewählt.")
            return
        
        # Calculate total size
        total_size_to_delete = sum(
            self.scan_results[loc]['size'] for loc in locations_to_delete
        )
        
        # Show summary and confirm
        print(f"\n{'='*70}")
        print(f"WARNUNG: Du bist dabei {format_size(total_size_to_delete)} zu löschen!")
        print(f"{'='*70}")
        print(f"\nAusgewählte Locations ({len(locations_to_delete)}):")
        for loc in locations_to_delete:
            result = self.scan_results[loc]
            print(f"  • {loc} - {format_size(result['size'])}")
        print()
        
        if not confirm_action("Wirklich löschen?", default=False):
            print("❌ Abgebrochen.")
            return
        
        # Perform deletion
        print(f"\n{'='*70}")
        print("LÖSCHE DATEIEN...")
        print(f"{'='*70}\n")
        
        total_deleted_files = 0
        total_freed_bytes = 0
        
        for loc in locations_to_delete:
            print(f"Bearbeite: {loc}...")
            success, message, deleted, freed = self.delete_location(loc)
            
            if success:
                print(f"  {message}")
                total_deleted_files += deleted
                total_freed_bytes += freed
            else:
                print(f"  ❌ Fehler: {message}")
            print()
        
        print("=" * 70)
        print("BEREINIGUNG ABGESCHLOSSEN")
        print("=" * 70)
        print(f"\nGesamt gelöscht: {total_deleted_files:,} Dateien")
        print(f"Gesamt freigegeben: {format_size(total_freed_bytes)}")
        print()


def main():
    """Main application entry point"""
    cleaner = TempFileCleanerExtended()
    
    # Print header
    cleaner.print_header()
    
    # Scan all locations
    cleaner.scan_all_locations()
    
    # Create report
    print("Erstelle erweiterten Markdown-Report...")
    report_path = cleaner.create_markdown_report()
    print(f"✓ Report erstellt: {report_path}\n")
    
    # Offer cleanup
    if cleaner.total_size > 0:
        if confirm_action("Möchtest du jetzt Dateien löschen?", default=False):
            cleaner.interactive_cleanup()
        else:
            print("\n✓ Keine Bereinigung durchgeführt.")
            print("  Du kannst den Report jederzeit einsehen für Details.")
    else:
        print("ℹ Keine temporären Dateien zum Löschen gefunden.")
    
    print(f"\n✓ Fertig! Report: {report_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Programm durch Benutzer abgebrochen.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unerwarteter Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)