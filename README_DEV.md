# Windows Temp File Cleaner - Developer Documentation

## Version 2.0 - Extended Edition

This document describes the extended architecture of the Windows Temp File Cleaner v2.0.

## Architecture Overview

The application is now split into modular components for better maintainability:

```
win_temp_cleaner/
├── main.py           # Main application logic (TempFileCleanerExtended class)
├── config.py         # Location definitions (50+ temp file locations)
├── utils.py          # Utility functions (process/service management)
├── README.md         # User documentation
├── README_DEV.md     # This file
└── .gitignore        # Git ignore rules
```

## Module Descriptions

### config.py

Defines all temporary file locations grouped by priority and category.

**Key Classes:**
- `LocationCategory`: Enum-like class defining categories (system, browser, gaming, etc.)
- `Priority`: Defines priority levels (HIGH, MEDIUM, LOW, CRITICAL, NEVER)

**Data Structures:**
- `HIGH_PRIORITY_LOCATIONS`: Large files, high impact (Windows.old, crash dumps, etc.)
- `MEDIUM_PRIORITY_LOCATIONS`: Application caches, browser data
- `LOW_PRIORITY_LOCATIONS`: Small files, conditional deletion
- `VIEW_ONLY_LOCATIONS`: Never delete (Windows Installer, WinSxS)

**Key Functions:**
- `get_all_locations()`: Returns all location configurations
- `get_safe_locations()`: Returns only safe-to-delete locations
- `get_locations_by_category(category)`: Filter by category
- `get_locations_by_priority(priority)`: Filter by priority

### utils.py

Provides utility functions for system operations.

**Key Classes:**

1. **ProcessManager**
   - `is_process_running(process_names)`: Check if processes are running
   - `get_running_processes(process_names)`: Get list of running processes

2. **ServiceManager**
   - `stop_service(service_name)`: Stop Windows service
   - `start_service(service_name)`: Start Windows service
   - `is_service_running(service_name)`: Check service status

3. **PermissionManager**
   - `is_admin()`: Check if running with admin rights
   - `takeown_path(path)`: Take ownership of files/folders

4. **FileOperations**
   - `delete_directory(path, max_retries)`: Delete with retry logic
   - `get_directory_size(path)`: Calculate directory size
   - `kill_explorer()`: Kill Windows Explorer
   - `start_explorer()`: Start Windows Explorer

5. **DISMOperations**
   - `analyze_component_store()`: Analyze WinSxS
   - `cleanup_component_store(reset_base)`: Clean WinSxS

**Helper Functions:**
- `format_size(bytes)`: Format bytes to human-readable
- `confirm_action(prompt, default)`: User confirmation dialog

### main.py

Main application logic with the `TempFileCleanerExtended` class.

**Key Methods:**

1. **Scanning:**
   - `scan_location(location)`: Scan single location
   - `scan_all_locations()`: Scan all configured locations
   - `expand_location_paths(location)`: Handle multi-path locations

2. **Reporting:**
   - `create_markdown_report()`: Generate detailed markdown report
   - Organized by priority and category
   - Includes warnings and recommendations

3. **Cleanup:**
   - `delete_location(location_name)`: Delete files at location
   - `interactive_cleanup()`: Interactive cleanup UI
   - Handles process checks, service stops, permissions

## Location Configuration Format

Each location is a dictionary with these keys:

```python
{
    'name': str,                    # Display name
    'path': str,                    # Single path (optional)
    'paths': List[str],             # Multiple paths (optional)
    'category': LocationCategory,   # Category classification
    'priority': Priority,           # Priority level
    'safe_delete': bool,            # Is it safe to delete?
    'requires_admin': bool,         # Needs admin rights?
    'requires_takeown': bool,       # Needs ownership change?
    'requires_system_rights': bool, # Needs SYSTEM level access?
    'method': str,                  # Deletion method
    'service_to_stop': str,         # Service to stop (optional)
    'process_check': List[str],     # Processes to check (optional)
    'expected_size_mb': int,        # Expected size in MB
    'description': str,             # User-friendly description
    'warning': str,                 # Warning message (optional)
    'is_file': bool,                # Is single file? (optional)
    'patterns': List[str],          # File patterns (optional)
}
```

