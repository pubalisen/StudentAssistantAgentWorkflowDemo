"""Simulated UCSC Student Records Database.

In production, this would query BigQuery or Cloud SQL. For this demo,
we use in-memory records for two sample students.
"""

STUDENT_RECORDS = {
    "maria.chen": {
        "student_id": "1847293",
        "name": "Maria Chen",
        "email": "mchen@ucsc.edu",
        "major": "Computer Science B.S.",
        "college": "Rachel Carson College",
        "year": "Junior (3rd year)",
        "enrollment_status": "Active — Full-time",
        "gpa": 3.72,
        "units_completed": 112,
        "units_required": 180,
        "advisor": "Dr. James Davis",
        "enrollment_pass": "Pass 1 — November 6, 2025",

        "current_quarter": "Fall 2025",
        "enrolled_courses": [
            {"code": "CSE 130", "title": "Principles of Computer Systems Design", "professor": "Dr. Ethan Miller", "units": 5, "schedule": "MWF 10:40-11:45 AM, E2-192"},
            {"code": "CSE 114A", "title": "Foundations of Programming Languages", "professor": "Dr. Cormac Flanagan", "units": 5, "schedule": "TuTh 1:30-3:05 PM, J Baskin 165"},
            {"code": "CSE 115A", "title": "Software Engineering (DC)", "professor": "Dr. Richard Jullig", "units": 5, "schedule": "MWF 1:20-2:25 PM, Soc Sci 2 075"},
        ],

        "completed_courses": [
            {"code": "CSE 12",   "title": "Computer Systems & Assembly",       "grade": "A",  "quarter": "Fall 2023"},
            {"code": "CSE 13S",  "title": "Computer Systems & C Programming",  "grade": "A-", "quarter": "Fall 2023"},
            {"code": "CSE 16",   "title": "Applied Discrete Mathematics",      "grade": "B+", "quarter": "Fall 2023"},
            {"code": "MATH 19A", "title": "Calculus I",                        "grade": "A",  "quarter": "Fall 2023"},
            {"code": "CSE 30",   "title": "Programming Abstractions: Python",  "grade": "A",  "quarter": "Winter 2024"},
            {"code": "MATH 19B", "title": "Calculus II",                       "grade": "A-", "quarter": "Winter 2024"},
            {"code": "MATH 21",  "title": "Linear Algebra",                    "grade": "B+", "quarter": "Winter 2024"},
            {"code": "CSE 100",  "title": "Logic Design",                      "grade": "A-", "quarter": "Spring 2024"},
            {"code": "CSE 101",  "title": "Data Structures & Algorithms",      "grade": "A",  "quarter": "Spring 2024"},
            {"code": "AM 10",    "title": "Mathematical Methods for Engineers", "grade": "B+", "quarter": "Spring 2024"},
            {"code": "CSE 102",  "title": "Analysis of Algorithms",            "grade": "A-", "quarter": "Fall 2024"},
            {"code": "CSE 120",  "title": "Computer Architecture",             "grade": "B+", "quarter": "Fall 2024"},
            {"code": "CSE 107",  "title": "Probability & Statistics",          "grade": "A",  "quarter": "Winter 2025"},
            {"code": "CSE 103",  "title": "Computational Models",              "grade": "A-", "quarter": "Winter 2025"},
            {"code": "STAT 131", "title": "Intro to Probability Theory",       "grade": "B+", "quarter": "Spring 2025"},
            {"code": "CSE 180",  "title": "Database Systems I",                "grade": "A",  "quarter": "Spring 2025"},
        ],

        "remaining_requirements": [
            "CSE 130 — Principles of Computer Systems Design (in progress)",
            "CSE 114A — Foundations of Programming Languages (in progress)",
            "CSE 115A — Software Engineering / DC (in progress)",
            "2 upper-division electives from approved list",
            "1 Capstone (CSE 115B or CSE 195)",
        ],

        "financial_aid": {
            "pell_grant": "$3,498/year",
            "cal_grant": "$14,226/year",
            "uc_blue_and_gold": "Eligible (family income < $80K)",
            "merit_scholarship": "Dean's List Scholarship — $2,500/year",
            "total_aid": "$20,224/year",
            "remaining_cost": "$2,328/year (books, personal)",
        },

        "recommendations": [
            "On track for graduation in Spring 2026 (4-year plan ✅)",
            "Consider CSE 183 (Web Applications) or CSE 185E (Tech Writing) as electives",
            "Strong candidate for undergraduate research — talk to Dr. Miller about systems research",
            "Apply for TA positions in CSE 12 or CSE 30 (GPA qualifies)",
            "Register for capstone (CSE 195 Senior Design) in Winter 2026",
        ],
    },

    "james.rivera": {
        "student_id": "1923841",
        "name": "James Rivera",
        "email": "jrivera@ucsc.edu",
        "major": "Biology B.S.",
        "college": "Crown College",
        "year": "Sophomore (2nd year)",
        "enrollment_status": "Active — Full-time",
        "gpa": 2.84,
        "units_completed": 68,
        "units_required": 180,
        "advisor": "Dr. Beth Bhatt (Biology) / Dr. James Davis (CSE)",
        "enrollment_pass": "Pass 2 — November 13, 2025",

        "current_quarter": "Fall 2025",
        "enrolled_courses": [
            {"code": "BIOL 101", "title": "Ecology & Evolution", "professor": "Dr. Beth Shapiro", "units": 5, "schedule": "MWF 9:20-10:25 AM, Thimann 001"},
            {"code": "CHEM 8B",  "title": "Organic Chemistry II", "professor": "Dr. Scott Oliver", "units": 5, "schedule": "TuTh 10:00-11:35 AM, Phys Sci 114"},
            {"code": "CSE 30",   "title": "Programming Abstractions: Python", "professor": "Dr. Patrick Tantalo", "units": 5, "schedule": "MWF 1:20-2:25 PM, J Baskin 152"},
        ],

        "completed_courses": [
            {"code": "BIOL 20A",  "title": "Cell Biology",                     "grade": "B-", "quarter": "Fall 2024"},
            {"code": "CHEM 1A",   "title": "General Chemistry I",              "grade": "C+", "quarter": "Fall 2024"},
            {"code": "MATH 19A",  "title": "Calculus I",                       "grade": "B",  "quarter": "Fall 2024"},
            {"code": "WRIT 1",    "title": "Intro to University Writing",      "grade": "A-", "quarter": "Fall 2024"},
            {"code": "BIOL 20B",  "title": "Evolution & Ecology Intro",        "grade": "B",  "quarter": "Winter 2025"},
            {"code": "CHEM 1B",   "title": "General Chemistry II",             "grade": "C",  "quarter": "Winter 2025"},
            {"code": "MATH 19B",  "title": "Calculus II",                      "grade": "C+", "quarter": "Winter 2025"},
            {"code": "BIOL 20C",  "title": "Intro to Animal Physiology",       "grade": "B+", "quarter": "Spring 2025"},
            {"code": "CHEM 8A",   "title": "Organic Chemistry I",              "grade": "B-", "quarter": "Spring 2025"},
            {"code": "PHYS 6A",   "title": "Intro Physics I",                  "grade": "B",  "quarter": "Spring 2025"},
        ],

        "remaining_requirements_bio": [
            "BIOL 100 — Intro to Scientific Research (required)",
            "BIOL 105 — Biology of Invertebrates OR BIOL 115 — Marine Biology",
            "BIOL 110 — Intro to Molecular Biology",
            "4 upper-division BIOL electives (20 units)",
            "CHEM 108 — Biochemistry",
            "PHYS 6B/6C — Intro Physics II & III",
            "MATH 22 or AM 10",
            "Capstone: BIOL 195 Senior Thesis",
        ],

        "cs_switch_status": {
            "eligible_to_declare": "Not yet — need CSE 12, CSE 13S, CSE 16, CSE 30 (in progress)",
            "courses_that_transfer": ["MATH 19A (B — meets prereq)", "MATH 19B (C+ — meets min)"],
            "courses_needed_for_cs": [
                "CSE 12 — Computer Systems & Assembly (take Winter 2026)",
                "CSE 13S — Computer Systems & C Programming (take Winter 2026)",
                "CSE 16 — Applied Discrete Math (take Spring 2026)",
                "CSE 30 — Programming Abstractions: Python (in progress Fall 2025)",
            ],
            "estimated_extra_quarters": "3-4 quarters behind CS peers",
            "gpa_concern": "CS requires 2.8+ in screening courses — current 2.84 is very close to minimum",
        },

        "financial_aid": {
            "pell_grant": "$4,731/year",
            "cal_grant": "$14,226/year",
            "work_study": "$3,200/year (campus job)",
            "parent_contribution": "$4,500/year",
            "total_aid": "$22,157/year",
            "remaining_cost": "$7,743/year (housing, books, personal)",
            "note": "Switching majors does NOT affect financial aid eligibility",
        },

        "recommendations": [
            "⚠️ GPA of 2.84 is close to the 2.8 minimum for CS screening — need strong grades this quarter",
            "If switching to CS: take CSE 12 + CSE 13S together in Winter 2026",
            "Visit STEM Transfer Success Center (Baskin 101) for CS advising",
            "Consider tutoring for Chemistry — C+ trend is a risk for Bio continuation too",
            "Talk to pre-med advisor if med school is the goal — Bio B.S. may still be better path",
            "Apply for MESA (Math, Engineering, Science Achievement) tutoring program",
        ],
    },
}


