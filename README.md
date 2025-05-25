# Student Lab Usage Tracker & Report System

A comprehensive Python-based system for tracking student computer lab login/logout sessions and generating detailed usage reports with Excel export functionality.

## Overview

This system consists of two main components:
1. **JSON Record Generator** (`Generate_Json_Record.py`) - Processes raw login/logout text files and creates structured JSON data
2. **Report Generator** (`report_generator.py`) - Creates various usage reports from the JSON data in professional table formats, with Excel export options

## Features

### Session Tracking (`Generate_Json_Record.py`)
- Processes login and logout text files
- Filters student IDs starting with "UT" (case-insensitive)
- **Smart duplicate removal** - Removes near-duplicate entries within 1-second threshold
- Matches login/logout pairs to create complete sessions
- Handles multiple sessions per day per student
- Manages edge cases: incomplete sessions, logout-only records
- Calculates precise duration for each session
- Stores data in structured JSON format with comprehensive metadata
- **Auto-runs** before report generation for seamless workflow

### Report Generation (`report_generator.py`)
- **Daily Usage Reports** - View specific student's activity for any date
- **Overall Student Summary** - Complete summary across all dates for a student (**with Excel export**)
- **Monthly Usage Reports** - Complete monthly breakdown for any student
- **Weekly Usage Reports** - 7-day view (Monday–Sunday) for any student
- **All Students Report** - Overview of all students with rankings and summary (**with Excel export**)
- Menu-driven interface with professional table formatting
- **Auto-increment file naming** to prevent overwriting existing Excel reports

## File Structure

```
project_folder/
├── Generate_Json_Record.py    # JSON record generator (session tracker)
├── report_generator.py        # Report generation system
├── login.txt                  # Raw login data (input)
├── logoff.txt                 # Raw logout data (input)
├── student_sessions.json      # Processed data (auto-generated)
├── students_report/           # Folder where Excel reports are saved
└── README.md                  # This file
```

## Data Format

### Input Files Format
Both `login.txt` and `logoff.txt` should contain lines in this format:
```
COMPUTERNAME STUDENTID Day MM/DD/YYYY HH:MM:SS.ms
```

**Example:**
```
UNICOMTIC112 UT010665 Mon 04/07/2025 10:52:58.69
UNICOMTIC27 UT010032 Mon 04/07/2025 10:53:53.96
```

**Requirements:**
- Student IDs must start with "UT" or "ut" (case-insensitive)
- Timestamps include milliseconds for precision
- System automatically handles near-duplicate entries

### Output JSON Structure
```json
{
  "generated_at": "2025-05-26 14:30:00",
  "summary": {
    "total_students": 25,
    "total_login_records": 150,
    "total_logout_records": 145
  },
  "students": {
    "UT010665": {
      "student_id": "UT010665",
      "total_days": 5,
      "total_hours_all_days": 25.5,
      "total_sessions_all_days": 12,
      "days": {
        "2025-07-04": {
          "date": "2025-07-04",
          "weekday": "Friday",
          "total_sessions": 3,
          "completed_sessions": 2,
          "total_duration_minutes": 180,
          "total_duration_hours": 3.0,
          "sessions": [
            {
              "session_number": 1,
              "computer_name": "UNICOMTIC112",
              "login_time": "10:52:58",
              "logout_time": "12:30:45",
              "duration_minutes": 97,
              "duration_hours": 1.62,
              "status": "complete"
            }
          ]
        }
      }
    }
  }
}
```

## Installation & Setup

### Prerequisites
- Python 3.6 or higher
- Required libraries: `tabulate`, `pandas`, `openpyxl`

### Install Required Libraries
```bash
pip install tabulate pandas openpyxl
```

### Setup Files
1. Place your login data in `login.txt`
2. Place your logout data in `logoff.txt`
3. Ensure both files are in the same directory as the Python scripts

## Usage

### Method 1: Automatic (Recommended)
Simply run the report generator - it automatically processes the raw data first:

```bash
python report_generator.py
```

This will:
1. **Auto-run** `Generate_Json_Record.py` to process login/logout files
2. Generate `student_sessions.json`
3. Launch the interactive report menu

### Method 2: Manual Steps
If you prefer to run components separately:

**Step 1: Process Raw Data**
```bash
python Generate_Json_Record.py
```

**Step 2: Generate Reports**
```bash
python report_generator.py
```

## Report Types

### 1. Daily Usage Report
- **Input Required**: Student ID, Date (dd/MM/YYYY)
- **Shows**:
  - Summary statistics for the day
  - Detailed session breakdown with login/logout times
  - Duration calculations for each session
  - Session status (complete/incomplete/logout-only)

### 2. Overall Student Summary (All Dates) ⭐ **Excel Export Available**
- **Input Required**: Student ID
- **Shows**:
  - Complete summary across all dates
  - Total sessions, completed/incomplete breakdown
  - Total hours and minutes used
  - All session data in chronological order
- **Excel Export**: Multi-sheet workbook with summary and detailed session data

### 3. Monthly Usage Report
- **Input Required**: Student ID, Month (MM/YYYY)
- **Shows**:
  - Monthly summary statistics
  - Daily breakdown for the entire month
  - Average usage calculations

