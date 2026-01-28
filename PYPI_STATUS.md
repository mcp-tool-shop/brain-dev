# PyPI Publication Status Report

**Last Updated:** January 28, 2026  
**Total Projects:** 27+ (counting all subdirectories)  
**On PyPI:** 18 ✅  
**Pending Publisher Approval:** 2 ⏳  
**Not Python (npm/Node.js):** 5  
**Total Publishable Python:** 25 (18 published + 2 pending + ~5 others)

---

## 📊 Summary by Status

### ✅ Successfully Published to PyPI (18 packages)

**Recently Released (8-9 hours ago - Jan 28, 2026):**
1. **brain-dev** - MCP server for AI-powered code analysis
2. **nexus-router-adapter-http** - HTTP adapter for nexus-router
3. **nexus-router-adapter-stdout** - Debug adapter to stdout
4. **flexiflow** - Async component engine with events & state machines
5. **a11y-ci** - CI gate for a11y-lint scorecards
6. **a11y-lint** - Accessibility linter for CLI output
7. **payroll-engine** - US Payroll SaaS Engine with PSP
8. **nexus-router** - Event-sourced MCP router with provenance
9. **tool-scan** - Security scanner for MCP tools
10. **mcp-stress-test** - Stress testing framework for MCP

**Recently Released (Jan 18-24, 2026):**
11. **headless-wheel-builder** - Universal Python wheel builder (Jan 24)
12. **voice-soundboard** - AI-powered voice soundboard via MCP (Jan 23)
13. **aspire-ai** - Adversarial Student-Professor Reasoning Engine (Jan 22)
14. **integradio** - Vector-embedded Gradio components (Jan 20)
15. **file-compass** - Semantic file search with HNSW indexing (Jan 19)
16. **backpropagate** - Production-ready headless LLM fine-tuning (Jan 19)
17. **tool-compass** - Semantic MCP tool discovery gateway (Jan 18)
18. **comfy-headless** - Headless ComfyUI client with AI prompt intelligence (Jan 18)

---

### ⏳ Pending Publisher Approval (2 packages)

These have workflows configured and are waiting for PyPI to approve the trusted publisher:

| Package | Status | Last Release | Details |
|---------|--------|--------------|---------|
| **code-covered** | Pending | Recent | Code coverage analysis |
| **claude-collaborate** | Pending | Recent | Reference implementation |

**Action:** Approve on PyPI settings → Pending publishers to finalize publication

---

## ⚠️ Non-Python Packages (npm/Node.js) - 5 packages

These cannot be published to PyPI as they are JavaScript/Node.js projects. They should be published to **npm** instead.

| Package | Type | Location | Status |
|---------|------|----------|--------|
| **a11y-evidence-engine** | Node.js | `accessibility/a11y-evidence-engine/` | Should publish to npm |
| **a11y-mcp-tools** | Node.js | `accessibility/a11y-mcp-tools/` | Should publish to npm |
| **prov-engine-js** | Node.js | `core/prov-engine-js/` | Should publish to npm |
| **synthesis** | Node.js/Web | `core/synthesis/` | Should publish to npm |
| **venvkit** | Node.js/Hybrid | `core/venvkit/` | May need npm or PyPI |

**Recommendation:** Set up npm publishing workflows for these projects. Check if they have `.npmrc` or publish scripts configured.

---

## ❌ Missing from PyPI / Not Yet Published

Based on PyPI account verification, these projects are not in the 18 published packages:

### Projects to Investigate (7 candidates)

| Project | Location | Status | Notes |
|---------|----------|--------|-------|
| **audiobooker** | `media/audiobooker/` | Not on PyPI | Has pyproject.toml, verify status |
| **mcpt** | `automation/mcpt/` | Not on PyPI | Has pyproject.toml, verify status |
| **pathway** | `automation/pathway/` | Not on PyPI | Has pyproject.toml, verify status |
| **ally-demo-python** | `reference/ally-demo-python/` | Not on PyPI | Reference implementation? |
| **a11y-assist** | `accessibility/a11y-assist/` | Not on PyPI | Has pyproject.toml, check status |
| **context-window-manager** | `ai/context-window-manager/` | Not on PyPI | Has publish workflow, verify |
| **claude-collaborate** | `reference/claude-collaborate/` | ⏳ Pending | Awaiting publisher approval |

