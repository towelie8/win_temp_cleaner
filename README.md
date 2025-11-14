# Windows Temporary Files Cleaner

A comprehensive scanner and cleaner for Windows 10/11 temporary files. **Version 2.0 Extended** scans over **50 locations** and can find and delete **60-300 GB** of hidden temporary files!

> 🇩🇪 **Deutsche Version:** [README_GER.md](README_GER.md)

## New in Version 2.0

- **50+ Scan Locations** (previously only 9)
- **Intelligent Priority Sorting** (Critical → High → Medium → Low)
- **Category-Based Organization** (System, Browser, Gaming, Development, etc.)
- **Process Detection** (prevents deletion when apps are running)
- **Service Management** (stops/starts services safely)
- **Extended Reports** with size analysis and recommendations
- **Modular Architecture** for easy extension

## Why?

Windows automatically stores temporary files in **dozens of hidden locations**:

### System Caches (often 20-100 GB)
- **Windows.old** (15-30 GB) - Previous Windows installation
- **Windows Error Reports** (5-50 GB) - Crash dumps
- **CBS Logs** (up to 20 GB) - Windows Update logs
- **Defender Scan History** (10-20 GB) - Defender cache
- **ETL Diagnostic Logs** (10-50 GB) - Telemetry data
- **Delivery Optimization** (1-20 GB) - P2P Update cache

### Application Caches (often 10-50 GB)
- **Browser Caches** (Chrome, Firefox, Edge)
- **Discord, Teams, Slack, Spotify** - Chat/Media caches
- **GPU Shader Caches** (NVIDIA, AMD, Intel)
- **Development Tools** (npm, pip, Visual Studio)

### And many more!

These files can accumulate to **several hundred gigabytes** and:
- Waste valuable disk space
- Slow down system performance
- Reduce SSD lifespan through unnecessary writes
- Negatively impact FPS in games

## Features

### Complete Scan
- Scans **50+ critical locations**
- Finds hidden temp files that other tools miss
- Shows detailed size and file count statistics

### Intelligent Prioritization
- 🔴 **Critical**: Large files requiring special handling
- 🟠 **High**: Large, safely deletable files
- 🟡 **Medium**: Moderate size
- 🟢 **Low**: Small or conditionally deletable
- ⚫ **View Only**: NEVER delete (e.g., Windows Installer)

### Safety First
- Interactive confirmation before deletion
- Process detection (prevents deletion when app is running)
- Service management (stops/starts services safely)
- Admin rights check
- Detailed error handling
- Multiple confirmations for critical locations

### Detailed Reports
- Markdown reports with complete statistics
- Sorting by priority and category
- Warnings for critical locations
- Recommendations for optimal cleanup

### Selective Cleanup
- Choose specific locations to delete
- Delete only high priority
- Or all safe locations at once

## Quickstart

### Requirements
- Python 3.7 or higher
- Windows 10 or Windows 11
- Administrator rights (recommended for full access)

### Installation & Execution

```bash
# Clone repository
git clone https://github.com/towelie8/win_temp_cleaner
cd win_temp_cleaner

# Switch to dev branch for version 2.0
git checkout dev

# Run script with admin rights
python main.py
```

## Usage

### 1. Perform Scan
```bash
python main.py
```

The tool automatically scans all 50+ locations and shows:
- Found size per location
- Number of files
- Priority classification
- Warnings for critical locations

### 2. Generate Report

A detailed Markdown report is automatically created:
```
temp_scan_report_YYYYMMDD_HHMMSS.md
```

The report contains:
- Summary of total storage usage
- Breakdown by priority
- Breakdown by category
- Top 10 largest locations
- Detailed recommendations

### 3. Interactive Cleanup

Choose from different options:
```
Options:
  a       - Delete all SAFE locations
  h       - Delete only HIGH priority
  1,2,3   - Delete specific numbers (comma-separated)
  q       - Cancel
```

## Scanned Locations

