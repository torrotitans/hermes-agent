---
name: docker-container
description: Build, manage, and deploy Docker containers with multi-stage builds, Docker Compose, and container lifecycle management. USE FOR: docker build, docker run, docker compose, containerize application, Dockerfile, multi-stage build, container lifecycle, image optimization, container networking, volume management, container debugging, production container. DO NOT USE FOR: Kubernetes orchestration (use kubernetes-deploy skill), container registry management (use docker-registry skill).
---

# Docker Container Skill

## When to Use
- Building Docker images from Dockerfile
- Running containers locally or in production
- Docker Compose for multi-container applications
- Optimizing image size with multi-stage builds
- Managing container lifecycle (start, stop, restart, logs)
- Debugging container issues

## When NOT to Use
- Kubernetes orchestration (use kubernetes-deploy skill)
- Container registry operations (use docker-registry skill)
- Infrastructure as code for containers (use terraform skill)

## Inputs Required
- Application codebase location
- Dockerfile path (default: ./Dockerfile)
- Container name/tag
- Environment variables
- Port mappings
- Volume mounts

## Workflow

### 1. Create Dockerfile
Create a multi-stage Dockerfile following Torro standards:

```dockerfile
# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
CMD ["python", "engine/main.py"]
```

### 2. Build Image
```bash
docker build -t torro-app:latest -f deploy/Dockerfile .
```

### 3. Run Container
```bash
docker run -d \
  --name torro-container \
  -p 5000:5000 \
  -v $(pwd)/logs:/app/logs \
  -e APP_ENV=development \
  torro-app:latest
```

### 4. Docker Compose (Multi-Container)
Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: deploy/Dockerfile
    ports:
      - "5000:5000"
    environment:
      - APP_ENV=development
    volumes:
      - ./logs:/app/logs
    depends_on:
      - db
      - redis

  db:
    image: postgres:17
    environment:
      POSTGRES_USER: torro
      POSTGRES_PASSWORD: secure_password
      POSTGRES_DB: torro_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

Run with:
```bash
docker compose up -d
```

### 5. Container Lifecycle Management

| Command | Purpose |
| :--- | :--- |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker stop <container>` | Stop container gracefully |
| `docker start <container>` | Start stopped container |
| `docker restart <container>` | Restart container |
| `docker logs <container>` | View container logs |
| `docker exec -it <container> bash` | Execute command in container |
| `docker rm <container>` | Remove container |

### 6. Debug Container Issues
```bash
# View logs
docker logs torro-container

# Execute shell in running container
docker exec -it torro-container bash

# Inspect container details
docker inspect torro-container

# View resource usage
docker stats torro-container
```

## Examples

### Example 1: Production Flask App
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "engine.main:app"]
```

### Example 2: Multi-Stage for Node.js
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

FROM node:20-alpine AS runtime
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app .
EXPOSE 3000
CMD ["node", "server.js"]
```

## Troubleshooting

### Container Exits Immediately
- Check logs: `docker logs <container>`
- Verify CMD/ENTRYPOINT in Dockerfile
- Ensure all dependencies are installed

### Port Already in Use
```bash
docker run -p 8080:5000 ...  # Use different host port
```

### Volume Permission Issues
```bash
docker run -v $(pwd)/data:/app/data:rw ...
```

### Image Size Too Large
- Use multi-stage builds
- Use slim/alpine base images
- Remove unnecessary files
- Combine RUN commands with `&&`

## References
- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
