'from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from student import Student, StudentGroup, StudentGrade, get_subject_factory
from vizualization import Plot
from typing import List
import os



app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')
show_navbar = True

data: List[Student] = [];

def get_students():
    return data.copy()

def get_group():
    students = get_students()
    if not students:
        return None
    return StudentGroup(students)

def get_plot():
    return Plot()

def parse_json(data: dict) -> List[Student]:
    # Перевірка наявності ключа "students"
    if "students" not in data:
        raise ValueError('JSON має містити ключ "students"')
    students_data = data["students"]
    if not isinstance(students_data, list) or not students_data:
        raise ValueError('Ключ "students" має містити непустий список')

    res = []
    for idx, item in enumerate(students_data):
        # Перевірка ключа "name"
        if "name" not in item:
            raise ValueError(f'Студент #{idx + 1} не містить ключ "name"')
        # Перевірка ключа "grades"
        if "grades" not in item:
            raise ValueError(f'Студент #{idx + 1} не містить ключ "grades"')

        name = item["name"]
        grades = item["grades"]

        if not isinstance(grades, dict):
            raise ValueError(f'Поле "grades" у студента #{idx + 1} має бути словником')

        student_grades = []
        for subject, grade in grades.items():
            subject_obj = get_subject_factory(subject)
            student_grades.append(StudentGrade(subject_obj, grade))

        student = Student(name, student_grades)
        res.append(student)

    return res

@app.route("/")
def login():
    first_try = True
    return render_template("index.html", first_try = first_try)


@app.route("/upload", methods=["POST"])
def upload_file():
    first_try = True
    show_navbar = False
    global data
    uploaded_file = request.files["file"]
    if uploaded_file and uploaded_file.filename.endswith(".json"):
        try:
            res = json.load(uploaded_file)
            data = parse_json(res)
        except ValueError as err:
            return render_template("uploads.html", error=f"Структура JSON невалідна: {err}")
        except Exception:
            return render_template("uploads.html", error="Файл не є валідним JSON")
        # Перевірка на коректність структури (тепер вже не потрібна, бо вона є у parse_json)
        if not isinstance(data, list) or not data:
            return render_template("uploads.html", error="JSON не містить коректного списку студентів")
        show_navbar = True
        first_try = False
        return render_template("index.html", show_navbar=show_navbar, first_try = first_try)
        # return redirect(url_for("login"))
    return render_template("uploads.html", error="Файл не є JSON")

@app.route('/average_per_subject')
def aver_subject():
    group = get_group()
    plot = get_plot()
    if not group:
        return redirect(url_for("login"))
    subjects = group.get_subjects()
    averages = list(group.average_per_subject().values())
    plot.plot_bar_average_per_subject(
        subjects, averages, "Середнє значення по предметам", "static/image/avg_per_subject.png"
    )
    return render_template('average_per_subject.html', show_navbar = show_navbar)

@app.route('/average_per_student')
def aver_per_student():
    group = get_group()
    plot = get_plot()
    if not group:
        return redirect(url_for("login"))
    averages_dict = group.average_per_student()
    names = list(averages_dict.keys())
    avgs = list(averages_dict.values())
    students = zip(names, avgs)
    plot.plot_bar_average_per_student(
        names,
        avgs,
        "Середній бал для кожного студента",
        "static/image/avg_per_student.png"
    )
    return render_template('average_per_student.html', show_navbar = show_navbar, data = students)


@app.route('/mode')
def mode_page():
    group = get_group()
    if not group:
        return redirect(url_for("login"))
    subjects = group.get_subjects()
    modes = list(group.mode_by_subject().values())
    Plot.modes_per_subject(subjects, modes, "Мода по предмету", "static/image/mode.png")
    return render_template('mode.html', show_navbar = show_navbar)

@app.route('/list_of_students')
def list_of_students():
    students = get_students()
    if not students:
        return redirect(url_for("login"))
    return render_template('list_of_students.html', students=students, show_navbar = show_navbar)

# Форма для завантаження students.json
@app.route("/upload")
def upload_students():
    return render_template("uploads.html")

if __name__ == "__main__":
    app.run(debug=False)

