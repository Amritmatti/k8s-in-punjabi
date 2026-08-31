# Lesson 03 — Control Plane Components

Kubernetes Control Plane ਨੂੰ cluster ਦਾ **ਦਿਮਾਗ** ਸਮਝੋ। ਇਹ API requests, cluster state, scheduling ਅਤੇ reconciliation coordinate ਕਰਦਾ ਹੈ।

## 1. kube-apiserver
ਇਹ Kubernetes ਦਾ central API endpoint ਹੈ। `kubectl`, controllers, scheduler ਅਤੇ ਹੋਰ clients ਇਸ ਨਾਲ communicate ਕਰਦੇ ਹਨ।

ਸੌਖੀ analogy: **API Server = Kubernetes ਦਾ front door**.

## 2. etcd
`etcd` distributed key-value store ਹੈ ਜੋ cluster ਦੀ persistent state ਰੱਖਦਾ ਹੈ।

ਸੌਖੀ analogy: **etcd = cluster ਦੀ master record book**.

## 3. kube-scheduler
ਨਵੇਂ unscheduled Pod ਲਈ suitable worker node ਚੁਣਦਾ ਹੈ। CPU/memory requests, node selectors, affinity, taints/tolerations ਅਤੇ ਹੋਰ constraints decision ਨੂੰ ਪ੍ਰਭਾਵਿਤ ਕਰ ਸਕਦੇ ਹਨ।

ਸੌਖੀ analogy: **Scheduler = ਕਿਹੜੇ worker ਨੂੰ ਕਿਹੜਾ ਕੰਮ ਦੇਣਾ ਹੈ**.

## 4. kube-controller-manager
Controllers desired state ਅਤੇ actual state ਨੂੰ continuously compare ਕਰਕੇ reconciliation ਕਰਦੇ ਹਨ।

Example: Deployment ਵਿੱਚ `replicas: 3` ਹੈ ਅਤੇ ਇੱਕ Pod delete ਹੋ ਗਿਆ, ਤਾਂ relevant controllers replacement workload ਬਣਾਉਣ ਦੀ process drive ਕਰਦੇ ਹਨ।

## 5. cloud-controller-manager
Cloud environments ਵਿੱਚ cloud-provider-specific logic, ਜਿਵੇਂ nodes, load balancers ਅਤੇ routes ਨਾਲ integration, manage ਕਰਨ ਵਿੱਚ ਮਦਦ ਕਰਦਾ ਹੈ।

## Flow

```text
kubectl / API client
        |
        v
  kube-apiserver
     /   |    \
    v    v     v
  etcd Scheduler Controllers
         |         |
         +----+----+
              |
              v
         Worker Nodes
```

## ਯਾਦ ਰੱਖੋ

- API Server = Front door
- etcd = State store
- Scheduler = Placement decision
- Controllers = Desired state reconciliation
- Cloud Controller = Cloud integration

ਅਗਲੇ lessons ਵਿੱਚ ਹਰ component ਨੂੰ independently deep dive ਕਰਾਂਗੇ।
