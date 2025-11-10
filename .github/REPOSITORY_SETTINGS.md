# Repository Topics and Settings

This file documents the recommended GitHub repository settings.

## Repository Settings

### Basic Information
- **Name:** BAHR
- **Description:** Arabic Poetry Analysis Platform - Prosody Analyzer with Next.js 16 & FastAPI
- **Website:** (Add when deployed)
- **Topics:** See below

### Recommended Topics

Add these topics to your repository via GitHub Settings → Topics:

```
arabic
arabic-nlp
nlp
poetry
prosody
arabic-poetry
nextjs
fastapi
typescript
python
tailwind-css
shadcn-ui
camel-tools
meter-detection
arabic-language
classical-arabic
literary-analysis
machine-learning
```

### Features to Enable

- [x] Issues
- [x] Projects (create a Kanban board)
- [ ] Wiki (optional, we have docs/ folder)
- [x] Discussions (for Q&A)
- [ ] Sponsorships (optional for later)

### Branch Protection Rules

For `main` branch:
- [ ] Require pull request reviews before merging
- [ ] Require status checks to pass (when CI is set up)
- [ ] Require conversation resolution before merging
- [ ] Include administrators

### GitHub Pages (Optional)

If you want to host documentation:
- Source: `main` branch → `/docs` folder
- Theme: GitHub Pages theme or custom

## How to Apply These Settings

### Via GitHub Web Interface:

1. **Add Topics:**
   - Go to: https://github.com/goforwest/BAHR
   - Click ⚙️ (settings icon) next to "About"
   - Add topics from the list above
   - Save changes

2. **Update Description:**
   - Same location as topics
   - Add: "Arabic Poetry Analysis Platform - Prosody Analyzer with Next.js 16 & FastAPI"

3. **Enable Discussions:**
   - Settings → General → Features
   - Check "Discussions"

4. **Set up Projects:**
   - Projects tab → New project
   - Template: "Board"
   - Columns: Backlog, In Progress, Review, Done

### Via GitHub CLI (Alternative):

```bash
# Update description
gh repo edit --description "Arabic Poetry Analysis Platform - Prosody Analyzer with Next.js 16 & FastAPI"

# Add topics (one command)
gh repo edit --add-topic "arabic,arabic-nlp,nlp,poetry,prosody,nextjs,fastapi,typescript,python,tailwind-css,shadcn-ui"

# Enable discussions
gh repo edit --enable-discussions

# Enable issues (already enabled by default)
gh repo edit --enable-issues
```

## Repository Insights

Once set up, your repository will be discoverable via:
- Topic searches (e.g., #arabic-nlp)
- Language statistics (TypeScript + Python)
- GitHub Explore
- Awesome lists (if you submit)

## Social Preview Image (Optional)

Create a custom repository social preview:
1. Settings → General → Social preview
2. Upload 1280x640 image with:
   - "بَحْر BAHR" logo
   - "Arabic Poetry Analysis"
   - Tech stack icons (Next.js, FastAPI)
