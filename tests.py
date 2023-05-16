# TODO: Add the test cases that you'll be submitting to this file!
#       Make sure your test cases are all named starting with
#       test_ and that they have unique names.

# You may need to import pytest in order to run your tests.
# You are free to import hypothesis and use hypothesis for testing.
# This file will not be graded for style with PythonTA

import course
import survey
import criterion
import grouper
import pytest

from criterion import InvalidAnswerError


@pytest.fixture
def empty_course() -> course.Course:
    return course.Course('csc148')


@pytest.fixture
def students() -> list[course.Student]:
    return [course.Student(1, 'Zoro'),
            course.Student(2, 'Aaron'),
            course.Student(3, 'Gertrude'),
            course.Student(4, 'Yvette')]


@pytest.fixture
def alpha_grouping(students_with_answers) -> grouper.Grouping:
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[0],
                                      students_with_answers[3]]))
    grouping.add_group(grouper.Group([students_with_answers[1],
                                      students_with_answers[2]]))
    return grouping


@pytest.fixture
def greedy_grouping(students_with_answers) -> grouper.Grouping:
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[1],
                                      students_with_answers[3]]))
    grouping.add_group(grouper.Group([students_with_answers[0],
                                      students_with_answers[2]]))
    return grouping


@pytest.fixture
def sa_grouping(students_with_answers) -> grouper.Grouping:
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[2],
                                      students_with_answers[0]]))
    grouping.add_group(grouper.Group([students_with_answers[3],
                                      students_with_answers[1]]))
    return grouping


@pytest.fixture
def questions() -> list[survey.Question]:
    return [survey.MultipleChoiceQuestion(1, 'why?', ['a', 'b']),
            survey.NumericQuestion(2, 'what?', -2, 4),
            survey.YesNoQuestion(3, 'really?'),
            survey.CheckboxQuestion(4, 'how?', ['a', 'b', 'c'])]


@pytest.fixture
def criteria(answers) -> list[criterion.Criterion]:
    return [criterion.HomogeneousCriterion(),
            criterion.HeterogeneousCriterion(),
            criterion.LonelyMemberCriterion(),
            criterion.HomogeneousCriterion()]


@pytest.fixture()
def weights() -> list[int]:
    return [2, 5, 7, 4]


@pytest.fixture
def answers() -> list[list[survey.Answer]]:
    return [[survey.Answer('a'), survey.Answer('b'),
             survey.Answer('a'), survey.Answer('b')],
            [survey.Answer(0), survey.Answer(4),
             survey.Answer(-1), survey.Answer(1)],
            [survey.Answer(True), survey.Answer(False),
             survey.Answer(True), survey.Answer(True)],
            [survey.Answer(['a', 'b']), survey.Answer(['a', 'b']),
             survey.Answer(['a']), survey.Answer(['b'])]]


@pytest.fixture
def students_with_answers(students, questions, answers) -> list[course.Student]:
    for i, student in enumerate(students):
        for j, question in enumerate(questions):
            student.set_answer(question, answers[j][i])
    return students


@pytest.fixture
def course_with_students(empty_course, students) -> course.Course:
    empty_course.enroll_students(students)
    return empty_course


@pytest.fixture
def course_with_students_with_answers(empty_course,
                                      students_with_answers) -> course.Course:
    empty_course.enroll_students(students_with_answers)
    return empty_course


@pytest.fixture
def survey_(questions, criteria, weights) -> survey.Survey:
    s = survey.Survey(questions)
    for i, question in enumerate(questions):
        s.set_weight(weights[i], question)
        s.set_criterion(criteria[i], question)
    return s


@pytest.fixture
def group(students) -> grouper.Group:
    return grouper.Group(students)


def get_member_ids(grouping: grouper.Grouping) -> set[frozenset[int]]:
    member_ids = set()
    for group in grouping.get_groups():
        ids = []
        for member in group.get_members():
            ids.append(member.id)
        member_ids.add(frozenset(ids))
    return member_ids


def compare_groupings(grouping1: grouper.Grouping,
                      grouping2: grouper.Grouping) -> None:
    assert get_member_ids(grouping1) == get_member_ids(grouping2)


