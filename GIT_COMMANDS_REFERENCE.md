# 🚀 GitHub Deployment - Complete Terminal Commands Reference

**Project**: Secure Coding Review  
**Repository**: https://github.com/Pratikshaprabhakarbande/CodeAlpha_SecureCodingReview  
**Date**: May 23, 2026  

---

## ✅ Complete Command Sequence (Ready to Use)

Copy and paste these commands in order. This is the exact sequence that was executed:

### Step 1: Verify Git Installation
```bash
git --version
```

**Expected Output**:
```
git version 2.53.0.windows.2
```

---

### Step 2: Check Repository Status
```bash
cd c:\CodeAlpha_SecureCodingReview
git status
```

**Expected Output** (on first run):
```
fatal: not a git repository
```

This is normal - repository not initialized yet.

---

### Step 3: Initialize Git Repository
```bash
git init
git config user.name "Pratiksha Prabhakarbande"
git config user.email "pratikshaprabhakarbande@example.com"
git status
```

**Expected Output**:
```
Initialized empty Git repository in C:/CodeAlpha_SecureCodingReview/.git/
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what you want to commit)
        .gitignore
        PROJECT_SUMMARY.md
        README.md
        app.py
        ...
```

---

### Step 4: Stage All Files
```bash
git add .
git status
```

**Expected Output**:
```
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .gitignore
        new file:   PROJECT_SUMMARY.md
        new file:   README.md
        new file:   app.py
        ...
```

---

### Step 5: Create Initial Commit
```bash
git commit -m "Completed Secure Coding Review cybersecurity internship project"
git log --oneline
```

**Expected Output**:
```
[master (root-commit) 6a9e4dd] Completed Secure Coding Review cybersecurity internship project
 8 files changed, 2240 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 PROJECT_SUMMARY.md
 ...

6a9e4dd (HEAD -> master) Completed Secure Coding Review cybersecurity internship project
```

---

### Step 6: Rename Branch to Main
```bash
git branch -M main
git branch -v
```

**Expected Output**:
```
* main 6a9e4dd Completed Secure Coding Review cybersecurity internship project
```

---

### Step 7: Check for Existing Remote
```bash
git remote -v
```

**Expected Output** (First time):
```
(no output - which means no remote exists)
```

---

### Step 8: Add GitHub Remote
```bash
git remote add origin https://github.com/Pratikshaprabhakarbande/CodeAlpha_SecureCodingReview.git
git remote -v
```

**Expected Output**:
```
origin  https://github.com/Pratikshaprabhakarbande/CodeAlpha_SecureCodingReview.git (fetch)
origin  https://github.com/Pratikshaprabhakarbande/CodeAlpha_SecureCodingReview.git (push)
```

---

### Step 9: Push to GitHub
```bash
git push -u origin main
```

**Expected Output**:
```
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 2 threads
Compressing objects: 100% (7/7), done.
Writing objects: 100% (9/9), 2.24 KiB | 2.24 MiB/s, done.
Total 9 (delta 0), reused 0 (delta 0), from 0
remote: 
remote: Create a pull request for 'main' on GitHub by visiting:
remote:      https://github.com/Pratikshaprabhakarbande/CodeAlpha_SecureCodingReview/pull/new/main
remote: 
To https://github.com/Pratikshaprabhakarbande/CodeAlpha_SecureCodingReview.git
 * [new branch]      main -> main
```

---

### Step 10: Verify Deployment Success
```bash
git status
git log --oneline
git remote -v
```

**Expected Output**:
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean

6a9e4dd (HEAD -> main, origin/main) Completed Secure Coding Review cybersecurity internship project

origin  https://github.com/Pratikshaprabhakarbande/CodeAlpha_SecureCodingReview.git (fetch)
origin  https://github.com/Pratikshaprabhakarbande/CodeAlpha_SecureCodingReview.git (push)
```

---

## 🔄 Common Git Commands for Future Updates

### After Making Changes to Files
```bash
git status
git add .
git commit -m "Description of changes"
git push origin main
```

### To View Commit History
```bash
git log --oneline
git log --oneline -5  # Last 5 commits
```

### To Check What Changed
```bash
git diff
git diff HEAD~1  # Compare to previous commit
```

### To Undo Recent Changes
```bash
# Before committing
git checkout -- filename.py

