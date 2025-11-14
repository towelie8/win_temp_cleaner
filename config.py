#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration file for Windows Temp File Cleaner
Defines all temporary file locations to be scanned and cleaned
"""

import os

# Get current username for dynamic path expansion
USERNAME = os.environ.get('USERNAME', 'User')


class LocationCategory:
    """Categories for grouping temp locations"""
    SYSTEM = "system"
    BROWSER = "browser"
    APPLICATION = "application"
    GAMING = "gaming"
    DEVELOPMENT = "development"
    CLOUD = "cloud"
    LOGS = "logs"
    VIEW_ONLY = "view_only"


class Priority:
    """Priority levels for cleanup"""
    HIGH = 1      # Large files, safe to delete
    MEDIUM = 2    # Moderate size, safe to delete
    LOW = 3       # Small files or conditional deletion
    CRITICAL = 4  # High priority but requires special handling
    NEVER = 99    # Never delete (view only)


# ==================== HIGH PRIORITY LOCATIONS ====================

HIGH_PRIORITY_LOCATIONS = [
    {
        'name': 'Windows.old',
        'path': r'C:\Windows.old',
        'category': LocationCategory.SYSTEM,
        'priority': Priority.CRITICAL,
        'safe_delete': True,
        'requires_admin': True,
        'requires_takeown': True,
        'method': 'takeown_and_delete',
        'expected_size_mb': 15000,
        'description': 'Previous Windows installation backup',
        'warning': 'Only delete if >30 days since upgrade and system is stable'
    },
    {
        'name': 'Windows Upgrade Files ($Windows.~BT)',
        'path': r'C:\$Windows.~BT',
        'category': LocationCategory.SYSTEM,
        'priority': Priority.CRITICAL,
        'safe_delete': True,
        'requires_admin': True,
        'requires_takeown': True,
        'method': 'takeown_and_delete',
        'expected_size_mb': 10000,
        'description': 'Windows upgrade temporary files'
    },
    {
        'name': 'Windows Upgrade Files ($Windows.~WS)',
        'path': r'C:\$Windows.~WS',
        'category': LocationCategory.SYSTEM,
        'priority': Priority.CRITICAL,
        'safe_delete': True,
        'requires_admin': True,
        'requires_takeown': True,
        'method': 'takeown_and_delete',
        'expected_size_mb': 5000,
        'description': 'Windows setup temporary files'
    },
    {
        'name': 'WinRE Agent Files',
        'path': r'C:\$WinREAgent',
        'category': LocationCategory.SYSTEM,
        'priority': Priority.HIGH,
        'safe_delete': True,
        'requires_admin': True,
        'method': 'simple_delete',
        'expected_size_mb': 1000,
        'description': 'Windows Recovery Environment agent files'
    },
    {
        'name': 'Windows Error Reporting - ReportQueue',
        'paths': [
            r'C:\ProgramData\Microsoft\Windows\WER\ReportQueue',
            os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\WER\ReportQueue')
        ],
        'category': LocationCategory.SYSTEM,
        'priority': Priority.HIGH,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 5000,
        'description': 'Windows Error Reporting crash reports'
    },
    {
        'name': 'Windows Error Reporting - ReportArchive',
        'paths': [
            r'C:\ProgramData\Microsoft\Windows\WER\ReportArchive',
            os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\WER\ReportArchive')
        ],
        'category': LocationCategory.SYSTEM,
        'priority': Priority.HIGH,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 3000,
        'description': 'Archived crash reports'
    },
    {
        'name': 'Application Crash Dumps',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\CrashDumps'),
        'category': LocationCategory.SYSTEM,
        'priority': Priority.HIGH,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 2000,
        'description': 'User-mode application crash dumps'
    },
    {
        'name': 'Memory Dump Files',
        'path': r'C:\Windows\MEMORY.DMP',
        'category': LocationCategory.SYSTEM,
        'priority': Priority.HIGH,
        'safe_delete': True,
        'requires_admin': True,
        'method': 'simple_delete',
        'expected_size_mb': 16000,
        'description': 'Complete/Kernel memory dumps (BSOD)',
        'is_file': True  # This is a single file, not a directory
    },
    {
        'name': 'Minidump Files',
        'path': r'C:\Windows\Minidump',
        'category': LocationCategory.SYSTEM,
        'priority': Priority.HIGH,
        'safe_delete': True,
        'requires_admin': True,
        'method': 'simple_delete',
        'expected_size_mb': 500,
        'description': 'Small memory dumps (256KB each)'
    },
    {
        'name': 'Live Kernel Reports',
        'path': r'C:\Windows\LiveKernelReports',
        'category': LocationCategory.SYSTEM,
        'priority': Priority.HIGH,
        'safe_delete': True,
        'requires_admin': True,
        'method': 'simple_delete',
        'expected_size_mb': 1000,
        'description': 'Kernel crash reports'
    },
    {
        'name': 'CBS Logs (Component Based Servicing)',
        'paths': [
            r'C:\Windows\Logs\CBS\CBS.log',
            r'C:\Windows\Logs\CBS',
        ],
        'category': LocationCategory.LOGS,
        'priority': Priority.CRITICAL,
        'safe_delete': True,
        'requires_admin': True,
        'service_to_stop': 'TrustedInstaller',
        'method': 'service_stop_delete',
        'expected_size_mb': 10000,
        'description': 'Windows Update and component servicing logs',
        'warning': 'Can grow to 20+ GB in buggy situations'
    },
    {
        'name': 'Delivery Optimization Cache',
        'path': r'C:\Windows\SoftwareDistribution\DeliveryOptimization',
        'category': LocationCategory.SYSTEM,
        'priority': Priority.HIGH,
        'safe_delete': True,
        'requires_admin': True,
        'method': 'simple_delete',
        'expected_size_mb': 10000,
        'description': 'P2P Windows Update distribution cache'
    },
    {
        'name': 'Windows Defender Scan History',
        'path': r'C:\ProgramData\Microsoft\Windows Defender\Scans\History',
        'category': LocationCategory.SYSTEM,
        'priority': Priority.HIGH,
        'safe_delete': True,
        'requires_admin': True,
        'service_to_stop': 'WinDefend',
        'method': 'service_stop_delete',
        'expected_size_mb': 15000,
        'description': 'Windows Defender scan cache files (mpcache-*.bin)',
        'warning': 'Can grow to 20+ GB with large cache files'
    },
    {
        'name': 'Diagnostic ETL Logs',
        'path': r'C:\ProgramData\Microsoft\Diagnosis\ETLLogs',
        'category': LocationCategory.LOGS,
        'priority': Priority.CRITICAL,
        'safe_delete': True,
        'requires_admin': True,
        'requires_system_rights': True,
        'method': 'elevated_delete',
        'expected_size_mb': 30000,
        'description': 'Windows telemetry and diagnostic data',
        'warning': 'Often overlooked but can be HUGE (50+ GB)'
    },
]


# ==================== MEDIUM PRIORITY LOCATIONS ====================

MEDIUM_PRIORITY_LOCATIONS = [
    # Original basic locations
    {
        'name': 'Windows Temp',
        'path': r'C:\Windows\Temp',
        'category': LocationCategory.SYSTEM,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': True,
        'method': 'simple_delete',
        'expected_size_mb': 500,
        'description': 'System-wide temporary files'
    },
    {
        'name': 'User Temp',
        'path': os.path.expandvars(r'%TEMP%'),
        'category': LocationCategory.SYSTEM,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 3000,
        'description': 'User temporary files'
    },
    {
        'name': 'Windows Update Cache',
        'path': r'C:\Windows\SoftwareDistribution\Download',
        'category': LocationCategory.SYSTEM,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': True,
        'service_to_stop': 'wuauserv',
        'method': 'service_stop_delete',
        'expected_size_mb': 2000,
        'description': 'Downloaded Windows updates'
    },
    {
        'name': 'Prefetch',
        'path': r'C:\Windows\Prefetch',
        'category': LocationCategory.SYSTEM,
        'priority': Priority.LOW,
        'safe_delete': True,
        'requires_admin': True,
        'method': 'simple_delete',
        'expected_size_mb': 100,
        'description': 'Application prefetch data'
    },
    
    # Browser caches
    {
        'name': 'Chrome Cache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache'),
        'category': LocationCategory.BROWSER,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'process_check': ['chrome.exe'],
        'method': 'process_check_delete',
        'expected_size_mb': 1000,
        'description': 'Google Chrome cache'
    },
    {
        'name': 'Edge Cache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache'),
        'category': LocationCategory.BROWSER,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'process_check': ['msedge.exe'],
        'method': 'process_check_delete',
        'expected_size_mb': 1000,
        'description': 'Microsoft Edge cache'
    },
    {
        'name': 'Firefox Cache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\Mozilla\Firefox\Profiles'),
        'category': LocationCategory.BROWSER,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'process_check': ['firefox.exe'],
        'method': 'process_check_delete',
        'expected_size_mb': 1000,
        'description': 'Mozilla Firefox cache'
    },
    
    # Application caches
    {
        'name': 'Discord Cache',
        'paths': [
            os.path.expandvars(r'%APPDATA%\Discord\Cache'),
            os.path.expandvars(r'%APPDATA%\Discord\Code Cache'),
            os.path.expandvars(r'%APPDATA%\Discord\GPUCache'),
        ],
        'category': LocationCategory.APPLICATION,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'process_check': ['Discord.exe'],
        'method': 'process_check_delete',
        'expected_size_mb': 5000,
        'description': 'Discord cached images and media'
    },
    {
        'name': 'Microsoft Teams Cache (Classic)',
        'paths': [
            os.path.expandvars(r'%APPDATA%\Microsoft\Teams\Application Cache'),
            os.path.expandvars(r'%APPDATA%\Microsoft\Teams\Cache'),
            os.path.expandvars(r'%APPDATA%\Microsoft\Teams\blob_storage'),
            os.path.expandvars(r'%APPDATA%\Microsoft\Teams\databases'),
            os.path.expandvars(r'%APPDATA%\Microsoft\Teams\GPUcache'),
            os.path.expandvars(r'%APPDATA%\Microsoft\Teams\IndexedDB'),
            os.path.expandvars(r'%APPDATA%\Microsoft\Teams\Local Storage'),
            os.path.expandvars(r'%APPDATA%\Microsoft\Teams\tmp'),
        ],
        'category': LocationCategory.APPLICATION,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'process_check': ['Teams.exe'],
        'method': 'process_check_delete',
        'expected_size_mb': 2000,
        'description': 'Microsoft Teams cache (Classic version)'
    },
    {
        'name': 'Slack Cache',
        'paths': [
            os.path.expandvars(r'%APPDATA%\Slack\Cache'),
            os.path.expandvars(r'%APPDATA%\Slack\Code Cache'),
        ],
        'category': LocationCategory.APPLICATION,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'process_check': ['slack.exe'],
        'method': 'process_check_delete',
        'expected_size_mb': 2000,
        'description': 'Slack message and file cache'
    },
    {
        'name': 'Spotify Cache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\Spotify\Data'),
        'category': LocationCategory.APPLICATION,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'process_check': ['Spotify.exe'],
        'method': 'process_check_delete',
        'expected_size_mb': 10000,
        'description': 'Spotify streaming cache',
        'warning': 'Can be configured to use up to 10% of free disk space'
    },
    {
        'name': 'Zoom Cache',
        'paths': [
            os.path.expandvars(r'%APPDATA%\Zoom\logs'),
            os.path.expandvars(r'%APPDATA%\Zoom\cache'),
        ],
        'category': LocationCategory.APPLICATION,
        'priority': Priority.LOW,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 500,
        'description': 'Zoom meeting logs and cache'
    },
    
    # Gaming
    {
        'name': 'NVIDIA DXCache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\NVIDIA\DXCache'),
        'category': LocationCategory.GAMING,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 5000,
        'description': 'NVIDIA DirectX shader cache'
    },
    {
        'name': 'NVIDIA GLCache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\NVIDIA\GLCache'),
        'category': LocationCategory.GAMING,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 2000,
        'description': 'NVIDIA OpenGL shader cache'
    },
    {
        'name': 'AMD DXCache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\AMD\DxCache'),
        'category': LocationCategory.GAMING,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 3000,
        'description': 'AMD DirectX shader cache'
    },
    {
        'name': 'AMD VkCache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\AMD\VkCache'),
        'category': LocationCategory.GAMING,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 2000,
        'description': 'AMD Vulkan shader cache'
    },
    {
        'name': 'Intel Shader Cache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\Intel\ShaderCache'),
        'category': LocationCategory.GAMING,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 1000,
        'description': 'Intel GPU shader cache'
    },
    {
        'name': 'DirectX Shader Cache',
        'paths': [
            os.path.expandvars(r'%LOCALAPPDATA%\D3DSCache'),
            os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\D3DSCache'),
        ],
        'category': LocationCategory.GAMING,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 3000,
        'description': 'DirectX shader cache'
    },
    
    # Development tools
    {
        'name': 'npm Cache',
        'paths': [
            os.path.expandvars(r'%APPDATA%\npm-cache'),
            os.path.expandvars(r'%LOCALAPPDATA%\npm-cache'),
        ],
        'category': LocationCategory.DEVELOPMENT,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 5000,
        'description': 'Node.js package manager cache'
    },
    {
        'name': 'pip Cache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\pip\cache'),
        'category': LocationCategory.DEVELOPMENT,
        'priority': Priority.MEDIUM,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 2000,
        'description': 'Python package installer cache'
    },
]


# ==================== LOW PRIORITY LOCATIONS ====================

LOW_PRIORITY_LOCATIONS = [
    {
        'name': 'Windows Explorer Thumbnails',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Explorer'),
        'category': LocationCategory.SYSTEM,
        'priority': Priority.LOW,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 200,
        'description': 'Cached thumbnail images'
    },
    {
        'name': 'IE Cache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\INetCache'),
        'category': LocationCategory.BROWSER,
        'priority': Priority.LOW,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 100,
        'description': 'Internet Explorer cache'
    },
    {
        'name': 'Icon Cache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Explorer'),
        'patterns': ['iconcache_*.db'],
        'category': LocationCategory.SYSTEM,
        'priority': Priority.LOW,
        'safe_delete': True,
        'requires_admin': False,
        'process_check': ['explorer.exe'],
        'method': 'explorer_restart_delete',
        'expected_size_mb': 200,
        'description': 'Cached icon images',
        'warning': 'Requires explorer.exe restart'
    },
    {
        'name': 'Font Cache',
        'paths': [
            r'C:\Windows\ServiceProfiles\LocalService\AppData\Local\FontCache',
            r'C:\Windows\System32\FNTCACHE.DAT',
        ],
        'category': LocationCategory.SYSTEM,
        'priority': Priority.LOW,
        'safe_delete': True,
        'requires_admin': True,
        'service_to_stop': 'FontCache',
        'method': 'service_stop_delete',
        'expected_size_mb': 50,
        'description': 'Font rendering cache'
    },
    {
        'name': 'Recent Documents',
        'paths': [
            os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Recent'),
            os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Recent\AutomaticDestinations'),
            os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Recent\CustomDestinations'),
        ],
        'category': LocationCategory.SYSTEM,
        'priority': Priority.LOW,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 50,
        'description': 'Recently used files and jump lists'
    },
    {
        'name': 'Notification Cache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Notifications'),
        'patterns': ['wpndatabase.db*'],
        'category': LocationCategory.SYSTEM,
        'priority': Priority.LOW,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 50,
        'description': 'Windows notification history'
    },
    {
        'name': 'Cryptnet URL Cache',
        'path': os.path.expandvars(r'%USERPROFILE%\AppData\LocalLow\Microsoft\CryptnetUrlCache'),
        'category': LocationCategory.SYSTEM,
        'priority': Priority.LOW,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 100,
        'description': 'Certificate revocation list cache'
    },
    {
        'name': 'Windows Store Cache',
        'path': os.path.expandvars(r'%LOCALAPPDATA%\Packages\Microsoft.WindowsStore_8wekyb3d8bbwe\LocalCache'),
        'category': LocationCategory.SYSTEM,
        'priority': Priority.LOW,
        'safe_delete': True,
        'requires_admin': False,
        'method': 'simple_delete',
        'expected_size_mb': 500,
        'description': 'Microsoft Store cache'
    },
]


# ==================== VIEW ONLY LOCATIONS ====================

VIEW_ONLY_LOCATIONS = [
    {
        'name': 'Windows Installer Cache',
        'path': r'C:\Windows\Installer',
        'category': LocationCategory.VIEW_ONLY,
        'priority': Priority.NEVER,
        'safe_delete': False,
        'requires_admin': True,
        'method': 'display_only',
        'expected_size_mb': 30000,
        'description': 'MSI installer cache - NEVER DELETE',
        'warning': 'Deleting breaks application repair, uninstall, and updates'
    },
    {
        'name': 'WinSxS Component Store',
        'path': r'C:\Windows\WinSxS',
        'category': LocationCategory.VIEW_ONLY,
        'priority': Priority.NEVER,
        'safe_delete': False,
        'requires_admin': True,
        'method': 'dism_cleanup',
        'expected_size_mb': 10000,
        'description': 'Windows component store - Use DISM only',
        'warning': 'Only clean with: Dism.exe /online /Cleanup-Image /StartComponentCleanup'
    },
]


# ==================== COMBINED LOCATIONS ====================

def get_all_locations():
    """Returns all location configurations in priority order"""
    return (
        HIGH_PRIORITY_LOCATIONS +
        MEDIUM_PRIORITY_LOCATIONS +
        LOW_PRIORITY_LOCATIONS +
        VIEW_ONLY_LOCATIONS
    )


def get_locations_by_category(category):
    """Returns all locations for a specific category"""
    return [loc for loc in get_all_locations() if loc['category'] == category]


def get_locations_by_priority(priority):
    """Returns all locations for a specific priority level"""
    return [loc for loc in get_all_locations() if loc.get('priority') == priority]


def get_safe_locations():
    """Returns only locations that are safe to delete"""
    return [loc for loc in get_all_locations() if loc.get('safe_delete', False)]