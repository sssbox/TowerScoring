from celery.decorators import task

import time

@task()
def test_task():
    for i in range(1,60):
        print i
        time.sleep(1)