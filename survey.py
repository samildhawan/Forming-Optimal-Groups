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

This file contains a class that describes a survey as well as classes that
describe different types of questions that can be asked on a survey.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Union
from criterion import InvalidAnswerError, HomogeneousCriterion

if TYPE_CHECKING:
    from criterion import Criterion
    from grouper import Grouping
    from course import Student


class Question:
    """An abstract class representing a question used in a survey

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """Initialize this question with the text <text>.
        "What is the name of this course?"

        Preconditions:
            - len(text) > 0
        """
        self.id = id_
        self.text = text

    def __str__(self) -> str:
        """Return a string representation of this question that contains both
        the text of this question and a description of all possible answers
        to this question.

        You can choose the precise format of this string.
        """
        raise NotImplementedError

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.
        """
        raise NotImplementedError

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return a float between 0.0 and 1.0 indicating how similar two
        answers are.

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question
        """
        raise NotImplementedError


class MultipleChoiceQuestion(Question):
    """A question whose answers can be one of several options

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str
    options: list[str]

    def __init__(self, id_: int, text: str, options: list[str]) -> None:
        """Initialize a question with the text <text> and id <id> and
        possible answers given in <options>.

        Preconditions:
            - No two elements in <options> are the same string
            - <options> contains at least two elements
            - len(text) > 0
        """
        Question.__init__(self, id_, text)
        self.options = options

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return f'The question is: {0}, \n and your options are: \n {1}'.format(
            self.text, str(self.options))

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.

        An answer is valid if its content is one of the answer options for this
        question.
        """
        for option in self.options:
            if option == answer.content:
                return True
        return False

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return 1.0 iff <answer1>.content and <answer2>.content are equal and
        0.0 otherwise.

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question.
        """
        if answer1.content == answer2.content:
            return 1.0
        return 0.0


class NumericQuestion(Question):
    """A question whose answer can be an integer between some minimum and
    maximum value (inclusive).

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str
    min_: int
    max_: int

    def __init__(self, id_: int, text: str, min_: int, max_: int) -> None:
        """Initialize a question with id <id_> and text <text> whose possible
        answers can be any integer between <min_> and <max_> (inclusive)

        Preconditions:
            - min_ < max_
            - len(text) > 0
        """
        Question.__init__(self, id_, text)
        self.min_ = min_
        self.max_ = max_

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        question_text = Question.__str__(self)
        return f'{question_text}' + '\n' + \
            f'Please provide an answer between: \n {0}, {1}'.format(self.min_,
                                                                    self.max_)

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff the content of <answer> is an integer between the
        minimum and maximum (inclusive) possible answers to this question.
        """
        return (isinstance(answer.content, int)
                and self.min_ <= answer.content <= self.max_)

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return the similarity between <answer1> and <answer2> over the range
        of possible answers to this question.

        Similarity is calculated as follows:
        1. first find the absolute difference between <answer1>.content and
           <answer2>.content.
        2. divide the value from step 1 by the difference between the maximum
           and minimum possible answers.
        3. subtract the value of step 2 from 1.0

        For example:
        - Maximum similarity is 1.0 and occurs when <answer1> == <answer2>
        - Minimum similarity is 0.0 and occurs when <answer1> is the minimum
            possible answer and <answer2> is the maximum possible answer
            (or vice versa).

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question
        """
        abs_diff = abs(answer1.content - answer2.content)

        return float(1.0 - (abs_diff / (self.max_ - self.min_)))


class YesNoQuestion(Question):
    """A question whose answer is either yes (represented by True) or
    no (represented by False).

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """Initialize a question with the text <text> and id <id>.

        Preconditions:
            - len(text) > 0
        """
        Question.__init__(self, id_, text)

    def __str__(self) -> str:
        """Return a string representation of this question including
        the text of the question.

        You can choose the precise format of this string.
        """
        question_text = Question.__str__(self)
        return f'{question_text}' + '\n' + 'Please choose between Yes or No:'

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.

        An answer is valid if its content is one of the answer options for
        this question.
        """
        return isinstance(answer.content, bool)

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return 1.0 iff <answer1>.content and <answer2>.content are equal
        and 0.0 otherwise.

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question.
        """
        if answer1.content == answer2.content:
            return 1.0
        return 0.0


