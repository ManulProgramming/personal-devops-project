#!/usr/bin/env bash
# Prints student info and basic system info (Linux lab, Task 4)

# Locate the info file relative to this script, so it works from any directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFO_FILE="$SCRIPT_DIR/../Boyarkin_Dmitriy_info.txt"

echo "=============================="
echo "Student Information"
echo "=============================="
echo "Name: Dmitriy"
echo "Surname: Boyarkin"
echo "Group: IT2-2312"
echo "Student ID: 37752"
echo "=============================="
echo "System Information"
echo "=============================="
echo "Username: $(whoami)"
echo "Hostname: $(hostname)"
echo "Current Date: $(date)"
echo "Operating System: $(uname -sr)"
echo "Disk Usage: $(df -h / | awk 'NR==2 {print $3 " used of " $2 " (" $5 ")"}')"
echo "Memory Usage: $(free -m | awk '/^Mem:/ {print $3 " MB used of " $2 " MB"}')"
echo "=============================="

if [ -f "$INFO_FILE" ]; then
  echo "Student information file exists."
else
  echo "Student information file does not exist."
fi
