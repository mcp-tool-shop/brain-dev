# PyPI Publishing Instructions

## Status: All Projects Ready! 🚀

### Projects Ready to Publish (6 projects)

These projects now have publish workflows configured and just need you to create GitHub releases to trigger PyPI publication:

1. **audiobooker** - `media/audiobooker/`
2. **mcpt** - `automation/mcpt/`
3. **pathway** - `automation/pathway/`
4. **ally-demo-python** - `reference/ally-demo-python/`
5. **a11y-assist** - `accessibility/a11y-assist/`
6. **context-window-manager** - `ai/context-window-manager/` (already has workflow)

### Still Pending PyPI Approval (2 projects)

These are ready to publish but need approval in PyPI's pending publishers:

1. **code-covered** - Go to https://pypi.org/manage/account/publishing/ and approve
2. **claude-collaborate** - Go to https://pypi.org/manage/account/publishing/ and approve

---

## How to Publish

### Option 1: GitHub Web UI (Easiest)

For each project that needs publishing:

1. Go to the repository on GitHub
   - Example: https://github.com/mcp-tool-shop/audiobooker

2. Click **Releases** on the right sidebar

3. Click **Draft a new release**

4. Fill in:
   - **Tag version:** Use the version from `pyproject.toml`
     - Example: `v1.0.0` (use `v` prefix)
   - **Release title:** Same as tag or descriptive
     - Example: `Release 1.0.0`
   - **Description:** What's new (optional)

5. Click **Publish release**

6. GitHub Actions will automatically:
   - Build the wheel and tarball
   - Run package checks
   - Upload to PyPI

### Option 2: Command Line (Using gh CLI)

```bash
cd path/to/project
# Get version from pyproject.toml
VERSION=$(grep 'version' pyproject.toml | head -1 | awk -F'"' '{print $2}')

# Create and publish release
gh release create "v${VERSION}" --title "Release ${VERSION}" --generate-notes
```

---

## Workflow Details

Each project now has `.github/workflows/publish.yml` that:

1. **Triggers on:** GitHub release published
2. **Builds:** Python wheel and source distribution
3. **Validates:** Checks for common issues with `twine check`
4. **Publishes to:** PyPI using GitHub's trusted publisher system (no tokens needed!)

---

## Checking Status

After you publish a release:

1. **Check GitHub Actions:** https://github.com/mcp-tool-shop/PROJECT/actions
   - Watch for the **Publish to PyPI** workflow
   - Should complete in 1-2 minutes

2. **Check PyPI:** https://pypi.org/project/PROJECT_NAME/
   - New version should appear within minutes

3. **Verify installed:** 
   ```bash
   pip install --upgrade PROJECT_NAME
   ```

---

## Release Checklist

Before releasing each project, verify:

- [ ] Version in `pyproject.toml` is correct
- [ ] README.md exists and is current
- [ ] LICENSE file exists
- [ ] `git add` and `git commit` any final changes
- [ ] `git push` to main branch
- [ ] Create release on GitHub with matching version tag

---

## For Multiple Releases

Create all 6 releases in order:

```
1. audiobooker → v1.1.0 (or current version)
2. mcpt → vX.X.X
3. pathway → vX.X.X
4. ally-demo-python → vX.X.X
5. a11y-assist → vX.X.X
6. context-window-manager → v0.6.2 (or current)
```

Each will publish independently as you create the release.

---

## Approving Pending Publishers

For `code-covered` and `claude-collaborate`:

1. Go to https://pypi.org/manage/account/publishing/
2. Under "Pending publishers", click the project
3. Review repository details
4. Click "Approve"

Once approved, their workflows will work too!

---

## Need Help?

- **Workflow failed?** Check GitHub Actions logs for error details
- **Version mismatch?** Make sure tag matches `pyproject.toml` version
- **PyPI credentials?** Using trusted publishers - no manual tokens needed
- **Still pending?** Reach out on PyPI's support

---

**Total projects to publish: 6 + 2 pending = 8**  
**Time to publish all: ~10-15 minutes**  
**Effort: Click 6-8 times on GitHub + 2 approvals on PyPI** ✨

Good luck! 🚀
