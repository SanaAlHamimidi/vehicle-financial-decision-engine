# Vehicle Financial Decision Engine — Website

CS163 · Group 20 · Nyi Wai Yan Tun & Sana Al Hamimidi

## Files

| File | Description |
|---|---|
| `index.html` | Home / Project Summary |
| `eda.html` | Exploratory Data Analysis |
| `analysis.html` | Analysis Methods |
| `ml.html` | ML Models |
| `findings.html` | Major Findings |
| `style.css` | Shared stylesheet |
| `main.js` | Shared JavaScript |

---

## How to Publish on GitHub Pages

### Step 1 — Create a GitHub Repository
1. Go to [github.com](https://github.com) and sign in
2. Click **New repository**
3. Name it something like `vfde-project` or `cs163-group20`
4. Set it to **Public**
5. Click **Create repository**

### Step 2 — Upload your files
**Option A — Drag & drop (easiest):**
1. On your new repo page, click **"uploading an existing file"**
2. Drag all 7 files (`index.html`, `eda.html`, `analysis.html`, `ml.html`, `findings.html`, `style.css`, `main.js`) into the upload area
3. Click **Commit changes**

**Option B — Git command line:**
```bash
git init
git add .
git commit -m "Initial website upload"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 3 — Enable GitHub Pages
1. Go to your repository's **Settings** tab
2. Scroll down to **Pages** in the left sidebar
3. Under **Source**, select **Deploy from a branch**
4. Set branch to **main** and folder to **/ (root)**
5. Click **Save**

### Step 4 — Get your URL
After ~1 minute, your site will be live at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/
```

---

## Adding Charts Later
Each page has placeholder sections marked `[ ... Chart Coming Soon ]`.
Replace the `.chart-placeholder` divs with your actual chart images or embed scripts (e.g., Chart.js, Plotly, Tableau Public).

Example — replacing a placeholder with an image:
```html
<!-- Before -->
<div class="chart-placeholder">[ My Chart ]</div>

<!-- After -->
<img src="charts/my-chart.png" alt="My Chart" style="width:100%; border-radius:12px;" />
```
