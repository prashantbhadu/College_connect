# This import ensures the Celery app is always loaded when Django starts,
# so that shared_task decorators across all apps use the correct app instance.
from .celery import app as celery_app

__all__ = ('celery_app',)
