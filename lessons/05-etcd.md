# Lesson 05 — etcd

## etcd ਕੀ ਹੈ?

etcd ਇੱਕ distributed, consistent key-value store ਹੈ। Kubernetes ਇਸਨੂੰ cluster ਦੀ persistent state store ਵਜੋਂ ਵਰਤਦਾ ਹੈ।

ਜੇ Kubernetes ਇੱਕ office ਹੈ:

- API Server = reception
- Scheduler = manager
- Controllers = supervisors
- Worker nodes = workers
- **etcd = master record book**

## API Server ਅਤੇ etcd

```text
kubectl -> API Server <-> etcd
                  |
                  +-> controllers / scheduler / nodes
```

Clients ਨੂੰ etcd directly query ਕਰਨ ਦੀ ਬਜਾਏ Kubernetes API use ਕਰਨੀ ਚਾਹੀਦੀ ਹੈ।

## Production concerns

etcd control plane ਲਈ critical ਹੈ। ਇਸ ਲਈ regular tested backups, restricted access, TLS, encryption-at-rest strategy, disk performance monitoring ਅਤੇ quorum planning important ਹਨ।

## Backup concept

Deployment ਦੇ ਅਨੁਸਾਰ exact commands ਵੱਖ ਹੋ ਸਕਦੇ ਹਨ। `etcdctl snapshot save` ਇੱਕ common utility operation ਹੈ, ਪਰ production ਵਿੱਚ version-compatible backup/restore procedure ਅਤੇ restore testing follow ਕਰੋ।

## Interview

**Q: etcd unavailable ਹੋਵੇ ਤਾਂ?**

Kubernetes ਦੀ persistent cluster state unavailable ਹੋ ਸਕਦੀ ਹੈ ਅਤੇ control plane severely impacted ਹੋ ਸਕਦਾ ਹੈ। Existing containers ਕੁਝ ਸਮੇਂ ਲਈ ਚੱਲ ਸਕਦੇ ਹਨ, ਪਰ new API operations ਅਤੇ reconciliation ਪ੍ਰਭਾਵਿਤ ਹੋ ਸਕਦੇ ਹਨ। ਇਸ ਲਈ etcd backup/restore critical ਹੈ।
