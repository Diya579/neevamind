# How to Access the .env File

The `.env` file exists but is hidden because it starts with a dot (`.`). Here are multiple ways to access it:

## Method 1: Using Terminal/Command Line

### View the file:
```bash
cat /home/z/my-project/.env
```

### Edit the file:
```bash
nano /home/z/my-project/.env
# or
vim /home/z/my-project/.env
```

### List all files including hidden ones:
```bash
ls -la /home/z/my-project/
```

## Method 2: Using File Explorer

### On Windows/Mac/Linux:
1. **Show hidden files** in your file explorer:
   - **Windows**: View tab > Hidden items
   - **Mac**: Command + Shift + . (period)
   - **Linux**: Ctrl + H (in most file managers)

2. Navigate to `/home/z/my-project/`
3. You should see `.env` and `.env.example`

## Method 3: Using Code Editors/IDEs

### VS Code:
1. Open the project folder
2. Click on the "Explorer" icon
3. If you don't see `.env`, click the "..." menu and select "Show Hidden Files"

### Other editors:
- Most IDEs have an option to show hidden files in their settings

## Method 4: Copy to a visible file

If you prefer working with visible files, you can create a copy:

```bash
cp /home/z/my-project/.env /home/z/my-project/env-config.txt
```

## Current .env File Contents:

```
# NeevaMind Environment Configuration
# ====================================

# Application Security
SECRET_KEY=your-very-secure-secret-key-change-this-in-production

# Database Configuration (MySQL via XAMPP)
DATABASE_URL=mysql+pymysql://root:@localhost/neevamind

# AI API Configuration
COHERE_API_KEY=useyourownkey

# Application Environment
FLASK_ENV=development

# Server Configuration
FLASK_APP=app.py
FLASK_DEBUG=True

# Session Configuration
SESSION_TYPE=filesystem
SESSION_PERMANENT=False
PERMANENT_SESSION_LIFETIME=86400  # 24 hours in seconds

# Database Settings (Alternative formats if needed)
# DB_HOST=localhost
# DB_PORT=3306
# DB_NAME=neevamind
# DB_USER=root
# DB_PASSWORD=diya

# CORS Settings
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_HEADERS=Content-Type,Authorization

# Security Headers
SECURE_HEADERS=true
CSP_ENABLED=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=neevamind.log

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600  # 1 hour

# File Upload Settings (if needed)
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads

# Email Configuration (for notifications)
EMAIL_ENABLED=false
SMTP_SERVER=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
EMAIL_FROM=

# Analytics and Monitoring
ANALYTICS_ENABLED=false
MONITORING_ENABLED=false

# Feature Flags
FEATURE_AI_INSIGHTS=true
FEATURE_WEEKLY_REPORTS=true
FEATURE_USER_REGISTRATION=true
FEATURE_PASSWORD_RESET=false
```

## Verification Commands:

Run these commands to verify the files exist:

```bash
# Check if .env exists
ls -la /home/z/my-project/.env

# Check if .env.example exists
ls -la /home/z/my-project/.env.example

# List all files including hidden ones
ls -la /home/z/my-project/ | grep env

# Find all env files
find /home/z/my-project -name "*env*"
```

## Important Notes:

1. **The file exists** - it's just hidden by default
2. **It's configured correctly** with your MySQL and Cohere API settings
3. **It's tracked by git** (not in .gitignore)
4. **It contains all necessary configuration** for the Flask application

If you still can't see it, try the terminal commands above to access and edit the file directly.
