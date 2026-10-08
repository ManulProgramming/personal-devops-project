# DevOps Lab 1

## Start

```bash
cd ~/personal-devops-project
git remote add origin https://github.com/<your-username>/personal-devops-project.git
git remote -v
git push -u origin main
git push origin development                     # optional: shows the branch on GitHub

# Docker part (needs Docker installed)
docker build -t personal-devops-project .

# Start Jenkins (section 4 below), create the job, run it, screenshot it.
```

Prerequisites: Linux / WSL2 / macOS with `git`, `docker` (with compose plugin) and `python3`.

---

## 1. Linux

All commands run in `~/personal-devops-project`.

### Task 1 - Structure and basic commands
```bash
pwd                          # print working directory (where am I)
ls -la                       # list files incl. hidden, with details
cd scripts && cd ..          # change directory
mkdir -p experiment/tmp      # make directories (-p = create parents)
touch experiment/a.txt       # create empty file / update timestamp
cp experiment/a.txt experiment/b.txt     # copy
mv experiment/b.txt experiment/c.txt     # move / rename
rm experiment/c.txt          # remove file
rm -r experiment             # remove directory recursively
cat Boyarkin_Dmitriy_info.txt       # print whole file
head -n 3 config/app.conf    # first 3 lines
tail -n 3 logs/application.log   # last 3 lines
cat config/app.conf
```

### Task 2 - Search and processing
```bash
find ~/devops -name application.log        # locate file by name
grep ERROR logs/application.log            # lines with ERROR
grep WARNING logs/application.log          # lines with WARNING
grep -c ERROR logs/application.log         # COUNT of ERROR lines -> 3
tail -n 5 logs/application.log             # last 5 lines
```

### Task 3 - Permissions
```bash
ls -l demo/
# -rw------- private.txt   (600)
# -rw-r--r-- public.txt    (644)
chmod 600 demo/private.txt
chmod 644 demo/public.txt
# try: chmod o-r demo/public.txt  then undo with chmod o+r
```
Explanation to say/write:
- **r** read (view content), **w** write (modify/delete content), **x** execute (run file / enter directory).
- **owner** (u) = the user who owns the file; **group** (g) = users in the file's group; **others** (o) = everyone else.
- `ls -l` shows 10 characters: type, then owner/group/others triplets. `rw-r--r--` = owner read+write, group read, others read.
- Numbers: r=4, w=2, x=1. 600 = owner rw, nobody else. 644 = owner rw, others read-only. **755** = owner rwx, group/others r-x (typical for scripts and directories).
- Why different: `private.txt` holds sensitive data, so only the owner gets access (least privilege). `public.txt` is meant to be shared, so others may read but must not modify it.

### Task 4 - Bash script
```bash
ls -l scripts/
./scripts/Boyarkin_Dmitriy_system.sh       # works because chmod +x was applied
cat scripts/Boyarkin_Dmitriy_system.sh     # walk through it in the video
```
Explain: shebang `#!/usr/bin/env bash` picks the interpreter; `$(command)` runs a command and inserts the output; `if [ -f file ]` tests whether a file exists; the script finds the info file relative to its own location so it works from any directory.

### Task 5 - Processes
```bash
ps                       # processes of current terminal
ps aux                   # all processes: USER PID %CPU %MEM ... COMMAND
ps aux | grep -i bash    # pick one, read PID / owner / %CPU / %MEM from the line
top                      # live view, press q to quit (Shift+P sort by CPU, Shift+M by memory)
```
Pick e.g. your own `bash` process and read out the PID, user, %CPU, %MEM from the `ps aux` row.
- **Process**: a running instance of a program, with its own memory, state and resources.
- **PID**: Process ID, the unique number the kernel assigns to each process; used by `kill <PID>`.
- **ps vs top**: `ps` is a one-time snapshot; `top` is a live, continuously updating view sorted by resource use.

---

## 2. Git & GitHub

### Task 6 - Repository
```bash
git config --global user.name  "John Doe"
git config --global user.email "example@example.com"
git status
git init
```

### Task 7 - Commit history (what the generator creates)

| # | Commit message | What changed |
|---|---|---|
| 1 | Initial project structure | README + app/scripts/config/logs/tests dirs |
| 2 | Add student information | `Boyarkin_Dmitriy_info.txt` |
| 3 | Add Linux system script | `scripts/Boyarkin_Dmitriy_system.sh` |
| 4 | Add project configuration and .gitignore | `config/app.conf`, `.gitignore`, `.env.example` |
| 5 | Add application source code and unit tests | `app/main.py`, `tests/test_app.py` |
| 6 | Add Docker configuration | `Dockerfile`, `.dockerignore` |
| 7 | Add Docker Compose configuration | `docker-compose.yml` |
| 8 | Add Jenkinsfile and local Jenkins setup | `Jenkinsfile`, `jenkins/` |
| 9 | Add file permission demo files | `demo/private.txt`, `demo/public.txt` |
| 10 | Add workflow documentation on development branch | `docs/WORKFLOW.md` (on `development`) |
| 11 | Merge branch 'development' into main | merge commit |

