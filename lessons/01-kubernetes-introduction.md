# Lesson 01 — Kubernetes ਕੀ ਹੈ? ☸️

## Kubernetes ਨੂੰ ਬਿਲਕੁਲ simple ਤਰੀਕੇ ਨਾਲ ਸਮਝੋ

ਮੰਨ ਲਓ ਤੁਹਾਡੀ ਇੱਕ web application ਹੈ। Application ਨੂੰ Docker containers ਵਿੱਚ ਚਲਾਇਆ ਗਿਆ ਹੈ। ਸ਼ੁਰੂ ਵਿੱਚ 1 container manage ਕਰਨਾ ਆਸਾਨ ਹੈ। ਪਰ ਜਦੋਂ 10, 100 ਜਾਂ 1000 containers ਹੋ ਜਾਣ ਤਾਂ questions ਆਉਂਦੇ ਹਨ:

- Container crash ਹੋ ਜਾਵੇ ਤਾਂ ਕੌਣ restart ਕਰੇਗਾ?
- Traffic ਵੱਧ ਜਾਵੇ ਤਾਂ containers ਕਿਵੇਂ ਵਧਣਗੇ?
- ਨਵਾਂ application version safely ਕਿਵੇਂ deploy ਹੋਵੇਗਾ?
- ਇੱਕ container ਤੋਂ ਦੂਜੇ container ਤੱਕ traffic ਕਿਵੇਂ ਜਾਵੇਗਾ?
- Container ਕਿਸ machine ਉੱਤੇ ਚੱਲੇ?

ਇਹਨਾਂ problems ਨੂੰ automate ਕਰਨ ਲਈ Kubernetes ਵਰਤਿਆ ਜਾਂਦਾ ਹੈ।

## Kubernetes ਕੀ ਕਰਦਾ ਹੈ?

Kubernetes containers ਦਾ **orchestrator** ਹੈ। ਇਹ desired state ਨੂੰ maintain ਕਰਨ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰਦਾ ਹੈ।

Example:

> ਤੁਸੀਂ Kubernetes ਨੂੰ ਕਿਹਾ: “ਮੇਰੀ application ਦੀਆਂ 3 replicas ਚੱਲਣੀਆਂ ਚਾਹੀਦੀਆਂ ਹਨ।”

ਜੇ ਇੱਕ Pod crash ਹੋ ਗਿਆ ਅਤੇ ਸਿਰਫ਼ 2 ਰਹਿ ਗਏ, Kubernetes controllers ਇੱਕ ਨਵਾਂ Pod ਬਣਾਉਣ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰਨਗੇ ਤਾਂ ਜੋ desired count ਮੁੜ 3 ਹੋ ਜਾਵੇ।

## Cluster

Kubernetes ਦਾ environment **cluster** ਕਿਹਾ ਜਾਂਦਾ ਹੈ। ਇੱਕ cluster ਵਿੱਚ broadly ਦੋ roles ਹੁੰਦੇ ਹਨ:

### 1. Control Plane

ਇਹ cluster ਦਾ ਦਿਮਾਗ ਹੈ। ਇਹ decisions ਅਤੇ cluster state manage ਕਰਦਾ ਹੈ।

ਮੁੱਖ components:

- kube-apiserver — Kubernetes ਦੀ central API
- etcd — cluster state ਦਾ key-value database
- kube-scheduler — Pod ਲਈ suitable node ਚੁਣਦਾ ਹੈ
- kube-controller-manager — controllers ਚਲਾਉਂਦਾ ਹੈ

### 2. Worker Node

ਇੱਥੇ application workloads ਚੱਲਦੇ ਹਨ। ਮੁੱਖ components:

- kubelet — node ਉੱਤੇ Pods ਦੀ lifecycle manage ਕਰਦਾ ਹੈ
- container runtime — containers ਚਲਾਉਂਦਾ ਹੈ
- kube-proxy — Service networking ਲਈ traditional node-level component

## kubectl ਕੀ ਹੈ?

`kubectl` Kubernetes cluster ਨਾਲ ਗੱਲ ਕਰਨ ਲਈ command-line tool ਹੈ।

```bash
kubectl get nodes
kubectl get pods -A
kubectl get namespaces
```

ਆਮ flow:

```text
You
  |
  | kubectl
  v
kube-apiserver
  |
  +---- etcd
  +---- scheduler
  +---- controllers
  |
  v
Worker Node
  |
  +---- kubelet
  +---- container runtime
  |
  v
Pod
```

## ਪਹਿਲੀ practice

ਜੇ ਤੁਹਾਡੇ ਕੋਲ Kubernetes cluster available ਹੈ:

```bash
kubectl run nginx --image=nginx
kubectl get pods
kubectl describe pod nginx
kubectl delete pod nginx
```

## ਯਾਦ ਰੱਖੋ

**Kubernetes = containers ਨੂੰ production ਵਿੱਚ deploy, manage, scale, network ਅਤੇ recover ਕਰਨ ਲਈ orchestration platform.**

ਅਗਲੇ lesson ਵਿੱਚ ਅਸੀਂ **Kubernetes Cluster Architecture** ਨੂੰ component-by-component ਸਮਝਾਂਗੇ।
