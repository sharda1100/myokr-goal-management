# MyOKR Deployment Guide

## Quick Deploy on Render (Free)

### 1. Prepare Your Repository
- Ensure all deployment files are committed to GitHub
- Files needed: `Procfile`, `requirements.txt`, `runtime.txt`, `build.sh`, `wsgi.py`

### 2. Deploy on Render
1. Go to [render.com](https://render.com) and sign up
2. Click "New Web Service"
3. Connect your GitHub account
4. Select repository: `myokr-goal-management`
5. Configure:
   - **Name**: `myokr-app` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn wsgi:app`
   - **Instance Type**: `Free`

### 3. Environment Variables
Add these in Render dashboard:
```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this
DATABASE_URL=sqlite:///myokr.db
```

### 4. Deploy
- Click "Create Web Service"
- Wait for deployment (5-10 minutes)
- Your app will be available at: `https://your-app-name.onrender.com`

## Alternative: Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key-here`

## Testing Locally Before Deployment

```bash
# Test with production config
set FLASK_ENV=production
python wsgi.py
```

## Troubleshooting

### Common Issues:
1. **Build fails**: Check `build.sh` permissions
2. **App won't start**: Verify `wsgi.py` and `Procfile`
3. **Database errors**: Ensure `init_db.py` runs in build script

### Logs:
- Render: Check deployment logs in dashboard
- Railway: View logs in project dashboard

## Post-Deployment

1. Visit your deployed app URL
2. Register a new admin account
3. Create sample OKRs to test functionality
4. Check analytics dashboard

## Security Notes

- Change SECRET_KEY in production
- Use environment variables for sensitive data
- Enable HTTPS (automatic on Render/Railway)
