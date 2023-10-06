"""

Removed update check

"""

from ..utils import check_for_update


def check_for_update_function():
    pass


check_for_update.check_for_update = check_for_update_function
