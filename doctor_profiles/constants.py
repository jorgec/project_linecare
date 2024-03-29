QUEUE_DISPLAY_CODES = (
    'queueing',
    'pending',
    'in_progress',
    'finishing',
)

QUEUE_INACTIVE = (
    'pending',
)

QUEUE_ACTIVE = (
    'in_progress',
    'finishing',
)

QUEUE_WAITING = (
    'queueing',
)

QUEUE_CANCELLED_CODES = (
    'cancelled_by_patient',
    'cancelled_by_doctor',
    'rescheduled_by_patient',
    'rescheduled_by_doctor',
)

QUEUE_DONE_CODES = (
    'Done',
)


QUEUE_NOT_CANCELLED_CODES = (
    'pending',
    'queueing',
    'in_progress',
    'finishing',
    'done',
)

# lol
QUEUE_NOT_CANCELLED_BUT_NOT_DONE_CODES = (
    'pending',
    'queueing',
    'in_progress',
    'finishing',
)


QUEUE_STATUS_CODES = (
    ('pending', 'Pending'),
    ('queueing', 'Queueing'),
    ('in_progress', 'In Progress'),
    ('finishing', 'Finishing'),
    ('done', 'Done'),
    ('cancelled_by_patient', 'Cancelled by patient'),
    ('cancelled_by_doctor', 'Cancelled by doctor'),
    ('rescheduled_by_patient', 'Rescheduled by patient'),
    ('rescheduled_by_doctor', 'Rescheduled by doctor'),
)

QUEUE_STATUS_MESSAGES = {
    'pending': {
        'message': 'In inactive queue. Please signify your arrival.',
        'color': 'secondary'
    },
    'queueing': {
        'message': 'Added to active queue; please wait to be called.',
        'color': 'info'
    },
    'in_progress': {
        'message': 'Please come in',
        'color': 'success'
    },
    'finishing': {
        'message': 'Thank you!',
        'color': 'success'
    },
    'done': {
        'message': 'Thank you!',
        'color': 'success'
    },
    'cancelled_by_patient': {
        'message': 'Appointment cancelled by patient',
        'color': 'danger'
    },
    'cancelled_by_doctor': {
        'message': 'Your appointment has been cancelled by the doctor',
        'color': 'danger'
    },
    'rescheduled_by_patient': {
        'message': 'Appointment cancelled by patient',
        'color': 'danger'
    },
    'rescheduled_by_doctor': {
        'message': 'Your appointment has been rescheduled by the doctor',
        'color': 'warning'
    },
}


APPOINTMENT_TYPES = (
    ('checkup', 'Check Up'),
    ('followup', 'Follow Up'),
    ('lab_result', 'Lab Result'),
    ('consultation', 'Consultation'),
)

ANSWER_TYPES = (
    ('free_text', 'Free Text'),
    ('choices', 'Choices'),
    ('choices_with_free_answer', 'Choices with free answer')
)

ANSWER_SELECTION_TYPES = (
    ('single_answer', 'Single Answer'),
    ('multiple_answers', 'Multiple Answers'),
)

ANSWER_DATA_TYPES = (
    ('boolean', 'Boolean'),
    ('numeric', 'Numeric'),
    ('text', 'Text')
)

QUESTION_FLOW = (
    ('linear', 'Linear'),
    ('fork', 'Fork')
)

FORK_OPERATORS = (
    ('>', 'is greater than'),
    ('<', 'is less than'),
    ('>=', 'is greater than or equal to'),
    ('<=', 'is less than or equal to'),
    ('==', 'is equal to'),
    ('!-', 'not equal to')
)

QUESTIONNAIRE_RESTRICTION_CHOICES = (
    ('private', 'Private'), # accessible only to creator
    ('internal', 'Internal'), # accessible to doctors in same medical institution
    ('public', 'Public') # accessible to all doctors
)

QUESTIONNAIRE_HOOKS = (
    ('pre_appointment', 'Before the appointment'),
    ('post_appointment', 'After the appointment'),
    ('during_appointment', 'During the Appointment')
)
