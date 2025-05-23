# Student Lab Usage Tracker & Report System

A comprehensive Python-based system for tracking student computer lab login/logout sessions and generating detailed usage reports.

## Overview

This system consists of two main components:
1. **Session Tracker** - Processes raw login/logout text files and creates structured JSON data
2. **Report Generator** - Creates various usage reports from the JSON data in professional table formats

## Features

### Session Tracking
- Processes login and logout text files
- Matches login/logout pairs to create sessions
- Handles multiple sessions per day
- Calculates duration for each session
- Stores data in structured JSON format
- Silent operation (no console output)

### Report Generation
- **Daily Usage Reports** - View specific student's activity for any date
- **Monthly Usage Reports** - Complete monthly breakdown for any student
- **Weekly Usage Reports** - 7-day view (Monday-Sunday) for any student
- **All Students Report** - Overview of all students with rankings
- Menu-driven interface with professional table formatting

## File Structure

```
project_folder/
├── session_tracker.py      # Main tracker script
├── report_generator.py     # Report generation system
├── login.txt              # Raw login data (input)
├── logoff.txt             # Raw logout data (input)
├── student_sessions.json  # Processed data (generated)
└── README.md              # This file
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
UNICOMTIC120 UT010665 Mon 04/07/2025 10:55:57.70
```

### Output JSON Structure
```json
{
  "generated_at": "2025-05-23 14:30:00",
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
- `tabulate` library for table formatting

### Install Required Library
```bash
pip install tabulate
```

### Setup Files
1. Place your login data in `login.txt`
2. Place your logout data in `logout.txt`
3. Ensure both files are in the same directory as the scripts

## Usage

### Step 1: Process Raw Data
Run the session tracker to process your login/logout files:

```bash
python session_tracker.py
```

This will:
- Read `login.txt` and `logout.txt`
- Process and match login/logout pairs
- Generate `student_sessions.json`
- Run silently without output

### Step 2: Generate Reports
Run the report generator to create various usage reports:

```bash
python report_generator.py
```

This will display a menu with options:

```
==================================================
STUDENT LAB USAGE REPORT SYSTEM
==================================================
1. View Student Daily Usage
2. View Student Monthly Usage
3. View Student Weekly Usage
4. Generate All Students Report
5. Exit
--------------------------------------------------
```

## Report Types

### 1. Daily Usage Report
- **Input Required**: Student ID, Date (dd/MM/YYYY)
- **Shows**: 
  - Summary statistics for the day
  - Detailed session breakdown
  - Login/logout times for each session
  - Duration calculations

### 2. Monthly Usage Report
- **Input Required**: Student ID, Month (MM/YYYY)
- **Shows**:
  - Monthly summary statistics
  - Daily breakdown for entire month
  - Total and average usage

### 3. Weekly Usage Report
- **Input Required**: Student ID, Any date in target week (dd/MM/YYYY)
- **Shows**:
  - Full week view (Monday to Sunday)
  - Daily breakdown for each day
  - Weekly summary statistics

### 4. All Students Report
- **Input Required**: None
- **Shows**:
  - Complete overview of all students
  - Ranked by total usage hours
  - Overall system statistics
  - Top 10 users (if more than 10 students)

## Sample Report Output

```
+----------------+-------+
| Metric         | Value |
+================+=======+
| Total Sessions | 3     |
| Completed      | 2     |
| Total Hours    | 4.25  |
+----------------+-------+

SESSION DETAILS:
+----------+-------------+------------+-------------+-------+---------+----------+
| Session# | Computer    | Login Time | Logout Time | Hours | Minutes | Status   |
+==========+=============+============+=============+=======+=========+==========+
| 1        | UNICOMTIC27 | 10:52:58   | 12:30:45    | 1.62  | 97      | complete |
| 2        | UNICOMTIC27 | 14:15:20   | 16:45:10    | 2.50  | 150     | complete |
| 3        | UNICOMTIC32 | 17:30:00   | N/A         | 0.00  | 0       | incomplete|
+----------+-------------+------------+-------------+-------+---------+----------+
```

## Key Features

### Data Processing
- **Smart Session Matching**: Automatically pairs logins with corresponding logouts
- **Multiple Sessions**: Handles multiple login/logout cycles per day
- **Incomplete Sessions**: Tracks logins without matching logouts
- **Orphaned Logouts**: Handles logouts without corresponding logins
- **Duration Calculation**: Precise time calculations in hours and minutes

### Error Handling
- **File Validation**: Checks for missing or corrupted files
- **Date Validation**: Validates all date inputs
- **Student ID Validation**: Checks for valid student IDs
- **Graceful Failures**: Continues processing even with some invalid data

### User Experience
- **Menu-Driven Interface**: Easy navigation through report options
- **Flexible Date Input**: Accepts dd/MM/YYYY format for user convenience
- **Professional Tables**: Clean, formatted output using tabulate library
- **Progress Feedback**: Clear status messages and error handling

## Troubleshooting

### Common Issues

**1. "pip not recognized" Error**
- Make sure Python and pip are properly installed
- Try using `python -m pip install tabulate`
- On some systems, use `pip3` instead of `pip`

**2. "File not found" Error**
- Ensure `login.txt` and `logout.txt` are in the same directory as scripts
- Check file names match exactly (case-sensitive)
- Verify files contain data in correct format

**3. "No data found" Messages**
- Check date format (use dd/MM/YYYY)
- Verify student ID exists in the data
- Ensure session tracker was run first to generate JSON file

**4. Invalid Date Format**
- Use exactly dd/MM/YYYY format (e.g., 04/07/2025)
- Include leading zeros for single-digit days/months
- Use 4-digit years

### File Permissions
- Ensure read permissions on input files (`login.txt`, `logout.txt`)
- Ensure write permissions for output file (`student_sessions.json`)

## Technical Details

### Dependencies
- **Python Standard Library**: datetime, json, os, calendar
- **External Library**: tabulate (for table formatting)

### Performance
- Efficiently processes large datasets
- Memory-optimized for handling thousands of records
- Fast session matching algorithms

### Data Integrity
- Validates all input data before processing
- Handles malformed records gracefully
- Preserves original timestamps with precision

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your input data format matches the examples
3. Ensure all required files are present and accessible

## Version History

- **v1.0**: Initial release with basic session tracking
- **v1.1**: Added comprehensive reporting system
- **v1.2**: Enhanced error handling and user interface

---

**Note**: This system is designed for educational/administrative use in computer lab environments. Ensure compliance with your institution's data privacy policies when handling student information.