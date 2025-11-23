# Deployment Checklist

## Pre-Deployment

- [x] All source files committed
- [x] `requirements.txt` updated with all dependencies
- [x] `Procfile` created for Railway
- [x] `railway.json` configured
- [x] `.gitignore` excludes sensitive files
- [x] `runtime.txt` specifies Python version
- [x] Code tested locally

## GitHub Setup

- [ ] Repository created on GitHub
- [ ] All files pushed to GitHub
- [ ] Repository is public or Railway has access
- [ ] `.gitignore` working correctly

## Railway Setup

- [ ] Railway account created
- [ ] Logged into Railway
- [ ] New project created
- [ ] GitHub repository connected
- [ ] Environment variables set:
  - [ ] `OPENROUTER_API_KEY` = `your-api-key-here` (see SECRETS.md for your key)
  - [ ] `PORT` (auto-set by Railway)

## Deployment

- [ ] Railway detected project correctly
- [ ] Build completed successfully
- [ ] Application started without errors
- [ ] Public URL accessible
- [ ] Application loads in browser

## Testing

- [ ] File upload works (Excel)
- [ ] File upload works (PDF)
- [ ] Financial data extraction works
- [ ] Entity information can be entered
- [ ] Directors can be edited
- [ ] Notes can be edited
- [ ] Validation runs successfully
- [ ] PDF preview works
- [ ] PDF generation works
- [ ] PDF download works
- [ ] AI features work (if enabled)

## Post-Deployment

- [ ] Application URL saved
- [ ] Team members notified
- [ ] Documentation updated with URL
- [ ] Monitoring set up
- [ ] Error alerts configured (optional)

## Environment Variables Reference

```
OPENROUTER_API_KEY=your-api-key-here
PORT=8501 (auto-set by Railway)
```

## Quick Deploy Commands

```bash
# 1. Commit and push
git add .
git commit -m "Ready for Railway deployment"
git push origin main

# 2. Then in Railway:
# - Select repository
# - Add environment variables
# - Deploy!
```

## Troubleshooting

If deployment fails:
1. Check Railway build logs
2. Verify all files are in GitHub
3. Check `requirements.txt` is complete
4. Verify `Procfile` syntax
5. Check environment variables are set

## Success Criteria

✅ App accessible via Railway URL
✅ All features working
✅ File uploads functional
✅ PDF generation working
✅ No errors in logs

