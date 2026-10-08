# DevOps Workflow - Boyarkin Dmitriy (IT2-2312, ID 37752)

Linux (project + scripts) -> Git (history) -> GitHub (remote) ->
Jenkins (checkout, build, test) -> Docker (build image, run container) -> SUCCESS

A push to GitHub is the trigger point: Jenkins pulls the exact commit,
verifies it, and packages it as a Docker image.
