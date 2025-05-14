def has_perm(user, name, criteria_type):
    """
    Checks if the user has the given permission by name and criteria_type.
    """
    return user.role.criteria.filter(name=name, criteria_type=criteria_type).exists()


def hr_criteria_add_perm(user):
    return has_perm(user, 'HR', 'add')

def hr_criteria_edit_perm(user):
    return has_perm(user, 'HR', 'edit')

def hr_criteria_delete_perm(user):
    return has_perm(user, 'HR', 'delete')

def hr_criteria_view_perm(user):
    return has_perm(user, 'HR', 'view')



def form_criteria_add_perm(user):
    return has_perm(user, 'Form', 'add')

def form_criteria_edit_perm(user):
    return has_perm(user, 'Form', 'edit')

def form_criteria_delete_perm(user):
    return has_perm(user, 'Form', 'delete')

def form_criteria_view_perm(user):
    return has_perm(user, 'Form', 'view')



def tasks_criteria_add_perm(user):
    return has_perm(user, 'Tasks', 'add')

def tasks_criteria_edit_perm(user):
    return has_perm(user, 'Tasks', 'edit')

def tasks_criteria_delete_perm(user):
    return has_perm(user, 'Tasks', 'delete')

def tasks_criteria_view_perm(user):
    return has_perm(user, 'Tasks', 'view')



def data_criteria_add_perm(user):
    return has_perm(user, 'Data', 'add')

def data_criteria_edit_perm(user):
    return has_perm(user, 'Data', 'edit')

def data_criteria_delete_perm(user):
    return has_perm(user, 'Data', 'delete')

def data_criteria_view_perm(user):
    return has_perm(user, 'Data', 'view')



def users_criteria_add_perm(user):
    return has_perm(user, 'Users', 'add')

def users_criteria_edit_perm(user):
    return has_perm(user, 'Users', 'edit')

def users_criteria_delete_perm(user):
    return has_perm(user, 'Users', 'delete')

def users_criteria_view_perm(user):
    return has_perm(user, 'Users', 'view')



def documents_criteria_add_perm(user):
    return has_perm(user, 'Documents', 'add')

def documents_criteria_edit_perm(user):
    return has_perm(user, 'Documents', 'edit')

def documents_criteria_delete_perm(user):
    return has_perm(user, 'Documents', 'delete')

def documents_criteria_view_perm(user):
    return has_perm(user, 'Documents', 'view')



def finance_criteria_add_perm(user):
    return has_perm(user, 'Finance', 'add')

def finance_criteria_edit_perm(user):
    return has_perm(user, 'Finance', 'edit')

def finance_criteria_delete_perm(user):
    return has_perm(user, 'Finance', 'delete')

def finance_criteria_view_perm(user):
    return has_perm(user, 'Finance', 'view')
