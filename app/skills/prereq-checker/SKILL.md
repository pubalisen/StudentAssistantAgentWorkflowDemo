---
name: prereq-checker
description: >
  Checks prerequisite chains for UC Santa Cruz courses. Traces the full
  dependency tree for any course (direct and transitive prerequisites).
  Supports CS, Biology, and Biochemistry majors. Uses real 2025-2026
  UCSC catalog data.
---

# Prerequisite Checker Instructions

When a student asks about prerequisites for a course:

## Step 1: Identify the Course
Parse the course code (e.g., "CSE 130", "BIOL 100", "CHEM 8A").
Accept flexible input: "CS 130", "cse130", "Computer Systems Design".

## Step 2: Load Reference Data
Use `load_skill_resource` to read:
- `references/cs-prereqs.md` for CSE/MATH/AM courses
- `references/bio-prereqs.md` for BIOL/CHEM/BIOE courses

## Step 3: Build the Prerequisite Chain
For the target course:
1. Find its direct prerequisites
2. For each prerequisite, find ITS prerequisites (recursive)
3. Continue until you reach courses with no prerequisites
4. Present as a dependency tree

## Step 4: Output Format

```
Target: CSE 130 — Principles of Computer Systems Design

Prerequisite Chain:
CSE 130
├── CSE 120 (Computer Architecture)
│   ├── CSE 100 (Logic Design)
│   │   └── CSE 12 (Computer Systems & Assembly)
│   │       └── CSE 30 (Programming Abstractions: Python) ← Entry level
│   └── CSE 13S (Computer Systems & C Programming)
│       └── CSE 12
└── CSE 101 (Data Structures & Algorithms)
    ├── CSE 13S
    ├── CSE 16 (Applied Discrete Mathematics)
    │   └── MATH 19A (Calculus I) ← Entry level
    └── MATH 19B (Calculus II)
        └── MATH 19A

Total courses in chain: 8
Entry-level courses (no prereqs): CSE 30, MATH 19A
```

## Step 5: Additional Context
- Note if any courses are offered only in specific quarters
- Mention if the student's current coursework satisfies any prerequisites
- Suggest the optimal order to take courses
