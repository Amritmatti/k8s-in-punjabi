# Lesson 08 — Worker Node

Worker Node ਉਹ machine ਹੈ ਜਿੱਥੇ application workloads ਦੇ Pods ਚੱਲਦੇ ਹਨ। ਇੱਕ node physical server, VM ਜਾਂ cloud instance ਹੋ ਸਕਦਾ ਹੈ।

## Main components

```text
Worker Node
├── kubelet
├── container runtime
├── kube-proxy (when used)
└── Pods
```

### kubelet
Node ਦਾ Kubernetes agent। ਇਹ API Server ਨਾਲ node ਅਤੇ Pod lifecycle information exchange ਕਰਦਾ ਹੈ ਅਤੇ configured workloads ਨੂੰ run ਕਰਨ ਲਈ container runtime ਨਾਲ coordinate ਕਰਦਾ ਹੈ।

### Container runtime
Container images pull ਕਰਕੇ containers create/start/stop ਕਰਦਾ ਹੈ। Kubernetes runtime ਨਾਲ CRI ਰਾਹੀਂ interact ਕਰਦਾ ਹੈ। Common runtimes ਵਿੱਚ containerd ਅਤੇ CRI-O ਸ਼ਾਮਲ ਹਨ।

### kube-proxy
Kubernetes Services ਲਈ node-level network rules maintain ਕਰਨ ਵਿੱਚ ਮਦਦ ਕਰਦਾ ਹੈ। Modern clusters ਵਿੱਚ networking implementation ਦੇ ਅਨੁਸਾਰ kube-proxy ਦੀ ਭੂਮਿਕਾ ਵੱਖ ਹੋ ਸਕਦੀ ਹੈ।

## Node inspect ਕਰੋ

```bash
kubectl get nodes -o wide
kubectl describe node <node-name>
kubectl get pods -A -o wide
```

## Capacity vs Allocatable

Node ਦੀ total capacity ਅਤੇ Kubernetes workloads ਲਈ allocatable resources ਇੱਕੋ ਚੀਜ਼ ਨਹੀਂ ਹਨ। System daemons ਅਤੇ reservations resources consume ਕਰ ਸਕਦੇ ਹਨ।

## Interview

**Q: Pod worker node ਉੱਤੇ ਕਿਵੇਂ ਚੱਲਦਾ ਹੈ?**

API Server object accept ਕਰਦਾ ਹੈ → Scheduler node select ਕਰਦਾ ਹੈ → kubelet ਉਸ node ਉੱਤੇ Pod specification observe ਕਰਦਾ ਹੈ → container runtime containers start ਕਰਦਾ ਹੈ।
