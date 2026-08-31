# Lesson 16 — DNS & CoreDNS

Kubernetes ਵਿੱਚ Service ਨੂੰ IP ਯਾਦ ਰੱਖਣ ਦੀ ਬਜਾਏ DNS name ਨਾਲ access ਕਰਨਾ convenient ਹੈ। Cluster DNS service discovery provide ਕਰਦਾ ਹੈ।

## Flow

```text
Frontend Pod
    |
    | backend.production.svc.cluster.local
    v
CoreDNS
    |
    v
Service -> backend Pods
```

## Typical DNS names

Same namespace:

```text
http://backend
```

Different namespace:

```text
http://backend.production
```

Full cluster DNS name:

```text
backend.production.svc.cluster.local
```

## CoreDNS

CoreDNS cluster DNS service ਹੈ। ਇਹ Kubernetes Services ਅਤੇ ਹੋਰ supported DNS records ਲਈ name resolution provide ਕਰਦਾ ਹੈ।

```bash
kubectl get pods -n kube-system
kubectl get svc -n kube-system
```

## DNS troubleshooting

```bash
kubectl run dns-test --image=busybox:1.36 -it --rm --restart=Never -- nslookup kubernetes.default
kubectl exec -it <pod-name> -- cat /etc/resolv.conf
```

ਜੇ Service name resolve ਨਹੀਂ ਹੁੰਦਾ ਤਾਂ namespace, Service name, CoreDNS Pods, CoreDNS logs ਅਤੇ network policies check ਕਰੋ।

## Important

DNS name resolution ਅਤੇ Service traffic routing ਇੱਕੋ ਚੀਜ਼ ਨਹੀਂ ਹਨ। DNS ਨਾਮ ਨੂੰ address ਵਿੱਚ resolve ਕਰਦਾ ਹੈ; Service backend endpoints ਤੱਕ traffic route ਕਰਨ ਦਾ abstraction ਦਿੰਦੀ ਹੈ।

## Interview

**Q: `my-service.default.svc.cluster.local` ਵਿੱਚ `default` ਕੀ ਹੈ?**

ਇਹ Service ਦਾ namespace ਹੈ। `svc` Kubernetes Service DNS hierarchy ਦਾ ਹਿੱਸਾ ਹੈ ਅਤੇ ਅਖੀਰਲਾ domain cluster DNS suffix ਹੁੰਦਾ ਹੈ।
