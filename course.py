"""CSC148 Assignment 1

=== CSC148 Winter 2023 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Misha Schwartz, Mario Badr, Christine Murad, Diane Horton,
Sophia Huynh, Jaisie Sin, Tom Ginsberg, Jonathan Calver, and Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Misha Schwartz, Mario Badr, Diane Horton, Sophia Huynh,
Jonathan Calver, and Jacqueline Smith

=== Module Description ===
This file contains classes that describe a university course and the students
who are enrolled in these courses.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from survey import Answer, Survey, Question


# Provided helper function
def sort_students(lst: list[Student], attribute: str) -> list[Student]:
    """Return a shallow copy of <lst> sorted by <attribute> in non-decreasing
    order.

    Being a shallow copy means that a new list is returned, but it contains
    ids of the same Student objects as in <lst>; no new Student objects are
    created. The conseqence of this is that aliasing exists. Suggestion: draw
    a memory model diagram to ensure that you understand this.

    Preconditions:
        - <attribute> is an attribute name for the Student class

    >>> s1 = Student(1, 'Misha')
    >>> s2 = Student(2, 'Diane')
    >>> s3 = Student(3, 'Mario')
    >>> sort_students([s1, s3, s2], 'id') == [s1, s2, s3]
    True
    >>> sort_students([s1, s2, s3], 'name') == [s2, s3, s1]
    True
    """
    return sorted(lst, key=lambda student: getattr(student, attribute))


class Student:
    """A Student who can be enrolled in a university course.

    === Public Attributes ===
    id: the id of the student
    name: the name of the student

    === Private Attributes ===
    _answers: The answers the student gives to the questions.
        Each key is the question, and its value is the student's answer in
        response to the question

    === Representation Invariants ===
    name is not the empty string
    """
    id: int
    name: str
    _answers: dict[Question, Answer]

    def __init__(self, id_: int, name: str) -> None:
        """Initialize a student with name <name> and id <id>

        Precondition: len(name) > 0, and id > 0

        >>> diane = Student(1, 'Diane')
        >>> diane.name
        'Diane'
        >>> diane.id
        1
        """
        self.id = id_
        self.name = name
        self._answers = {}

    def __str__(self) -> str:
        """Return the name of this student
        >>> diane = Student(1, 'Diane')
        >>> diane.__str__()
        'Diane'
        """
        return f'{self.name}'

    def has_answer(self, question: Question) -> bool:
        """Return True iff this student has an answer for a question with the
        same id as <question> and that answer is a valid answer for <question>.
        """
        # Multiple cases where this can return False
        # - student hasn't given an answer,
        # - student's answer is not valid or
        # - question doesn't exist in _answers
        student_answer = self.get_answer(question)
        for q in self._answers:
            if q.id == question.id:
                if student_answer is not None \
                        and student_answer.is_valid(question):
                    return True
        return False

    def set_answer(self, question: Question, answer: Answer) -> None:
        """Record this student's answer <answer> to the question <question>.

        If this student already has an answer recorded for the question, then
        replace it with <answer>.
        """
        for q in self._answers:
            # check to see if question already exists in dict of answers, and
            # replace existing answer
            if q.id == question.id:
                self._answers[q] = answer
        # if question doesn't exist in dict of answers, record student's answer
        else:
            self._answers[question] = answer

    def get_answer(self, question: Question) -> Optional[Answer]:
        """Return this student's answer to the question <question>.
        Return None if this student does not have an answer to <question>
        """
        # Two cases of returning None; if question does not exist in dict, or
        # if question DOES exist in dict, but student hasn't answered (ie; None)
        for q in self._answers:
            if q.id == question.id:
                # Question does exist in dict
                if self._answers[q] is not None:
                    # Student has answered question
                    return self._answers[q]
                # Student doesn't have answer to question
                if self._answers[q] is None:
                    return None
        # Question does not exist in dict
        return None


class Course:
    """A University Course

    === Public Attributes ===
    name: the name of the course
    students: a list of students enrolled in the course

    === Representation Invariants ===
    - No two students in this course have the same id
    - name is not the empty string
    - name can not contain special characters
    """
    name: str
    students: list[Student]

    def __init__(self, name: str) -> None:
        """Initialize a course with the name of <name>.
        >>> CSC148 = Course('CSC148', [])
        >>> CSC148.name
        'CSC148'

        Precondition: len(name) > 0
        """
        self.name = name
        self.students = []

    def enroll_students(self, students: list[Student]) -> None:
        """Enroll all students in <students> in this course.

        If adding any student would violate a representation invariant,
        do not add any of the students in <students> to the course.
        """
        for student in students:
            # Check if student id exists in the course
            if student.id in students:
                pass
            # Check if student's name is an empty string
            elif len(student.name) == 0:
                pass
            else:
                # If both rep.invariants aren't violated, enroll student
                self.students.append(student)

    def all_answered(self, survey: Survey) -> bool:
        """Return True iff all the students enrolled in this course have a
        valid answer for every question in <survey>.
        """
        all_questions_in_survey = survey.get_questions()
        for student in self.students:
            for question in all_questions_in_survey:
                if student.has_answer(question) \
                        and student.get_answer(question) is not None:
                    return True
        return False

    def get_students(self) -> tuple[Student]:
        """Return a tuple of all students enrolled in this course.

        The students in this tuple should be in order according to their id
        from the lowest id to the highest id.

        Hint: the sort_students function might be useful
        """
        return tuple(sort_students(self.students, 'id'))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing', 'survey'],
                                'disable': ['E9992']})