## Deletion Methods

The `method` field specifies how to delete files:

- `simple_delete`: Direct file deletion
- `process_check_delete`: Check processes before deleting
- `service_stop_delete`: Stop service, delete, restart service
- `takeown_and_delete`: Take ownership first, then delete
- `elevated_delete`: Requires SYSTEM-level permissions
- `explorer_restart_delete`: Kill explorer, delete, restart explorer
- `display_only`: Show info only, never delete
- `dism_cleanup`: Use DISM tool for cleanup

## Safety Features

1. **Admin Check**: Warns if not running as administrator
2. **Process Detection**: Prevents deletion if app is running
3. **Service Management**: Stops/starts services safely
4. **Confirmation Prompts**: Multiple confirmations before deletion
5. **Error Handling**: Robust error handling with detailed logs
6. **Priority System**: Critical items require explicit selection

## Adding New Locations

To add a new temp file location:

1. Open `config.py`
2. Add to appropriate priority list (HIGH/MEDIUM/LOW)
3. Fill in all required fields:
   ```python
   {
       'name': 'My New Location',
       'path': r'C:\Path\To\Location',
       'category': LocationCategory.SYSTEM,
       'priority': Priority.MEDIUM,
       'safe_delete': True,
       'requires_admin': False,
       'method': 'simple_delete',
       'expected_size_mb': 500,
       'description': 'What this location contains',
   }
   ```
4. Test thoroughly before committing

## Testing

### Manual Testing Checklist

- [ ] Run as regular user
- [ ] Run as administrator
- [ ] Test scan without deletion
- [ ] Test individual location deletion
- [ ] Test bulk deletion
- [ ] Test process detection
- [ ] Test service stop/start
- [ ] Verify report generation
- [ ] Check error handling

### Test Scenarios

1. **Without Admin Rights:**
   - Should warn about limited access
   - Should skip admin-required locations
   - Should still scan user-accessible locations

2. **With Running Applications:**
   - Should detect running processes
   - Should prevent deletion if app is running
   - Should warn user

3. **Service Management:**
   - Should successfully stop services
   - Should delete files while service stopped
   - Should restart services after deletion

## Known Limitations

1. **SYSTEM-Level Access**: Some locations (ETL logs) require SYSTEM privileges
2. **File in Use**: Cannot delete files currently in use by Windows
3. **Windows Installer**: Never delete - breaks application management
4. **WinSxS**: Only clean via DISM, not direct deletion

## Future Enhancements

Potential improvements for future versions:

1. **Scheduled Cleanup**: Auto-run on schedule
2. **GUI Version**: PyQt or Tkinter interface
3. **Disk Analyzer**: Visual treemap of disk usage
4. **Cloud Integration**: Backup before deletion
5. **Undo Feature**: Restore deleted files (complex)
6. **Performance Monitoring**: Track FPS/boot time improvements
7. **Multi-Language**: Translation support
8. **Installer**: Windows installer package
9. **Silent Mode**: Command-line automation

## Contributing

When contributing to this project:

1. Follow existing code style
2. Add docstrings to all functions
3. Update this document for architectural changes
4. Test on Windows 10 and Windows 11
5. Consider backwards compatibility
6. Add entries to CHANGELOG.md

## Branches

- `master`: Stable release (v1.0)
- `dev`: Active development (v2.0)
- Feature branches: `feature/your-feature-name`

## Version History

- **v1.0** (master): Basic cleaner with 9 locations
- **v2.0** (dev): Extended version with 50+ locations, modular architecture

## License

MIT License - See LICENSE file for details.

## Author

GitHub: @towelie8

---

Last Updated: 2025-11-14