```bash
git log
git log --oneline
git show --stat HEAD~2       # show what one commit changed
```

### Task 8 - .gitignore
```bash
cat .gitignore
git status                         # clean, although logs/application.log and backup/ exist
ls logs backup                     # they exist on disk
git ls-files | grep -E 'log$|backup'   # shows only logs/.gitkeep, no application.log
git check-ignore -v logs/application.log backup/notes.txt   # shows which rule ignores them
```
Why it matters in DevOps: keeps secrets (`.env` with passwords/API keys) out of history (once pushed, leaked secrets are hard to remove), avoids noise and huge/generated files (logs, build output, backups), keeps repos small and clean, and keeps CI builds reproducible because only source is versioned.

### Task 9 - Branch and merge (already done by the generator; replay it live)
```bash
git branch                         # * main, development
git log --oneline --graph
# to demonstrate live, make a second one:
git branch feature-demo
git switch feature-demo
echo "Extra note" >> docs/WORKFLOW.md
git add docs && git commit -m "Extend workflow notes"
git switch main
git merge feature-demo
git log --oneline --graph
```
Purpose of branches: work on features/fixes in isolation without breaking `main`, allow parallel work, review changes before merging, and let CI test branches separately.

### Task 10 - GitHub
```bash
git remote add origin https://github.com/<user>/personal-devops-project.git
git remote -v
git push -u origin main        # -u sets upstream so later "git push" works alone
```

**push vs pull**: `push` uploads your local commits to the remote; `pull` downloads remote commits and merges them into your branch (`fetch` + `merge`).

---

## 3. Docker

### Task 11-12 - Dockerfile, build, run
Show `cat Dockerfile` and explain each instruction:
- `FROM python:3.12-alpine` base image to start from
- `WORKDIR /app` working directory for following instructions and the container start directory
- `COPY app/ /app/` copy files from the host build context into the image
- `RUN adduser -D appuser` execute a command at build time (creates a non-root user)
- `EXPOSE 8080` documents the port the app would listen on (it does not publish it)
- `CMD ["python","main.py"]` default command when the container starts

```bash
docker build -t boyarkin-dmitriy-devops .
docker images
docker run --name boyarkin-dmitriy-container boyarkin-dmitriy-devops     # Ctrl+C to stop (heartbeat keeps it alive)
# second terminal:
docker ps
docker ps -a
```

### Task 13 - Environment variables
```bash
docker rm -f boyarkin-dmitriy-container
docker run \
  -e STUDENT_NAME=Dmitriy -e STUDENT_SURNAME=Boyarkin \
  -e STUDENT_GROUP=IT2-2312 -e STUDENT_ID=37752 \
  --name boyarkin-dmitriy-container boyarkin-dmitriy-devops
# for the "can use these values" proof, change one: -e STUDENT_NAME=Test
```
- **Environment variable**: a named value (KEY=value) passed to a process from outside.
- **Why useful in Docker**: one image can run with different configuration (dev/test/prod) without rebuilding.
- **Why no secrets in the image**: image layers are permanent and shareable; anyone with the image (or registry access) can read hard-coded passwords via `docker history`/extraction. Pass secrets at runtime or via secret managers instead.

### Task 14 - Container management
```bash
docker run -d --name boyarkin-dmitriy-container boyarkin-dmitriy-devops   # detached
docker logs boyarkin-dmitriy-container
docker logs -f boyarkin-dmitriy-container          # follow, Ctrl+C to leave
docker exec -it boyarkin-dmitriy-container sh      # shell inside; run: ls, whoami, env | grep STUDENT, exit
docker stop boyarkin-dmitriy-container
docker start boyarkin-dmitriy-container
docker stop boyarkin-dmitriy-container && docker rm boyarkin-dmitriy-container
```
**Image vs container**: an image is a read-only template (code + dependencies + config), like a class or an installer. A container is a running (or stopped) instance created from an image, like an object. One image can create many containers.

### Task 15 - Compose
```bash
docker rm -f boyarkin-dmitriy-container 2>/dev/null
docker compose up -d           # (omit -d to stay in the foreground; Ctrl+C to stop)
docker compose ps
docker ps
docker compose logs
docker compose down
```
Why Compose: describes the whole application (image, name, env vars, ports, volumes, multiple services) in one versioned YAML file; one command starts/stops everything; reproducible and easy to share, instead of long `docker run` commands.