### 4. Weekly Usage Report
- **Input Required**: Student ID, any date in target week (dd/MM/YYYY)
- **Shows**:
  - Full week view (Monday to Sunday)
  - Daily breakdown with weekday names
  - Weekly summary statistics

### 5. All Students Report ⭐ **Excel Export Available**
- **Input Required**: None
- **Shows**:
  - Complete overview of all students
  - Ranked by total usage hours (descending)
  - System-wide statistics (logins, logouts, generation time)
  - Top 10 most active students (if >10 students)
- **Excel Export**: Multi-sheet workbook with overall summary and detailed student data

## Excel Export Features

### Available for Reports 2 & 5
When prompted:
```
Do you want to download this report as an Excel file? (y/n):
```

### Smart File Management
- **Auto-directory creation**: Creates `../students_report/` if it doesn't exist
- **Auto-increment naming**: Prevents overwriting existing files
  - Example: `UT010665_summary_2025-05-26.xlsx`
  - If exists: `UT010665_summary_2025-05-26_1.xlsx`, `UT010665_summary_2025-05-26_2.xlsx`, etc.

### Excel Workbook Structure
- **Multiple sheets** for organized data presentation
- **Summary sheet** with key metrics
- **Detail sheet** with complete session information
- **Professional formatting** ready for sharing or analysis

## Advanced Features

### Smart Data Processing
- **Near-duplicate removal**: Eliminates entries within 1-second threshold
- **UT ID filtering**: Only processes student IDs starting with "UT"
- **Flexible session matching**: Handles incomplete sessions and logout-only records
- **Weekday calculation**: Automatically determines day of week for each session

### Error Handling
- Graceful handling of missing files
- Invalid date format detection
- Student ID validation
- Comprehensive error messages

### User Experience
- **Interactive menus** with clear navigation
- **Professional table formatting** using tabulate library
- **Progress feedback** during data processing
- **Flexible date input formats** (dd/MM/YYYY)

## Sample Output

```
==================================================
STUDENT LAB USAGE REPORT SYSTEM
==================================================
1. View Student Daily Usage
2. View Student Overall Summary (All Dates)
3. View Student Monthly Usage
4. View Student Weekly Usage
5. Generate All Students Report
6. Exit
--------------------------------------------------

DAILY USAGE REPORT - UT010665
Date: 04/07/2025
==================================================

SUMMARY:
+----------------------+-------+
| Metric               | Value |
+======================+=======+
| Total Sessions       | 3     |
| Completed Sessions   | 2     |
| Total Duration (Hours)| 4.12  |
| Total Duration (Minutes)| 247 |
+----------------------+-------+

SESSION DETAILS:
+----------+-------------+------------+-------------+-------+---------+------------+
| Session# | Computer    | Login Time | Logout Time | Hours | Minutes | Status     |
+==========+=============+============+=============+=======+=========+============+
| 1        | UNICOMTIC112| 10:52:58   | 12:30:45    | 1.62  | 97      | complete   |
| 2        | UNICOMTIC112| 13:00:00   | 15:30:00    | 2.50  | 150     | complete   |
| 3        | UNICOMTIC112| 16:00:00   | N/A         | 0.00  | 0       | incomplete |
+----------+-------------+------------+-------------+-------+---------+------------+
```

## Troubleshooting

### Common Issues

**1. "ModuleNotFoundError: No module named 'tabulate'"**
```bash
pip install tabulate pandas openpyxl
```

**2. "Error: student_sessions.json not found"**
- The system auto-runs `Generate_Json_Record.py` 
- Ensure `login.txt` and `logoff.txt` exist in the same directory

**3. "No data loaded" message**
- Check that `login.txt` and `logoff.txt` contain valid data
- Verify student IDs start with "UT"
- Ensure files are not empty

**4. Excel export fails**
- Close any open Excel files with the same name
- Check write permissions for `students_report/` directory
- Ensure `pandas` and `openpyxl` are installed

**5. Date format errors**
- Use exact format: dd/MM/YYYY (e.g., 04/07/2025)
- For months: MM/YYYY (e.g., 07/2025)

## Technical Details

### Dependencies
- **Python Standard Library**: `datetime`, `json`, `os`, `calendar`, `collections`, `subprocess`
- **External Libraries**:
  - `tabulate` - Professional console table formatting
  - `pandas` - Excel file generation and data manipulation
  - `openpyxl` - Excel writing engine

### Performance Features
- **Efficient data structures** using defaultdict for fast lookups
- **Smart sorting algorithms** for chronological data presentation
- **Memory-optimized** processing for large datasets
- **Fast duplicate detection** with time-based tolerance

### Data Integrity
- **Robust parsing** with comprehensive error handling
- **Session validation** ensures data accuracy
- **Status tracking** for complete/incomplete sessions
- **Timestamp precision** with millisecond accuracy

## Version History

- **v1.0**: Basic login/logout tracking
- **v1.1**: Added reports and tabulated views  
- **v1.2**: Added Excel export for summaries and overall reports
- **v1.3**: Auto-renaming of reports, new menu layout
- **v1.4**: **Current** - Smart duplicate removal, UT filtering, auto-workflow, enhanced error handling, Excel export for menu options 2 & 5

---

**Security Note**: This tool processes student data. Always follow your institution's data privacy policies when storing, processing, or exporting student information. Excel reports contain personally identifiable information and should be handled according to institutional guidelines.