# After committing (undo last commit, keep changes)
git reset --soft HEAD~1

# After committing (undo last commit, discard changes)
git reset --hard HEAD~1
```

### To Create a New Branch (for future features)
```bash
git checkout -b feature-name
git push -u origin feature-name
```

---

## ⚠️ Error Handling Guide

### Issue: "fatal: not a git repository"
**Solution**: You need to initialize git first
```bash
git init
```

---

### Issue: "The authenticity of host 'github.com' can't be established"
**Solution**: This is normal on first connection. Type `yes` and press Enter.

---

### Issue: "Permission denied (publickey)"
**Solution**: You need to set up SSH keys or use HTTPS (included in your setup)

---

### Issue: Remote Origin Already Exists
**Solution**: Remove and replace it
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

---

### Issue: Branch Already Exists with Name "main"
**Solution**: This shouldn't happen, but if it does:
```bash
git branch -D main  # Delete the old main
git branch -M main  # Rename current branch to main
```

---

## 📋 One-Command Deployment (For Reference)

This is a single command that does everything (for future similar projects):

```bash
cd /path/to/project && git init && git config user.name "Your Name" && git config user.email "your@email.com" && git add . && git commit -m "Initial commit" && git branch -M main && git remote add origin https://github.com/username/repo.git && git push -u origin main
```

---

## 📁 Project Structure After Deployment

```
CodeAlpha_SecureCodingReview/
├── .git/                              # Git repository data
├── .gitignore                          # Git ignore rules
├── app.py                              # Main vulnerable app
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
├── review_report.md                    # Security analysis
├── PROJECT_SUMMARY.md                  # Project overview
├── GITHUB_DEPLOYMENT_GUIDE.md          # Deployment guide
├── bandit_report.txt                   # Text security report
└── bandit_report_raw.json              # JSON security report
```

---

## ✅ Verification Checklist

After completing all steps, verify:

- [ ] `git status` shows "nothing to commit, working tree clean"
- [ ] `git log --oneline` shows your commits
- [ ] `git remote -v` shows GitHub origin
- [ ] Repository is visible at https://github.com/Pratikshaprabhakarbande/CodeAlpha_SecureCodingReview
- [ ] All files appear on GitHub
- [ ] README.md renders properly on GitHub
- [ ] Branch is set to "main"

---

## 🚀 Quick Copy-Paste Command Set

### For Beginners (Run one at a time)
```bash
# 1. Navigate to project
cd c:\CodeAlpha_SecureCodingReview

# 2. Initialize
git init

# 3. Configure
git config user.name "Pratiksha Prabhakarbande"
git config user.email "pratikshaprabhakarbande@example.com"

# 4. Stage files
git add .

# 5. Commit
git commit -m "Completed Secure Coding Review cybersecurity internship project"

# 6. Rename branch
git branch -M main

# 7. Add remote
git remote add origin https://github.com/Pratikshaprabhakarbande/CodeAlpha_SecureCodingReview.git

# 8. Push
git push -u origin main

# 9. Verify
git status
git log --oneline
```

### For Advanced Users (Copy entire block and paste)
```bash
cd c:\CodeAlpha_SecureCodingReview && \
git init && \
git config user.name "Pratiksha Prabhakarbande" && \
git config user.email "pratikshaprabhakarbande@example.com" && \
git add . && \
git commit -m "Completed Secure Coding Review cybersecurity internship project" && \
git branch -M main && \
git remote add origin https://github.com/Pratikshaprabhakarbande/CodeAlpha_SecureCodingReview.git && \
git push -u origin main && \
git status && \
git log --oneline
```

---

## 📊 Final Status

**Repository**: ✅ Created and deployed  
**Main Branch**: ✅ Set as default  
**All Files**: ✅ Pushed to GitHub  
**Remote Connection**: ✅ Verified  
**Commits**: ✅ Professional message  
**Status**: ✅ Ready for interview/portfolio  

---

**Deployment Date**: May 23, 2026  
**Status**: 🟢 COMPLETE & VERIFIED  
**Ready For**: LinkedIn, Resume, Interviews, Applications
