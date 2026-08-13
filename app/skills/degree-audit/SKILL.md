---
name: degree-audit
description: >
  Audits degree progress for UC Santa Cruz students. Checks completed
  courses against degree requirements for CS, Biology, Biochemistry,
  and MCD Biology majors. Shows remaining requirements and estimated
  quarters to graduation.
---

# Degree Audit Instructions

When a student asks about their degree progress or remaining requirements:

## Step 1: Identify the Major
Ask or infer the student's major:
- Computer Science B.S.
- Computer Science B.A.
- Biology B.S.
- Biology B.A.
- Molecular, Cell & Developmental Biology B.S.
- Biochemistry & Molecular Biology B.S.

## Step 2: Load Requirements
Use `load_skill_resource` to read:
- `references/degree-requirements.md` for CS majors
- `references/bio-degree-requirements.md` for Biology/Biochem majors

## Step 3: Gather Student Info
Ask the student:
1. What courses have they completed? (or approximate year/quarter)
2. What's their current GPA?
3. Any courses in progress?

## Step 4: Audit
Compare completed courses against requirements:
- Lower-division requirements
- Upper-division core
- Upper-division electives
- Disciplinary communication (DC)
- Capstone
- General Education (note: varies by residential college)

## Step 5: Output Format

```
📋 Degree Audit — Computer Science B.S.

✅ Completed Requirements:
- [x] Lower-division: CSE 30, CSE 12, CSE 13S, CSE 16, MATH 19A/19B
- [x] CSE 100, CSE 101, CSE 102

⏳ In Progress:
- [ ] CSE 130 (this quarter)

❌ Remaining Requirements:
- [ ] CSE 103 — Computational Models
- [ ] CSE 107 — Probability & Statistics
- [ ] CSE 114A — Foundations of Programming Languages
- [ ] CSE 120 — Computer Architecture
- [ ] 1 DC course (CSE 115A recommended)
- [ ] 1 Capstone (CSE 115B or CSE 195)
- [ ] 3 electives from approved list

📊 Progress: 62% complete
⏰ Estimated quarters remaining: 4-5
💡 Recommended next quarter: CSE 103, CSE 107, CSE 114A
```

## Step 6: Recommendations
- Suggest course ordering based on prerequisites
- Flag any deadline concerns (6th quarter major declaration, etc.)
- Note if they're on track for 4-year graduation
