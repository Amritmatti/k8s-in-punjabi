# Lesson 14 — Service

Pods ephemeral ਹੁੰਦੇ ਹਨ ਅਤੇ ਉਹਨਾਂ ਦੇ IP addresses change ਹੋ ਸਕਦੇ ਹਨ। **Service** stable network endpoint ਦਿੰਦੀ ਹੈ ਅਤੇ matching Pods ਤੱਕ traffic route ਕਰਨ ਵਿੱਚ ਮਦਦ ਕਰਦੀ ਹੈ।

## Basic ClusterIP Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP
```

## Selector ਕਿਵੇਂ ਕੰਮ ਕਰਦਾ ਹੈ?

Service ਦਾ:

```yaml
selector:
  app: nginx
```

ਉਹ Pods select ਕਰਦਾ ਹੈ ਜਿਨ੍ਹਾਂ ਉੱਤੇ `app=nginx` label ਹੈ।

## Traffic flow

```text
Client Pod
   |
   v
Service:80
   |
   +----> Pod A:80
   +----> Pod B:80
   +----> Pod C:80
```

Service ਆਪ application process ਨਹੀਂ ਚਲਾਉਂਦੀ; ਇਹ stable virtual endpoint ਅਤੇ service discovery/load-distribution mechanism provide ਕਰਦੀ ਹੈ।

## Service types

### ClusterIP
Cluster ਦੇ ਅੰਦਰ reachable virtual IP। ਇਹ default type ਹੈ।

### NodePort
ਹਰ eligible node ਉੱਤੇ ਇੱਕ port expose ਕਰਕੇ external traffic ਨੂੰ Service ਤੱਕ ਲਿਆ ਸਕਦਾ ਹੈ।

### LoadBalancer
Cloud/provider integration ਨਾਲ external load balancer provision ਕਰਨ ਲਈ ਵਰਤੀ ਜਾ ਸਕਦੀ ਹੈ। Exact behavior environment ਉੱਤੇ depend ਕਰਦਾ ਹੈ।

### ExternalName
DNS CNAME-style mapping provide ਕਰਦਾ ਹੈ; ਇਸਦੀ behavior ClusterIP service ਤੋਂ ਵੱਖਰੀ ਹੈ।

## Commands

```bash
kubectl apply -f examples/service.yaml
kubectl get svc
kubectl describe svc nginx
kubectl get endpointslice
```

## Troubleshooting

ਜੇ Service traffic ਨਹੀਂ ਦੇ ਰਹੀ:

```bash
kubectl get svc nginx -o yaml
kubectl get pods --show-labels
kubectl get endpointslice -l kubernetes.io/service-name=nginx
```

ਸਭ ਤੋਂ ਪਹਿਲਾਂ selector ਅਤੇ Pod labels match ਕਰਦੇ ਹਨ ਜਾਂ ਨਹੀਂ check ਕਰੋ, ਫਿਰ targetPort ਅਤੇ application listening port verify ਕਰੋ।

## Interview

**Q: Service ਦੀ ਲੋੜ ਕਿਉਂ ਹੈ?**

Pods replace/recreate ਹੋਣ ਨਾਲ IP ਬਦਲ ਸਕਦਾ ਹੈ। Service stable discovery endpoint ਦਿੰਦੀ ਹੈ ਅਤੇ matching backend Pods ਤੱਕ traffic distribute ਕਰ ਸਕਦੀ ਹੈ।
