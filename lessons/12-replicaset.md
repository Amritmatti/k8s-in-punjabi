# Lesson 12 — ReplicaSet

ReplicaSet ਦਾ ਕੰਮ Pods ਦੀ desired number maintain ਕਰਨਾ ਹੈ। ਆਮ ਤੌਰ ਤੇ ਤੁਸੀਂ ReplicaSet ਨੂੰ manually manage ਨਹੀਂ ਕਰਦੇ; Deployment ReplicaSet create ਅਤੇ manage ਕਰਦਾ ਹੈ।

## Example

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-rs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
```

## Flow

```text
Deployment (usually)
       |
       v
   ReplicaSet
       |
   +---+---+
   v   v   v
 Pod Pod Pod
```

## Selector important ਹੈ

ReplicaSet ਆਪਣੇ selector ਨਾਲ matching Pods ਨੂੰ track ਕਰਦਾ ਹੈ। Template ਦੇ labels selector ਨਾਲ match ਕਰਨੇ ਚਾਹੀਦੇ ਹਨ।

```bash
kubectl apply -f <file>.yaml
kubectl get rs
kubectl get pods -l app=nginx
kubectl describe rs nginx-rs
```

## Self-healing

ਜੇ managed Pod delete ਹੁੰਦਾ ਹੈ ਅਤੇ ReplicaSet ਦੀ desired replica count ਘੱਟ ਹੋ ਜਾਂਦੀ ਹੈ, controller replacement Pod create ਕਰਦਾ ਹੈ।

## ReplicaSet vs ReplicationController

ReplicaSet modern `apps/v1` API ਵਿੱਚ ਵਰਤਿਆ ਜਾਂਦਾ ਹੈ ਅਤੇ set-based selectors support ਕਰਦਾ ਹੈ। ReplicationController legacy resource ਹੈ।

## Interview

**Q: Deployment ਦੀ ਲੋੜ ਹੋਣ ਦੇ ਬਾਵਜੂਦ ReplicaSet ਕਿਉਂ ਜਾਣੀਏ?**

Deployment internally ReplicaSet ਦਾ ਵਰਤੋਂ ਕਰਕੇ Pods ਦੀ replica management ਕਰਦਾ ਹੈ ਅਤੇ rolling updates/rollbacks ਵਰਗੀਆਂ higher-level capabilities ਦਿੰਦਾ ਹੈ।
