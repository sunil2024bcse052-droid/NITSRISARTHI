import sqlite3

DB_PATH = "college_data.db"


def create_tables(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        short_name TEXT PRIMARY KEY,
        course_code TEXT,
        course_name TEXT,
        credits INTEGER,
        faculty_name TEXT
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS timetable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        semester TEXT,
        section TEXT,
        day TEXT,
        hour INTEGER,
        time_slot TEXT,
        course_short_name TEXT
    )
    """)


courses_data = [
    ("OOP", "Object Oriented Programming", "CST201", 3, "Dr. Mohd Yaseen Mir / Dr. Snobar Mushtaq"),
    ("OOP Lab", "Object Oriented Programming - Lab", "CSL202", 1, "Dr. Mohd Yaseen Mir / Dr. Snobar Mushtaq"),
    ("DBMS", "Database Management Systems", "CST203", 3, "Dr. Ifrah Raouf / Dr. Pramod Kumar Yadav"),
    ("DBMS Lab", "Database Management Systems - Lab", "CSL204", 1, "Dr. Ifrah Raouf / Dr. Pramod Kumar Yadav"),
    ("SE", "Software Engineering", "CST205", 3, "New Faculty 1"),
    ("EDC", "Electronic Devices and Circuits", "ECT205", 3, "ECE Faculty"),
    ("EDC Lab", "Electronic Devices and Circuits Lab", "ECL206", 1, "ECE Faculty"),
    ("DM", "Discrete Mathematics", "MAT207", 3, "Math Faculty"),
    ("EntDev", "Entrepreneurship Development", "HST006", 3, "HSS Faculty"),
    ("DAA", "Design & Analysis of Algorithms", "CST306", 3, "Dr. Shaima Qureshi / New Faculty 5"),
    ("µP", "Microprocessor", "CST307", 3, "Prof. Roohie Naaz Mir / New Faculty 4"),
    ("µP Lab", "Microprocessor - Lab", "CSL308", 1, "Prof. Roohie Naaz Mir / New Faculty 4"),
    ("OS", "Operating Systems", "CST309", 3, "Dr. Mohammad Ahsan Chishti"),
    ("Python", "Python Programming", "CST310", 3, "Dr. Sparsh Sharma / Dr. Mohd Yaseen Mir"),
    ("Python Lab", "Python Programming - Lab", "CSL311", 1, "Dr. Sparsh Sharma / Dr. Mohd Yaseen Mir"),
    ("OE-Python", "Open Elective-I Python", "CST203", 3, "New Faculty 2"),
    ("OE-DBMS", "Open Elective-I Database Management System", "CST310", 3, "New Faculty 3"),
    ("CS", "Communication Systems", "ECT307", 3, "ECE Faculty"),
    ("CS Lab", "Communication Systems Lab", "ECL308", 1, "ECE Faculty"),
    ("CD", "Compiler Design", "CST415", 3, "Dr. Tawseef Ayoub"),
    ("NS", "Network Security", "CST417", 4, "New Faculty 6 / Dr. Insha Majeed"),
    ("NS Lab", "Network Security - Lab", "CSL418", 1, "New Faculty 6 / Dr. Insha Majeed"),
    ("Pre-Project", "Pre-Project", "CSP419", 2, "All Faculty Members"),
    ("Seminar", "Seminar", "CSS420", 1, "All Faculty Members"),
    ("E II - ML", "Elective II - Machine Learning", "CST051", 3, "Dr. Veningston K / New Faculty 4"),
    ("E III - DA", "Elective-III Data Analytics", "CST037", 3, "New Faculty 2"),
    ("E III - ADB", "Elective-III Advanced DBMS", "CST022", 3, "New Faculty 3"),
    ("E IV - DL", "Elective-IV Deep Learning", "CST044", 3, "Dr. Snobar Mushtaq"),
    ("E IV - CLF", "Elective-IV Cyber Laws and Forensics", "CST032", 3, "Dr. Ifrah Raouf"),
    ("OR", "Operations Research & Optimization", "MTH715", 3, "Math Faculty"),
    ("NGN", "Next Generation Networks", "CST501", 3, "Dr. Mir Salim Ul Islam"),
    ("NGN Lab", "Next Generation Networks Lab", "CSP502", 1, "Dr. Mir Salim Ul Islam"),
    ("SA", "System Architecture", "CST503", 3, "New Faculty 5"),
    ("E I - AI", "Elective I - Artificial Intelligence and Fuzzy Logic", "CST847", 3, "Dr. Mir Salim Ul Islam"),
    ("E II - NSS", "Elective II - Network and System Security", "CST835", 3, "Dr. Sparsh Sharma"),
    ("E III - IoT", "Elective III - Internet of Things", "CST806", 3, "Dr. Pramod Kumar Yadav"),
    ("ToC", "Advanced Automata and Theory of Computation", "CST604", 3, "New Faculty 6"),
    ("RM", "Research Methodology", "CST605", 3, "HSS Faculty"),
    ("PD-I", "Project Dissertation - I", "CSP606", 3, "All Faculty Members"),
    ("E-VII-BG", "Elective VII Big Data", "CST843", 3, "Dr. Insha Majeed"),
    ("E-VIII-DL", "Elective VIII Deep Learning", "CST845", 3, "Dr. Veningston K"),
]

timetable_data = [
    ("3rd", "A", "Monday", 3, "10:40-11:30", "DBMS"),
    ("3rd", "A", "Monday", 6, "1:10-2:00", "SE"),
    ("3rd", "A", "Monday", 7, "2:00-2:50", "OOP"),
    ("3rd", "A", "Monday", 8, "2:50-3:40", "DM"),
    ("3rd", "A", "Tuesday", 1, "9:00-9:50", "DM"),
    ("3rd", "A", "Tuesday", 3, "10:40-11:30", "EDC"),
    ("3rd", "A", "Tuesday", 5, "12:20-01:10", "DBMS"),
    ("3rd", "A", "Wednesday", 1, "9:00-9:50", "EntDev"),
    ("3rd", "A", "Wednesday", 2, "09:50-10:40", "OOP"),
    ("3rd", "A", "Wednesday", 3, "10:40-11:30", "DBMS Lab"),
    ("3rd", "A", "Wednesday", 7, "2:00-2:50", "DBMS"),
    ("3rd", "A", "Wednesday", 9, "3:40-4:30", "EDC Lab"),
    ("3rd", "A", "Thursday", 4, "11:30-12:20", "EntDev"),
    ("3rd", "A", "Thursday", 5, "12:20-01:10", "SE"),
    ("3rd", "A", "Friday", 2, "09:50-10:40", "EntDev"),
    ("3rd", "A", "Friday", 3, "10:40-11:30", "OOP"),
    ("3rd", "A", "Friday", 4, "11:30-12:20", "SE"),
    ("3rd", "A", "Friday", 5, "12:20-01:10", "EDC"),
    ("3rd", "B", "Monday", 2, "09:50-10:40", "OOP"),
    ("3rd", "B", "Monday", 3, "10:40-11:30", "OOP Lab"),
    ("3rd", "B", "Monday", 4, "11:30-12:20", "DBMS"),
    ("3rd", "B", "Monday", 9, "3:40-4:30", "DM"),
    ("3rd", "B", "Tuesday", 6, "1:10-2:00", "SE"),
    ("3rd", "B", "Tuesday", 7, "2:00-2:50", "DBMS"),
    ("3rd", "B", "Tuesday", 8, "2:50-3:40", "DM"),
    ("3rd", "B", "Wednesday", 3, "10:40-11:30", "EntDev"),
    ("3rd", "B", "Wednesday", 4, "11:30-12:20", "EDC"),
    ("3rd", "B", "Wednesday", 8, "2:50-3:40", "OOP"),
    ("3rd", "B", "Thursday", 1, "9:00-9:50", "OOP"),
    ("3rd", "B", "Thursday", 2, "09:50-10:40", "EntDev"),
    ("3rd", "B", "Thursday", 3, "10:40-11:30", "EDC"),
    ("3rd", "B", "Thursday", 4, "11:30-12:20", "EDC Lab"),
    ("3rd", "B", "Thursday", 7, "2:00-2:50", "DBMS"),
    ("3rd", "B", "Thursday", 8, "2:50-3:40", "SE"),
    ("3rd", "B", "Friday", 1, "9:00-9:50", "EntDev"),
    ("3rd", "B", "Friday", 3, "10:40-11:30", "DBMS Lab"),
    ("3rd", "B", "Friday", 6, "1:10-2:00", "SE"),
    ("5th", "A", "Monday", 1, "9:00-9:50", "µP Lab"),
    ("5th", "A", "Monday", 3, "10:40-11:30", "DAA"),
    ("5th", "A", "Monday", 4, "11:30-12:20", "OS"),
    ("5th", "A", "Monday", 7, "2:00-2:50", "Python"),
    ("5th", "A", "Monday", 10, "4:30-5:20", "OE-Python"),
    ("5th", "A", "Tuesday", 1, "9:00-9:50", "Python"),
    ("5th", "A", "Tuesday", 3, "10:40-11:30", "µP"),
    ("5th", "A", "Tuesday", 4, "11:30-12:20", "DAA"),
    ("5th", "A", "Tuesday", 6, "1:10-2:00", "CS"),
    ("5th", "A", "Tuesday", 10, "4:30-5:20", "OE-DBMS"),
    ("5th", "A", "Wednesday", 3, "10:40-11:30", "µP"),
    ("5th", "A", "Wednesday", 4, "11:30-12:20", "DAA"),
    ("5th", "A", "Wednesday", 7, "2:00-2:50", "OS"),
    ("5th", "A", "Wednesday", 9, "3:40-4:30", "CS"),
    ("5th", "A", "Thursday", 1, "9:00-9:50", "Python"),
    ("5th", "A", "Thursday", 2, "09:50-10:40", "OS"),
    ("5th", "A", "Thursday", 3, "10:40-11:30", "µP"),
    ("5th", "A", "Thursday", 6, "1:10-2:00", "CS"),
    ("7th", "A", "Monday", 1, "9:00-9:50", "E II - ML"),
    ("7th", "A", "Monday", 5, "12:20-01:10", "E IV - DL"),
    ("7th", "A", "Monday", 8, "2:50-3:40", "CD"),
    ("7th", "A", "Monday", 9, "3:40-4:30", "Pre-Project"),
    ("7th", "A", "Tuesday", 2, "09:50-10:40", "NS"),
    ("7th", "A", "Tuesday", 4, "11:30-12:20", "OR"),
    ("7th", "A", "Tuesday", 5, "12:20-01:10", "E II - ML"),
    ("7th", "A", "Wednesday", 1, "9:00-9:50", "NS"),
    ("7th", "A", "Wednesday", 2, "09:50-10:40", "CD"),
    ("7th", "A", "Wednesday", 4, "11:30-12:20", "OR"),
    ("7th", "A", "Wednesday", 5, "12:20-01:10", "E III - ADB"),
    ("7th", "A", "Thursday", 3, "10:40-11:30", "CD"),
    ("7th", "A", "Thursday", 5, "12:20-01:10", "E III - DA"),
    ("7th", "A", "Thursday", 7, "2:00-2:50", "NS"),
    ("7th", "A", "Thursday", 8, "2:50-3:40", "Seminar"),
    ("7th", "A", "Friday", 1, "9:00-9:50", "E III - DA"),
    ("7th", "A", "Friday", 2, "09:50-10:40", "E IV - DL"),
    ("7th", "A", "Friday", 7, "2:00-2:50", "E II - ML"),
    ("1st M.Tech", "-", "Monday", 2, "09:50-10:40", "E I - AI"),
    ("1st M.Tech", "-", "Monday", 3, "10:40-11:30", "E III - IoT"),
    ("1st M.Tech", "-", "Monday", 4, "11:30-12:20", "NGN"),
    ("1st M.Tech", "-", "Monday", 5, "12:20-01:10", "SA"),
    ("1st M.Tech", "-", "Thursday", 4, "11:30-12:20", "E II - NSS"),
    ("3rd M.Tech", "-", "Monday", 2, "09:50-10:40", "E-VIII-DL"),
    ("3rd M.Tech", "-", "Monday", 3, "10:40-11:30", "E-VII-BG"),
    ("3rd M.Tech", "-", "Monday", 4, "11:30-12:20", "ToC"),
    ("3rd M.Tech", "-", "Monday", 5, "12:20-01:10", "RM"),
    ("3rd M.Tech", "-", "Thursday", 9, "3:40-4:30", "PD-I"),
]


def load_data():
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    conn.executemany(
        "INSERT OR REPLACE INTO courses VALUES (?, ?, ?, ?, ?)",
        [(short, code, name, credits, faculty) for short, name, code, credits, faculty in courses_data]
    )

    conn.executemany(
        "INSERT INTO timetable (semester, section, day, hour, time_slot, course_short_name) VALUES (?, ?, ?, ?, ?, ?)",
        timetable_data
    )

    conn.commit()
    print(f"Loaded {len(courses_data)} courses and {len(timetable_data)} timetable entries into {DB_PATH}")
    conn.close()


if __name__ == "__main__":
    load_data()