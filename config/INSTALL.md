# Setup for work machine

## 1. Clone (if not already)
```
git clone https://github.com/altnew/Channels.git
cd Channels
```

## 2. Configure git push access
```
git config user.email "almaz.tegizbekov@gmail.com"
git config user.name "Almaz Tegizbekov"
```

## 3. Run the sync agent
```
python config/sync.py
```

The script polls every 5 minutes for `config/tasks/pending.md`.
When found, it runs the task via `claude -p` and pushes the result back.

## 4. To run in background (keeps working after terminal close)
**Windows (PowerShell):**
```
Start-Process -NoNewWindow python -ArgumentList "config/sync.py" -RedirectStandardOutput "sync.log"
```

**Or via Task Scheduler:**
- Action: `python`
- Arguments: `C:\Users\<you>\Channels\config\sync.py`
- Trigger: At startup
- Check: "Run whether user is logged on or not"

## Test
After starting, I will push a test task. Check `sync.log` for output.
