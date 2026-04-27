from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('placements', '0002_placementpost_min_cgpa'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlacementRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=200)),
                ('role_type', models.CharField(choices=[('fulltime', 'Full Time'), ('internship', 'Internship'), ('parttime', 'Part Time')], default='fulltime', max_length=20)),
                ('placement_status', models.CharField(choices=[('placed', 'Placed'), ('internship', 'Internship'), ('ppo', 'PPO')], default='placed', max_length=20)),
                ('placement_year', models.PositiveIntegerField()),
                ('branch', models.CharField(blank=True, choices=[('CSE', 'Computer Science & Engineering'), ('ECE', 'Electronics & Communication Engineering'), ('EEE', 'Electrical & Electronics Engineering'), ('ME', 'Mechanical Engineering'), ('CE', 'Civil Engineering'), ('IT', 'Information Technology'), ('CHE', 'Chemical Engineering'), ('BT', 'Biotechnology'), ('OTHER', 'Other')], max_length=10)),
                ('package_lpa', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('package_display', models.CharField(blank=True, help_text='e.g. 12 LPA or 35K/month', max_length=100)),
                ('location', models.CharField(blank=True, max_length=150)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('placement_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='placement_records', to='placements.placementpost')),
                ('recorded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recorded_placements', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(limit_choices_to={'user_type': 'student'}, on_delete=django.db.models.deletion.CASCADE, related_name='placement_records', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-placement_year', 'company_name', 'student__username'],
            },
        ),
    ]