### ✅ Confirmed Fixed

- **nexus-router-adapter-http** ✅ NOW ON PyPI (was not on list but got published 8 hours ago)
- **voice-soundboard** ✅ FIXED (Python 3.14 compatible)
**Details:**
- Has `pyproject.toml` indicating Python project
- Complex project with build/publish features
- May have been intentionally excluded from PyPI (reference implementation)

**Action:** Check git history or documentation for why it wasn't published

---

### 3. Other Potential Issues

Check these projects if they're not accounted for in the "On PyPI" list:

| Project | Location | To Investigate |
|---------|----------|-----------------|
| **comfy-headless** (media) | `media/comfy-headless/` | Duplicate of root-level? Check if both exist |
| **a11y-assist** | `accessibility/a11y-assist/` | Python or Node.js? |
| **a11y-ci** | `accessibility/a11y-ci/` | Python or Node.js? |
| **a11y-lint** | `accessibility/a11y-lint/` | Python or Node.js? |
| **nexus-router-adapter-http** | `core/nexus-router-adapter-http/` | May be npm package |

---

## 🔧 Projects Needing Action

### High Priority (Blocking Issues)

| Project | Issue | Action |
|---------|-------|--------|
| **voice-soundboard** | Python 3.14 incompatibility | Update dependencies or Python requirements |
| **Non-Python packages** | Published to wrong registry | Set up npm publishing |

### Medium Priority (Verification Needed)

| Project | Issue | Action |
|---------|-------|--------|
| **reference/headless-wheel-builder** | Unknown reason | Investigate & clarify |
| **accessibility/** subprojects | Type unclear | Determine language & registry |

---

## 📋 Checklist for New Python Packages

Before publishing to PyPI, ensure:

- [ ] `pyproject.toml` with all required fields (name, version, description)
- [ ] `requires-python` specified (e.g., `>=3.10`)
- [ ] All dependencies are compatible with declared Python versions
- [ ] `README.md` at project root for PyPI display
- [ ] `LICENSE` file present
- [ ] Version follows semantic versioning (e.g., `1.0.0`, not `1.0-beta`)
- [ ] No conflicts with existing PyPI package names
- [ ] Entry points configured (if CLI or MCP server)
- [ ] Tests pass locally
- [ ] Run: `python -m build` successfully creates `.whl` and `.tar.gz`

---

## 📚 Publishing Workflow Reference

### For Python Packages

```bash
# 1. Build distribution
python -m build

# 2. Test locally
pip install dist/package-name-version.whl

# 3. Upload to PyPI (requires API token)
python -m twine upload dist/*
```

### For Node.js Packages

```bash
# 1. Build (if needed)
npm run build

# 2. Test locally
npm install

# 3. Publish to npm (requires npm account)
npm publish
```

---

## 🔗 Resources

- **PyPI:** https://pypi.org/
- **npm Registry:** https://www.npmjs.com/
- **Building Packages:** https://packaging.python.org/tutorials/packaging-projects/
- **Publishing to PyPI:** https://packaging.python.org/guides/publishing-distribution-packages-to-pypi/

---

## 📝 Notes

- Some projects in `reference/` may be intentionally excluded from PyPI (examples/templates)
- `code-covered/` appears to be a special project - verify its purpose
- Consider creating GitHub Actions workflows for automated publishing on version tags
- Maintain this document as new packages are added or publishing status changes

---

## Next Steps

1. **Verify Non-Python Packages:** Confirm all 5 npm packages are properly registered/publishing to npm
2. **Fix voice-soundboard:** Resolve Python 3.14 compatibility issue
3. **Audit Reference Projects:** Determine which should be published vs. kept as examples
4. **Set Up CI/CD:** Add automated PyPI publishing workflows to GitHub Actions
5. **Document Blockers:** Create issues for any remaining publication failures

