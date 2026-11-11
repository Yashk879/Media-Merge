# MediaMerge — Media Asset Management & Streaming

MediaMerge is a Python Full-Stack media platform combining:

- Digital Asset Management (DAM)
- Media upload and metadata
- HLS streaming
- AES-128 encrypted HLS / DRM-ready delivery
- Subscription plans
- JWT authentication
- Rights / licensing management
- Royalty tracking
- Watch history and progress
- Content-based recommendations
- Admin management
- PostgreSQL persistence
- Redis + Celery background processing
- MinIO/S3-compatible object storage
- FFmpeg media processing

## Architecture

Browser
  |
  | HTTP / REST / HLS
  v
Django + Django REST Framework
  |---- PostgreSQL
  |---- Redis
  |---- Celery workers
  |---- MinIO/S3
  |---- FFmpeg
  |
  v
HLS player (hls.js)

## Important DRM note

This project implements **AES-128 encrypted HLS, authenticated entitlement checks, and short-lived signed object URLs**.

That is useful media protection for an MVP, but it is **not the same thing as commercial multi-DRM**. Production Widevine/FairPlay/PlayReady requires a DRM provider/license server, secure key management/KMS/HSM, platform-specific packaging, and additional security controls. This ZIP does not pretend to be a complete commercial DRM license service.

## Quick setup

### 1. Requirements

Install:

- Python 3.11+
- Docker Desktop
- Docker Compose
- Git (optional)
- FFmpeg if running processing outside Docker

### 2. Start infrastructure

```bash
docker compose up -d postgres redis minio
```

### 3. Create virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install packages

```bash
pip install -r requirements.txt
```

### 5. Environment

```bash
copy .env.example .env
```

On macOS/Linux:

```bash
cp .env.example .env
```

The defaults are suitable for local development.

### 6. Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Start Django

```bash
python manage.py runserver
```

### 8. Start Celery worker

Windows:

```powershell
celery -A config worker -l info --pool=solo
```

macOS/Linux:

```bash
celery -A config worker -l info
```

### 9. Open

- Web app: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/
- MinIO console: http://127.0.0.1:9001/

## Docker-only option

The Docker Compose file also contains a Django service and Celery worker. For a simple local deployment:

```bash
docker compose up --build
```

Then run migrations in the Django container:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

## Main API endpoints

### Authentication

POST `/api/auth/register/`
POST `/api/auth/login/`
POST `/api/auth/refresh/`
GET `/api/auth/me/`

### Media

GET `/api/media/assets/`
POST `/api/media/assets/`
GET `/api/media/assets/<id>/`
POST `/api/media/assets/<id>/process/`
GET `/api/media/assets/<id>/stream/`

### Subscriptions

GET `/api/subscriptions/plans/`
POST `/api/subscriptions/subscribe/`
GET `/api/subscriptions/me/`

### Rights

GET `/api/rights/`
POST `/api/rights/`

### Royalties

GET `/api/royalties/`
POST `/api/royalties/`

### Recommendations

GET `/api/recommendations/`

### Watch history

POST `/api/watch-history/`
GET `/api/watch-history/`

## Demo workflow

1. Register a user.
2. Create/login with an account.
3. Open Django admin.
4. Create a media asset or upload it through the API.
5. Give the asset a category and metadata.
6. Create a subscription plan.
7. Subscribe the user.
8. Add rights for the asset.
9. Upload/process a video.
10. FFmpeg converts it into HLS.
11. The HLS playlist is stored in object storage.
12. The stream endpoint verifies subscription + rights.
13. The browser loads the HLS playlist with hls.js.
14. Watch events are stored.
15. Recommendation endpoint uses content similarity from metadata/tags.

## Production improvements

Before production, add:

- Widevine/FairPlay/PlayReady license service
- CDN
- signed CloudFront/Cloud CDN URLs
- KMS/HSM key storage
- antivirus scanning
- resumable/multipart uploads
- video thumbnails and sprites
- multiple bitrate HLS/DASH ladders
- payment gateway such as Stripe/Razorpay
- email service
- object lifecycle policies
- audit logging
- rate limiting
- WAF
- observability
- automated tests and CI/CD
- Kubernetes if scale requires it
