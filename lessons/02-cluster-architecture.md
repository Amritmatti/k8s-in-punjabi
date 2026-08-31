# Lesson 02 — Kubernetes Cluster Architecture 🏗️

Kubernetes cluster ਨੂੰ ਇੱਕ company ਵਾਂਗ ਸੋਚੋ। **Control Plane management team** ਹੈ ਅਤੇ **Worker Nodes actual workers** ਹਨ।

## Control Plane

### kube-apiserver
ਇਹ Kubernetes ਦਾ front door ਹੈ। `kubectl` ਅਤੇ ਹੋਰ clients API Server ਨੂੰ requests ਭੇਜਦੇ ਹਨ। Authentication, authorization ਅਤੇ admission ਤੋਂ ਬਾਅਦ request process ਹੁੰਦੀ ਹੈ।

Example:

```bash
kubectl get pods
```

ਇਸ command ਵਿੱਚ kubectl API Server ਨਾਲ communicate ਕਰਦਾ ਹੈ।

### etcd
`etcd` ਇੱਕ consistent, highly-available key-value store ਹੈ ਜਿਸ ਵਿੱਚ Kubernetes ਦਾ cluster state ਰੱਖਿਆ ਜਾਂਦਾ ਹੈ। ਇਸਨੂੰ cluster ਦੀ **state memory** ਸਮਝੋ।

### kube-scheduler
ਜਦੋਂ ਇੱਕ ਨਵਾਂ Pod ਬਣਦਾ ਹੈ ਅਤੇ ਉਸ ਲਈ node assign ਨਹੀਂ ਹੋਇਆ, scheduler available nodes ਨੂੰ evaluate ਕਰਕੇ suitable node ਚੁਣਦਾ ਹੈ। Resources, constraints, affinity/anti-affinity ਅਤੇ ਹੋਰ scheduling rules decision ਨੂੰ ਪ੍ਰਭਾਵਿਤ ਕਰ ਸਕਦੇ ਹਨ।

### kube-controller-manager
ਇਹ controllers ਦਾ collection ਚਲਾਉਂਦਾ ਹੈ। Controllers actual state ਨੂੰ desired state ਦੇ ਨੇੜੇ ਲਿਆਉਣ ਲਈ continuously observe ਅਤੇ act ਕਰਦੇ ਹਨ।

Example: Deployment ਦੀ desired replicas 3 ਹਨ ਪਰ currently 2 Pods ਹਨ — controllers missing workload create ਕਰਨ ਦੀ process initiate ਕਰਦੇ ਹਨ।

## Worker Node

### kubelet
ਹਰ node ਉੱਤੇ agent। ਇਹ API Server ਤੋਂ Pod specifications ਨਾਲ related information ਲੈਂਦਾ ਹੈ ਅਤੇ ensure ਕਰਦਾ ਹੈ ਕਿ defined containers ਚੱਲ ਰਹੇ ਹਨ ਅਤੇ healthy state maintain ਕਰਨ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰਦਾ ਹੈ।

### Container Runtime
ਇਹ actual containers run ਕਰਦਾ ਹੈ। Kubernetes ਵਿੱਚ CRI-compatible runtime ਵਰਤਿਆ ਜਾਂਦਾ ਹੈ, ਜਿਵੇਂ containerd ਜਾਂ CRI-O।

### kube-proxy
Node ਉੱਤੇ Kubernetes Service ਦੇ networking rules implement ਕਰਨ ਲਈ ਵਰਤਿਆ ਜਾਣ ਵਾਲਾ component ਹੈ। ਕੁਝ modern networking implementations kube-proxy ਨੂੰ replace ਵੀ ਕਰ ਸਕਦੀਆਂ ਹਨ।

## Complete flow

```text
kubectl
   |
   v
API Server
   |
   +--------> etcd (state)
   |
   +--------> Scheduler
   |
   +--------> Controllers
   |
   v
Selected Worker Node
   |
   +--> kubelet
   |
   +--> Container Runtime
   |
   +--> Pod
```

## Hands-on

```bash
kubectl get nodes -o wide
kubectl get pods -A -o wide
kubectl get componentstatuses
```

> ਨੋਟ: `componentstatuses` modern Kubernetes versions ਵਿੱਚ deprecated/removed ਹੋ ਸਕਦਾ ਹੈ। Cluster health ਲਈ ਆਪਣੇ Kubernetes version ਦੇ supported commands ਅਤੇ API resources ਵਰਤੋ।

## ਯਾਦ ਰੱਖੋ

- **API Server = Front door**
- **etcd = Cluster state store**
- **Scheduler = Pod placement decision**
- **Controllers = Desired state maintain ਕਰਨ ਵਾਲੇ loops**
- **kubelet = Node agent**
- **Runtime = Containers ਚਲਾਉਂਦਾ ਹੈ**

ਅਗਲੇ lessons ਵਿੱਚ ਹਰ component ਨੂੰ ਹੋਰ deep level ਤੇ code, API requests ਅਤੇ real request flows ਨਾਲ ਸਮਝਾਂਗੇ।
