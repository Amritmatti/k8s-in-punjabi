# Lesson 18 — ConfigMap

ConfigMap application configuration ਨੂੰ container image ਤੋਂ ਵੱਖ ਰੱਖਣ ਲਈ Kubernetes resource ਹੈ। Non-sensitive values ਲਈ ਵਰਤੋ। Passwords/API keys ਲਈ Secret ਵਰਤੋ।

## Create

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: production
  LOG_LEVEL: info
```

## Environment variable

```yaml
envFrom:
  - configMapRef:
      name: app-config
```

## File ਵਜੋਂ mount

```yaml
volumes:
  - name: config
    configMap:
      name: app-config
```

```yaml
volumeMounts:
  - name: config
    mountPath: /etc/app
    readOnly: true
```

## Commands

```bash
kubectl create configmap app-config --from-literal=APP_ENV=production
kubectl get configmap app-config -o yaml
kubectl describe configmap app-config
```

## Important

ConfigMap **secret store ਨਹੀਂ ਹੈ**। Base64 encoding ਨੂੰ encryption ਨਾ ਸਮਝੋ। Sensitive data ਲਈ Secret ਅਤੇ appropriate encryption/access controls ਵਰਤੋ।

## Interview

**Q: ConfigMap ਕਿਉਂ?** Application configuration ਨੂੰ image rebuild ਕੀਤੇ ਬਿਨਾਂ environment-specific ਤਰੀਕੇ ਨਾਲ inject ਕਰਨ ਲਈ।
