# Development Workflow - Working Across Multiple Machines

This guide explains how to work on this project across multiple machines using Git for synchronization.

## Overview

This workflow allows you to:
- Work on Machine 1, commit and push your changes
- Switch to Machine 2, pull the latest changes, and continue working
- Keep both machines in sync through GitHub

---

## Initial Setup (One-Time Per Machine)

### On Each New Machine:

#### 1. Clone the Repository
```bash
cd ~/projects  # or your preferred location
git clone https://github.com/karth2k1/clustering-platform.git
cd clustering-platform
```

#### 2. Set Up Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r backend/requirements.txt
```

#### 3. Set Up Frontend (if working on frontend)
```bash
cd frontend
npm install
cd ..
```

#### 4. Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual values
# (Database URLs, API keys, secrets, etc.)
```

#### 5. Initialize Database (if needed)
```bash
cd backend
# Run any database setup scripts or migrations
python run.py  # This will create initial DB if needed
```

---

## Daily Workflow

### Starting Work on Machine 1

```bash
cd ~/projects/clustering-platform

# ALWAYS pull first to get latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Start working...
```

### Ending Session on Machine 1

```bash
# Check what changed
git status

# Add all changes
git add .

# Commit with a descriptive message
git commit -m "Add feature X: description of what you did"

# Push to GitHub
git push origin main

# Deactivate virtual environment (optional)
deactivate
```

### Starting Work on Machine 2

```bash
cd ~/projects/clustering-platform

# ALWAYS pull to get latest changes from Machine 1
git pull origin main

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Continue working...
```

### Ending Session on Machine 2

```bash
# Same as Machine 1
git add .
git commit -m "Continue feature X: what you accomplished"
git push origin main
deactivate
```

---

## What Gets Synced vs. What Doesn't

### ✅ SYNCED (Committed to Git)
- All source code (`.py`, `.tsx`, `.ts`, `.js`, etc.)
- Configuration files (`package.json`, `requirements.txt`, etc.)
- Documentation (`.md` files)
- Static assets
- Schema definitions
- Migration files

### ❌ NOT SYNCED (In .gitignore)
- `venv/` - Virtual environment (recreate on each machine)
- `node_modules/` - Frontend dependencies (reinstall with `npm install`)
- `*.db`, `*.sqlite` - Database files
- `backend/uploads/*` - User uploaded files
- `.env` - Environment variables (create manually on each machine)
- `__pycache__/` - Python cache
- `.DS_Store` - OS files
- `*.log` - Log files

---

## Common Scenarios

### Scenario 1: Forgot to Push Before Leaving Machine 1

**On Machine 2:**
You won't see the latest changes. Don't start working yet!

**Solution:**
1. Go back to Machine 1
2. Commit and push your changes
3. Return to Machine 2 and pull

### Scenario 2: Forgot to Pull Before Starting Work

**Result:** You might create conflicts when you try to push.

**Solution:**
```bash
# Try to push
git push origin main

# If it fails, pull first
git pull origin main

# Git will try to auto-merge
# If conflicts occur, resolve them manually
# Then commit and push
git add .
git commit -m "Merge changes from other machine"
git push origin main
```

### Scenario 3: Work in Progress (Not Ready to Commit)

**Option 1 - Use Git Stash:**
```bash
# Save work temporarily
git stash save "WIP: working on feature X"

# Push any committed work
git push origin main

# On other machine, pull and continue elsewhere
git pull origin main

# Later, return to first machine and restore
git stash pop
```

**Option 2 - Commit WIP:**
```bash
git add .
git commit -m "WIP: Feature X - not complete yet"
git push origin main

# On other machine
git pull origin main
# Continue working and make another commit when done
```

**Option 3 - Use Feature Branches:**
```bash
# Create a branch for your feature
git checkout -b feature/new-algorithm

# Commit and push the branch
git add .
git commit -m "Working on new algorithm"
git push origin feature/new-algorithm

# On other machine, fetch and checkout the branch
git fetch origin
git checkout feature/new-algorithm

# When done, merge back to main
git checkout main
git merge feature/new-algorithm
git push origin main
```

### Scenario 4: Database Data Needs to Be Synced

**Problem:** Database files (`.db`) are not synced.

**Solutions:**

**For Development:**
- Keep SQL dump files in a `database/` folder (commit these)
- Use database seeders/fixtures
- Document how to recreate test data