def lookup_student_record(
    student_username: str,
    info_type: str = "all",
) -> str:
    """Look up a UCSC student's academic record by their username.

    This simulates a BigQuery/database lookup for student data.

    Args:
        student_username: The student's UCSC username (e.g., "maria.chen" or "james.rivera").
            Available students: maria.chen, james.rivera
        info_type: What type of information to return. Options:
            - "all" — Full student profile (default)
            - "grades" — Completed courses and grades
            - "gpa" — GPA and academic standing
            - "enrolled" — Currently enrolled courses
            - "remaining" — Remaining degree requirements
            - "financial" — Financial aid summary
            - "recommendations" — Personalized recommendations

    Returns:
        Formatted student record data.
    """
    record = STUDENT_RECORDS.get(student_username)
    if not record:
        available = ", ".join(STUDENT_RECORDS.keys())
        return (
            f"Student '{student_username}' not found. "
            f"Available students for demo: {available}"
        )

    name = record["name"]

    if info_type == "gpa":
        return (
            f"## {name} — Academic Standing\n"
            f"- **GPA:** {record['gpa']}\n"
            f"- **Major:** {record['major']}\n"
            f"- **Year:** {record['year']}\n"
            f"- **Units:** {record['units_completed']}/{record['units_required']} completed\n"
            f"- **Progress:** {record['units_completed']/record['units_required']*100:.0f}%\n"
            f"- **College:** {record['college']}\n"
            f"- **Advisor:** {record['advisor']}"
        )

    if info_type == "grades":
        lines = [f"## {name} — Completed Courses & Grades\n"]
        for c in record["completed_courses"]:
            lines.append(f"- **{c['code']}** {c['title']} — {c['grade']} ({c['quarter']})")
        return "\n".join(lines)

    if info_type == "enrolled":
        lines = [f"## {name} — Currently Enrolled ({record['current_quarter']})\n"]
        for c in record["enrolled_courses"]:
            lines.append(
                f"- **{c['code']}** {c['title']}\n"
                f"  Prof: {c['professor']} | {c['units']} units | {c['schedule']}"
            )
        return "\n".join(lines)

    if info_type == "remaining":
        lines = [f"## {name} — Remaining Requirements ({record['major']})\n"]
        reqs = record.get("remaining_requirements") or record.get("remaining_requirements_bio", [])
        for r in reqs:
            lines.append(f"- {r}")
        if "cs_switch_status" in record:
            lines.append(f"\n### CS Switch Analysis")
            cs = record["cs_switch_status"]
            lines.append(f"- **Eligible to declare CS:** {cs['eligible_to_declare']}")
            lines.append(f"- **Courses that transfer:** {', '.join(cs['courses_that_transfer'])}")
            lines.append(f"- **Extra quarters needed:** {cs['estimated_extra_quarters']}")
            lines.append(f"- **GPA concern:** {cs['gpa_concern']}")
            lines.append(f"\n**Courses still needed for CS:**")
            for c in cs["courses_needed_for_cs"]:
                lines.append(f"  - {c}")
        return "\n".join(lines)

    if info_type == "financial":
        lines = [f"## {name} — Financial Aid Summary\n"]
        fa = record["financial_aid"]
        for k, v in fa.items():
            label = k.replace("_", " ").title()
            lines.append(f"- **{label}:** {v}")
        return "\n".join(lines)

    if info_type == "recommendations":
        lines = [f"## {name} — Personalized Recommendations\n"]
        for r in record["recommendations"]:
            lines.append(f"- {r}")
        return "\n".join(lines)

    # info_type == "all" — return everything
    parts = []
    parts.append(f"# Student Record: {name}\n")
    parts.append(f"| Field | Value |")
    parts.append(f"|-------|-------|")
    parts.append(f"| Student ID | {record['student_id']} |")
    parts.append(f"| Email | {record['email']} |")
    parts.append(f"| Major | {record['major']} |")
    parts.append(f"| Year | {record['year']} |")
    parts.append(f"| College | {record['college']} |")
    parts.append(f"| GPA | {record['gpa']} |")
    parts.append(f"| Units | {record['units_completed']}/{record['units_required']} |")
    parts.append(f"| Advisor | {record['advisor']} |")
    parts.append(f"| Enrollment Pass | {record['enrollment_pass']} |")
    parts.append(f"| Status | {record['enrollment_status']} |")
    parts.append("")

    parts.append(lookup_student_record(student_username, "enrolled"))
    parts.append("")
    parts.append(lookup_student_record(student_username, "grades"))
    parts.append("")
    parts.append(lookup_student_record(student_username, "remaining"))
    parts.append("")
    parts.append(lookup_student_record(student_username, "financial"))
    parts.append("")
    parts.append(lookup_student_record(student_username, "recommendations"))

    return "\n".join(parts)
