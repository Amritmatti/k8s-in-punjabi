# Lesson 13 — Deployment

Deployment production applications ਲਈ ਸਭ ਤੋਂ common workload resources ਵਿੱਚੋਂ ਇੱਕ ਹੈ। ਇਹ ReplicaSets manage ਕਰਦਾ ਹੈ ਅਤੇ declarative updates, rolling rollout ਅਤੇ rollback provide ਕਰਦਾ ਹੈ।

## Basic Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
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
          ports:
            - containerPort: 80
```

## Request flow

```text
kubectl apply
     |
     v
API Server
     |
     v
Deployment object
     |
     v
Deployment Controller
     |
     v
ReplicaSet
     |
     v
Pods
     |
     v
Scheduler -> Node -> kubelet -> Runtime
```

## Create and inspect

```bash
kubectl apply -f examples/deployment.yaml
kubectl get deployment
kubectl get rs
kubectl get pods -l app=nginx
kubectl rollout status deployment/nginx
```

## Scaling

```bash
kubectl scale deployment nginx --replicas=5
kubectl get deployment nginx
```

## Rolling update

```bash
kubectl set image deployment/nginx nginx=nginx:1.28
kubectl rollout status deployment/nginx
kubectl rollout history deployment/nginx
```

Deployment new ReplicaSet create ਕਰ ਸਕਦਾ ਹੈ ਅਤੇ Pods gradually replace ਕਰਦਾ ਹੈ। Exact rollout behavior strategy settings ਉੱਤੇ depend ਕਰਦਾ ਹੈ।

## Rollback

```bash
kubectl rollout undo deployment/nginx
kubectl rollout status deployment/nginx
```

## Useful troubleshooting

```bash
kubectl describe deployment nginx
kubectl describe rs <replicaset-name>
kubectl get events --sort-by=.metadata.creationTimestamp
```

## Interview

**Q: Deployment ਅਤੇ ReplicaSet ਵਿੱਚ difference?**

ReplicaSet replica count maintain ਕਰਦਾ ਹੈ। Deployment ReplicaSets ਨੂੰ manage ਕਰਕੇ rollout, revision history ਅਤੇ rollback ਵਰਗੀਆਂ capabilities provide ਕਰਦਾ ਹੈ।
