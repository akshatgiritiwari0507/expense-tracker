# Deployment Guide

This guide provides step-by-step instructions for deploying the Basic Expense Tracker to production using Render.

## Live Demo

**See the deployed app:** https://expense-tracker-dycf.onrender.com/dashboard

## Deploying to Render

Render is a cloud platform that makes it easy to deploy web applications. Follow these steps to deploy your expense tracker with all features including income tracking, search functionality, and password management.

### Prerequisites

1. **GitHub Repository**
   - Push your code to a GitHub repository
   - Ensure all files are committed and pushed

2. **Render Account**
   - Sign up at [render.com](https://render.com)
   - You can use your GitHub account for easy authentication

### Step 1: Create New Web Service

1. **Log in to Render Dashboard**
   - Click "New +" button
   - Select "Web Service"

2. **Connect Repository**
   - Choose "GitHub" (or GitLab/Bitbucket)
   - Authorize Render to access your repositories
   - Select your expense-tracker repository

3. **Configure Service**
   ```
   Name: expense-tracker
   Environment: Python 3
   Region: Choose nearest to your users
   Branch: main (or your default branch)
   ```

### Step 2: Build Configuration

Set the following build settings:

```bash
Build Command: pip install -r requirements.txt
Start Command: gunicorn run:app
Runtime: Python 3
```

### Step 3: Environment Variables

Add the following environment variables in Render dashboard:

1. **SECRET_KEY**
   - Generate a secure random key
   - Example: `python -c "import secrets; print(secrets.token_hex(32))"`
   - Add to environment variables

2. **FLASK_ENV**
   - Value: `production`

3. **DATABASE_URL** (if using PostgreSQL)
   - Add a PostgreSQL database to your Render service
   - Render will automatically provide the DATABASE_URL
   - Copy the connection string to environment variables

### Step 5: Deploy

1. **Create Service**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

2. **Monitor Deployment**
   - Watch the build logs for any errors
   - Once deployed, you'll get a public URL

### Step 6: Verify Deployment

1. **Test the Application**
   - Visit your Render URL
   - Try signing up for a new account
   - Add an expense to verify database connectivity

2. **Test All Features**
   - **User Authentication:** Signup, login, logout, password change
   - **Expense Management:** Add, edit, delete, view expenses
   - **Income Tracking:** Add, edit, delete, view income
   - **Search Functionality:** Search by category/source and description
   - **Dashboard:** View financial summary and recent activity
   - **Date Filtering:** Filter expenses/income by date range
   - **Visual Features:** Today's entries highlighted, proper date sorting

3. **Check Logs**
   - If issues occur, check Render logs
   - Common issues: missing environment variables, database connection errors

## 🔧 Production Configuration

### Security Settings

Ensure your production environment has:

```env
SECRET_KEY=your-secure-random-key-here
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### Database Migration

If you need to update database schema in production:

1. **SSH into your Render instance** (if available)
2. **Run migration commands** if using Flask-Migrate
3. **Or manually update** through database admin panel

## 🌐 Alternative Deployment Options

### Heroku

```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-database-url
git push heroku main
```

### DigitalOcean App Platform

1. Create App from GitHub repository
2. Set build and start commands
3. Configure environment variables
4. Deploy

### VPS Deployment

For manual VPS deployment:

```bash
# Clone repository
git clone <your-repo>
cd expense-tracker

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export SECRET_KEY="your-key"
export DATABASE_URL="your-db-url"

# Run with Gunicorn
gunicorn run:app --bind 0.0.0.0:8000
```

## 🔍 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check requirements.txt for correct versions
   - Ensure all dependencies are listed
   - Check Python version compatibility

2. **Database Connection Errors**
   - Verify DATABASE_URL format
   - Check if database is running
   - Ensure firewall allows connection

3. **Application Not Starting**
   - Check start command: `gunicorn run:app`
   - Verify import paths
   - Check application logs

4. **Static Files Not Loading**
   - Ensure static folder structure is correct
   - Check Flask configuration for static files

### Debugging Tips

1. **Check Render Logs**
   - Go to your service dashboard
   - Click "Logs" tab
   - Look for error messages

2. **Local Testing**
   - Test with production settings locally
   - Use same environment variables
   - Simulate production environment

3. **Database Issues**
   - Test database connection manually
   - Check database permissions
   - Verify schema exists

## 📊 Monitoring and Maintenance

### Performance Monitoring

1. **Render Metrics**
   - Monitor CPU and memory usage
   - Check response times
   - Set up alerts for high usage

2. **Database Monitoring**
   - Monitor query performance
   - Check connection limits
   - Optimize slow queries

### Backups

1. **Database Backups**
   - Render automatically backs up PostgreSQL
   - Export regular backups for safety
   - Test backup restoration

2. **Code Backups**
   - Keep code in GitHub
   - Tag releases
   - Maintain deployment history

## 🔒 Security Best Practices

1. **Regular Updates**
   - Keep dependencies updated
   - Check for security vulnerabilities
   - Update Python packages regularly

2. **Environment Security**
   - Use strong SECRET_KEY
   - Rotate database passwords
   - Limit database permissions

3. **HTTPS**
   - Render automatically provides HTTPS
   - Ensure all links use HTTPS
   - Redirect HTTP to HTTPS

## 📈 Scaling

When your application grows:

1. **Upgrade Resources**
   - Increase memory/CPU on Render
   - Scale database if needed
   - Consider load balancing

2. **Optimize Database**
   - Add indexes for common queries
   - Optimize slow queries
   - Consider read replicas

3. **Caching**
   - Implement Redis caching
   - Cache static assets
   - Use CDN for static files

---

For additional support, check the [Render Documentation](https://render.com/docs) or create an issue in the GitHub repository.
