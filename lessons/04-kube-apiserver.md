# Lesson 04 — kube-apiserver Deep Dive

`kube-apiserver` Kubernetes ਦੀ central API boundary ਹੈ।

## Request flow

```text
kubectl
  |
  v
kube-apiserver
  |
  +--> Authentication
  +--> Authorization
  +--> Admission
  +--> API validation
  |
  +--> persist/read state via etcd
  |
  v
Response
```

### Authentication
Request ਕਿਸ identity ਤੋਂ ਆਈ ਹੈ, ਇਹ establish ਕੀਤਾ ਜਾਂਦਾ ਹੈ। Kubernetes certificates, service-account tokens ਅਤੇ external identity integrations ਵਰਗੇ mechanisms support ਕਰ ਸਕਦਾ ਹੈ।

### Authorization
Identity ਨੂੰ requested verb/resource/namespace ਲਈ permission ਹੈ ਜਾਂ ਨਹੀਂ? RBAC ਇੱਕ common authorization mechanism ਹੈ।

```text
User: dev-user
Verb: get
Resource: pods
Namespace: production
```

### Admission
Admission controls object ਨੂੰ validate ਜਾਂ mutate ਕਰ ਸਕਦੇ ਹਨ ਅਤੇ policies enforce ਕਰ ਸਕਦੇ ਹਨ।

### etcd
API Server Kubernetes state ਨੂੰ etcd ਵਿੱਚ persist ਕਰਦਾ ਹੈ। Clients ਨੂੰ etcd directly expose ਨਹੀਂ ਕਰਨਾ ਚਾਹੀਦਾ।

## Practice

```bash
kubectl create deployment nginx --image=nginx --replicas=3
kubectl get deployment nginx -o yaml
kubectl get pods -l app=nginx
```

## Troubleshooting

```bash
kubectl cluster-info
kubectl get --raw=/version
kubectl get --raw=/readyz?verbose
```

**Key point:** `kubectl` ਆਮ ਤੌਰ ਤੇ API Server ਨਾਲ ਗੱਲ ਕਰਦਾ ਹੈ; API Server cluster operations ਦੀ central gateway ਹੈ।