---

## 4. Jenkins (20 pts) - running it locally

The repo contains `jenkins/Dockerfile` and `jenkins/docker-compose.yml`: a Jenkins with the Docker CLI and Python installed, talking to your host's Docker daemon through the mounted socket (so images/containers built by the pipeline appear in your own `docker images` / `docker ps`). This is fine for a lab but not for production, since socket access is root-equivalent.

```bash
cd ~/personal-devops-project/jenkins
docker compose up -d --build
docker logs jenkins           # find the "initial admin password" block
# or: docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
1. Open http://localhost:8080, paste the password, choose **Install suggested plugins**, create the admin user.
2. If a plugin is missing: **Manage Jenkins > Plugins > Available** and install "Pipeline" and "Git" (included in suggested).
3. **New Item** > name exactly `Boyarkin_Dmitriy_DevOps` > **Pipeline** > OK.
4. Under **Pipeline**: Definition = **Pipeline script from SCM**; SCM = **Git**; Repository URL = `https://github.com/<user>/personal-devops-project.git`; Branch = `*/main`; Script Path = `Jenkinsfile`. (A public repo needs no credentials.) Save.
5. **Build Now**. Open the build, then **Console Output**; it must end with `Finished: SUCCESS`. The **Stage View** on the job page shows Checkout, Build, Test, Docker Build, Docker Run.
6. In a terminal show: `docker images boyarkin-dmitriy-devops`, `docker ps` (container `boyarkin-dmitriy-container` running), and note the commit hash printed in the Checkout stage (`git log -1 --oneline`), plus the "Git Revision" on the build page.

### Task 19 - environment variables in Jenkins
They are defined in the `environment { }` block of the Jenkinsfile and printed in the Checkout stage ("Student: Dmitriy Boyarkin / Group: IT2-2312 / Student ID: 37752" in the Console Output). If your instructor wants them configured in the Jenkins UI instead: tick **This project is parameterized** on the job and add String Parameters `STUDENT_NAME`, `STUDENT_SURNAME`, `STUDENT_GROUP`, `STUDENT_ID`, then remove the lines of those four variables from the `environment` block. Doing both is not recommended, as the block overrides parameters.

### Pipeline explanation (Task 21 questions 7-8)
- Pipeline starts: Jenkins reads the `Jenkinsfile` from the repo, allocates an agent/workspace, and runs the stages in order: **Checkout** (pull the exact commit from GitHub) > **Build** (syntax/compile checks) > **Test** (unit tests + the Bash script) > **Docker Build** (image from the Dockerfile) > **Docker Run** (start container, show logs).
- If a stage fails: the pipeline stops, later stages are skipped, the build is marked FAILED (red) and the `post { failure }` block runs. This is the point: broken code never reaches the Docker image/run stage. If **Docker Build** fails, no new image exists, so the container is not (re)started with that change.

### Jenkins troubleshooting
- `permission denied ... docker.sock`: the compose file uses `user: root`, so make sure you started it from `jenkins/` with that file; on Docker Desktop (Windows/macOS) the socket path works inside WSL2/Linux VM as is.
- `python3: not found`: you used the stock Jenkins image; rebuild with `docker compose up -d --build` in `jenkins/`.
- Container name already in use: the Docker Run stage does `docker rm -f` first; also run `docker compose down` to remove the Compose one (same name).
- Checkout failed: wrong repo URL/branch, or private repo (make it public or add credentials).
- Port 8080 busy: change `"8080:8080"` to `"8081:8080"`.

---

## 5. Integrated workflow (Task 21 - answers)
1. **Why Linux**: the standard server/CI/container OS; gives the shell, scripting, permissions and tools that all later steps run on (Docker images and Jenkins agents are Linux).
2. **Why Git**: version control: history of every change, branching, collaboration, ability to roll back and to know exactly which version was built.
3. **Why GitHub**: remote hosting of the repo: backup, sharing, collaboration, and a central source that other systems (Jenkins) can pull from.
4. **Why Jenkins needs GitHub**: Jenkins has to fetch the source code and the Jenkinsfile from a reachable, central place; it then builds the exact commit and can be triggered by changes.
5. **Why Jenkins builds the Docker image**: to produce the same reproducible, portable artifact every time, in a clean automated environment, instead of "it works on my machine".
6. **Image vs container**: template vs running instance (see Docker section).
7. **What happens when the pipeline starts**: see above.
8. **If a stage fails**: see above.

Flow in one sentence: you create the project on Linux, track it with Git, publish it to GitHub, Jenkins pulls it, builds and tests it, packages it into a Docker image and runs it as a container; a failure at any step stops the chain.