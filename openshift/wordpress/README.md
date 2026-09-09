# WordPress on OpenShift Sandbox

Hands-on lab for deploying **WordPress + MariaDB** on Red Hat OpenShift Sandbox and exposing WordPress publicly with an OpenShift **Route**.

> Learning lab only. This is not a production-ready WordPress architecture.

## Architecture

Internet -> OpenShift Route -> WordPress Service :8080 -> WordPress Pod / Apache :8080 -> MariaDB Service :3306 -> MariaDB Pod

The WordPress container is built specifically for OpenShift's non-root security model. The standard WordPress Apache configuration listens on port 80, which can fail under the `restricted-v2` SCC because the container runs with a namespace-assigned non-root UID. This lab changes Apache to port 8080 instead. OpenShift Route still exposes the application externally over HTTPS.

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

## 4. Build the OpenShift-compatible WordPress image

The standard WordPress image starts Apache on port 80. OpenShift Sandbox normally runs workloads with the `restricted-v2` SCC and a namespace-assigned non-root UID, so this lab builds a small derived image that changes Apache to port 8080.

Apply the ImageStream and BuildConfig:

```bash
oc apply -f wordpress-build.yaml
```

Start the build:

```bash
oc start-build wordpress-openshift --follow
```

Verify the build and image:

```bash
oc get builds
oc get imagestream
oc get imagestreamtag wordpress-openshift:latest
```

## 5. Deploy WordPress

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

The WordPress pod should become `1/1 Running`.

## 6. Expose WordPress publicly

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

The Route uses edge TLS termination and redirects HTTP to HTTPS. The external connection uses HTTPS/443 while the Route sends traffic internally to the WordPress Service on port 8080.

## 7. Finish WordPress setup

Open the public URL and complete the WordPress setup.

Set:

- Site title
- Administrator username
- Strong administrator password
- Administrator email

## 8. Verify

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

### WordPress Apache reports `Permission denied` on port 80

This means the standard WordPress image is trying to bind Apache to privileged port 80 while running under the OpenShift non-root security model.

Rebuild the OpenShift-specific image:

```bash
oc start-build wordpress-openshift --follow
oc rollout restart deployment/wordpress
oc rollout status deployment/wordpress
```

Verify the container is using port 8080:

```bash
oc get pod -l app=wordpress -o yaml | grep -A3 containerPort
```

Do **not** grant the application the `privileged` SCC just to make Apache use port 80. Using an unprivileged application port is the preferred approach for this lab.

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
oc delete -f wordpress-build.yaml
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
- ImageStreams
- BuildConfigs
- OpenShift Routes
- Non-root container operation
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
7. OpenShift Pipelines
8. GitHub Actions CI/CD
9. Production WordPress architecture
