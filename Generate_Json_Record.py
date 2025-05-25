import json
import re
from datetime import datetime, timedelta
from collections import defaultdict
import os

class StudentSessionTracker:
    def __init__(self):
        self.login_data = []
        self.logout_data = []
        self.sessions = defaultdict(lambda: defaultdict(list))
    
    def parse_log_line(self, line):
        """Parse a single log line and extract computer name, student ID, and timestamp"""
        line = line.strip()
        if not line:
            return None
        
        # Split the line into parts
        parts = line.split()
        if len(parts) < 4:
            return None
        
        try:
            computer_name = parts[0]
            student_id = parts[1]
            
            # Parse date and time
            date_str = parts[2]  # Mon
            date_part = parts[3]  # 04/07/2025 (MM/DD/YYYY format)
            time_part = parts[4]  # 10:52:58.69
            
            # Create datetime object - MM/DD/YYYY format (04/07/2025 = April 7th, 2025)
            datetime_str = f"{date_part} {time_part}"
            timestamp = datetime.strptime(datetime_str, "%m/%d/%Y %H:%M:%S.%f")
            
            return {
                'computer_name': computer_name,
                'student_id': student_id,
                'timestamp': timestamp,
                'date': timestamp.date().strftime("%Y-%m-%d"),
                'weekday': timestamp.strftime("%A")
            }
        except (ValueError, IndexError) as e:
            return None
    
    def load_login_file(self, filepath):
        """Load and parse login data from text file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    parsed = self.parse_log_line(line)
                    if parsed:
                        self.login_data.append(parsed)
        except FileNotFoundError:
            pass
        except Exception as e:
            pass
    
    def load_logout_file(self, filepath):
        """Load and parse logout data from text file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    parsed = self.parse_log_line(line)
                    if parsed:
                        self.logout_data.append(parsed)
        except FileNotFoundError:
            pass
        except Exception as e:
            pass
    
    def calculate_sessions(self):
        """Calculate sessions by matching login and logout times"""
        # Sort data by student_id, date, and timestamp
        self.login_data.sort(key=lambda x: (x['student_id'], x['date'], x['timestamp']))
        self.logout_data.sort(key=lambda x: (x['student_id'], x['date'], x['timestamp']))
        
        # Group by student and date
        login_by_student_date = defaultdict(list)
        logout_by_student_date = defaultdict(list)
        
        for login in self.login_data:
            key = (login['student_id'], login['date'])
            login_by_student_date[key].append(login)
        
        for logout in self.logout_data:
            key = (logout['student_id'], logout['date'])
            logout_by_student_date[key].append(logout)
        
        # Match logins with logouts
        all_keys = set(login_by_student_date.keys()) | set(logout_by_student_date.keys())
        
        for student_id, date in all_keys:
            logins = login_by_student_date.get((student_id, date), [])
            logouts = logout_by_student_date.get((student_id, date), [])
            
            # Create sessions
            sessions = []
            logout_index = 0
            
            for i, login in enumerate(logins):
                session = {
                    'session_number': i + 1,
                    'computer_name': login['computer_name'],
                    'login_time': login['timestamp'].strftime("%H:%M:%S"),
                    'logout_time': None,
                    'duration_minutes': 0,
                    'duration_hours': 0.0,
                    'status': 'incomplete'
                }
                
                # Find matching logout (first logout after this login)
                while logout_index < len(logouts) and logouts[logout_index]['timestamp'] <= login['timestamp']:
                    logout_index += 1
                
                if logout_index < len(logouts):
                    logout = logouts[logout_index]
                    session['logout_time'] = logout['timestamp'].strftime("%H:%M:%S")
                    
                    # Calculate duration
                    duration = logout['timestamp'] - login['timestamp']
                    session['duration_minutes'] = int(duration.total_seconds() / 60)
                    session['duration_hours'] = round(duration.total_seconds() / 3600, 2)
                    session['status'] = 'complete'
                    logout_index += 1
                
                sessions.append(session)
            
            # Handle any remaining logouts (logouts without matching logins)
            while logout_index < len(logouts):
                logout = logouts[logout_index]
                session = {
                    'session_number': len(sessions) + 1,
                    'computer_name': logout['computer_name'],
                    'login_time': None,
                    'logout_time': logout['timestamp'].strftime("%H:%M:%S"),
                    'duration_minutes': 0,
                    'duration_hours': 0.0,
                    'status': 'logout_only'
                }
                sessions.append(session)
                logout_index += 1
            
            if sessions:
                # Calculate total time for the day
                total_minutes = sum(s['duration_minutes'] for s in sessions if s['status'] == 'complete')
                total_hours = round(total_minutes / 60, 2)
                
                self.sessions[student_id][date] = {
                    'date': date,
                    'weekday': logins[0]['weekday'] if logins else (logouts[0]['weekday'] if logouts else None),
                    'total_sessions': len(sessions),
                    'completed_sessions': len([s for s in sessions if s['status'] == 'complete']),
                    'total_duration_minutes': total_minutes,
                    'total_duration_hours': total_hours,
                    'sessions': sessions
                }
    
    def generate_json_report(self, output_filepath):
        """Generate JSON report with all student session data"""
        report = {
            'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'summary': {
                'total_students': len(self.sessions),
                'total_login_records': len(self.login_data),
                'total_logout_records': len(self.logout_data)
            },
            'students': {}
        }
        
        for student_id, dates in self.sessions.items():
            student_data = {
                'student_id': student_id,
                'total_days': len(dates),
                'days': {}
            }
            
            # Calculate overall statistics
            total_hours = sum(day_data['total_duration_hours'] for day_data in dates.values())
            total_sessions = sum(day_data['total_sessions'] for day_data in dates.values())
            
            student_data['total_hours_all_days'] = round(total_hours, 2)
            student_data['total_sessions_all_days'] = total_sessions
            
            # Add daily data
            for date, day_data in sorted(dates.items()):
                student_data['days'][date] = day_data
            
            report['students'][student_id] = student_data
        
        # Save to JSON file
        try:
            with open(output_filepath, 'w', encoding='utf-8') as file:
                json.dump(report, file, indent=2, ensure_ascii=False)
        except Exception as e:
            pass
    
    def print_summary(self):
        """Print a summary of the processed data"""
        pass

def main():
    # Initialize tracker
    tracker = StudentSessionTracker()
    
    # File paths (modify these according to your file locations)
    login_file = "login.txt"
    logout_file = "logoff.txt"
    output_file = "student_sessions.json"
    
    # Load data files
    tracker.load_login_file(login_file)
    tracker.load_logout_file(logout_file)
    
    if not tracker.login_data and not tracker.logout_data:
        return
    
    # Process sessions
    tracker.calculate_sessions()
    
    # Generate JSON report
    tracker.generate_json_report(output_file)
    
    # Print summary
    tracker.print_summary()

if __name__ == "__main__":
    main()