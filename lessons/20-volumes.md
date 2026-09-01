# Lesson 20 — Volumes

Container filesystem ephemeral ਹੋ ਸਕਦਾ ਹੈ। Kubernetes Volumes Pod ਦੇ containers ਨੂੰ storage attach ਕਰਨ ਦਾ abstraction ਦਿੰਦੇ ਹਨ।

## emptyDir

Pod ਦੇ lifetime ਲਈ node-local temporary storage:

```yaml
volumes:
  - name: shared
    emptyDir: {}
```

ਇੱਕ Pod ਦੇ multiple containers ਇਸਨੂੰ share ਕਰ ਸਕਦੇ ਹਨ। Pod delete ਹੋਣ ਤੇ data normally ਜਾਂਦਾ ਹੈ।

## Mount

```yaml
volumeMounts:
  - name: shared
    mountPath: /shared
```

## hostPath

```yaml
volumes:
  - name: host-data
    hostPath:
      path: /var/lib/myapp
      type: DirectoryOrCreate
```

`hostPath` node ਦੇ filesystem ਨਾਲ tightly coupled ਹੈ ਅਤੇ security/portability concerns ਕਰਕੇ production applications ਲਈ carefully use ਕਰੋ।

## Persistent storage

Long-lived application data ਲਈ ਆਮ architecture:

```text
Pod
 |
 v
PVC
 |
 v
PV
 |
 v
Storage backend
```

## Important distinction

- Volume = Pod ਦੇ ਅੰਦਰ storage attach ਕਰਨ ਦਾ mechanism
- PVC = application ਦੀ storage request
- PV = cluster ਵਿੱਚ provisioned storage resource
- StorageClass = dynamic provisioning ਦੀ policy/template

## Hands-on inspection

```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl get pv
kubectl get pvc
kubectl get storageclass
```

## Interview

**Q: Container restart ਹੋਣ ਤੇ data ਹਮੇਸ਼ਾ delete ਹੁੰਦਾ ਹੈ?**

Container filesystem ਦੀ lifetime ਅਤੇ Pod volume ਦੀ lifetime ਵੱਖ ਹਨ। Volume type decide ਕਰਦੀ ਹੈ ਕਿ data ਕਿੰਨਾ ਸਮਾਂ ਰਹਿੰਦਾ ਹੈ। Persistent data ਲਈ persistent storage use ਕਰੋ।
