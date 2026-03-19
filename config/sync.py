#!/usr/bin/env python3
"""
Kai Agent — выполняет задания из GitHub репо через Claude Code.
Запуск: python agent.py (работает в фоне, проверяет каждые 5 мин)
"""
import subprocess, time, os, shutil
from pathlib import Path
from datetime import datetime

REPO_DIR = Path(__file__).parent.parent  # root of git repo
TASKS_DIR = Path(__file__).parent / "tasks"
CHECK_INTERVAL = 300  # 5 минут
CLAUDE_CMD = "claude"  # или полный путь

def git(*args):
    r = subprocess.run(["git"] + list(args), cwd=REPO_DIR,
                       capture_output=True, text=True, timeout=60)
    return r.returncode == 0, r.stdout + r.stderr

def run():
    print(f"[{datetime.now():%H:%M}] Kai Agent started. Checking every {CHECK_INTERVAL}s")

    while True:
        try:
            # Pull latest
            git("pull", "-q")

            pending = TASKS_DIR / "pending.md"
            if pending.exists():
                task = pending.read_text(encoding="utf-8").strip()
                print(f"\n[{datetime.now():%H:%M}] TASK: {task[:80]}...")

                # Mark as running
                running = TASKS_DIR / "running.md"
                shutil.move(str(pending), str(running))
                git("add", "-A")
                git("commit", "-m", "kai: task started")
                git("push")

                # Execute via Claude Code
                try:
                    result = subprocess.run(
                        [CLAUDE_CMD, "-p", task],
                        capture_output=True, text=True, timeout=600
                    )
                    output = result.stdout.strip()
                    if result.returncode != 0:
                        output = f"ERROR (code {result.returncode}):\n{result.stderr}\n{output}"
                except subprocess.TimeoutExpired:
                    output = "ERROR: timeout (10 min)"
                except Exception as e:
                    output = f"ERROR: {e}"

                # Save result
                result_file = TASKS_DIR / "result.md"
                result_file.write_text(
                    f"# Result\n**Time:** {datetime.now():%Y-%m-%d %H:%M}\n\n{output}",
                    encoding="utf-8"
                )

                # Archive
                history = TASKS_DIR / "history"
                history.mkdir(exist_ok=True)
                ts = datetime.now().strftime("%Y%m%d_%H%M")
                (history / f"{ts}_task.md").write_text(task, encoding="utf-8")
                (history / f"{ts}_result.md").write_text(output, encoding="utf-8")

                # Cleanup and push
                if running.exists():
                    running.unlink()
                git("add", "-A")
                git("commit", "-m", f"kai: task done @ {datetime.now():%H:%M}")
                git("push")

                print(f"[{datetime.now():%H:%M}] DONE. Result: {len(output)} chars")

        except Exception as e:
            print(f"[{datetime.now():%H:%M}] Error: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run()
