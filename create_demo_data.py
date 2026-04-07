import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusconnect.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from accounts.models import UserProfile, Skill
from placements.models import PlacementPost
from alumni.models import AlumniPost
from django.utils import timezone
from datetime import timedelta

def create_demo_data():
    print("Creating demo data...")
    
    # 1. Create Skills
    skills = ['Python', 'Django', 'React', 'Java', 'SQL', 'AWS', 'Docker', 'Machine Learning', 'Data Analysis']
    skill_objs = {}
    for s in skills:
        skill_objs[s], _ = Skill.objects.get_or_create(name=s)
        
    print(f"Created {len(skills)} skills")
    
    # 2. Create Admin User
    if not UserProfile.objects.filter(username='admin').exists():
        admin = UserProfile.objects.create_superuser(
            username='admin',
            email='admin@collegeconnect.com',
            password='admin@123',
        )
        print("Created admin user")
        
    # 3. Create Demo Student
    if not UserProfile.objects.filter(username='student1').exists():
        student = UserProfile.objects.create(
            username='student1',
            first_name='Alex',
            last_name='Johnson',
            email='student1@collegeconnect.com',
            user_type='student',
            branch='CSE',
            semester=6,
            bio='Aspiring software engineer passionate about backend development.',
            is_verified=True,
            profile_completed=True,
            password=make_password('Test@1234')
        )
        student.skills.add(skill_objs['Python'], skill_objs['Django'], skill_objs['SQL'])
        print("Created student1 user")
        
    # 4. Create Demo Alumni
    if not UserProfile.objects.filter(username='alumni1').exists():
        alumni = UserProfile.objects.create(
            username='alumni1',
            first_name='Sarah',
            last_name='Williams',
            email='alumni1@collegeconnect.com',
            user_type='alumni',
            branch='CSE',
            graduation_year=2021,
            current_company='Google',
            current_role='Software Engineer II',
            bio='Backend engineer at Google. Happy to help current students with interview prep.',
            is_verified=True,
            profile_completed=True,
            linkedin_url='https://linkedin.com/in/#',
            password=make_password('Test@1234')
        )
        alumni.skills.add(skill_objs['Python'], skill_objs['Java'], skill_objs['AWS'])
        print("Created alumni1 user")
    else:
        alumni = UserProfile.objects.get(username='alumni1')

    # 5. Create Placements
    if PlacementPost.objects.count() == 0:
        PlacementPost.objects.create(
            company_name='Google',
            role='Software Engineering Intern',
            role_type='internship',
            ctc='1,00,000 / month',
            eligibility_criteria='Pursuing B.Tech/M.Tech in CS or related field.\nStrong knowledge of Data Structures and Algorithms.',
            description='As a Software Engineering Intern, you will work on core products, collaborating with experienced engineers.',
            deadline=timezone.now() + timedelta(days=15),
            posted_by=alumni,
            is_active=True
        )
        PlacementPost.objects.create(
            company_name='Amazon',
            role='SDE-1',
            role_type='fulltime',
            ctc='24 LPA',
            eligibility_criteria='B.Tech CSE/IT with 8.0+ CGPA.',
            description='Amazon is hiring SDE-1s for the AWS team. Expect challenging problems in distributed systems.',
            deadline=timezone.now() + timedelta(days=3),
            posted_by=alumni,
            is_active=True
        )
        print("Created placement posts")

    # 6. Create Alumni Posts
    if AlumniPost.objects.count() == 0:
        AlumniPost.objects.create(
            title='How I cracked Google campus placements',
            content='It all comes down to consistency. I solved 2 LeetCode problems every day for 6 months. Focus on Graphs, DP, and Trees. Also, do not ignore Core CS subjects like OS, DBMS, and Networks. Let me know if you need specific advice!',
            author=alumni,
            post_type='success',
            tags='google, interview, preparation'
        )
        print("Created alumni posts")

    print("\n✅ Demo data initialization complete!")
    print("Credentials:")
    print(" - Student: student1 / Test@1234")
    print(" - Alumni: alumni1 / Test@1234")
    print(" - Admin: admin / admin@123")

if __name__ == '__main__':
    create_demo_data()
