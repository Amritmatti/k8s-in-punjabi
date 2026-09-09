# WordPress on OpenShift Sandbox

Hands-on lab for deploying **WordPress + MariaDB** on Red Hat OpenShift Sandbox and exposing WordPress publicly with an OpenShift **Route**.

> Learning lab only. This is not a production-ready WordPress architecture.

## Architecture

Internet -> OpenShift Route -> WordPress Service -> WordPress Pod -> MariaDB Service -> MariaDB Pod

Both applications use PersistentVolumeClaims (PVCs).

## Prerequisites

- OpenShift Sandbox account
- A Sandbox project/namespace
- `oc` CLI (recommended)
- A default StorageClass or another StorageClass available in the Sandbox

## 1. Login

Copy the login command from the OpenShift Sandbox console:

```bash
oc login <OPENSHIFT_API_URL> --token=<YOUR_TOKEN>
oc whoami
oc project
```

Never commit your token, kubeconfig, or real passwords to Git.

## 2. Create database credentials

Create one secret containing the variables required by MariaDB and WordPress:

```bash
oc create secret generic wordpress-db-secret \
  --from-literal=MARIADB_ROOT_PASSWORD='<CHOOSE_A_STRONG_ROOT_PASSWORD>' \
  --from-literal=MARIADB_PASSWORD='<CHOOSE_A_STRONG_DATABASE_PASSWORD>' \
  --from-literal=WORDPRESS_DATABASE_PASSWORD='<SAME_DATABASE_PASSWORD>'
```

The value of `MARIADB_PASSWORD` and `WORDPRESS_DATABASE_PASSWORD` must be identical.

## 3. Deploy MariaDB

```bash
oc apply -f mariadb.yaml
oc get pods -w
oc get pvc
```

Wait for the MariaDB pod to become `Running` and `Ready`.

## 4. Deploy WordPress

```bash
oc apply -f wordpress.yaml
oc get pods -w
```

Check:

```bash
oc get deployment
oc get svc
oc get pvc
```

## 5. Expose WordPress publicly

Create an OpenShift Route:

```bash
oc apply -f route.yaml
```

Get the public hostname:

```bash
oc get route wordpress
```

Or:

```bash
oc get route wordpress -o jsonpath='{.spec.host}{"\\n"}'
```

Open the returned hostname in your browser using HTTPS.

The Route uses edge TLS termination and redirects HTTP to HTTPS.

## 6. Finish WordPress setup

Open the public URL and complete the WordPress setup.

Set:

- Site title
- Administrator username
- Strong administrator password
- Administrator email

## 7. Verify

```bash
oc get pods
oc get svc
oc get route
oc get pvc
oc get deployment
```

View logs:

```bash
oc logs deployment/mariadb
oc logs deployment/wordpress
```

Check events:

```bash
oc get events --sort-by=.lastTimestamp
```

## Troubleshooting

### PVC is Pending

```bash
oc get storageclass
oc describe pvc mariadb-data
oc describe pvc wordpress-data
```

If the Sandbox does not provide a default StorageClass, add the appropriate `storageClassName` to the PVC manifests.

### WordPress is not ready

```bash
oc describe pod -l app=wordpress
oc logs deployment/wordpress
```

### MariaDB is not ready

```bash
oc describe pod -l app=mariadb
oc logs deployment/mariadb
```

### Route does not work

```bash
oc get route wordpress
oc get svc wordpress
oc get endpoints wordpress
oc get pods
```

The Route must point to the WordPress Service, and the Service must have ready endpoints.

## Clean up

```bash
oc delete -f route.yaml
oc delete -f wordpress.yaml
oc delete -f mariadb.yaml
oc delete secret wordpress-db-secret
```

Verify:

```bash
oc get all
oc get pvc
```

## What this lab teaches

- OpenShift Projects
- Deployments
- Pods
- Services
- Secrets
- PersistentVolumeClaims
- Environment variables
- Labels and selectors
- OpenShift Routes
- Public application exposure
- Application-to-database communication
- Basic OpenShift troubleshooting

## Next learning steps

1. ConfigMaps
2. Readiness and liveness probes
3. Resource requests and limits
4. NetworkPolicy
5. TLS certificates
6. HPA
7. ImageStreams
8. OpenShift Pipelines
9. GitHub Actions CI/CD
10. Production WordPress architecture
