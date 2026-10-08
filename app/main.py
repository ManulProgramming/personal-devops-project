"""DevOps student application. Reads personal data from environment variables."""
import os
import signal
import sys
import time


def student_info(env=None):
    env = os.environ if env is None else env
    return {
        "name": env.get("STUDENT_NAME", "Dmitriy"),
        "surname": env.get("STUDENT_SURNAME", "Boyarkin"),
        "group": env.get("STUDENT_GROUP", "IT2-2312"),
        "student_id": env.get("STUDENT_ID", "37752"),
    }


def banner(info):
    line = "=" * 32
    return "\n".join([
        line,
        "DevOps Student Application",
        line,
        "Name: " + info["name"],
        "Surname: " + info["surname"],
        "Group: " + info["group"],
        "Student ID: " + info["student_id"],
        "Application is running successfully!",
    ])


def main():
    # Python as PID 1 ignores SIGTERM by default; handle it so `docker stop` is instant
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    print(banner(student_info()), flush=True)
    if os.environ.get("KEEP_ALIVE", "true").lower() != "true":
        return
    beat = 0
    while True:  # heartbeat keeps the container running so logs/exec/stop can be demonstrated
        beat += 1
        print("[heartbeat %d] application is alive" % beat, flush=True)
        time.sleep(5)


if __name__ == "__main__":
    main()
