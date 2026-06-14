#!/bin/bash

echo "Watching repository for changes... (Press Ctrl+C to stop)"

IGNORE_PATTERN='\.git|__pycache__|watcher\.log|build|dist|bin|\.o$|venv|\.venv'

commit_pending=0
commit_deadline=0

# Cleanup on exit
cleanup() {
    echo -e "\nStopping watcher..."
    kill "$INOTIFY_PID" 2>/dev/null
    exit 0
}
trap cleanup INT TERM

# Start inotifywait in the background, feeding its output into a named pipe
PIPE="/tmp/watch-$$.fifo"
mkfifo "$PIPE"
inotifywait -m -r -e modify -e create -e delete -e move . 2>/dev/null > "$PIPE" &
INOTIFY_PID=$!

# Main loop: read from pipe with 1-second timeout using 'read -t'
while true; do
    if read -t 1 event < "$PIPE"; then
        # Filter ignored events
        if echo "$event" | grep -qE "$IGNORE_PATTERN"; then
            echo "Ignored: $event"
            continue
        fi

        echo "Detected: $event"

        if [ "$commit_pending" -eq 0 ]; then
            commit_pending=1
            commit_deadline=$(( $(date +%s) + 300 ))
            echo "Commit scheduled at $(date -d "@$commit_deadline" '+%H:%M:%S')"
        fi
    fi

    # Check if a commit is pending and deadline has passed
    if [ "$commit_pending" -eq 1 ] && [ $(date +%s) -ge "$commit_deadline" ]; then
        git add .
        if git diff --cached --quiet; then
            echo "No changes to commit."
        else
            git commit -m "Auto update $(date '+%Y-%m-%d %H:%M:%S')"
            if git push; then
                echo "Changes pushed."
            else
                echo "Push failed – will retry next cycle."
                # Keep the pending flag so it retries? Or reset? We'll reset for simplicity.
            fi
        fi
        commit_pending=0
    fi
done

# Cleanup (though unreachable due to infinite loop, but trap handles it)
rm -f "$PIPE"