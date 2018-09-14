import subprocess
from settings import ENGINE_PATH

def add_job(project_id, user_id, job_type):
    try:
        subprocess_str = ENGINE_PATH + str(project_id) + " " + str(user_id) + job_type
        subprocess.Popen(subprocess_str, shell=True)
    except Exception as e:
        raise e