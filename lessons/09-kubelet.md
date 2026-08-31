# Lesson 09 — kubelet

`kubelet` ਹਰ worker node ਉੱਤੇ ਚੱਲਣ ਵਾਲਾ primary Kubernetes node agent ਹੈ। ਇਹ ensure ਕਰਨ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰਦਾ ਹੈ ਕਿ node ਉੱਤੇ configured Pods ਦੇ containers expected state ਵਿੱਚ ਚੱਲ ਰਹੇ ਹੋਣ।

## Flow

```text
API Server
    |
    v
  kubelet
    |
    +--> Container Runtime
    |
    +--> Pod containers
```

kubelet API Server ਤੋਂ Pod-related information ਲੈਂਦਾ ਹੈ ਅਤੇ local node ਉੱਤੇ runtime ਨਾਲ coordinate ਕਰਦਾ ਹੈ।

## kubelet ਕੀ ਨਹੀਂ ਕਰਦਾ?

- ਇਹ scheduler ਨਹੀਂ ਹੈ।
- ਇਹ application-level business logic ਨਹੀਂ ਚਲਾਉਂਦਾ।
- ਇਹ cluster ਦਾ persistent database ਨਹੀਂ ਹੈ।

## Useful commands

Node ਉੱਤੇ systemd ਵਾਲੇ installations ਵਿੱਚ:

```bash
systemctl status kubelet
journalctl -u kubelet -f
```

Cluster ਤੋਂ:

```bash
kubectl describe node <node-name>
kubectl get pods -A -o wide
```

## Troubleshooting

ਜੇ node `NotReady` ਹੈ ਤਾਂ ਪਹਿਲਾਂ:

```bash
kubectl get nodes
kubectl describe node <node-name>
```

ਫਿਰ node ਉੱਤੇ kubelet logs ਅਤੇ container runtime health check ਕਰੋ। CNI/network, certificates, disk pressure, memory pressure ਅਤੇ runtime errors ਵੀ investigate ਕਰੋ।

## ਯਾਦ ਰੱਖੋ

**Scheduler decides where. kubelet makes sure the workload runs on that node.**
