# Lesson 07 — kube-controller-manager

Kubernetes controllers **desired state** ਅਤੇ **actual state** ਨੂੰ continuously compare ਕਰਦੇ ਹਨ। ਇਸ process ਨੂੰ reconciliation ਕਹਿੰਦੇ ਹਨ।

## Real example

ਤੁਸੀਂ ਲਿਖਦੇ ਹੋ:

```yaml
spec:
  replicas: 3
```

ਜੇ ਇੱਕ Pod delete ਹੋ ਜਾਵੇ, Kubernetes ਦਾ controller observe ਕਰਦਾ ਹੈ ਕਿ desired state 3 ਹੈ ਪਰ actual state ਘੱਟ ਹੈ ਅਤੇ replacement Pod ਬਣਾਉਣ ਦੀ process ਕਰਦਾ ਹੈ।

## Reconciliation

```text
Desired State
      |
      v
Controller -> Observe -> Compare
                         |
                    Difference?
                         |
                         v
                       Action
                         |
                         v
                   Actual State
```

## Common controllers

- Deployment controller
- ReplicaSet controller
- Node controller
- Job controller

`kube-controller-manager` control plane ਵਿੱਚ controller processes ਨੂੰ run ਕਰਦਾ ਹੈ।

## Hands-on

```bash
kubectl create deployment nginx --image=nginx --replicas=3
kubectl get pods
kubectl delete pod <pod-name>
kubectl get pods -w
```

ਥੋੜ੍ਹੀ ਦੇਰ ਵਿੱਚ replacement Pod ਆ ਸਕਦਾ ਹੈ। ਇਹ Kubernetes ਦੇ self-healing/reconciliation model ਨੂੰ demonstrate ਕਰਦਾ ਹੈ।

## Interview

**Q: Controller ਅਤੇ Scheduler ਵਿੱਚ difference?**

Scheduler Pod ਲਈ node placement decide ਕਰਦਾ ਹੈ। Controller desired ਅਤੇ actual state ਦੇ difference ਨੂੰ reconcile ਕਰਦਾ ਹੈ।
