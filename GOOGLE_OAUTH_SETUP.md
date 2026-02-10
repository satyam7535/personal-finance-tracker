# Fixing Google OAuth on Render & Register Page Auto-Redirect

## Issue 1: Google OAuth Not Visible on Render

### Problem
The Google Sign-In button is not showing on your Render deployment login page, but works fine locally.

### Root Cause
Google OAuth requires:
1. **Google OAuth credentials** (`GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`) to be configured in environment variables
2. **Site domain** to be configured in Django's Sites framework (matches your actual domain)
3. **Redirect URIs** to be authorized in Google Cloud Console

On Render, one or more of these is likely missing.

### Solution

#### Step 1: Configure Environment Variables in Render

1. Go to your Render Dashboard → Your Service → **Environment** tab

2. Add these environment variables:
   ```
   GOOGLE_CLIENT_ID = your-google-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET = your-google-client-secret
   ```

   > Get these from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

#### Step 2: Configure Google Cloud Console

1. Go to [Google Cloud Console → APIs & Services → Credentials](https://console.cloud.google.com/apis/credentials)

2. Click on your OAuth 2.0 Client ID

3. Add **Authorized redirect URIs**:
   ```
   https://your-app-name.onrender.com/accounts/google/login/callback/
   ```

4. Add **Authorized JavaScript origins**:
   ```
   https://your-app-name.onrender.com
   ```

5. Replace `your-app-name` with your actual Render service name

6. Click **Save**

#### Step 3: Configure Django Site Domain

The Google OAuth button visibility depends on `{% get_providers %}` template tag from django-allauth, which checks:
- If `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set
- If the Site domain is configured correctly

**Option A: Via Django Admin (Recommended)**

1. Visit `https://your-app.onrender.com/admin/`

2. Login as superuser (create one if needed):
   ```bash
   # On Render, use the Shell feature or run via render.yaml
   python manage.py createsuperuser
   ```

3. Go to **Sites** → Click on `example.com`

4. Update:
   - **Domain name**: `your-app-name.onrender.com`  
   - **Display name**: `Finance Tracker`

5. Save

**Option B: Via Management Command**

Create a custom management command to auto-configure the site domain during deployment.

---

## Issue 2: Register Page Auto-Redirects to Dashboard

### Problem
When you visit `/auth/register/` while already logged in, you're automatically redirected to the dashboard.

### Current Behavior
In `core/views.py` line 10-11:
```python
if request.user.is_authenticated:
    return redirect('reports:dashboard')
```

### Two Options

#### Option 1: Keep the Redirect (Current - Recommended)
**Why:** Prevents confusion. If you're logged in, you don't need to register again.

**No changes needed.** This is standard practice.

#### Option 2: Allow Logged-In Users to View Register Page  
**Why:** For testing or if you want flexibility.

**Change Required:**
```python
def register_view(request):
    \"\"\"Handle user registration.\"\"\"
    # Remove or comment out the redirect
    # if request.user.is_authenticated:
    #     return redirect('reports:dashboard')

    if request.method == 'POST':
        # ... rest of the code
```

**Downside:** Confusing UX - why would a logged-in user see a registration form?

### Recommendation
**Keep the current behavior** (auto-redirect to dashboard). This is the expected UX pattern.

If you need to test registration:
1. Logout first: Visit `/auth/logout/`
2. Then visit `/auth/register/`

OR

Open an incognito/private browser window

---

## Summary of Fixes Needed for Google OAuth

| Step | Action | Where |
|------|--------|-------|
| 1 | Add `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` | Render Dashboard → Environment |
| 2 | Add authorized redirect URI | Google Cloud Console |
| 3 | Update Site domain | Django Admin → Sites |

After completing these steps, the Google Sign-In button will appear on Render!

---

## Quick Troubleshooting

### Google Button Still Not Showing?

**Check template debug:**

Add this temporarily to `login.html` after line 32:
```html
{% get_providers as socialaccount_providers %}
<p>Debug: Providers = {{ socialaccount_providers }}</p>
{% if socialaccount_providers %}
```

If it shows `Providers = []`, then environment variables aren't set correctly.

### How to Create Superuser on Render

**Via Render Shell:**
1. Go to Render Dashboard → Your Service → **Shell** tab
2. Run: `python manage.py createsuperuser`
3. Follow prompts

**Via render.yaml (Not Recommended for production):**
```yaml
# Don't do this - security risk!
```

Better: Create locally, migrate database, or use Render Shell.