**For Production:**
- Use a shared cloud database (PostgreSQL, MySQL)
- Both machines connect to the same database server

### Scenario 5: Uploaded Files Need to Be Synced

**Problem:** Files in `backend/uploads/` are not synced.

**Solutions:**

**For Development:**
- Accept that test uploads won't sync (usually okay)
- Keep sample files in a `examples/` folder (commit these)

**For Production:**
- Use cloud storage (AWS S3, Azure Blob Storage, Google Cloud Storage)
- Both machines access the same cloud bucket

---

## Best Practices

### ✅ DO:
- **Always pull before starting work**
- **Always push when ending a session**
- Write clear, descriptive commit messages
- Commit frequently (small, logical chunks)
- Test your code before committing
- Keep your `.gitignore` up to date
- Document any machine-specific setup in this file

### ❌ DON'T:
- Don't commit `.env` files (they contain secrets)
- Don't commit `venv/` or `node_modules/`
- Don't commit database files
- Don't commit API keys or passwords
- Don't commit large binary files (unless necessary)
- Don't force push (`git push --force`) on shared branches

---

## Useful Git Commands

### Check Status
```bash
git status                    # See what changed
git log --oneline -10        # See recent commits
git diff                     # See unstaged changes
git diff --staged            # See staged changes
```

### Undo Changes
```bash
git restore <file>           # Discard changes to a file
git restore --staged <file>  # Unstage a file
git reset --soft HEAD~1      # Undo last commit (keep changes)
git reset --hard HEAD~1      # Undo last commit (discard changes)
```

### Branch Operations
```bash
git branch                   # List branches
git branch <name>            # Create branch
git checkout <name>          # Switch to branch
git checkout -b <name>       # Create and switch to branch
git merge <branch>           # Merge branch into current branch
git branch -d <name>         # Delete branch (local)
```

### Remote Operations
```bash
git remote -v                # Show remote URLs
git fetch origin             # Fetch changes without merging
git pull origin main         # Fetch and merge
git push origin main         # Push to remote
git push origin <branch>     # Push specific branch
```

---

## Troubleshooting

### Issue: "fatal: not a git repository"
**Solution:** You're not in the project directory
```bash
cd ~/projects/clustering-platform
```

### Issue: "Permission denied (publickey)"
**Solution:** Set up SSH keys or use HTTPS with token
```bash
# Check your remote URL
git remote -v

# If using SSH, set up SSH keys on GitHub
# Or switch to HTTPS
git remote set-url origin https://github.com/karth2k1/clustering-platform.git
```

### Issue: "Your branch is behind 'origin/main'"
**Solution:** Pull the changes
```bash
git pull origin main
```

### Issue: "Your local changes would be overwritten by merge"
**Solution:** Commit or stash your changes first
```bash
# Option 1: Commit changes
git add .
git commit -m "Save work before pulling"
git pull origin main

# Option 2: Stash changes
git stash
git pull origin main
git stash pop
```

### Issue: Merge Conflicts
**Solution:** Resolve conflicts manually
```bash
# Git will mark conflict files
git status

# Open conflicted files and look for:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> origin/main

# Edit the file to resolve
# Then:
git add <resolved-file>
git commit -m "Resolve merge conflict"
git push origin main
```

---

## Environment Variables Reference

Create a `.env` file on each machine with these variables:

```bash
# Database
DATABASE_URL=sqlite:///./clustering.db

# Security
SECRET_KEY=your-secret-key-here

# API Keys (if needed)
API_KEY=your-api-key-here

# Development Settings
DEBUG=True
ENVIRONMENT=development
```

**Note:** Never commit the `.env` file. Only commit `.env.example` with dummy values.

---

## Quick Reference Cheat Sheet

### Start Work
```bash
git pull origin main
source venv/bin/activate
```

### End Work
```bash
git add .
git commit -m "Descriptive message"
git push origin main
deactivate
```

### Emergency Sync Check
```bash
git status                    # What's changed locally?
git log origin/main..HEAD     # What commits haven't been pushed?
git log HEAD..origin/main     # What commits are on remote?
```

---

## Questions or Issues?

If you encounter problems not covered here:
1. Check Git documentation: https://git-scm.com/doc
2. Search on Stack Overflow
3. Review GitHub's Git guides: https://docs.github.com/en/get-started

---

**Last Updated:** December 17, 2024

