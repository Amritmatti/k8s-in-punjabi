# Lesson 10 — Container Runtime & CRI

Kubernetes ਖੁਦ containers ਨੂੰ directly run ਨਹੀਂ ਕਰਦਾ। Node ਉੱਤੇ ਇੱਕ **container runtime** containers ਦਾ actual lifecycle manage ਕਰਦਾ ਹੈ।

## Common runtimes

- containerd
- CRI-O

## CRI ਕੀ ਹੈ?

**Container Runtime Interface (CRI)** Kubernetes ਅਤੇ container runtime ਵਿਚਕਾਰ standard interface ਹੈ। ਇਸ ਨਾਲ kubelet runtime-specific implementation ਤੋਂ decouple ਰਹਿੰਦਾ ਹੈ।

## Request flow

```text
Kubernetes API Server
        |
      Scheduler
        |
      kubelet
        |
       CRI
        |
Container Runtime
        |
   Container / Pod
```

## Image lifecycle

ਜਦੋਂ Pod ਲਈ image ਚਾਹੀਦੀ ਹੈ, kubelet runtime ਨੂੰ image pull ਕਰਨ ਅਤੇ container lifecycle manage ਕਰਨ ਲਈ request ਕਰਦਾ ਹੈ। Runtime image ਨੂੰ local storage ਵਿੱਚ ਰੱਖ ਸਕਦਾ ਹੈ ਅਤੇ container create/start/stop ਕਰਦਾ ਹੈ।

## Useful troubleshooting

```bash
kubectl describe pod <pod-name>
```

ਜੇ `ImagePullBackOff` ਜਾਂ `ErrImagePull` ਮਿਲੇ ਤਾਂ image name/tag, registry access, credentials ਅਤੇ node network check ਕਰੋ।

Node ਉੱਤੇ runtime ਦੇ ਅਨੁਸਾਰ commands ਵੱਖ ਹੋ ਸਕਦੀਆਂ ਹਨ। ਉਦਾਹਰਨ ਲਈ containerd ਵਾਲੇ systems ਵਿੱਚ:

```bash
systemctl status containerd
journalctl -u containerd -f
```

## Important distinction

**CRI** interface ਹੈ; **containerd/CRI-O** implementation/runtime ਹਨ। Kubernetes ਨੂੰ runtime ਨਾਲ integrate ਕਰਨ ਲਈ CRI ਵਰਤਿਆ ਜਾਂਦਾ ਹੈ।
