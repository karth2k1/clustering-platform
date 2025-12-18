# Frontend Setup & Run Guide

Complete guide for setting up the React-based frontend for the clustering platform.

---

## Prerequisites: Install Node.js & npm

### Step 1: Check If Already Installed

```bash
# Check Node.js version
node --version

# Check npm version
npm --version
```

**If you see version numbers** (e.g., `v20.x.x` and `10.x.x`), you're good! Skip to [Frontend Setup](#frontend-setup).

**If you see "command not found"**, continue with installation below.

---

### Step 2: Install Node.js & npm (macOS)

You're on macOS, so here are your options:

#### **Option 1: Using Homebrew** (Recommended - Easiest)

```bash
# If you don't have Homebrew, install it first:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js (npm comes with it)
brew install node

# Verify installation
node --version
npm --version
```

#### **Option 2: Official Installer**

1. Go to https://nodejs.org/
2. Download the **LTS (Long Term Support)** version for macOS
3. Run the installer (`.pkg` file)
4. Follow the installation wizard
5. Verify in terminal:
   ```bash
   node --version
   npm --version
   ```

#### **Option 3: Using nvm (Node Version Manager)** - For Advanced Users

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart terminal or run:
source ~/.zshrc

# Install Node.js LTS
nvm install --lts

# Verify
node --version
npm --version
```

---

### Step 3: Verify Installation

```bash
node --version
# Should show: v20.x.x or v18.x.x

npm --version
# Should show: 10.x.x or 9.x.x
```

✅ **If you see version numbers, you're ready!**

---

## Frontend Setup

Now that Node.js and npm are installed, let's set up the frontend:

### 1. Navigate to Frontend Directory

```bash
cd /Users/kkarupas/cursor/projects/clustering-platform/frontend
```

### 2. Install Frontend Dependencies

This will download all required packages (React, TypeScript, Vite, etc.):

```bash
npm install
```

**What to expect:**
- This takes 2-5 minutes depending on your internet speed
- You'll see a progress bar and package names scrolling by
- At the end, you'll see "added XXX packages"

**If you see warnings**, that's normal! Only worry about **errors** (in red).

### 3. Start Development Server

```bash
npm run dev
```

**Success!** You should see:

```
  VITE v5.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

The frontend is now running on **http://localhost:5173**

---

## Complete Startup Guide

To use the full platform, you need both backend AND frontend running:

### Terminal 1: Start Backend

```bash
cd /Users/kkarupas/cursor/projects/clustering-platform/backend
python run.py
```

✅ Backend runs on: **http://localhost:8000**

### Terminal 2: Start Frontend

```bash
cd /Users/kkarupas/cursor/projects/clustering-platform/frontend
npm run dev
```

✅ Frontend runs on: **http://localhost:5173**

### Open Your Browser

Go to: **http://localhost:5173**

You should see the clustering platform interface!

## Features Available

### AI-Assisted Mode (`/ai-mode`)
- **File Upload**: Drag-and-drop CSV/JSON files
- **Device Management**: Add/delete devices, configure WebAPI
- **Data Ingestion**: View uploaded files and run automatic clustering
- **Device Sync**: Fetch data from devices via WebAPI

### Advanced Mode (`/advanced-mode`)
- **Data File Browser**: Browse all ingested files with search and filters
- **Notebook Launcher**: Create and launch Jupyter notebooks with pre-populated code

## Backend Connection

Make sure the backend is running:
```bash
cd /Users/kkarupas/cursor/projects/clustering-platform
source venv/bin/activate
cd backend
python run.py
```

Backend should be running on **http://localhost:8000**

## Configuration

If backend is on a different port, create `.env` file in `frontend/`:
```
VITE_API_URL=http://localhost:8000
```

## Build for Production

```bash
npm run build
```

Built files will be in `frontend/dist/`

## Troubleshooting

### Problem: "command not found: npm"

