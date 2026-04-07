import os
import django
import sys

# Set up Django environment
sys.path.append('c:\\Users\\prash\\OneDrive\\Desktop\\collegeconnect')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusconnect.settings')
django.setup()

from placements.forms import PlacementPostForm
from accounts.models import UserProfile

def test_form_validation():
    # Attempt to validate a form with DD-MM-YYYY date
    data = {
        'company_name': 'Test Company',
        'role': 'Test Role',
        'role_type': 'fulltime',
        'ctc': '10 LPA',
        'eligibility_criteria': 'All good',
        'deadline': '15-10-2026',  # DD-MM-YYYY
        'application_link': 'https://google.com',
        'description': 'Test description'
    }
    
    form = PlacementPostForm(data=data)
    if form.is_valid():
        print("Form is valid with DD-MM-YYYY!")
    else:
        print("Form is INVALID with DD-MM-YYYY")
        print("Errors:", form.errors.as_data())

    # Test with YYYY-MM-DD
    data['deadline'] = '2026-10-15'
    form2 = PlacementPostForm(data=data)
    if form2.is_valid():
        print("Form is valid with YYYY-MM-DD!")
    else:
        print("Form is INVALID with YYYY-MM-DD")
        print("Errors:", form2.errors.as_data())

if __name__ == "__main__":
    test_form_validation()
