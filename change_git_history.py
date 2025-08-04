import os
import subprocess
import random
from datetime import datetime, timedelta

# ✅ Set your correct repo path here
repo_path = r"D:\paul\Projects\healthcare-scheduling"

# ✅ The email you want to take over (target this author)
old_email = "realsiddheshko@gmail.com"

# ✅ Your identity
new_name = "CodeHelixor"
new_email = "j.virtualtour.ceo@gmail.com"


def modify_history():
    if not os.path.isdir(repo_path):
        raise NotADirectoryError(f"❌ Directory does not exist: {repo_path}")

    if not os.path.isdir(os.path.join(repo_path, ".git")):
        raise FileNotFoundError(f"❌ Not a Git repository (no .git directory in {repo_path})")

    status_result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )
    if status_result.stdout.strip():
        raise RuntimeError("Repository has unstaged or uncommitted changes. Please commit/stash them before rewriting history.")

    print(f"[INFO] Working on repository: {repo_path}")

    # 1. Remove old filter-branch backups (safe cleanup)
    subprocess.run(["git", "update-ref", "-d", "refs/original/refs/heads/main"], cwd=repo_path, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "update-ref", "-d", "refs/original/refs/heads/master"], cwd=repo_path, stderr=subprocess.DEVNULL)

    # 2. Bash env-filter script (for git filter-branch)
    env_filter_script = f"""
if [ "$GIT_AUTHOR_EMAIL" = "{old_email}" ]
then
    export GIT_AUTHOR_NAME="{new_name}"
    export GIT_AUTHOR_EMAIL="{new_email}"
    export GIT_COMMITTER_NAME="{new_name}"
    export GIT_COMMITTER_EMAIL="{new_email}"
fi
"""

    print("[INFO] Rewriting Git history...")

    # 3. Run git filter-branch
    subprocess.run(
        ["git", "filter-branch", "-f", "--env-filter", env_filter_script, "--", "--all"],
        cwd=repo_path,
        check=True
    )

    # 4. Garbage collection
    subprocess.run(["git", "gc", "--prune=now"], cwd=repo_path, check=True)

    print("[DONE] Git history modified: commits from", old_email, "are now yours!")


if __name__ == "__main__":
    modify_history()