### 🔴 Critical Priority (Special Handling)
| Location | Typical Size | Description |
|----------|--------------|-------------|
| Windows.old | 15-30 GB | Previous Windows installation |
| $Windows.~BT | 3-20 GB | Windows upgrade files |
| CBS Logs | 0.1-20 GB | Update/Component logs |
| WER Reports | 1-10 GB | Windows Error Reports |
| Memory Dumps | 1-64 GB | BSOD crash dumps |
| Defender Scan History | 10-20 GB | Defender cache files |
| ETL Diagnostic Logs | 10-50 GB | Telemetry data |

### 🟠 High Priority (Large, Safe Files)
- Delivery Optimization Cache (1-20 GB)
- Adobe Temp Files (0.5-100 GB)
- Application Crash Dumps (1-5 GB)
- Live Kernel Reports (0.5-2 GB)

### 🟡 Medium Priority (Moderate Size)
- Browser Caches (Chrome, Firefox, Edge)
- Discord, Teams, Slack, Spotify Caches
- GPU Shader Caches (NVIDIA, AMD, Intel, DirectX)
- Development Tool Caches (npm, pip, NuGet)
- Windows Update Cache

### 🟢 Low Priority (Small)
- Windows Explorer Thumbnails
- Icon Cache
- Font Cache
- Recent Documents
- Notification Cache

### ⚫ View Only (NEVER DELETE)
- Windows Installer Cache (C:\Windows\Installer)
- WinSxS Component Store (DISM only)

## Safety Notes

### What is Safe?
All locations with green checkmark in report
Locations with "High" or "Medium" priority
Temporary caches and browser data

### What is NOT Safe?
**Windows Installer Cache** - Breaks updates/uninstallation
**Direct WinSxS deletion** - Use DISM tools only!

### Recommended Procedure
1. **Backup important data** before major cleanups
2. **Run as administrator** for full access
3. **Read report** before deletion
4. **For Windows.old**: Only delete if >30 days since upgrade
5. **Close apps** before cleaning their caches

## Typical Results

After a complete cleanup, you can expect:

- **Storage freed**: 60 MB - 300+ GB (depending on system age)
- **Faster PC**: Less disk I/O, more available cache
- **Better SSD lifespan**: Reduced write operations
- **Improved FPS**: Through freed GPU shader cache space

### Example: 2-year-old gaming system
```
Scan Results:
- Windows.old: 28 GB
- CBS Logs: 12 GB
- WER Reports: 8 GB
- Defender History: 15 GB
- GPU Shader Caches: 6 GB
- Browser Caches: 4 GB
- Discord/Teams: 3 GB
----------------------------
Total freed: 76 GB
```

## Documentation

- **README.md** (this file) - User documentation
- **README_GER.md** - German version
- **README_DEV.md** - Developer documentation and architecture
- **config.py** - All location definitions
- **utils.py** - Utility functions
- **main.py** - Main application

## Development

### Project Structure
```
win_temp_cleaner/
├── main.py           # Main application
├── config.py         # 50+ location definitions
├── utils.py          # Process/service management
├── README.md         # User documentation (English)
├── README_GER.md     # User documentation (German)
├── README_DEV.md     # Developer documentation
└── .gitignore
```

## ❓ FAQ

**Q: Is it safe to delete all temp files?**  
**A:** Yes, all locations marked as "safe_delete=True" are safe. Windows recreates temporary files as needed.

**Q: Why do I find more files than tool XYZ?**  
**A:** We scan 50+ locations including hidden system caches that many tools miss (e.g., ETL Logs, Defender History, CBS Logs).

**Q: Do I need administrator rights?**  
**A:** Recommended! Without admin rights, system temp folders cannot be scanned (~30% of locations).

**Q: Can I run the tool regularly?**  
**A:** Yes! Completely safe to run monthly or when storage is low.

**Q: What happens to my personal data?**  
**A:** The tool ONLY deletes temporary system and cache files. Documents, photos, downloads remain untouched.

**Q: Can the tool damage my system?**  
**A:** No, if you follow the warnings. We NEVER delete critical system folders like Windows Installer or WinSxS directly.

## License

MIT License - See LICENSE file

## Author

**GitHub:** [@towelie8](https://github.com/towelie8)

## Give a Star!

If this tool helped you free up disk space, give the repository a star on GitHub! ⭐

