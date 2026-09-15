# Platform Topology

Target baseline:
- Container build with multi-stage Dockerfile
- Runtime config through env vars
- Kubernetes deployment with service + ingress

Reliability controls:
- readiness/liveness probes
- resource requests/limits
- rolling update strategy

Security controls:
- non-root user
- read-only root fs where possible
- minimal base image
