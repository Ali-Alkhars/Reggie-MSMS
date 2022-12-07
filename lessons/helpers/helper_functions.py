from lessons.models import Invoice, User
from django.contrib.auth.models import Group
from django.utils import timezone

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

"""
A helper function which checks the user group of the user with the given id
and return the group's name as string
"""
def get_user_group_from_id(user_id):
    user = User.objects.get(id=user_id)
    if not user.groups.exists():
        raise Exception("User groups do not exist. Try running 'python3 manage.py create_user_groups'")

    for key in USER_GROUPS.keys():
        if key == user.groups.all()[0].name:
            return key

    return ''

"""
A helper function which assigns the user given (as user id) to the 
director user group
"""
def promote_admin_to_director(user_id):
    user = User.objects.get(id=user_id)

    # Remove the user from the admin group
    admin_group = Group.objects.get(name='admin') 
    admin_group.user_set.remove(user)

    # Add the user to the director group
    director_group = Group.objects.get(name='director') 
    director_group.user_set.add(user)

"""
A helper function which deletes the given user (as user id)
"""
def delete_user(user_id):
    user = User.objects.get(id=user_id)
    user.delete()

"""
A helper function which returns the given user's (as user id)
full name
"""
def get_user_full_name(user_id):
    user = User.objects.get(id=user_id)
    return f"{user.first_name} {user.last_name}"

"""
A helper function that checks if the user is student or not
"""
def userOrAdmin(request):
    if (get_user_group(request) == 'student'):
        return True
    return False

"""
A helper function which records a payment made by a student
"""
def record_payment(paid, invoice):
    invoice.unpaid -= paid
    invoice.update_date = timezone.now()
    invoice.save()

"""
A helper function which creates an invoice from a given student and lesson
"""
def create_invoice(lesson, student):
    lesson_price = lesson.numberOfLessons * lesson.DurationOfLesson

    invoice = Invoice.objects.create (
            reference= f"{student.id}-{lesson.id}",
            price= lesson_price,
            unpaid= lesson_price,
            creation_date= timezone.now(),
            update_date= timezone.now(),
            student= student,
            lesson= lesson
    )
    return invoice
