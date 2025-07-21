import os
import subprocess
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv

# Load Git identity from .env
load_dotenv()
GIT_USER_NAME = os.getenv("GIT_USER_NAME")
GIT_USER_EMAIL = os.getenv("GIT_USER_EMAIL")

# Run a shell command
def run_command(command, env=None):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print("❌ Error:", result.stderr.strip())
    return result.stdout.strip()

# Build environment with git identity and commit datetime
def build_git_env(commit_datetime):
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = commit_datetime
    env["GIT_COMMITTER_DATE"] = commit_datetime
    env["GIT_AUTHOR_NAME"] = GIT_USER_NAME
    env["GIT_COMMITTER_NAME"] = GIT_USER_NAME
    env["GIT_AUTHOR_EMAIL"] = GIT_USER_EMAIL
    env["GIT_COMMITTER_EMAIL"] = GIT_USER_EMAIL
    return env

# Create a single commit at a specific datetime
def make_commit(commit_datetime):
    with open("activity.txt", "a") as f:
        f.write(f"Commit on {commit_datetime}\n")

    run_command("git add activity.txt")
    env = build_git_env(commit_datetime)
    run_command(f'git commit -m "Backdated commit on {commit_datetime}"', env=env)

# Generate multiple commits across a date range
def generate_commits(start_date, end_date, default_commits=10, special_commits=25, special_days=None):
    if special_days is None:
        special_days = set()

    current = start_date
    while current <= end_date:
        month_day = current.strftime("%m-%d")
        is_special = month_day in special_days
        num_commits = random.randint(default_commits, special_commits) if is_special else default_commits

        for i in range(num_commits):
            hour = 8 + (i % 10)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_time = current.replace(hour=hour, minute=minute, second=second)
            make_commit(commit_time.isoformat())

        print(f"{'⭐️' if is_special else '✅'} {num_commits} commits on {current.date()}")
        current += timedelta(days=1)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    # Change to your desired start date
    start_date = datetime(2025, 6, 5)
    end_date = datetime.today()

    special_dates = {
        "06-01",  # Just a sample special day
        "12-25",  # Christmas
    }

    generate_commits(
        start_date=start_date,
        end_date=end_date,
        default_commits=10,
        special_commits=25,
        special_days=special_dates
    )

    # Final push to GitHub
    run_command("git push origin main")  # Change 'main' if your branch is different