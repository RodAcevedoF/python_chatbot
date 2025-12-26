# Deployment Guide - Hotel Costa Azul Chatbot

## Security Checklist

### 1. **Rate Limiting** (Implemented)

- `/chat`: 20 requests/minute per IP
- `/hotel-info`: 60 requests/minute per IP
- `/reindex`: 3 requests/hour per IP
- Root endpoint: 30 requests/minute per IP

### 2. **Environment Variables** (Required)

Create a `.env` file (never commit this!):

```bash
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Security Settings
ADMIN_API_KEY=your_secure_random_key_here  # For /reindex endpoint
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Production Settings (optional)
ENV=production
LOG_LEVEL=INFO
```

**Generate a secure ADMIN_API_KEY:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. **CORS Configuration**

- Default: Restricts to specified origins only
- Development: Uses wildcard (change for production!)
- Set `ALLOWED_ORIGINS` environment variable with your domain

### 4. **Input Validation** (Implemented)

- Message length: Max 1000 characters
- Session ID length: Max 100 characters
- Empty message rejection
- Input sanitization (strip whitespace)

### 5. **API Key Protection** (Implemented)

- `/reindex` endpoint requires `x-api-key` header
- Set `ADMIN_API_KEY` in environment variables
- Example usage:
  ```bash
  curl -X POST https://yourapi.com/reindex \
    -H "x-api-key: your_admin_api_key"
  ```

---

## Pre-Deployment Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
# Linux/Mac
export SUPABASE_URL="your_url"
export SUPABASE_KEY="your_key"
export OPENAI_API_KEY="your_key"
export ADMIN_API_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
export ALLOWED_ORIGINS="https://yourdomain.com"

# Windows (PowerShell)
$env:SUPABASE_URL="your_url"
$env:SUPABASE_KEY="your_key"
$env:OPENAI_API_KEY="your_key"
$env:ADMIN_API_KEY="your_secure_key"
$env:ALLOWED_ORIGINS="https://yourdomain.com"
```

### 3. Index Hotel Data

```bash
python cli.py reindex
```

### 4. Test Locally

```bash
python cli.py run-server
```

---

## Production Deployment Options

### Option 1: Docker Deployment (Recommended)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  chatbot:
    build: .
    ports:
      - '8000:8000'
    env_file:
      - .env
    restart: unless-stopped
```

Deploy:

```bash
docker-compose up -d
```

### Option 2: Gunicorn (Production Server)

Install:

```bash
pip install gunicorn
```

Run:

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
```

### Option 3: Azure App Service

1. Install Azure CLI
2. Create App Service:

```bash
az webapp up --name hotel-chatbot --runtime "PYTHON:3.11"
```

3. Set environment variables:

```bash
az webapp config appsettings set --name hotel-chatbot \
  --settings SUPABASE_URL="your_url" \
            SUPABASE_KEY="your_key" \
            OPENAI_API_KEY="your_key" \
            ADMIN_API_KEY="your_admin_key" \
            ALLOWED_ORIGINS="https://yourdomain.com"
```

### Option 4: AWS EC2 / DigitalOcean

1. SSH into server
2. Clone repository
3. Install dependencies
4. Set up systemd service:

Create `/etc/systemd/system/chatbot.service`:

```ini
[Unit]
Description=Hotel Chatbot
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/hotel_chatbot
Environment="PATH=/var/www/hotel_chatbot/venv/bin"
EnvironmentFile=/var/www/hotel_chatbot/.env
ExecStart=/var/www/hotel_chatbot/venv/bin/gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable chatbot
sudo systemctl start chatbot
```

---

## Additional Security Recommendations

### 1. **Use HTTPS**

- Get SSL certificate (Let's Encrypt is free)
- Configure reverse proxy (Nginx/Caddy)

Example Nginx config:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. **Add Request Logging**

```python
# In app/main.py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    return response
```

### 3. **Monitor API Usage**

- Set up monitoring (Sentry, DataDog, etc.)
- Track OpenAI API costs
- Monitor rate limit hits

### 4. **Implement Health Checks**

Add to `app/main.py`:

```python
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

### 5. **Database Security**

- Using Supabase RLS (Row Level Security)
- Environment variables for credentials
- No hardcoded secrets
- Consider: IP whitelisting in Supabase dashboard

### 6. **DDoS Protection**

- Use Cloudflare or similar CDN
- Enable rate limiting at CDN level
- Consider: WAF (Web Application Firewall)

### 7. **Secrets Management**

For production, consider:

- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault
- Google Cloud Secret Manager

---

## Cost Management

### OpenAI API Costs

- Set usage limits in OpenAI dashboard
- Monitor token usage
- Consider caching frequent responses

### Supabase Costs

- Free tier: 500MB database, 1GB file storage
- Monitor database size
- Set up billing alerts

---

## Monitoring & Maintenance

### 1. **Check Logs Regularly**

```bash
# Docker
docker-compose logs -f

# Systemd
sudo journalctl -u chatbot -f
```

### 2. **Update Dependencies**

```bash
pip list --outdated
pip install --upgrade package_name
```

### 3. **Backup Database**

- Enable automated backups in Supabase
- Export hotel_info.json regularly
- Version control your code

### 4. **Performance Monitoring**

```bash
# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s http://yourapi.com/chat
```

---

## Testing Checklist Before Going Live

- [ ] Environment variables set correctly
- [ ] Rate limiting works (test with multiple requests)
- [ ] CORS allows only your domain
- [ ] Admin endpoints require API key
- [ ] Input validation rejects invalid data
- [ ] Error messages don't leak sensitive info
- [ ] SSL certificate installed and working
- [ ] Health check endpoint responds
- [ ] Logging captures important events
- [ ] Monitoring/alerting configured
- [ ] Backup strategy in place
- [ ] Load testing completed
- [ ] API documentation updated

---

## Quick Test Commands

```bash
# Test rate limiting (should fail after 20 requests)
for i in {1..25}; do
  curl -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d '{"message":"test","session_id":"test"}';
done

# Test admin endpoint without API key (should fail)
curl -X POST http://localhost:8000/reindex

# Test admin endpoint with API key (should succeed)
curl -X POST http://localhost:8000/reindex \
  -H "x-api-key: your_admin_key"

# Test CORS
curl -H "Origin: https://evil.com" \
  --verbose http://localhost:8000/hotel-info
```

---

## Support & Troubleshooting

**Common Issues:**

1. **Rate limit errors**: Adjust limits in `app/main.py`
2. **CORS errors**: Add your domain to `ALLOWED_ORIGINS`
3. **OpenAI timeout**: Increase `temperature` or reduce context
4. **Supabase connection**: Check environment variables

**Need help?** Check logs first, then review this guide.

---

## License & Security Disclosure

## If you find a security vulnerability, please report it!

**Last Updated:** December 2025
