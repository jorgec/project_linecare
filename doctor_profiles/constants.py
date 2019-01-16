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

QUEUE_INACTIVE = (
    'pending', 'queueing'
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
    'finishing': '',
    'done': {
        'message': 'Thank you!',
        'color': 'success'
    },
    'cancelled_by_patient': '',
    'cancelled_by_doctor': {
        'message': 'Your appointment has been cancelled by the doctor',
        'color': 'danger'
    },
    'rescheduled_by_patient': '',
    'rescheduled_by_doctor': '',
}


APPOINTMENT_TYPES = (
    ('checkup', 'Check Up'),
    ('followup', 'Follow Up'),
    ('lab_result', 'Lab Result'),
    ('consultation', 'Consultation'),
)