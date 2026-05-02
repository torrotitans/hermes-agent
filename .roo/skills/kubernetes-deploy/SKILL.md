---
name: kubernetes-deploy
description: Deploy and manage applications on Kubernetes with manifests, deployments, services, ConfigMaps, Secrets, and Helm charts. USE FOR: kubectl apply, k8s manifests, deployments, services, ingress, configmap, secrets, helm charts, kubernetes debugging, pod scaling, rolling updates, resource limits, kubernetes troubleshooting. DO NOT USE FOR: Docker container build (use docker-container skill), infrastructure provisioning (use terraform skill), cloud-specific services (use cloud-provider skills).
---

# Kubernetes Deploy Skill

## When to Use
- Deploying applications to Kubernetes clusters
- Creating/updating Kubernetes manifests
- Managing deployments, services, ingress
- Configuring ConfigMaps and Secrets
- Helm chart creation and deployment
- Scaling applications (HPA)
- Rolling updates and rollbacks
- Debugging pod issues

## When NOT to Use
- Building Docker images (use docker-container skill)
- Infrastructure provisioning (use terraform skill)
- Cloud-specific managed services (use aws-eks, azure-aks, gcp-gke skills)

## Inputs Required
- Application container image
- Namespace (default: default)
- Resource requirements (CPU, memory)
- Environment variables
- Service type (ClusterIP, NodePort, LoadBalancer)
- Ingress configuration (if external access needed)

## Workflow

### 1. Create Kubernetes Namespace
```yaml
# manifests/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: torro-app
  labels:
    app: torro
```

Apply:
```bash
kubectl apply -f manifests/namespace.yaml
```

### 2. Create ConfigMap
```yaml
# manifests/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: torro-config
  namespace: torro-app
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
  DATABASE_HOST: "postgres-service"
  REDIS_HOST: "redis-service"
```

### 3. Create Secret
```yaml
# manifests/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: torro-secret
  namespace: torro-app
type: Opaque
stringData:
  DATABASE_PASSWORD: "secure_password"
  API_KEY: "api_key_value"
```

Or use kubectl:
```bash
kubectl create secret generic torro-secret \
  --from-literal=DATABASE_PASSWORD=secure_password \
  --from-literal=API_KEY=api_key_value \
  -n torro-app
```

### 4. Create Deployment
```yaml
# manifests/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: torro-app
  namespace: torro-app
  labels:
    app: torro
spec:
  replicas: 3
  selector:
    matchLabels:
      app: torro
  template:
    metadata:
      labels:
        app: torro
    spec:
      containers:
      - name: torro-app
        image: torro-app:latest
        ports:
        - containerPort: 5000
        env:
        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: torro-config
              key: APP_ENV
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: torro-secret
              key: DATABASE_PASSWORD
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 5. Create Service
```yaml
# manifests/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: torro-service
  namespace: torro-app
spec:
  selector:
    app: torro
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: ClusterIP
```

For external access:
```yaml
# manifests/service-loadbalancer.yaml
apiVersion: v1
kind: Service
metadata:
  name: torro-service-external
  namespace: torro-app
spec:
  selector:
    app: torro
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

### 6. Create Ingress
```yaml
# manifests/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: torro-ingress
  namespace: torro-app
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: torro.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: torro-service
            port:
              number: 80
```

### 7. Create HorizontalPodAutoscaler
```yaml
# manifests/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: torro-hpa
  namespace: torro-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: torro-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
```

### 8. Apply All Manifests
```bash
kubectl apply -f manifests/namespace.yaml
kubectl apply -f manifests/configmap.yaml
kubectl apply -f manifests/secret.yaml
kubectl apply -f manifests/deployment.yaml
kubectl apply -f manifests/service.yaml
kubectl apply -f manifests/ingress.yaml
kubectl apply -f manifests/hpa.yaml
```

Or apply all at once:
```bash
kubectl apply -f manifests/
```

## Helm Chart Structure

### Chart.yaml
```yaml
apiVersion: v2
name: torro-app
description: Torro Application Helm Chart
type: application
version: 0.1.0
appVersion: "1.0.0"
```

### values.yaml
```yaml
replicaCount: 3

image:
  repository: torro-app
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  host: torro.example.com

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

### templates/deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-app
  labels:
    app: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}
    spec:
      containers:
      - name: {{ .Release.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: 5000
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
```

### Deploy with Helm
```bash
# Install
helm install torro-release ./torro-app -n torro-app

# Upgrade
helm upgrade torro-release ./torro-app -n torro-app

# Uninstall
helm uninstall torro-release -n torro-app

# Status
helm status torro-release -n torro-app
```

## Kubernetes Lifecycle Commands

| Command | Purpose |
| :--- | :--- |
| `kubectl get pods -n <namespace>` | List pods |
| `kubectl get deployments -n <namespace>` | List deployments |
| `kubectl get services -n <namespace>` | List services |
| `kubectl describe pod <pod> -n <namespace>` | Detailed pod info |
| `kubectl logs <pod> -n <namespace>` | View pod logs |
| `kubectl exec -it <pod> -n <namespace> -- bash` | Execute in pod |
| `kubectl scale deployment <name> --replicas=5 -n <namespace>` | Scale deployment |
| `kubectl rollout status deployment <name> -n <namespace>` | Check rollout status |
| `kubectl rollout undo deployment <name> -n <namespace>` | Rollback deployment |
| `kubectl delete pod <pod> -n <namespace>` | Delete pod |

## Troubleshooting

### Pod Not Starting
```bash
# Check pod status
kubectl describe pod <pod-name> -n <namespace>

# View logs
kubectl logs <pod-name> -n <namespace>
```

### Common Issues

| Issue | Solution |
| :--- | :--- |
| ImagePullBackOff | Check image name/tag, verify registry access |
| CrashLoopBackOff | Check logs, verify app starts correctly |
| Pending | Check resource quotas, node capacity |
| OOMKilled | Increase memory limits |

### Debug Commands
```bash
# Check events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Check resource usage
kubectl top pods -n <namespace>

# Port forward for local debugging
kubectl port-forward svc/torro-service 8080:80 -n <namespace>
```

## Examples

### Example 1: Simple Flask App Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask
  template:
    spec:
      containers:
      - name: flask
        image: flask-app:latest
        ports:
        - containerPort: 5000
```

### Example 2: StatefulSet for Database
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    spec:
      containers:
      - name: postgres
        image: postgres:17
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

## References
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Helm Documentation](https://helm.sh/docs/)
