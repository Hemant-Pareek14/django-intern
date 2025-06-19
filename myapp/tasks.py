from celery import shared_task

@shared_task
def sample_task():
    print("Task executed successfully!")
    return "Task executed successfully!"