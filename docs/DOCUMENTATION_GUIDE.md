# 📖 Documentation Creation Guide

**For All Agents & Contributors: Where to Create New Documentation**

---

## 🎯 Quick Decision Tree

```
Do you need to create documentation?
│
├─ Is it for END USERS or EXTERNAL DEVELOPERS?
│  │
│  ├─ YES → Create in `docs/` ✅
│  │  Examples:
│  │  - Installation guide
│  │  - API reference
│  │  - User tutorial
│  │  - Architecture overview
│  │  - Skill documentation
│  │
│  └─ NO → Continue below
│
├─ Is it INTERNAL ANALYSIS or EXPERIMENTATION?
│  │
│  ├─ YES → Create in `.dev-docs/` ✅
│  │  Examples:
│  │  - Session summary
│  │  - Phase report
│  │  - Design analysis
│  │  - Issue investigation
│  │  - Failed attempts
│  │
│  └─ NO → STOP, ask in prompt
│
└─ NOT SURE? → Ask before creating ❌
   Do NOT create files without understanding their purpose
```

---

## 📁 Where Each Document Type Goes

### `docs/` - PRODUCTION DOCUMENTATION

| Document Type | Purpose | Location | Example |
|---|---|---|---|
| Quick Start | Get users started fast | `docs/QUICK_START.md` | 5-minute setup |
| Setup Guide | Detailed installation | `docs/SETUP.md` | Step-by-step install |
| User Reference | What users need to know | `docs/MAESTRO_REFERENCE.md` | How to use Maestro |
| API Reference | API endpoints & usage | `docs/API.md` | Endpoint documentation |
| Skill Catalog | Available skills | `docs/SKILLS.md` | Skill descriptions |
| Contributing | How to contribute | `docs/CONTRIBUTING.md` | Contribution rules |
| Dev Guide | Development setup | `docs/DEVELOPMENT/` | Monorepo, testing, etc. |
| Workflow Doc | User workflows | `docs/CV_MANAGEMENT/` | CV generation process |

### `.dev-docs/` - DEVELOPMENT DOCUMENTATION

| Document Type | Purpose | Location | Example |
|---|---|---|---|
| Session Summary | What happened today | `.dev-docs/sessions/` | Work progress notes |
| Phase Report | What was completed | `.dev-docs/phases/` | Phase 1 completion |
| Status Report | Current state | `.dev-docs/reports/` | Weekly status update |
| Architecture Analysis | Design decisions | `.dev-docs/architecture/` | Monorepo analysis |
| Technical Analysis | Deep dive | `.dev-docs/maestro/` | Agent system analysis |
| Investigation Notes | Problem analysis | `.dev-docs/guides/` | Debugging guide |

---

## 🚫 What NEVER Goes in Root (`/`)

**FORBIDDEN in root:**
- ❌ Analysis documents
- ❌ Session summaries
- ❌ Status reports
- ❌ Phase completion docs
- ❌ Random Markdown files
- ❌ Old draft documentation

**ONLY allowed in root:**
- ✅ `README.md` (project start)
- ✅ `package.json`, `pnpm-workspace.yaml` (config files)
- ✅ `.env.example` (template)

---

## 📋 How to Create a Document

### Step 1: Determine Purpose
Ask yourself: "Who is this for?"
- Users/External? → `docs/`
- Internal/Analysis? → `.dev-docs/`

### Step 2: Choose Location
Use the decision tree or table above

### Step 3: Create File
Use proper naming:
- **For production**: `TOPIC.md` or `TOPIC/SUBTOPIC.md`
- **For development**: `REPORT_topic_YYYYMMDD.md` or `ANALYSIS_topic.md`

### Step 4: Structure Content
Always include:
```markdown
# Title

**Purpose**: What is this for?
**Audience**: Who should read this?
**Date**: YYYY-MM-DD (for dev docs)

---

## Content

[Your content here]

---

**Last updated**: YYYY-MM-DD
```

### Step 5: Reference in Index
- Production → Update `docs/README.md`
- Development → Update `.dev-docs/README.md`

---

## ✅ Checklist Before Creating

- [ ] Purpose is clear (user guide vs internal analysis)
- [ ] Location is correct (`docs/` vs `.dev-docs/`)
- [ ] Similar doc doesn't already exist
- [ ] Filename is descriptive
- [ ] Content is well-structured
- [ ] Proper markdown formatting
- [ ] Added to appropriate README.md index

---

## 🤖 For AI Agents

**Default Behavior:**
1. When creating docs, ALWAYS ask: "Is this for users or internal?"
2. If unsure, say so in the prompt
3. Wait for confirmation before creating
4. Reference this guide in your reasoning

**Good Responses:**
- ✅ "This is an installation guide for users → I'll create `docs/SETUP.md`"
- ✅ "This is a session analysis → I'll create `.dev-docs/sessions/SESSION_*.md`"
- ✅ "I'm not sure if this is for users or internal. Should I create `docs/` or `.dev-docs/`?"

**Bad Responses:**
- ❌ Create file without saying where
- ❌ Create in root directory
- ❌ Create without understanding purpose
- ❌ Ignore this guide

---

## 📞 Questions?

- Structure unclear? → Read `docs/README.md`
- Dev docs structure? → Read `.dev-docs/README.md`
- Still unsure? → Ask in your prompt before creating

---

**Last Updated**: 2026-09-15
**Applies To**: All agents, all contributors
