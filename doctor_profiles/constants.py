QUEUE_DISPLAY_CODES = (
    'Pending',
    'Queueing',
    'In Progress',
    'Finishing',
)

QUEUE_INACTIVE = (
    'Pending',
)

QUEUE_ACTIVE = (
    'In Progress',
    'Finishing',
)

QUEUE_WAITING = (
    'Queueing',
)

QUEUE_CANCELLED_CODES = (
    'Cancelled by patient',
    'Cancelled by doctor',
    'Rescheduled by patient',
    'Rescheduled by doctor',
)

QUEUE_DONE_CODES = (
    'Done',
)

QUEUE_STATUS_CODES = (
    ('Pending', 'Pending'),
    ('Queueing', 'Queueing'),
    ('In Progress', 'In Progress'),
    ('Finishing', 'Finishing'),
    ('Done', 'Done'),
    ('Cancelled by patient', 'Cancelled by patient'),
    ('Cancelled by doctor', 'Cancelled by doctor'),
    ('Rescheduled by patient', 'Rescheduled by patient'),
    ('Rescheduled by doctor', 'Rescheduled by doctor'),
)


APPOINTMENT_TYPES = (
    ('checkup', 'Check Up'),
    ('followup', 'Follow Up'),
    ('lab_result', 'Lab Result'),
)