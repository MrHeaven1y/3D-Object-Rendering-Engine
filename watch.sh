#!/bin/bash

echo "Watching repository for changes..."

IGNORE_PATTERN='\.git|__pycache__|watcher\.log|build|dist|bin|\.o$|venv|\.venv'

commit_pending=0
commit_deadline=0

inotifywait -m -r \
    -e modify -e create -e delete -e move \
    . 2>/dev/null |
while true; do
    if read -t 1 event; then
        # Filter ignored events
        if echo "$event" | grep -qE "$IGNORE_PATTERN"; then
            echo "Ignored: $event"
            continue
        fi

        echo "Detected: $event"

        if [ "$commit_pending" -eq 0 ]; then
            commit_pending=1
            commit_deadline=$(( $(date +%s) + 300 ))
            echo "Commit scheduled at $(date -d @$commit_deadline '+%H:%M:%S')"
        fi
    fi

    if [ "$commit_pending" -eq 1 ] && [ $(date +%s) -ge $commit_deadline ]; then
        git add .

        if git diff --cached --quiet; then
            echo "No changes to commit."
        else
            git commit -m "Auto update $(date '+%Y-%m-%d %H:%M:%S')"
            git push
            echo "Changes pushed."
        fi

        commit_pending=0
    fi
done