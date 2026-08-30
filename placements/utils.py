"""
placements/utils.py

Email notification logic has been moved to placements/tasks.py as a Celery task.
Threading was removed in favour of Celery for retries, durability, and observability.

This file is kept for any future placement-related utility helpers.
"""
