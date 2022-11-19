from lessons.models import User

USER_GROUPS = {
        'student': {
            User: ['add', 'change', 'delete', 'view'],
        },
        'admin': {
            User: ['add', 'change', 'delete', 'view'],
        },
        'director': {
            User: ['add', 'change', 'delete', 'view'],
        }
    }