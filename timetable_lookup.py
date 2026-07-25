import sqlite3

DB_PATH = "college_data.db"


def get_timetable(semester=None, section=None, day=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT t.semester, t.section, t.day, t.hour, t.time_slot,
           t.course_short_name, c.course_name, c.faculty_name
    FROM timetable t
    LEFT JOIN courses c ON t.course_short_name = c.short_name
    WHERE 1=1
    """
    params = []

    if semester:
        query += " AND t.semester LIKE ?"
        params.append(f"%{semester}%")
    if section:
        query += " AND t.section = ?"
        params.append(section)
    if day:
        query += " AND t.day = ?"
        params.append(day)

    query += " ORDER BY t.hour"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows


def format_timetable_results(rows):
    if not rows:
        return "No timetable entries found for that search."

    lines = []
    for row in rows:
        semester, section, day, hour, time_slot, short_name, course_name, faculty = row
        lines.append(
            f"{day}, Hour {hour} ({time_slot}): {short_name} - {course_name or 'N/A'} "
            f"[Faculty: {faculty or 'N/A'}] (Sem {semester}, Sec {section})"
        )
    return "\n".join(lines)


def find_course_by_keyword(keyword):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT course_code, short_name, course_name, credits, faculty_name FROM courses WHERE course_name LIKE ? OR short_name LIKE ?",
        (f"%{keyword}%", f"%{keyword}%")
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    print("Testing timetable lookup...")
    results = get_timetable(semester="3rd", section="A", day="Monday")
    print(format_timetable_results(results))