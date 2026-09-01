# Lesson 19 — Secrets

Kubernetes Secret sensitive values ਜਿਵੇਂ passwords, tokens ਅਤੇ keys ਨੂੰ API objects ਵਿੱਚ represent ਕਰਨ ਲਈ ਵਰਤੀ ਜਾਂਦੀ ਹੈ। Secret ਨੂੰ **automatically secure/encrypted** ਮੰਨਣਾ ਗਲਤ ਹੈ; cluster configuration ਅਤੇ access controls ਵੀ important ਹਨ।

## Example

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  USERNAME: demo
  PASSWORD: change-me
```

`stringData` plain text input ਨੂੰ Kubernetes API ਰਾਹੀਂ Secret data ਵਿੱਚ convert ਕਰਨ ਲਈ convenient ਹੈ। Real credentials ਨੂੰ Git repository ਵਿੱਚ commit ਨਾ ਕਰੋ।

## Environment variable

```yaml
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: app-secret
        key: PASSWORD
```

## Volume mount

```yaml
volumes:
  - name: secret-volume
    secret:
      secretName: app-secret
```

## Commands

```bash
kubectl create secret generic app-secret --from-literal=PASSWORD='change-me'
kubectl get secret app-secret
kubectl describe secret app-secret
```

Sensitive values inspect ਕਰਦੇ ਸਮੇਂ `kubectl get secret -o yaml` output ਨੂੰ casually share ਨਾ ਕਰੋ। Secret data commonly base64-encoded representation ਵਿੱਚ ਦਿਖ ਸਕਦੀ ਹੈ; **base64 encryption ਨਹੀਂ ਹੈ**।

## Production security

- Least-privilege RBAC ਦਿਓ।
- etcd encryption-at-rest configure ਕਰੋ ਜਿੱਥੇ required ਹੈ।
- Secrets ਨੂੰ Git ਵਿੱਚ plain text commit ਨਾ ਕਰੋ।
- External secret manager/KMS integrations ਜਿੱਥੇ appropriate ਹੋਣ use ਕਰੋ।
- Rotation strategy ਰੱਖੋ।

## ConfigMap vs Secret

| ConfigMap | Secret |
|---|---|
| Normal configuration | Sensitive values ਲਈ intended |
| Log level, feature flags | Passwords, tokens, keys |
| Encryption ਦਾ substitute ਨਹੀਂ | Base64 encryption ਨਹੀਂ ਹੈ |

## Interview

**Q: ਕੀ Kubernetes Secret encrypted ਹੁੰਦੀ ਹੈ?**

Default behavior ਅਤੇ cluster setup ਦੇ ਅਨੁਸਾਰ storage protection ਵੱਖ ਹੋ ਸਕਦੀ ਹੈ। Secret ਨੂੰ automatically encrypted-at-rest ਮੰਨ ਕੇ ਨਾ ਚੱਲੋ; etcd encryption-at-rest ਅਤੇ access controls explicitly configure/verify ਕਰੋ।
