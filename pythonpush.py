#!/usr/bin/env python3
"""
Simple Git Auto Pusher
Usage: python3 pythonpush.py --commits 55
"""

import sys
import time
import random
import subprocess
from pathlib import Path

COMMIT_MESSAGES = [
    "chore: minor updates",
    "style: improve formatting",
    "docs: update comments",
    "refactor: small cleanup",
    "chore: maintenance",
    "fix: minor tweaks",
]

def run_command(cmd, cwd="."):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr

def main():
    commits = 55
    
    # Allow passing number of commits
    if len(sys.argv) > 2 and sys.argv[1] == "--commits":
        try:
            commits = int(sys.argv[2])
        except:
            commits = 55

    repo_path = str(Path(".").resolve())

    if not Path(repo_path, ".git").exists():
        print("✗ No git repository found in this folder!")
        print("Please run 'git init' first.")
        sys.exit(1)

    print(f"\n🚀 Starting auto pusher - Making {commits} commits")
    print(f"   Repository: {repo_path}\n")

    success = 0

    for i in range(commits):
        msg = random.choice(COMMIT_MESSAGES)
        timestamp = time.strftime("%H:%M:%S")

        # Make a small change to README.md or create one if it doesn't exist
        readme = Path("README.md")
        if not readme.exists():
            readme.write_text("# My Project\n\nAuto generated commits.\n")

        with open("README.md", "a") as f:
            f.write(f"\n<!-- Update {i+1} at {timestamp} -->\n")

        # Git commands
        run_command(["git", "add", "README.md"], repo_path)
        code, _ = run_command(["git", "commit", "-m", msg], repo_path)

        if code == 0:
            success += 1
            print(f"  [{i+1}/{commits}] ✓ Commit done → {msg}")
        else:
            print(f"  [{i+1}/{commits}] ✗ Commit failed")

        if i < commits - 1:
            time.sleep(1.2)

    print(f"\n📊 Done! {success}/{commits} commits created.")

    # Push at the end
    print("📤 Pushing to GitHub...")
    code, output = run_command(["git", "push"], repo_path)
    if code == 0:
        print("✅ Push successful!")
    else:
        print("✗ Push failed (maybe already up to date)")

    print("\n✨ Finished!\n")


if __name__ == "__main__":
    main()