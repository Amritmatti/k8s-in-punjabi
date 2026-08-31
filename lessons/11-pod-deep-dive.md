# Lesson 11 — Pod Deep Dive

Pod Kubernetes ਦੀ **smallest deployable unit** ਹੈ। ਇੱਕ Pod ਵਿੱਚ ਇੱਕ ਜਾਂ ਕਈ containers ਹੋ ਸਕਦੇ ਹਨ ਜੋ network namespace ਅਤੇ attached volumes ਵਰਗੇ resources share ਕਰ ਸਕਦੇ ਹਨ।

## Basic Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
    - name: nginx
      image: nginx:1.27
      ports:
        - containerPort: 80
```

## Apply and inspect

```bash
kubectl apply -f examples/pod.yaml
kubectl get pod nginx -o wide
kubectl describe pod nginx
kubectl logs nginx
kubectl exec -it nginx -- sh
```

## Pod IP

ਆਮ Kubernetes networking ਵਿੱਚ ਹਰ Pod ਨੂੰ ਇੱਕ IP ਮਿਲਦਾ ਹੈ ਅਤੇ Pod ਦੇ containers same network namespace share ਕਰਦੇ ਹਨ। ਇਸ ਕਰਕੇ same Pod ਦੇ containers ਇੱਕੋ Pod IP ਉੱਤੇ ਆਪਸ ਵਿੱਚ communicate ਕਰ ਸਕਦੇ ਹਨ।

## Lifecycle

Common Pod phases:

- Pending
- Running
- Succeeded
- Failed
- Unknown

Pod phase ਨੂੰ container restart count ਜਾਂ readiness state ਨਾਲ confuse ਨਾ ਕਰੋ।

## Multi-container Pod

Sidecar ਵਰਗੇ patterns ਵਿੱਚ containers tightly coupled functionality share ਕਰ ਸਕਦੇ ਹਨ। ਉਦਾਹਰਨ: application container + log shipping sidecar। Unrelated applications ਨੂੰ ਇੱਕ Pod ਵਿੱਚ combine ਕਰਨਾ ਆਮ ਤੌਰ ਤੇ ਚੰਗੀ practice ਨਹੀਂ।

## Production rule

Application ਨੂੰ manually naked Pod ਦੇ ਰੂਪ ਵਿੱਚ run ਕਰਨ ਦੀ ਬਜਾਏ ਆਮ ਤੌਰ ਤੇ Deployment, StatefulSet, DaemonSet, Job ਆਦਿ workload controllers ਵਰਤੇ ਜਾਂਦੇ ਹਨ।

## Interview

**Q: Pod ਅਤੇ container ਵਿੱਚ difference?**

Container application process ਦੀ runtime unit ਹੈ। Pod Kubernetes ਦੀ scheduling/deployment unit ਹੈ ਜਿਸ ਵਿੱਚ ਇੱਕ ਜਾਂ ਵੱਧ containers ਹੋ ਸਕਦੇ ਹਨ।
