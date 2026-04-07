import os
import django
import sys

# Set up Django environment
sys.path.append('c:\\Users\\prash\\OneDrive\\Desktop\\collegeconnect')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusconnect.settings')
django.setup()

from placements.forms import PlacementPostForm

def test_form_validation():
    data = {
        'company_name': 'Test Company',
        'role': 'Test Role',
        'role_type': 'fulltime',
        'ctc': '10 LPA',
        'eligibility_criteria': 'All good',
        'deadline': '15-10-2026',
        'application_link': 'https://google.com',
        'description': 'Test description'
    }
    
    form = PlacementPostForm(data=data)
    print(f"Result for 15-10-2026: {'VALID' if form.is_valid() else 'INVALID'}")
    if not form.is_valid():
        print(f"Errors: {form.errors}")

if __name__ == "__main__":
    test_form_validation()