###############################################################################
# Task 2 Test cases: Student class
###############################################################################
class TestStudent:
    # Test cases for __init__
    def test__init__(self) -> None:
        diane = course.Student(1, 'Diane')
        assert diane.id == 1
        assert diane.name == 'Diane'

    # Test cases for __str__
    def test__str__(self) -> None:
        diane = course.Student(1, 'Diane')
        assert diane.__str__() == 'Diane'

    # Test cases for has_answer
    def test_has_answer_and_is_valid(self, questions) -> None:
        diane = course.Student(1, 'Diane')
        diane.set_answer(questions[1], survey.Answer(0))
        assert diane.has_answer(questions[1]) is True

    def test_has_wrong_answer(self, questions) -> None:
        tom = course.Student(2, 'Tom')
        tom.set_answer(questions[1], survey.Answer('n'))
        assert tom.has_answer(questions[1]) is False

    def test_has_no_answer(self, questions) -> None:
        sophia = course.Student(3, 'Sophia')
        assert sophia.has_answer(questions[1]) is False

    # Test cases for set_answer
    def test_set_answer(self, questions) -> None:
        diane = course.Student(1, 'Diane')
        diane.set_answer(questions[1], survey.Answer(0))
        assert diane.get_answer(questions[1]).content == 0

    def test_set_wrong_answer(self, questions) -> None:
        tom = course.Student(2, 'Tom')
        tom.set_answer(questions[2], survey.Answer('a'))
        assert tom.get_answer(questions[2]).content == 'a'

    # Test cases for get_answer
    def test_get_answer(self, questions) -> None:
        diane = course.Student(1, 'Diane')
        assert diane.get_answer(questions[1]) is None
        diane.set_answer(questions[1], survey.Answer(0))
        assert diane.get_answer(questions[1]).content == 0

    def test_get_answer_for_non_existing_question(self, questions) -> None:
        diane = course.Student(1, 'Diane')
        for q in questions:
            if q not in questions:
                diane.set_answer(q, survey.Answer(0))
                assert diane.get_answer(q).content == 0


###############################################################################
# Task 3 Test cases: Course class
###############################################################################
class TestCourse:
    """Test cases for the class Course in course.py"""

    # Test cases for __init__
    def test__init__(self) -> None:
        """Test the Course class initializer"""
        csc148 = course.Course('CSC148')
        assert csc148.name == 'CSC148'

    # Test cases for enroll_students
    def test_enroll_students(self) -> None:
        csc148 = course.Course("CSC148")
        student_list = [course.Student(1, "Diane"),
                        course.Student(2, "Tom")]
        csc148.enroll_students(student_list)
        assert csc148.students == student_list
        assert len(csc148.students) == 2

    def test_enroll_no_students(self) -> None:
        csc165 = course.Course("CSC148")
        student_list = []
        csc165.enroll_students(student_list)
        assert csc165.students == []
        assert len(csc165.students) == 0

    # Test cases for all_answered
    def test_all_answered(self, answers, questions) -> None:
        csc148 = course.Course('CSC148')
        list_of_questions = survey.Survey(questions)
        student_list = [course.Student(1, 'Diane'),
                        course.Student(2, 'Tom'),
                        course.Student(3, 'Sophia')]
        csc148.enroll_students(student_list)
        assert csc148.all_answered(list_of_questions) is False

    # Test cases for get_students
    def test_get_students(self) -> None:
        csc148 = course.Course('CSC148')
        students = [course.Student(1, 'Diane'),
                    course.Student(2, 'Tom'),
                    course.Student(3, 'Sophia')]
        csc148.enroll_students(students)
        assert isinstance(csc148.get_students(), tuple)


###############################################################################
# Task 4 Test cases: Question classes
###############################################################################
class TestYesNoQuestion:
    """Test cases for the class YesNoQuestion in survey.py"""

    def test_validate_answer(self, questions) -> None:
        assert questions[2].validate_answer(survey.Answer(True)) is True

    def test_get_similarity(self) -> None:
        question = survey.YesNoQuestion(1, 'Good day?')
        answer1 = survey.Answer(True)
        answer2 = survey.Answer(False)
        assert question.get_similarity(answer1, answer2) == 0.0
        answer2 = survey.Answer(True)
        assert question.get_similarity(answer1, answer2) == 1.0


###############################################################################
# Task 5 Test cases: Answer class
###############################################################################
class TestAnswer:
    """Test cases for the class Answer in survey.py"""

    def test_is_valid(self, questions) -> None:
        multiple_choice_ans = survey.Answer("a")
        checkbox_choice_ans = survey.Answer(["a", "b"])
        yes_no_ans = survey.Answer(True)
        numeric_ans = survey.Answer(1)

        assert multiple_choice_ans.is_valid(questions[0]) is True
        assert multiple_choice_ans.is_valid(questions[1]) is False
        assert checkbox_choice_ans.is_valid(questions[3]) is True
        assert checkbox_choice_ans.is_valid(questions[2]) is False
        assert yes_no_ans.is_valid(questions[1]) is True
        assert yes_no_ans.is_valid(questions[0]) is False
        assert numeric_ans.is_valid(questions[2]) is False
        assert numeric_ans.is_valid(questions[1]) is True


###############################################################################
# Task 6 Test cases: Criterion classes
###############################################################################
class TestHomogeneousCriterion:
    """Test cases for the class HomogeneousCriterion in criterion.py"""

    def test_score_homogeneous(self) -> None:
        q = survey.NumericQuestion(1, "choose", -2, 4)
        answer1 = survey.Answer(-2)
        answer2 = survey.Answer(4)
        c = criterion.HomogeneousCriterion()
        assert c.score_answers(q, [answer1, answer2]) == 0.0
        assert c.score_answers(q, [answer1]) == 1.0
        assert c.score_answers(q, [answer2]) == 1.0


