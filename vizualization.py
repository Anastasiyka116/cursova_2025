import matplotlib.pyplot as plt
import pandas as pd
from student import StudentGroup

class Plot():
    @staticmethod
    def plot_bar_average_per_subject(subjects, averages,title,filename):
        plt.figure(figsize=(12, 6))
        plt.bar(subjects, averages, color='skyblue')
        plt.title("Середній бал по кожному предмету")
        plt.xlabel("Предмет")
        plt.ylabel("Середній бал")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(filename)  # Зберігає малюнок!
        plt.close()


    @staticmethod
    def modes_per_subject(subjects, modes, title, filename):
        plt.figure(figsize=(12, 6))
        plt.bar(subjects, modes, color='skyblue')
        plt.title(title)
        plt.xlabel("Предмет")
        plt.ylabel("Мода")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(filename)   # Зберігає малюнок!
        plt.close()


    @staticmethod
    def boxplot(subjects, grades_per_subj, title, filename):
        plt.figure(figsize=(14, 6))
        plt.boxplot(grades_per_subj, tick_labels=subjects, widths=1, patch_artist=True,
                    showmeans=True, showfliers=True, medianprops={"color": "white", "linewidth": 0.5},
                    boxprops={"facecolor": "C0", "edgecolor": "white",
                              "linewidth": 0.5},
                    whiskerprops={"color": "C0", "linewidth": 1.5},
                    capprops={"color": "C0", "linewidth": 1.5})
        plt.title("boxplot")
        plt.ylabel("Оцінки")
        plt.tight_layout()

    @staticmethod
    def plot_bar_average_per_student(student_names, averages, title, filename):
        plt.figure(figsize=(12, 6))
        plt.bar(student_names, averages, color='lightgreen')
        plt.title(title)
        plt.xlabel("Студент")
        plt.ylabel("Середній бал")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
