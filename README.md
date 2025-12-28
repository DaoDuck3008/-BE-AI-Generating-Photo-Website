# Backend for ID Photo Processing System

## Overview

This project is a backend system for processing ID photos with print-ready output.  
It provides RESTful APIs to handle image processing tasks such as background handling, color adjustments, print layout generation, and final asset delivery.

The backend is designed with a **job-based workflow** to safely handle long-running image processing tasks, combined with **Redis** for temporary state management and status tracking.

---

## Key Features

- Job-based image processing workflow
- Status polling for long-running tasks
- Print-ready image generation (300 DPI)
- Standard ID photo layouts on 4R paper
- Redis-based job status storage
- Cloud storage integration for scalable asset delivery
- Structured error handling for frontend-safe responses

---

## Tech Stack

- **Backend Framework**: FastAPI (Python)
- **Image Processing**: Pillow, OpenCV
- **In-memory Store**: Redis
- **Cloud Storage**: Cloudinary
- **API Style**: RESTful APIs

> Although implemented in Python, the backend architecture and concepts are fully transferable to Node.js / Express applications.

---

## Backend Architecture

The backend follows a modular and layered design:

# Backend for ID Photo Processing System

## Overview

This project is a backend system for processing ID photos with print-ready output.  
It provides RESTful APIs to handle image processing tasks such as background handling, color adjustments, print layout generation, and final asset delivery.

The backend is designed with a **job-based workflow** to safely handle long-running image processing tasks, combined with **Redis** for temporary state management and status tracking.

---

## Key Features

- Job-based image processing workflow
- Status polling for long-running tasks
- Print-ready image generation (300 DPI)
- Standard ID photo layouts on 4R paper
- Redis-based job status storage
- Cloud storage integration for scalable asset delivery
- Structured error handling for frontend-safe responses

---

## Tech Stack

- **Backend Framework**: FastAPI (Python)
- **Image Processing**: Pillow, OpenCV
- **In-memory Store**: Redis
- **Cloud Storage**: Cloudinary
- **API Style**: RESTful APIs

> Although implemented in Python, the backend architecture and concepts are fully transferable to Node.js / Express applications.

---

## Backend Architecture

The backend follows a modular and layered design:

API Layer
↓
Stage Runner (run_stage_A, run_stage_B)
↓
Processing Modules (background_removal, layout, resize, color adjust)
↓
Redis (job status)
↓
Cloudinary (final image storage)

Each layer has a single responsibility to ensure maintainability and scalability.

---

## Job-Based Workflow

Image processing tasks may take several seconds, so the system uses a **job-based workflow** instead of blocking requests.

### Workflow Steps

1. Client selects an image and submits a processing request
2. Backend starts Stage A (Removing background and face alignment) and generates a `jobId`
3. Job status is stored and updated in Redis
4. Client polls job status using the `jobId`
5. When processing is complete, the backend returns the image URL
6. Client adjust background color, brightness, contrast and size of the image and submit another request with its `jopId`
7. Backend starts Stage B (adding background, color adjustment, resizement) then push the final image to Cloudinary to store
8. When every steps is complete, the backend send the final image URL back to frontend.

---

## How to run the project

1. Clone the repository

```bash
git clone <repository-url>
cd backend
```

2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure environment variables

```bash
Create a .env file:

CLOUDINARY_CLOUD_NAME=xxx
CLOUDINARY_API_KEY=xxx
CLOUDINARY_API_SECRET=xxx
REDIS_URL=redis://localhost:6379
```

5. Start Redis
   redis-server

6. Run the server

```bash
uvicorn app.main:app --reload
```
