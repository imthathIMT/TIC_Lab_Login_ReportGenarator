import json
from datetime import datetime
from collections import defaultdict

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
        
        parts = line.split()
        if len(parts) < 5:
            return None
        
        try:
            computer_name = parts[0]
            student_id = parts[1]
            
            # Check if student_id starts with UT or ut
            if not student_id.lower().startswith('ut'):
                return None
            
            # parts[2] is day of week (Mon, Tue, etc)
            date_part = parts[3]  # MM/DD/YYYY
            time_part = parts[4]  # HH:MM:SS.xx
            
            datetime_str = f"{date_part} {time_part}"
            timestamp = datetime.strptime(datetime_str, "%m/%d/%Y %H:%M:%S.%f")
            
            return {
                'computer_name': computer_name,
                'student_id': student_id,
                'timestamp': timestamp,
                'date': timestamp.date().strftime("%Y-%m-%d"),
                'weekday': timestamp.strftime("%A")
            }
        except (ValueError, IndexError):
            return None
    
    def load_login_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    parsed = self.parse_log_line(line)
                    if parsed:
                        self.login_data.append(parsed)
        except FileNotFoundError:
            pass
        except Exception:
            pass
    
    def load_logout_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    parsed = self.parse_log_line(line)
                    if parsed:
                        self.logout_data.append(parsed)
        except FileNotFoundError:
            pass
        except Exception:
            pass

    def remove_near_duplicates(self, threshold_seconds=1):
        def unique_entries_with_tolerance(data):
            data.sort(key=lambda x: (x['student_id'], x['date'], x['timestamp']))
            unique_list = []
            prev_entry = None
            
            for entry in data:
                if prev_entry is None:
                    unique_list.append(entry)
                    prev_entry = entry
                else:
                    same_student = entry['student_id'] == prev_entry['student_id']
                    same_date = entry['date'] == prev_entry['date']
                    time_diff = (entry['timestamp'] - prev_entry['timestamp']).total_seconds()
                    
                    if same_student and same_date and abs(time_diff) <= threshold_seconds:
                        # Near duplicate, skip
                        continue
                    else:
                        unique_list.append(entry)
                        prev_entry = entry
            return unique_list
        
        self.login_data = unique_entries_with_tolerance(self.login_data)
        self.logout_data = unique_entries_with_tolerance(self.logout_data)

    def calculate_sessions(self):
        self.login_data.sort(key=lambda x: (x['student_id'], x['date'], x['timestamp']))
        self.logout_data.sort(key=lambda x: (x['student_id'], x['date'], x['timestamp']))
        
        login_by_student_date = defaultdict(list)
        logout_by_student_date = defaultdict(list)
        
        for login in self.login_data:
            key = (login['student_id'], login['date'])
            login_by_student_date[key].append(login)
        
        for logout in self.logout_data:
            key = (logout['student_id'], logout['date'])
            logout_by_student_date[key].append(logout)
        
        all_keys = set(login_by_student_date.keys()) | set(logout_by_student_date.keys())
        
        for student_id, date in all_keys:
            logins = login_by_student_date.get((student_id, date), [])
            logouts = logout_by_student_date.get((student_id, date), [])
            
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
                
                while logout_index < len(logouts) and logouts[logout_index]['timestamp'] <= login['timestamp']:
                    logout_index += 1
                
                if logout_index < len(logouts):
                    logout = logouts[logout_index]
                    session['logout_time'] = logout['timestamp'].strftime("%H:%M:%S")
                    
                    duration = logout['timestamp'] - login['timestamp']
                    session['duration_minutes'] = int(duration.total_seconds() / 60)
                    session['duration_hours'] = round(duration.total_seconds() / 3600, 2)
                    session['status'] = 'complete'
                    logout_index += 1
                
                sessions.append(session)
            
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
            
            total_hours = sum(day_data['total_duration_hours'] for day_data in dates.values())
            total_sessions = sum(day_data['total_sessions'] for day_data in dates.values())
            
            student_data['total_hours_all_days'] = round(total_hours, 2)
            student_data['total_sessions_all_days'] = total_sessions
            
            for date, day_data in sorted(dates.items()):
                student_data['days'][date] = day_data
            
            report['students'][student_id] = student_data
        
        try:
            with open(output_filepath, 'w', encoding='utf-8') as file:
                json.dump(report, file, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def print_summary(self):
        pass

def main():
    tracker = StudentSessionTracker()
    login_file = "login.txt"
    logout_file = "logoff.txt"
    output_file = "student_sessions.json"
    
    tracker.load_login_file(login_file)
    tracker.load_logout_file(logout_file)
    
    if not tracker.login_data and not tracker.logout_data:
        print("No data loaded.")
        return
    
    print("Data loaded.")
    
    tracker.remove_near_duplicates(threshold_seconds=1)
    
    tracker.calculate_sessions()
    tracker.generate_json_report(output_file)

if __name__ == "__main__":
    main()
