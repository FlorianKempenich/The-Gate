import re
from thegate.domain.utilities import check_not_none

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class LetsencryptRegistrationValidator:

    def is_valid(self, email, *, agree_tos):
        check_not_none(email)
        def _valid(email):
            return EMAIL_REGEX.match(email)

        if not agree_tos or not _valid(email):
            return False

        return True
