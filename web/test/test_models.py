import pytest

from bfex.models import Faculty

class TestFaculty(object):
    def test_create(self):
        prof = Faculty()
        prof.name = "name"
        prof.email = "email@ualberta.ca"
        prof.faculty_id = 1
        prof.department = "cs"

        assert prof.department == "cs"

        # prof.save()
