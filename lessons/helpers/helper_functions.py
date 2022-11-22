from lessons.models import User

"""A dictionary of user groups, giving each group their set of permissions"""
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

"""
A helper function which checks the user group of the user who made the request
and return the group's name as string
"""
def get_user_group(request):
    if not request.user.groups.exists():
        raise Exception("User groups do not exist. Try running 'python3 manage.py create_user_groups'")

    for key in USER_GROUPS.keys():
        if key == request.user.groups.all()[0].name:
            return key

    return ''