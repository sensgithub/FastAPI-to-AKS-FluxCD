# Create .env file for variables for PostgreSQL
```
DATABASE_URL=postgres:[PASSWORD]@[URL]:5432/fastapi
POSTGRES_USER=postgres
POSTGRES_PASSWORD=[PASSWORD]
POSTGRES_DB=[DB_NAME]
```
# Commit to the Github repository

! Before Commit and deployment to Azure:

1. Make an App Registration
2. Give it Contributor access to the Subscription

# Trigger CI from commit
   - Dockerize the application
   - Build & deploy to AKS 

# Configure Service Principal & RBAC for FluxCD
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: [FLUX-APPLIER_NAME]
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: [FLUX-APPLIER_NAME]-role
rules:
- apiGroups: [""]  # Core API group
  resources: ["services", "configmaps", "secrets", "persistentvolumeclaims"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: [FLUX-APPLIER_NAME]-binding
subjects:
- kind: ServiceAccount
  name: [FLUX-APPLIER_NAME]
  namespace: default
roleRef:
  kind: ClusterRole
  name: [FLUX-APPLIER_NAME]-role
  apiGroup: rbac.authorization.k8s.io
```
# Access the app using service's URL:Port

![FastAPI Example](https://github.com/sensgithub/bakdata-task/blob/main/screenshots/fastapi-example.png?raw=true)