###############################################################################
# Task 7 Test cases: Group class
###############################################################################
class TestGroup:
    """Test cases for the class Group in grouper.py"""

    def test__len__(self, students) -> None:
        csc_148_rsg = grouper.Group(students)
        assert len(csc_148_rsg) == 4

    def test__does_not__contains__(self, students) -> None:
        csc_148_rsg = grouper.Group(students)
        michelle = course.Student(6, 'Michelle')
        assert michelle not in csc_148_rsg

    def test__does__contains__(self, students) -> None:
        csc_148_rsg = grouper.Group(students)
        assert students[0] and students[1] and students[2] and students[3] \
               in csc_148_rsg

    def test_get_members(self, students) -> None:
        csc_148_rsg = grouper.Group(students)
        csc_165_rsg = csc_148_rsg.get_members()
        assert id(csc_148_rsg) != id(csc_165_rsg)


###############################################################################
# Task 8 Test cases: Grouping class
###############################################################################
class TestGrouping:
    """Test cases for the class Grouping in grouper.py"""

    def test_add_group(self) -> None:
        students = [course.Student(1, 'Diane'),
                    course.Student(2, 'Tom'),
                    course.Student(3, 'Sophia')]
        group = grouper.Group(students)
        g = grouper.Grouping()
        g.add_group(group)
        assert group in g.get_groups()
        assert group.__len__() == 3


###############################################################################
# Task 9 Test cases: Survey class
###############################################################################
class TestSurvey:
    """Test cases for the class Survey in survey.py"""

    def test_get_questions(self, questions) -> None:
        list_of_question = survey.Survey(questions)
        assert list_of_question.get_questions() == questions

    def test_get_criterion(self, questions) -> None:
        list_of_questions = survey.Survey(questions)
        for q in questions:
            if q not in questions:
                assert False
            assert isinstance(list_of_questions._get_criterion(q),
                              criterion.HomogeneousCriterion)
        assert isinstance(list_of_questions._get_criterion(q),
                          criterion.HomogeneousCriterion)

    def test_get_weight(self, questions) -> None:
        list_of_questions = survey.Survey(questions)
        for q in questions:
            if q not in questions:
                assert list_of_questions.set_weight(1, q)
            assert list_of_questions._get_weight(q) == 1  # default weight

    def test_set_weight(self, questions) -> None:
        list_of_questions = survey.Survey(questions)
        for q in questions:
            if q not in questions:
                assert list_of_questions.set_weight(1, q)
            list_of_questions.set_weight(1, q)
        for weight in questions:
            assert list_of_questions._get_weight(weight) == 1

    def test_set_criterion(self, questions) -> None:
        list_of_questions = survey.Survey(questions)
        for q in questions:
            if q not in questions:
                assert False
            list_of_questions.set_criterion(criterion.HomogeneousCriterion(), q)
        for f in questions:
            assert isinstance(list_of_questions._get_criterion(f),
                              criterion.HomogeneousCriterion)

    def test_score_students(self, questions, students_with_answers) -> None:
        list_of_questions = survey.Survey(questions)
        score = list_of_questions.score_students(students_with_answers)
        assert round(score, 2) == 0.47

    def test_score_grouping(self, questions) -> None:
        list_of_questions = survey.Survey(questions)
        diane = course.Student(1, "Diane")
        tom = course.Student(2, "Tom")
        sophia = course.Student(3, "Sophia")
        students = [diane, tom, sophia]
        group = grouper.Group(students)
        g = grouper.Grouping()
        g.add_group(group)
        score = list_of_questions.score_grouping(g)
        assert round(score, 2) == 3


###############################################################################
# Task 10 Test cases: Grouper classes
###############################################################################
class TestAlphaGrouper:
    """Test case for the class AlphaGrouping in grouper.py"""

    def test_alpha_grouper(self) -> None:
        alpha_grouper = grouper.AlphaGrouper(3)
        students = [course.Student(1, 'Diane'),
                    course.Student(2, 'Tom'),
                    course.Student(3, 'Sophia')]
        csc148 = course.Course('CSC148')
        csc148.enroll_students(students)
        question = survey.CheckboxQuestion(1, "Good day?", ['a', 'b', 'c'])
        sur = survey.Survey([question])
        group = grouper.Group(students)
        # Check Diane is first
        assert (
                alpha_grouper.make_grouping(csc148, sur).get_groups(

                )[0].get_members()[0] == group.get_members()[0])
        # Check Sophia is second
        assert (
                alpha_grouper.make_grouping(csc148, sur).get_groups(

                )[0].get_members()[1] == group.get_members()[2])
        # Check Tom is last
        assert (
                alpha_grouper.make_grouping(csc148, sur).get_groups(

                )[0].get_members()[2] == group.get_members()[1])


class TestGreedyGrouper:
    """Test case for the class GreedyGrouping in grouper.py"""

    # def test_make_grouping_greedy(self):
    #