class CheckboxQuestion(MultipleChoiceQuestion):
    """A question whose answers can be one or more of several options

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """
    id: int
    text: str

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.

        An answer is valid iff:
            * It is a non-empty list.
            * It has no duplicate entries.
            * Every item in it is one of the answer options for this question.
        """
        if (isinstance(answer.content, list) and len(answer.content) > 0
                and len(answer.content) == len(set(answer.content))):
            for a in answer.content:
                if a in self.options:
                    return True
        return False

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return the similarity between <answer1> and <answer2>.

        Similarity is defined as the ratio between the number of strings that
        are common to both <answer1>.content and <answer2>.content over the
        total number of unique strings that appear in both <answer1>.content and
        <answer2>.content. If there are zero unique strings in common,
        return 1.0.

        For example, if <answer1>.content == ['a', 'b', 'c'] and
        <answer2>.content == ['c', 'b', 'd'], there are 2 strings common to
        both: 'c' and 'b'; and there are 4 unique strings that appear in both:
        'a', 'b', 'c', and 'd'. Therefore, the similarity between these two
        answers is 2/4 = 0.5.

        Preconditions:
            - <answer1> and <answer2> are both valid answers to this question
        """
        num_unique_answers = len(set(answer1.content + answer2.content))
        common_strings = 0.0
        for answer in answer1.content:
            if answer in answer2.content:
                common_strings += 1.0
        return common_strings / num_unique_answers


class Answer:
    """An answer to a question used in a survey

    === Public Attributes ===
    content: an answer to a single question
    """
    content: Union[str, bool, int, list[str]]

    def __init__(self,
                 content: Union[str, bool, int, list[str]]) -> None:
        """Initialize this answer with content <content>
        >>> answer = Answer(True)
        """
        self.content = content

    def is_valid(self, question: Question) -> bool:
        """Return True iff this answer is a valid answer to <question>"""
        return question.validate_answer(self)


