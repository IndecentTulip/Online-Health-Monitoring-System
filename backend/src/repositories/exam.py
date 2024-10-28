class Exam:
    def __init__(self, exam_id: int, patient_id: int, content: str):
        self.exam_id = exam_id
        self.patient_id = patient_id
        self.content = content

    def prescribe_exam(self, exam: 'Exam'):
        # Implementation for prescribing an exam
        pass

    def remove_exam(self, exam_id: int):
        # Implementation for removing an exam
        pass

    def return_list_of_exams(self, email: str):
        # Implementation for returning a list of exams based on email
        pass

