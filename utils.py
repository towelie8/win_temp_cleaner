#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for Windows Temp File Cleaner
Includes process checking, service management, and file operations
"""

import os
import subprocess
import time
from typing import List, Tuple, Optional


class ProcessManager:
    """Manages process checking and termination"""
    
    @staticmethod
    def is_process_running(process_names: List[str]) -> bool:
        """
        Check if any of the specified processes are running
        
        Args:
            process_names: List of process names to check (e.g., ['chrome.exe', 'firefox.exe'])
            
        Returns:
            True if any process is running, False otherwise
        """
        try:
            # Use tasklist command to get running processes
            result = subprocess.run(
                ['tasklist', '/FO', 'CSV', '/NH'],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                return False
                
            running_processes = result.stdout.lower()
            
            for process_name in process_names:
                if process_name.lower() in running_processes:
                    return True
                    
            return False
            
        except Exception as e:
            print(f"Fehler beim Prozess-Check: {e}")
            return True  # Assume process is running on error (safer)
    
    @staticmethod
    def get_running_processes(process_names: List[str]) -> List[str]:
        """
        Get list of which processes from the list are currently running
        
        Returns:
            List of running process names
        """
        running = []
        try:
            result = subprocess.run(
                ['tasklist', '/FO', 'CSV', '/NH'],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                return running
                
            running_processes = result.stdout.lower()
            
            for process_name in process_names:
                if process_name.lower() in running_processes:
                    running.append(process_name)
                    
        except Exception:
            pass
            
        return running


class ServiceManager:
    """Manages Windows service operations"""
    
    @staticmethod
    def stop_service(service_name: str) -> Tuple[bool, str]:
        """
        Stop a Windows service
        
        Args:
            service_name: Name of the service to stop
            
        Returns:
            Tuple of (success, message)
        """
        try:
            result = subprocess.run(
                ['net', 'stop', service_name],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                return True, f"Service '{service_name}' erfolgreich gestoppt"
            elif "nicht gestartet" in result.stdout.lower() or "not started" in result.stdout.lower():
                return True, f"Service '{service_name}' war bereits gestoppt"
            else:
                return False, f"Fehler beim Stoppen von '{service_name}': {result.stderr}"
                
        except Exception as e:
            return False, f"Exception beim Stoppen von '{service_name}': {str(e)}"
    
    @staticmethod
    def start_service(service_name: str) -> Tuple[bool, str]:
        """
        Start a Windows service
        
        Args:
            service_name: Name of the service to start
            
        Returns:
            Tuple of (success, message)
        """
        try:
            result = subprocess.run(
                ['net', 'start', service_name],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                return True, f"Service '{service_name}' erfolgreich gestartet"
            elif "bereits gestartet" in result.stdout.lower() or "already started" in result.stdout.lower():
                return True, f"Service '{service_name}' war bereits gestartet"
            else:
                return False, f"Fehler beim Starten von '{service_name}': {result.stderr}"
                
        except Exception as e:
            return False, f"Exception beim Starten von '{service_name}': {str(e)}"
    
    @staticmethod
    def is_service_running(service_name: str) -> bool:
        """Check if a service is currently running"""
        try:
            result = subprocess.run(
                ['sc', 'query', service_name],
                capture_output=True,
                text=True,
                check=False
            )
            
            return "RUNNING" in result.stdout
            
        except Exception:
            return False


class PermissionManager:
    """Manages file and folder permissions"""
    
    @staticmethod
    def is_admin() -> bool:
        """Check if script is running with administrator privileges"""
        try:
            # Try to read a system-only file
            with open(r'\\.\PHYSICALDRIVE0', 'rb'):
                pass
            return True
        except:
            return False
    
    @staticmethod
    def takeown_path(path: str) -> Tuple[bool, str]:
        """
        Take ownership of a file or directory
        
        Args:
            path: Path to take ownership of
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Take ownership
            result1 = subprocess.run(
                ['takeown', '/F', path, '/R', '/A', '/D', 'Y'],
                capture_output=True,
                text=True,
                check=False
            )
            
            # Grant full permissions to administrators
            result2 = subprocess.run(
                ['icacls', path, '/T', '/grant', 'administrators:F', '/C'],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result1.returncode == 0 and result2.returncode == 0:
                return True, "Berechtigungen erfolgreich gesetzt"
            else:
                errors = []
                if result1.returncode != 0:
                    errors.append(f"takeown: {result1.stderr}")
                if result2.returncode != 0:
                    errors.append(f"icacls: {result2.stderr}")
                return False, " | ".join(errors)
                
        except Exception as e:
            return False, f"Exception: {str(e)}"


class FileOperations:
    """File and directory operations with error handling"""
    
    @staticmethod
    def delete_directory(path: str, max_retries: int = 3) -> Tuple[int, int, List[str]]:
        """
        Delete directory contents with retry logic
        
        Args:
            path: Directory path to delete
            max_retries: Maximum number of retry attempts for locked files
            
        Returns:
            Tuple of (deleted_files, freed_bytes, errors)
        """
        deleted_files = 0
        freed_bytes = 0
        errors = []
        
        if not os.path.exists(path):
            errors.append(f"Pfad existiert nicht: {path}")
            return deleted_files, freed_bytes, errors
        
        # Handle single file
        if os.path.isfile(path):
            try:
                file_size = os.path.getsize(path)
                os.remove(path)
                deleted_files = 1
                freed_bytes = file_size
                return deleted_files, freed_bytes, errors
            except Exception as e:
                errors.append(f"Fehler bei {path}: {str(e)}")
                return deleted_files, freed_bytes, errors
        
        # Handle directory
        try:
            for dirpath, dirnames, filenames in os.walk(path, topdown=False):
                # Delete files
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    
                    for attempt in range(max_retries):
                        try:
                            file_size = os.path.getsize(file_path)
                            os.remove(file_path)
                            deleted_files += 1
                            freed_bytes += file_size
                            break  # Success, exit retry loop
                            
                        except PermissionError:
                            if attempt < max_retries - 1:
                                time.sleep(0.1)  # Wait a bit before retry
                            else:
                                errors.append(f"Zugriff verweigert: {file_path}")
                                
                        except FileNotFoundError:
                            break  # File already deleted
                            
                        except Exception as e:
                            if attempt < max_retries - 1:
                                time.sleep(0.1)
                            else:
                                errors.append(f"Fehler bei {file_path}: {str(e)}")
                
                # Delete empty directories
                for dirname in dirnames:
                    dir_path = os.path.join(dirpath, dirname)
                    try:
                        if not os.listdir(dir_path):  # Only if empty
                            os.rmdir(dir_path)
                    except (OSError, PermissionError):
                        pass  # Ignore errors for directories
                        
        except Exception as e:
            errors.append(f"Fehler beim Durchlaufen von {path}: {str(e)}")
        
        return deleted_files, freed_bytes, errors
    
    @staticmethod
    def get_directory_size(path: str) -> Tuple[int, int, List[str]]:
        """
        Calculate directory size
        
        Args:
            path: Directory path to calculate
            
        Returns:
            Tuple of (total_bytes, file_count, errors)
        """
        total_size = 0
        file_count = 0
        errors = []
        
        if not os.path.exists(path):
            return total_size, file_count, errors
        
        # Handle single file
        if os.path.isfile(path):
            try:
                return os.path.getsize(path), 1, errors
            except Exception as e:
                errors.append(f"Fehler bei {path}: {str(e)}")
                return 0, 0, errors
        
        # Handle directory
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
    
    @staticmethod
    def kill_explorer() -> bool:
        """Kill and restart Windows Explorer"""
        try:
            # Kill explorer
            subprocess.run(['taskkill', '/F', '/IM', 'explorer.exe'], 
                         capture_output=True, check=False)
            time.sleep(1)
            return True
        except Exception:
            return False
    
    @staticmethod
    def start_explorer() -> bool:
        """Start Windows Explorer"""
        try:
            subprocess.Popen('explorer.exe')
            time.sleep(1)
            return True
        except Exception:
            return False


class DISMOperations:
    """DISM (Deployment Image Servicing and Management) operations"""
    
    @staticmethod
    def analyze_component_store() -> Optional[dict]:
        """
        Analyze WinSxS component store
        
        Returns:
            Dictionary with analysis results or None on error
        """
        try:
            result = subprocess.run(
                ['Dism.exe', '/online', '/Cleanup-Image', '/AnalyzeComponentStore'],
                capture_output=True,
                text=True,
                check=False,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode != 0:
                return None
            
            # Parse output (basic parsing)
            output = result.stdout
            info = {
                'raw_output': output,
                'success': True
            }
            
            # Try to extract size information
            for line in output.split('\n'):
                if 'Actual Size of Component Store' in line or 'Größe des Komponentenspeichers' in line:
                    # Extract size (rough parsing)
                    parts = line.split(':')
                    if len(parts) > 1:
                        info['actual_size'] = parts[1].strip()
                        
            return info
            
        except Exception as e:
            print(f"Fehler bei DISM-Analyse: {e}")
            return None
    
    @staticmethod
    def cleanup_component_store(reset_base: bool = False) -> Tuple[bool, str]:
        """
        Clean up WinSxS component store
        
        Args:
            reset_base: If True, use /ResetBase (more aggressive, removes ability to uninstall updates)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            cmd = ['Dism.exe', '/online', '/Cleanup-Image', '/StartComponentCleanup']
            
            if reset_base:
                cmd.append('/ResetBase')
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                timeout=600  # 10 minutes timeout
            )
            
            if result.returncode == 0:
                return True, "WinSxS Cleanup erfolgreich"
            else:
                return False, f"DISM Fehler: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "DISM Timeout (>10 Minuten)"
        except Exception as e:
            return False, f"DISM Exception: {str(e)}"


def format_size(bytes_size: int) -> str:
    """Format bytes into human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def confirm_action(prompt: str, default: bool = False) -> bool:
    """
    Ask user for confirmation
    
    Args:
        prompt: Question to ask
        default: Default answer if user just presses Enter
        
    Returns:
        True if user confirms, False otherwise
    """
    yes_choices = ['ja', 'j', 'yes', 'y']
    no_choices = ['nein', 'n', 'no']
    
    default_str = " [Ja/nein]" if default else " [ja/Nein]"
    
    while True:
        response = input(prompt + default_str + ": ").strip().lower()
        
        if response == '':
            return default
        elif response in yes_choices:
            return True
        elif response in no_choices:
            return False
        else:
            print("Bitte 'ja' oder 'nein' eingeben.")