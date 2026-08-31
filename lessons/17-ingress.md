# Lesson 17 — Ingress

Ingress HTTP/HTTPS traffic ਨੂੰ cluster ਦੇ Services ਵੱਲ route ਕਰਨ ਲਈ API object ਹੈ। Ingress resource ਨੂੰ implement ਕਰਨ ਲਈ **Ingress Controller** ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ।

## Architecture

```text
Internet
   |
   v
Load Balancer
   |
   v
Ingress Controller
   |
   +---- /api ----> api-service
   |
   +---- /web ----> web-service
```

## Example

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web
                port:
                  number: 80
```

ਇਹ routing rule define ਕਰਦਾ ਹੈ; DNS record ਅਤੇ Ingress Controller ਦਾ deployment ਵੱਖਰੇ concerns ਹਨ।

## TLS

HTTPS ਲਈ Ingress ਵਿੱਚ TLS configuration ਅਤੇ certificate Secret use ਕੀਤਾ ਜਾ ਸਕਦਾ ਹੈ:

```yaml
spec:
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
```

## Ingress vs Service

- Service = cluster networking ਦਾ stable endpoint
- Ingress = HTTP/HTTPS routing rules
- Ingress Controller = rules ਨੂੰ actual proxy/load-balancing behavior ਵਿੱਚ implement ਕਰਦਾ ਹੈ

## Troubleshooting

```bash
kubectl get ingress
kubectl describe ingress app-ingress
kubectl get svc
kubectl get pods -A
```

Check ਕਰੋ: DNS → external load balancer → controller → Ingress rules → Service → backend endpoints।

## Modern note

Kubernetes ecosystem ਵਿੱਚ Gateway API ਵੀ modern traffic-routing model ਹੈ। Ingress ਅਜੇ ਵੀ widely used ਹੈ ਅਤੇ fundamentals ਲਈ ਜਾਣਨਾ important ਹੈ।
