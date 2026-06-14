#!/bin/bash

echo "Watching repository for changes..."

while true
do
    EVENT=$(inotifywait -r \
        -e modify \
        -e create \
        -e delete \
        -e move \
        . \
        --exclude '(\.git|__pycache__|watcher\.log|build|dist|bin|\.o$)')

    echo "Detected: $EVENT"

    sleep 300

    git add .

    if git diff --cached --quiet
    then
        echo "No changes to commit."
        continue
    fi

    git commit -m "Auto update $(date '+%Y-%m-%d %H:%M:%S')"

    git push

    echo "Changes pushed."
done