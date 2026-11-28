- JO: - Start a project called practice1 (continue from your S1 repo)
- Create an API with FastAPI (recommended) or any framework you like
- Add a GET /health endpoint that returns {"status": "ok"}
- Write a Dockerfile and run the API inside a container
Deliver: screenshot of /docs served from the container
 make this please
 
- Gemini: To complete your `practice1` assignment, follow these step-by-step instructions. Since I cannot access your local filesystem or Docker daemon directly, you will need to run these commands on your machine to generate the final screenshot.

**`main.py`**

```python
from fastapi import FastAPI

app = FastAPI(title="Practice 1 API", version="1.0.0")

@app.get("/health")
def health_check():
    return {"status": "ok"}

```

**`Dockerfile`**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir "fastapi[standard]"

COPY main.py .

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000"]

```

*(Note: `fastapi run` binds to `0.0.0.0` by default, which is required so you can access the container from your host browser).*

### 2. Build and Run the Docker Container

Make sure Docker Desktop (or the Docker daemon) is running, then execute these commands inside the `practice1` directory:

```bash
# Build the Docker image
docker build -t practice1-api .

# Run the container mapping port 8000
docker run -d -p 8000:8000 --name practice1-container practice1-api

```

### 3. Verify & Capture Deliverable

1. Open your browser and go to **`http://localhost:8000/docs`**.
2. Expand the **`GET /health`** endpoint, click **Try it out**, and click **Execute** to verify it returns `{"status": "ok"}` with a `200` status code.
3. Take a screenshot of the browser window (including the `localhost:8000/docs` URL bar and the `/health` endpoint) for your submission.
4. *(Optional)* Commit your new `practice1` folder to your S1 Git repository:
```bash
git add .
git commit -m "Add practice1 FastAPI app and Dockerfile"
git push

```
