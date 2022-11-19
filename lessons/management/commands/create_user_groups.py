from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from lessons.helpers.helper_functions import USER_GROUPS

"""
Class representing a command to create user groups.
Used to create different user level authorisations
"""
class Command(BaseCommand):
    def __init__(self):
        super().__init__()
    
    """
    A method for handling user group creation
    """
    def handle(self, *args, **options):
        for group in self.USER_GROUPS:
            got_group, created_group = Group.objects.get_or_create(name=group)
            for authorization in self.USER_GROUPS[group]:
                for permission_index, permission_name in enumerate(self.USER_GROUPS[group][authorization]):
                    permission_codename = permission_name + "_" + authorization._meta.model_name
                    try:
                        permission = Permission.objects.get(codename=permission_codename)
                        got_group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        print("Tried to add a non-exisiting permission when creating user groups!")