**Solution:** Node.js/npm not installed. Follow [Prerequisites](#prerequisites-install-nodejs--npm) above.

---

### Problem: "npm install" fails or shows errors

**Common Causes:**

1. **Old Node.js version**
   ```bash
   # Check your version
   node --version
   
   # Should be v18 or higher
   # If lower, update Node.js
   ```

2. **Permission issues**
   ```bash
   # Try with sudo (last resort)
   sudo npm install
   ```

3. **Corrupted cache**
   ```bash
   # Clear npm cache
   npm cache clean --force
   
   # Try again
   npm install
   ```

4. **Already running process**
   ```bash
   # Kill any running dev server first
   # Press Ctrl+C in the terminal running npm
   
   # Then try again
   npm install
   ```

---

### Problem: Frontend shows blank page

**Solutions:**

1. **Check if backend is running**
   ```bash
   # Test backend
   curl http://localhost:8000/
   
   # Should return JSON response
   ```

2. **Check browser console**
   - Open browser Dev Tools (F12 or Right-click → Inspect)
   - Go to "Console" tab
   - Look for error messages

3. **Clear browser cache**
   - Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

---

### Problem: CORS Errors

```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:5173' 
has been blocked by CORS policy
```

**Solution:** Backend CORS is configured correctly by default. If you see this:

1. Make sure backend is actually running on port 8000
2. Restart both backend and frontend
3. Check backend logs for startup errors

---

### Problem: "Port 5173 already in use"

**Solution:**

```bash
# Option 1: Kill the process using port 5173
lsof -ti:5173 | xargs kill -9

# Option 2: Use a different port
npm run dev -- --port 5174
```

---

### Problem: API Connection Errors

**Check these in order:**

1. ✅ **Backend running?**
   ```bash
   curl http://localhost:8000/
   ```

2. ✅ **Frontend .env correct?**
   ```bash
   # Check if file exists
   cat frontend/.env
   
   # Should show:
   # VITE_API_URL=http://localhost:8000
   ```

3. ✅ **Browser console errors?**
   - Open Dev Tools (F12)
   - Check Console and Network tabs

---

### Problem: Build Errors ("npm run build" fails)

**Solution:**

```bash
# Nuclear option: Complete reinstall
cd /Users/kkarupas/cursor/projects/clustering-platform/frontend

# Delete everything
rm -rf node_modules dist package-lock.json

# Reinstall
npm install

# Try build again
npm run build
```

---

### Problem: TypeScript errors during development

**Usually safe to ignore during development.**

If they block you:

```bash
# Option 1: Run without type checking (fastest)
npm run dev

# Option 2: Fix types (if you know TypeScript)
# Edit the files showing errors

# Option 3: Disable strict mode temporarily
# Edit tsconfig.json and set "strict": false
```

---

## Quick Command Reference

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Check for outdated packages
npm outdated

# Update packages (careful!)
npm update

# Clean install (if having issues)
rm -rf node_modules package-lock.json && npm install
```

---

## Understanding What's Happening

### What is npm?
**npm** = Node Package Manager. It downloads and manages JavaScript libraries your project needs.

### What does "npm install" do?
Downloads all packages listed in `package.json` and puts them in `node_modules/` folder.

### What does "npm run dev" do?
Starts a development server with:
- ✅ Hot reload (auto-refresh when you edit files)
- ✅ Fast builds
- ✅ Better error messages

### What is Vite?
The build tool that makes your React app fast. It bundles your code and serves it locally.

---

## Port Information

| Service | Default Port | URL |
|---------|--------------|-----|
| Frontend | 5173 | http://localhost:5173 |
| Backend | 8000 | http://localhost:8000 |

**Note:** If port 5173 is busy, Vite automatically tries 5174, 5175, etc.

---

## Development Workflow

### Typical Development Session

```bash
# Terminal 1: Backend
cd backend
python run.py
# Leave this running

# Terminal 2: Frontend (new terminal)
cd frontend
npm run dev
# Leave this running

# Now develop!
# Edit files and see changes instantly
```

### When to Restart

**Backend:** Restart if you change Python code and it doesn't auto-reload

**Frontend:** Usually auto-reloads! Only restart if:
- You added a new npm package
- You changed `.env` file
- Something seems broken

---

## Files You Can Ignore

These are generated and can be deleted safely (they'll be recreated):

- `node_modules/` - All downloaded packages (large!)
- `dist/` - Production build output
- `.vite/` - Vite cache
- `package-lock.json` - Dependency lock file (but good to keep)

**DO NOT DELETE:**
- `package.json` - Lists all dependencies (keep this!)
- `src/` - Your actual source code (keep this!)
- `vite.config.ts` - Build configuration (keep this!)

---

## Next Steps

Once your frontend is running:

1. **Go to http://localhost:5173**
2. **Click "AI Mode"** (easiest interface)
3. **Upload a demo dataset** from `datasets/sample_data/iris.csv`
4. **See clustering in action!**

---

## Need More Help?

### Check these files:
- **Main README:** `/README.md` - Project overview
- **Demo Guide:** `/DEMO_GUIDE.md` - How to demonstrate the platform
- **Backend Setup:** `/RUN.md` - Backend startup guide

### Common Questions:

**Q: Do I need to run npm install every time?**
A: No! Only when:
- First setup
- After pulling new code from Git
- After someone updates `package.json`

**Q: Can I use yarn instead of npm?**
A: Yes, but stick with npm for consistency with these docs.

**Q: How do I stop the servers?**
A: Press `Ctrl+C` in the terminal running them.

**Q: Where can I see what packages are installed?**
A: Look in `package.json` or run `npm list --depth=0`

---

**You're all set! Happy coding!** 🚀

