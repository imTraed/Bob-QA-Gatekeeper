# Repository Cleanup Guide

This guide explains how to prepare your local repository for pushing to a public GitHub repository.

## Files and Folders to Remove Before Publishing

The following files/folders should **NOT** be pushed to the public repository as they are part of the Python virtual environment or contain local data:

### Virtual Environment Folders (Already in .gitignore)
- `Lib/` - Python library files
- `Include/` - Python header files  
- `Scripts/` - Python executable scripts
- `venv/`, `env/`, `.venv/` - Virtual environment directories
- `pyvenv.cfg` - Virtual environment configuration

### Local Data (Already in .gitignore)
- `database/*.db` - SQLite database files
- `.env` - Your personal environment variables with API keys
- `__pycache__/` - Python bytecode cache
- `.vscode/` - VS Code settings

## What IS Included in the Repository

✅ **Source Code**
- `app.py` - Main application
- `config.py` - Configuration classes
- `setup_db.py` - Database initialization
- `translations.py` - Internationalization
- `models/` - Database models
- `routes/` - Flask blueprints
- `ai_integration/` - AI modules
- `static/` - CSS and JavaScript
- `templates/` - HTML templates

✅ **Configuration Templates**
- `.env.example` - Template for environment variables
- `.gitignore` - Git ignore rules
- `requirements.txt` - Python dependencies

✅ **Documentation**
- `README.md` - Project documentation
- `CONTRIBUTING.md` - Contribution guidelines
- `CLEANUP_GUIDE.md` - This file

✅ **Database Structure**
- `database/.gitkeep` - Keeps the directory in git (but not the .db files)

## Steps to Clean and Publish

### 1. Verify .gitignore is Working

Check what files git will track:
```bash
git status
```

You should NOT see:
- `Lib/`, `Include/`, `Scripts/`
- `.env` file
- `*.db` files
- `__pycache__/` folders

### 2. Remove Tracked Files (if any were committed before)

If you accidentally committed sensitive files before, remove them:
```bash
# Remove from git but keep locally
git rm --cached .env
git rm --cached -r Lib/
git rm --cached -r Include/
git rm --cached -r Scripts/
git rm --cached database/*.db

# Commit the removal
git commit -m "Remove sensitive and unnecessary files"
```

### 3. Verify No Sensitive Data in Code

Search for hardcoded secrets:
```bash
# Search for potential API keys
grep -r "sk-" . --exclude-dir={Lib,Include,Scripts,venv,.git}
grep -r "api_key" . --exclude-dir={Lib,Include,Scripts,venv,.git}
grep -r "password" . --exclude-dir={Lib,Include,Scripts,venv,.git}
```

All sensitive data should be loaded from environment variables using `os.getenv()`.

### 4. Create .env from .env.example

```bash
cp .env.example .env
# Edit .env and add your actual API keys
```

### 5. Test the Application

Make sure everything works with environment variables:
```bash
python setup_db.py
python app.py
```

### 6. Initialize Git Repository (if not already done)

```bash
git init
git add .
git commit -m "Initial commit - Clean repository ready for public release"
```

### 7. Push to GitHub

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/your-username/your-repo-name.git

# Push to GitHub
git push -u origin main
```

## Security Checklist

Before pushing to public GitHub, verify:

- [ ] `.env` file is NOT in the repository
- [ ] `.env.example` exists with placeholder values
- [ ] No API keys in source code
- [ ] No passwords in source code
- [ ] No database files (.db) in repository
- [ ] Virtual environment folders (Lib/, Include/, Scripts/) are not tracked
- [ ] `.gitignore` is properly configured
- [ ] All sensitive data uses environment variables
- [ ] README.md has clear setup instructions
- [ ] CONTRIBUTING.md exists for contributors

## What Users Will Need to Do

After cloning your public repository, users will need to:

1. Create a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`
4. Add their own API keys to `.env`
5. Run `python setup_db.py` to create the database
6. Run `python app.py` to start the application

## Emergency: Removing Committed Secrets

If you accidentally pushed secrets to GitHub:

1. **Immediately revoke/regenerate the exposed API keys**
2. Remove from git history:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   
   git push origin --force --all
   ```
3. Consider the exposed keys compromised and rotate them

## Additional Resources

- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [Python .gitignore template](https://github.com/github/gitignore/blob/main/Python.gitignore)
- [Best practices for API keys](https://cloud.google.com/docs/authentication/api-keys)

---

**Remember**: Once something is pushed to a public repository, assume it's public forever. Always double-check before pushing!