class Survey:
    """A survey containing questions as well as criteria and weights used to
    evaluate the quality of a group based on their answers to the survey
    questions.

    === Private Attributes ===
    _questions: a dictionary mapping a question's id to the question itself
    _criteria: a dictionary mapping a question's id to its associated criterion
    _weights: a dictionary mapping a question's id to a weight -- an integer
              representing the importance of this criteria.
    _default_criterion: The default criterion for this survey; used to evaluate
             the quality of a question based if the question doesn't already
             have an associated criteria
    _default_weight: The default weight for this survey; 1, used to evaluate the
            weight of the question should question not already have an assigned
            weight
    === Representation Invariants ===
    No two questions on this survey have the same id
    Each key in _questions equals the id attribute of its value
    The dictionaries _questions, _criteria, and _weights all have the same keys
    Each value in _weights is greater than 0

    NOTE: The weights associated with the questions in a survey do NOT have to
          sum up to any particular amount.
    """
    _questions: dict[int, Question]
    _criteria: dict[int, Criterion]
    _weights: dict[int, int]
    _default_criterion: HomogeneousCriterion
    _default_weight: int

    def __init__(self, questions: list[Question]) -> None:
        """Initialize a new survey that contains every question in <questions>.

        This new survey should use a HomogeneousCriterion as a default criterion
        and should use 1 as a default weight.
        """
        self._questions = {}
        self._criteria = {}
        self._weights = {}
        self._default_criterion = HomogeneousCriterion()
        self._default_weight = 1

        for question in questions:
            self._questions[question.id] = question
            self._criteria[question.id] = self._default_criterion
            self._weights[question.id] = self._default_weight

    def __len__(self) -> int:
        """Return the number of questions in this survey """
        return len(self._questions)

    def __contains__(self, question: Question) -> bool:
        """Return True iff there is a question in this survey with the same
        id as <question>.
        """
        if not isinstance(question, Question):
            return False
        return question.id in self._questions

    def __str__(self) -> str:
        """Return a string containing the string representation of all
        questions in this survey.

        You can choose the precise format of this string.
        """
        return f'Questions: {0}'.format(self.get_questions())

    def get_questions(self) -> list[Question]:
        """Return a list of all questions in this survey """
        question_list = []
        for q in self._questions:
            question_list.append(self._questions[q])
        return question_list

    def _get_criterion(self, question: Question) -> Criterion:
        """Return the criterion associated with <question> in this survey.

        Preconditions:
            - <question>.id occurs in this survey
        """
        if question.id not in self._criteria:
            return self._default_criterion
        return self._criteria[question.id]

    def _get_weight(self, question: Question) -> int:
        """Return the weight associated with <question> in this survey.

        Preconditions:
            - <question>.id occurs in this survey
        """
        if question.id not in self._weights:
            return self._default_weight
        return self._weights[question.id]

    def set_weight(self, weight: int, question: Question) -> bool:
        """Set the weight associated with <question> to <weight> and
        return True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.
        """
        if question.id not in self._questions:
            return False
        else:
            self._weights[question.id] = weight
            return True

    def set_criterion(self, criterion: Criterion, question: Question) -> bool:
        """Set the criterion associated with <question> to <criterion> and
        return True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.
        """
        if question.id not in self._questions:
            return False
        else:
            self._criteria[question.id] = criterion
            return True

    def score_students(self, students: list[Student]) -> float:
        """Return a quality score for <students> calculated based on their
        answers to the questions in this survey, and the associated criterion
        and weight for each question.

        The score is determined using the following algorithm:
        1. For each question in this survey, find the question's associated
           criterion (do we want homogeneous answers, for instance), weight,
           and <students> answers to the question. Use the score_answers method
           for its criterion to calculate how well the <students> answers
           satisfy the criterion. Multiply this quality score by the question's
           weight.
        2. Find the average of all quality scores from step 1.

        This method should NOT throw an InvalidAnswerError. If one occurs
        during the execution of this method or if there are no questions in
        <self>, return zero.

        Preconditions:
            - All students in <students> have an answer to all questions in this
            survey
            - len(students) > 0
        """
        score = 0
        # no questions in <self>
        if len(self._questions) == 0:
            return 0.0

        for question_id, question in self._questions.items():
            # get list of student answers for the question
            student_answers = []
            for student in students:
                # if InvalidAnswerError is raised, return 0
                if (not student.get_answer(question).is_valid(question)
                        or student.get_answer(question) == InvalidAnswerError):
                    return 0.0
                # since InvalidAnswerError isn't raised,
                # get the list of student answers to the question
                student_answers.append(student.get_answer(question))
            # Apply score algorithm
            score += self._criteria[question_id].score_answers(
                question, student_answers) * self._weights[question_id]
        # Get average of all quality score
        return score / len(self._questions)

    def score_grouping(self, grouping: Grouping) -> float:
        """Return a score for <grouping> calculated based on the answers of
        each student in each group in <grouping> to the questions in <self>.

        If there are no groups in <grouping> return 0.0. Otherwise, the score
        is determined using the following algorithm:
        1. For each group in <grouping>, calculate the score for the members of
           this based on their answers to the questions in this survey.
        2. Return the average of all the scores calculated in step 1.

        Preconditions:
            - All students in the groups in <grouping> have an answer to
              all questions in this survey
        """
        score = 0
        if len(grouping.get_groups()) == 0:
            return 0.0
        else:
            for group in grouping.get_groups():
                score += self.score_students(group.get_members())
        return score / len(grouping.get_groups())


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'criterion',
                                                  'course',
                                                  'grouper'],
                                'disable': ['E9992']})
