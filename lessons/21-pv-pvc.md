# Lesson 21 — PersistentVolume & PersistentVolumeClaim

Persistent applications ਲਈ Kubernetes ਵਿੱਚ **PV** ਅਤੇ **PVC** important concepts ਹਨ।

## Simple analogy

- PVC = "ਮੈਨੂੰ 20Gi storage ਚਾਹੀਦੀ ਹੈ"
- PV = "ਇਹ 20Gi storage available ਹੈ"
- StorageClass = "ਇਹ storage dynamically ਕਿਵੇਂ ਬਣਾਉਣੀ ਹੈ"

## PVC example

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

## Pod ਵਿੱਚ use

```yaml
volumes:
  - name: data
    persistentVolumeClaim:
      claimName: app-data
```

```yaml
volumeMounts:
  - name: data
    mountPath: /data
```

## Flow

```text
Application Pod
      |
      v
     PVC
      |
      v
     PV
      |
      v
Storage system
```

Dynamic provisioning enabled ਹੋਵੇ ਤਾਂ PVC ਇੱਕ StorageClass ਰਾਹੀਂ suitable PV/storage provision ਕਰਵਾ ਸਕਦੀ ਹੈ।

## Access modes

Common modes:

- `ReadWriteOnce` (RWO)
- `ReadOnlyMany` (ROX)
- `ReadWriteMany` (RWX)
- `ReadWriteOncePod` (RWOP)

Supported modes storage backend ਉੱਤੇ depend ਕਰਦੇ ਹਨ।

## Commands

```bash
kubectl get pv
kubectl get pvc
kubectl describe pvc app-data
kubectl get storageclass
```

ਜੇ PVC `Pending` ਰਹੇ ਤਾਂ StorageClass, provisioner/CSI driver, requested size, access mode ਅਤੇ storage backend events check ਕਰੋ।

## Interview

**Q: Pod delete ਹੋਣ ਨਾਲ PVC delete ਹੋ ਜਾਂਦੀ ਹੈ?**

ਨਹੀਂ, ਆਮ ਤੌਰ ਤੇ Pod ਅਤੇ PVC ਵੱਖ resources ਹਨ। PVC ਨੂੰ intentionally delete ਕਰਨ ਅਤੇ storage reclaim behavior ਨੂੰ separately understand ਕਰਨਾ ਚਾਹੀਦਾ ਹੈ।
