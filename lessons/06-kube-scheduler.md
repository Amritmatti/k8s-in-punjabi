# Lesson 06 — kube-scheduler

Scheduler ਦਾ ਮੁੱਖ ਕੰਮ ਹੈ **unscheduled Pod ਲਈ suitable node select ਕਰਨਾ**।

## Flow

```text
Pod created -> API Server -> Scheduler
                           |
                           v
                    suitable node
                           |
                           v
                        kubelet
                           |
                           v
                       Container
```

Scheduler placement decision ਕਰਦਾ ਹੈ; ਇਹ container ਨੂੰ run ਨਹੀਂ ਕਰਦਾ। Actual workload node ਦਾ kubelet/container runtime start ਕਰਦਾ ਹੈ।

## Scheduler ਕੀ ਵੇਖਦਾ ਹੈ?

- CPU/memory requests
- nodeSelector
- node affinity
- pod affinity/anti-affinity
- taints/tolerations
- topology constraints
- scheduling plugins

## Example

```yaml
spec:
  nodeSelector:
    workload: backend
```

Node ਨੂੰ label ਦਿਓ:

```bash
kubectl label node worker-1 workload=backend
```

Pod ਲਈ ਇਹ node eligible ਹੋ ਸਕਦਾ ਹੈ, ਜੇ ਹੋਰ constraints ਵੀ satisfy ਹੋਣ।

## Troubleshooting Pending Pod

```bash
kubectl get pod <pod-name>
kubectl describe pod <pod-name>
kubectl get nodes --show-labels
```

`describe` ਦੇ Events section ਵਿੱਚ scheduling failure ਦਾ reason ਅਕਸਰ ਮਿਲ ਜਾਂਦਾ ਹੈ।
