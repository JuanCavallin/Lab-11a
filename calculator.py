import matplotlib.pyplot as plt
import os

# Student = [name, id (3 digit)]
# Assignment = [name, points, id (5 digit)]
# Submission = [studentid, assignmentid, percentage of points]
# Total points for all assignments = 1000

students = {}
assignments = {}
submissions = {}
student_grades = {}

# Read student data
with open("data/students.txt", "r") as f:
    for line in f:
        sid = int(line[:3])
        name = line[3:].strip()
        students[sid] = name

# Read assignment data
with open("data/assignments.txt", "r") as f:
    lines = [line.strip() for line in f.readlines()]
    for i in range(0, len(lines), 3):
        name = lines[i]
        aid = int(lines[i + 1])
        points = int(lines[i + 2])
        assignments[aid] = {"name": name, "points": points}

# Read submission data
for filename in os.listdir("data/submissions"):
    with open(os.path.join("data/submissions", filename), "r") as f:
        for line in f:
            sid, aid, pct = line.strip().split("|")
            sid, aid, pct = int(sid), int(aid), float(pct)

            if aid not in submissions:
                submissions[aid] = {}
            submissions[aid][sid] = pct

            if sid not in student_grades:
                student_grades[sid] = []
            student_grades[sid].append((pct, assignments[aid]["points"]))

while(True):
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")

    option = input("\nEnter your selection: ")

    if option == "1":
        name = input("What is the student's name: ")
        found = False
        for sid, sname in students.items():
            if sname.lower() == name.lower():
                found = True
                scores = student_grades.get(sid, [])
                if not scores:
                    print("This student has no submissions.")
                else:
                    total_earned = sum((pct / 100) * pts for pct, pts in scores)
                    total_possible = sum(pts for _, pts in scores)
                    grade = round((total_earned / total_possible) * 100)
                    print(f"{grade}%")
        if not found:
            print("Student not found")

    elif option == "2":
        name = input("What is the assignment name: ")
        found = False
        for aid, adata in assignments.items():
            if adata["name"].lower() == name.lower():
                found = True
                scores = list(submissions.get(aid, {}).values())
                if not scores:
                    print("No submissions for this assignment.")
                else:
                    print(f"Min: {int(min(scores))}%")
                    print(f"Avg: {int(sum(scores)/len(scores))}%")
                    print(f"Max: {int(max(scores))}%")
        if not found:
            print("Assignment not found")

    elif option == "3":
        name = input("What is the assignment name: ")
        found = False
        for aid, adata in assignments.items():
            if adata["name"].lower() == name.lower():
                found = True
                scores = list(submissions.get(aid, {}).values())
                if not scores:
                    print("No submissions to display.")
                else:
                    plt.hist(scores, bins=[0,25,50,75,100], edgecolor='black')
                    plt.title(f"Score Distribution: {adata['name']}")
                    plt.xlabel("Percentage")
                    plt.ylabel("Number of Students")
                    plt.grid(True)
                    plt.tight_layout()
                    plt.show()
        if not found:
            print("Assignment not found")

    else:
        print("Invalid selection!")
