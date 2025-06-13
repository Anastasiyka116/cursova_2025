from abc import abstractmethod
from typing import List
import statistics
import json

class Subject:
    def __init__(self):
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    def __str__(self) -> str:
        return self.name()

class Mathematics(Subject): 
    def name(self) -> str:
        return "Математичний аналіз"

class DiscreteMathematics(Subject):
    def name(self) -> str:
        return "Дискретна математика"
    
class DifferentialEquations(Subject):
    def name(self) -> str:
        return "Диференціальні рівняння"
    
class ProbabilityTheory(Subject):
    def name(self) -> str:
        return "Теорія ймовірності"

class LinearAlgebra(Subject):
    def name(self) -> str:
        return "Лінійна алгебра"
    
class ComputerScience(Subject):
    def name(self) -> str:
        return "Комп'ютерні науки"
    
class English(Subject):
    def name(self) -> str:
        return "Англійська мова"

class PhysicalEducation(Subject):
    def name(self) -> str:
        return "Фізкультура"
    
class AlgorithmsAndDataStructures(Subject):
    def name(self) -> str:
        return "Алгоритми та структури даних"
    

def get_subject_factory(subject_name: str) -> Subject:
    if subject_name == "Математичний аналіз":
        return Mathematics()
    elif subject_name == "Дискретна математика":
        return DiscreteMathematics()
    elif subject_name == "Диференціальні рівняння":
        return DifferentialEquations()
    elif subject_name == "Теорія ймовірності":
        return ProbabilityTheory()
    elif subject_name == "Лінійна алгебра":
        return LinearAlgebra()
    elif subject_name == "Комп'ютерні науки":
        return ComputerScience()
    elif subject_name == "Англійська":
        return English()
    elif subject_name == "Фізкультура":
        return PhysicalEducation()
    elif subject_name == "Алгоритми та структури даних":
        return AlgorithmsAndDataStructures()
    else:
        raise ValueError(f"Не відомий предмет: {subject_name}")


class StudentGrade:
    def __init__(self, subject: Subject, grade: int):
        self._subject = subject
        self._grade = grade

    @property
    def subject(self) -> Subject:
        return self._subject
    
    @property
    def grade(self) -> int:
        return self._grade

class Student(json.JSONEncoder):
    def __init__(self, name: str, grades: List[StudentGrade]):
            self._name = name
            self._grades = grades  # dict

    @property
    def name(self) -> str:
        return self._name

    @property
    def grades(self) -> List[StudentGrade]:
        return self._grades

    def average(self) -> float:
        if not self._grades:
            return 0.0
        return sum(grade.grade for grade in self._grades) / len(self._grades)

    def grade_for_subject(self, subject: Subject) -> int:
        return self._grades.get(subject)
    
    def default(self, o):
        if isinstance(o, StudentGrade):
            return o.__dict__
        return super().default(o)

class StudentGroup:
    def __init__(self, students: List[Student]):
        self.students = students

    def grades_per_subject(self) -> dict[str, list[int]]:
        grades_per_subj = {}
        for student in self.students:
            for student_grade in student.grades:
                subject_name = student_grade.subject.name()

                if subject_name not in grades_per_subj:
                    grades_per_subj[subject_name]=[]
                grades_per_subj[subject_name].append(student_grade.grade)
        return grades_per_subj

    def mode_by_subject(self) -> dict[str, int]:
        modes = {}
        grades_dict = self.grades_per_subject()
        for subject, grades in grades_dict.items():
            try:
                modes[subject]= statistics.mode(grades)
            except statistics.StatisticsError:
                modes[subject] = None  # якщо моди немає
        return modes

    def average_per_subject(self) -> dict[str, float]:
        averages = {}
        grades_dict = self.grades_per_subject()
        for subject, grades in grades_dict.items():
            try:
                averages[subject] = statistics.mean(grades)
            except statistics.StatisticsError:
                averages[subject] = None  # якщо моди немає
        return averages

    def get_subjects(self) -> list[str]:
        if self.students:
            return [grade.subject.name() for grade in self.students[0].grades]
        return []

    def average_per_student(self) -> dict[str, float]:
        averages_student = {}
        for student in self.students:
            averages_student[student.name] = student.average()
        return averages_student



