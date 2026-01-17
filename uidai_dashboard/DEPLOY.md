# Deployment Guide for Aadhaar N.E.X.U.S

## Option 1: Streamlit Cloud (Recommended - FREE)

Streamlit Cloud is the easiest and recommended way to deploy Streamlit apps.

### Steps:

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/

2. **Sign in with GitHub**
   - Click "Sign in with GitHub"
   - Authorize Streamlit to access your repositories

3. **Deploy Your App**
   - Click "New app"
   - Select your repository: `kvkushal/UIDAI-Hackathon`
   - Branch: `main`
   - Main file path: `uidai_dashboard/app.py`
   - Click "Deploy!"

4. **Wait for Deployment**
   - Streamlit will install dependencies from `requirements.txt`
   - Your app will be live at: `https://[your-app-name].streamlit.app`

### Troubleshooting:
- If deployment fails, check logs in Streamlit Cloud dashboard
- Ensure `requirements.txt` is in the same folder as `app.py`
- Data file path should be relative: `data/district_equity_all_india.csv`

---

## Option 2: Vercel (Alternative)

Note: Vercel doesn't natively support Streamlit. You would need to:

1. Convert to a Flask/FastAPI backend with a React frontend, OR
2. Use Vercel's Serverless Functions (complex for Streamlit)

**Not recommended for Streamlit apps.** Use Streamlit Cloud instead.

---

## Option 3: Heroku

1. Create a `Procfile` in `uidai_dashboard/`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Create a `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   ```

3. Deploy:
   ```bash
   heroku login
   heroku create aadhaar-nexus
   git push heroku main
   ```

---

## Option 4: Railway.app

1. Go to https://railway.app/
2. Connect your GitHub repository
3. Select `uidai_dashboard` as the root directory
4. Railway will auto-detect Streamlit and deploy

---

## Recommended: Streamlit Cloud

For this hackathon, **Streamlit Cloud** is the best option because:
- Free tier available
- Native Streamlit support
- Automatic HTTPS
- Easy updates (push to GitHub = auto-deploy)
- No configuration needed

Your app URL will be: `https://aadhaar-nexus.streamlit.app` (or similar)
