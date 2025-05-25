import json
import os
from datetime import datetime, timedelta
from tabulate import tabulate
import calendar

class StudentReportGenerator:
    def __init__(self, json_file="student_sessions.json"):
        self.json_file = json_file
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Load data from JSON file"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"Error: {self.json_file} not found. Please run the session tracker first.")
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
        return True
    
    def format_date_input(self, date_str):
        """Convert dd/MM/YYYY to YYYY-MM-DD format"""
        try:
            date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return None
    
    def get_week_range(self, date_str):
        """Get week range (Monday to Sunday) for given date"""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            # Find Monday of the week
            monday = date_obj - timedelta(days=date_obj.weekday())
            # Find Sunday of the week
            sunday = monday + timedelta(days=6)
            return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")
        except ValueError:
            return None, None
    
    def view_daily_usage(self):
        """View student daily usage report"""
        if not self.data:
            print("No data available.")
            return
        
        student_id = input("Enter Student ID: ").strip()
        date_input = input("Enter Date (dd/MM/YYYY): ").strip()
        
        formatted_date = self.format_date_input(date_input)
        if not formatted_date:
            print("Invalid date format. Please use dd/MM/YYYY")
            return
        
        if student_id not in self.data['students']:
            print(f"Student ID {student_id} not found.")
            return
        
        student_data = self.data['students'][student_id]
        if formatted_date not in student_data['days']:
            print(f"No data found for {student_id} on {date_input}")
            return
        
        day_data = student_data['days'][formatted_date]
        
        print(f"\n{'='*60}")
        print(f"DAILY USAGE REPORT - {student_id}")
        print(f"Date: {date_input}")
        print(f"{'='*60}")
        
        # Summary table
        summary_data = [
            ["Total Sessions", day_data['total_sessions']],
            ["Completed Sessions", day_data['completed_sessions']],
            ["Total Duration (Hours)", f"{day_data['total_duration_hours']:.2f}"],
            ["Total Duration (Minutes)", day_data['total_duration_minutes']]
        ]
        
        print("\nSUMMARY:")
        print(tabulate(summary_data, headers=["Metric", "Value"], tablefmt="grid"))
        
        # Sessions detail table
        sessions_data = []
        for session in day_data['sessions']:
            sessions_data.append([
                session['session_number'],
                session['computer_name'],
                session['login_time'] or 'N/A',
                session['logout_time'] or 'N/A',
                f"{session['duration_hours']:.2f}",
                session['duration_minutes'],
                session['status']
            ])
        
        print("\nSESSION DETAILS:")
        headers = ["Session#", "Computer", "Login Time", "Logout Time", "Hours", "Minutes", "Status"]
        print(tabulate(sessions_data, headers=headers, tablefmt="grid"))
    



    def view_student_overall_summary(self):
        """View an overall summary and all session details for a specific student across all dates"""
        if not self.data:
            print("No data available.")
            return

        student_id = input("Enter Student ID: ").strip()

        if student_id not in self.data['students']:
            print(f"Student ID {student_id} not found.")
            return

        student_data = self.data['students'][student_id]
        if not student_data['days']:
            print(f"No usage data available for Student ID {student_id}.")
            return

        all_sessions = []

        total_hours = 0.0
        total_minutes = 0
        total_sessions = 0
        completed_sessions = 0
        incomplete_sessions = 0

        for date_str, day_data in student_data['days'].items():
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d/%m/%Y")

            for session in day_data['sessions']:
                duration_hours = session.get('duration_hours', 0.0)
                duration_minutes = session.get('duration_minutes', 0)
                status = session.get('status', 'Unknown')

                all_sessions.append([
                    formatted_date,
                    session.get('session_number', 'N/A'),
                    session.get('computer_name', 'N/A'),
                    session.get('login_time') or 'N/A',
                    session.get('logout_time') or 'N/A',
                    f"{duration_hours:.2f}",
                    duration_minutes,
                    status
                ])

                total_sessions += 1
                total_hours += duration_hours
                total_minutes += duration_minutes

                if status.lower() in ['completed', 'complete', 'finished', 'done']:
                    completed_sessions += 1
                else:
                    incomplete_sessions += 1

        if not all_sessions:
            print("No session records found for this student.")
            return

        # Adjust total_minutes into hours if needed
        extra_hours, total_minutes = divmod(total_minutes, 60)
        total_hours += extra_hours

        print(f"\n{'='*80}")
        print(f"STUDENT SUMMARY: {student_id}")
        print(f"{'='*80}")

        print(f"\n{'-'*80}")
        print("SUMMARY")
        print(f"{'-'*80}")
        print(f"Total Sessions     : {total_sessions}")
        print(f"Completed Sessions : {completed_sessions}")
        print(f"Incomplete Sessions: {incomplete_sessions}")
        print(f"Total Time Used    : {int(total_hours)} hours {int(total_minutes)} minutes")
        print(f"{'-'*80}")

        # Sort sessions by date, then session number
        all_sessions.sort(key=lambda x: (datetime.strptime(x[0], "%d/%m/%Y"), x[1]))

        headers = ["Date", "Session#", "Computer", "Login", "Logout", "Hours", "Minutes", "Status"]
        print("\nSESSION DETAILS:")
        print(tabulate(all_sessions, headers=headers, tablefmt="grid"))




    def view_monthly_usage(self):
        """View student monthly usage report"""
        if not self.data:
            print("No data available.")
            return
        
        student_id = input("Enter Student ID: ").strip()
        month_input = input("Enter Month (MM/YYYY): ").strip()
        
        try:
            month_obj = datetime.strptime(month_input, "%m/%Y")
            target_month = month_obj.strftime("%Y-%m")
        except ValueError:
            print("Invalid month format. Please use MM/YYYY")
            return
        
        if student_id not in self.data['students']:
            print(f"Student ID {student_id} not found.")
            return
        
        student_data = self.data['students'][student_id]
        
        # Filter days for the target month
        monthly_data = []
        total_hours = 0
        total_sessions = 0
        
        for date, day_data in student_data['days'].items():
            if date.startswith(target_month):
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d/%m/%Y")
                monthly_data.append([
                    formatted_date,
                    day_data['total_sessions'],
                    day_data['completed_sessions'],
                    f"{day_data['total_duration_hours']:.2f}",
                    day_data['total_duration_minutes']
                ])
                total_hours += day_data['total_duration_hours']
                total_sessions += day_data['total_sessions']
        
        if not monthly_data:
            print(f"No data found for {student_id} in {month_input}")
            return
        
        # Sort by date
        monthly_data.sort(key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"))
        
        print(f"\n{'='*70}")
        print(f"MONTHLY USAGE REPORT - {student_id}")
        print(f"Month: {calendar.month_name[month_obj.month]} {month_obj.year}")
        print(f"{'='*70}")
        
        # Summary
        print(f"\nMONTHLY SUMMARY:")
        summary_data = [
            ["Total Active Days", len(monthly_data)],
            ["Total Sessions", total_sessions],
            ["Total Hours", f"{total_hours:.2f}"],
            ["Average Hours/Day", f"{total_hours/len(monthly_data):.2f}" if monthly_data else "0.00"]
        ]
        print(tabulate(summary_data, headers=["Metric", "Value"], tablefmt="grid"))
        
        # Daily breakdown
        print(f"\nDAILY BREAKDOWN:")
        headers = ["Date", "Sessions", "Completed", "Hours", "Minutes"]
        print(tabulate(monthly_data, headers=headers, tablefmt="grid"))
    
    def view_weekly_usage(self):
        """View student weekly usage report"""
        if not self.data:
            print("No data available.")
            return
        
        student_id = input("Enter Student ID: ").strip()
        date_input = input("Enter any date in the week (dd/MM/YYYY): ").strip()
        
        formatted_date = self.format_date_input(date_input)
        if not formatted_date:
            print("Invalid date format. Please use dd/MM/YYYY")
            return
        
        week_start, week_end = self.get_week_range(formatted_date)
        if not week_start or not week_end:
            print("Error calculating week range.")
            return
        
        if student_id not in self.data['students']:
            print(f"Student ID {student_id} not found.")
            return
        
        student_data = self.data['students'][student_id]
        
        # Generate all dates in the week
        start_date = datetime.strptime(week_start, "%Y-%m-%d")
        weekly_data = []
        total_hours = 0
        total_sessions = 0
        
        for i in range(7):
            current_date = start_date + timedelta(days=i)
            date_str = current_date.strftime("%Y-%m-%d")
            formatted_display = current_date.strftime("%d/%m/%Y")
            day_name = current_date.strftime("%A")
            
            if date_str in student_data['days']:
                day_data = student_data['days'][date_str]
                weekly_data.append([
                    day_name,
                    formatted_display,
                    day_data['total_sessions'],
                    day_data['completed_sessions'],
                    f"{day_data['total_duration_hours']:.2f}",
                    day_data['total_duration_minutes']
                ])
                total_hours += day_data['total_duration_hours']
                total_sessions += day_data['total_sessions']
            else:
                weekly_data.append([day_name, formatted_display, 0, 0, "0.00", 0])
        
        print(f"\n{'='*70}")
        print(f"WEEKLY USAGE REPORT - {student_id}")
        start_display = datetime.strptime(week_start, "%Y-%m-%d").strftime("%d/%m/%Y")
        end_display = datetime.strptime(week_end, "%Y-%m-%d").strftime("%d/%m/%Y")
        print(f"Week: {start_display} to {end_display}")
        print(f"{'='*70}")
        
        # Summary
        active_days = len([row for row in weekly_data if int(row[2]) > 0])
        print(f"\nWEEKLY SUMMARY:")
        summary_data = [
            ["Active Days", active_days],
            ["Total Sessions", total_sessions],
            ["Total Hours", f"{total_hours:.2f}"],
            ["Average Hours/Day", f"{total_hours/7:.2f}"]
        ]
        print(tabulate(summary_data, headers=["Metric", "Value"], tablefmt="grid"))
        
        # Daily breakdown
        print(f"\nDAILY BREAKDOWN:")
        headers = ["Day", "Date", "Sessions", "Completed", "Hours", "Minutes"]
        print(tabulate(weekly_data, headers=headers, tablefmt="grid"))
    
    def generate_all_students_report(self):
        """Generate usage report for all students"""
        if not self.data:
            print("No data available.")
            return
        
        print(f"\n{'='*80}")
        print("ALL STUDENTS USAGE REPORT")
        print(f"{'='*80}")
        
        all_students_data = []
        
        for student_id, student_data in self.data['students'].items():
            all_students_data.append([
                student_id,
                student_data['total_days'],
                student_data['total_sessions_all_days'],
                f"{student_data['total_hours_all_days']:.2f}",
                f"{student_data['total_hours_all_days']/student_data['total_days']:.2f}" if student_data['total_days'] > 0 else "0.00"
            ])
        
        # Sort by total hours (descending)
        all_students_data.sort(key=lambda x: float(x[3]), reverse=True)
        
        print(f"\nOVERALL SUMMARY:")
        summary_data = [
            ["Total Students", len(self.data['students'])],
            ["Total Login Records", self.data['summary']['total_login_records']],
            ["Total Logout Records", self.data['summary']['total_logout_records']],
            ["Report Generated", self.data['generated_at']]
        ]
        print(tabulate(summary_data, headers=["Metric", "Value"], tablefmt="grid"))
        
        print(f"\nSTUDENT USAGE SUMMARY:")
        headers = ["Student ID", "Active Days", "Total Sessions", "Total Hours", "Avg Hours/Day"]
        print(tabulate(all_students_data, headers=headers, tablefmt="grid"))
        
        # Top 10 students by usage
        if len(all_students_data) > 10:
            print(f"\nTOP 10 STUDENTS BY USAGE:")
            print(tabulate(all_students_data[:10], headers=headers, tablefmt="grid"))
    
    def show_menu(self):
        """Display main menu"""
        print(f"\n{'='*50}")
        print("STUDENT LAB USAGE REPORT SYSTEM")
        print(f"{'='*50}")
        print("1. View Student Daily Usage")
        print("2. View Student Overall Summary (All Dates)")
        print("3. View Student Monthly Usage")
        print("4. View Student Weekly Usage")
        print("5. Generate All Students Report")
        print("6. Exit")
        print("-" * 50)
    
    def run(self):
        """Main program loop"""
        if not self.data:
            return
        
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.view_daily_usage()
            elif choice == '2':
                self.view_student_overall_summary()
            elif choice == '3':
                self.view_monthly_usage()
            elif choice == '4':
                self.view_weekly_usage()
            elif choice == '5':
                self.generate_all_students_report()
            elif choice == '6':
                print("Thank you for using Student Lab Usage Report System!")
                break
            else:
                print("Invalid choice. Please enter 1-6.")
            
            input("\nPress Enter to continue...")

def main():
    # Check if tabulate is installed
    try:
        import tabulate
    except ImportError:
        print("Error: 'tabulate' library is required.")
        print("Install it using: pip install tabulate")
        return
    
    reporter = StudentReportGenerator()
    reporter.run()

# This script is designed to generate reports based on student lab usage data.
import subprocess

try:
    subprocess.run(["python", "Generate_Json_Record.py"])
except FileNotFoundError:
    print("Note: Generate_Json_Record.py not found. Make sure it exists in the same directory.")
# Generate_Json_Record.py should be run before this script

if __name__ == "__main__":
    main()