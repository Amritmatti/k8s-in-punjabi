# Lesson 15 — Service Types & Service Discovery

Service ਦੇ types ਨੂੰ clear ਕਰਨਾ Kubernetes networking ਸਮਝਣ ਲਈ important ਹੈ।

## 1. ClusterIP

```yaml
spec:
  type: ClusterIP
```

Cluster ਦੇ ਅੰਦਰ applications ਲਈ stable virtual endpoint।

## 2. NodePort

```yaml
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30080
```

Node ਦੇ exposed port ਰਾਹੀਂ traffic Service ਤੱਕ ਆ ਸਕਦਾ ਹੈ। Production ਵਿੱਚ direct NodePort ਦੀ ਬਜਾਏ load balancer/Ingress architecture ਅਕਸਰ ਵਰਤਿਆ ਜਾਂਦਾ ਹੈ।

## 3. LoadBalancer

```yaml
spec:
  type: LoadBalancer
```

Supported cloud/provider environment ਵਿੱਚ external load balancer provision ਕਰਨ ਲਈ integration trigger ਕਰ ਸਕਦੀ ਹੈ।

## 4. ExternalName

External service ਲਈ DNS-based alias provide ਕਰਦਾ ਹੈ। ਇਸ ਵਿੱਚ normal ClusterIP backend behavior ਨਹੀਂ ਹੁੰਦਾ।

## Service discovery

Cluster ਵਿੱਚ applications Service ਨੂੰ DNS name ਰਾਹੀਂ discover ਕਰ ਸਕਦੀਆਂ ਹਨ। Typical name:

```text
<service>.<namespace>.svc.cluster.local
```

Example:

```text
nginx.default.svc.cluster.local
```

## Debugging

```bash
kubectl get svc
kubectl get endpointslice
kubectl run dns-test --image=busybox:1.36 -it --rm --restart=Never -- nslookup nginx
```

ਜੇ DNS resolve ਨਹੀਂ ਹੋ ਰਿਹਾ ਤਾਂ CoreDNS health ਅਤੇ Pod DNS configuration ਵੀ check ਕਰੋ।

## Key distinction

**Service = stable virtual endpoint. DNS = name resolution. Endpoints/EndpointSlices = backend addresses associated with the Service.**
