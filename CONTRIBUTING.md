# Contributing to SmartTourism City Guide

Thank you for your interest in contributing! This document explains how we work and how you can participate.

---

## 🔄 Workflow: GitHub Flow

We use **GitHub Flow** for all contributions. Here's how it works:

### Step 1: Create an Issue
Before starting work, create an issue describing what you want to implement:
- **Feature**: New functionality (F1-F6 components, enhancements)
- **Bugfix**: Fix for existing issues
- **Improvement**: Code quality, documentation, testing

### Step 2: Create a Feature Branch

```bash
git checkout -b feature/issue-<NUMBER>-<short-description>
# Example: feature/issue-5-smart-map-integration
```

**Branch naming rules:**
- `feature/issue-N-...` for new features
- `bugfix/issue-N-...` for bug fixes
- `docs/issue-N-...` for documentation

### Step 3: Implement Your Changes

- Write clean, readable code
- Follow the project's style guide (see below)
- Add tests for new functionality
- Update documentation if needed
- Commit with clear messages

### Step 4: Commit with References

```bash
git commit -m "Add smart map integration. Fixes #5"
git commit -m "Fix occupancy calculation. Refs #7"
```

**Message format:**
- Start with action verb (Add, Fix, Update, Remove, Refactor)
- Reference the issue: `Fixes #N` or `Refs #N`
- Keep first line under 50 characters
- Add detailed explanation in body if needed

### Step 5: Push and Create Pull Request

```bash
git push origin feature/issue-N-description
```

Then on GitHub:
1. Create a Pull Request from your branch to `main`
2. Include issue reference in PR title: "Feature: Smart map (#5)"
3. Describe what you implemented
4. Link related issues

### Step 6: Review & Merge

- Maintainers will review your PR
- Address any feedback
- Once approved, your PR will be merged to `main`
- The issue will be automatically closed (if PR references it)

---

## 💻 Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose

### Local Development

```bash
# Clone and enter repo
git clone https://github.com/pablorubal/SmartTourism-City-Guide.git
cd SmartTourism-City-Guide

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
make install

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start development
make dev
```

---

## 📋 Code Style Guide

### Python (Backend)

```bash
# Format with Black
black .

# Lint with Flake8
flake8 .

# Type checking with Mypy (optional)
mypy backend/
```

**Conventions:**
- Use type hints: `def get_poi(poi_id: int) -> POI:`
- Docstrings for modules, functions, and classes
- Maximum line length: 100 characters
- Use descriptive variable names

### JavaScript (Frontend)

```bash
cd frontend
npm run lint
npm run format
```

**Conventions:**
- Use ESLint + Prettier
- React hooks preferred over class components
- Descriptive component names
- Props with PropTypes or TypeScript

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest -v
pytest --cov=app  # Coverage report
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

**Coverage requirements:**
- Aim for >80% code coverage
- Critical paths should have >90%

---

## 📚 Documentation

Update docs when:
- Adding new features
- Changing API endpoints
- Modifying data models
- Updating setup instructions

**Documentation files:**
- `docs/API.md` - REST endpoints & examples
- `docs/ENTITIES.md` - NGSI-LD specifications
- `docs/ARCHITECTURE.md` - System design
- `docs/SETUP.md` - Installation guides
- README.md - Overview & quick start

---

## 🎯 Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Issue created and referenced in branch name
- [ ] Code follows style guide (black, eslint)
- [ ] Tests added/updated for new functionality
- [ ] All tests pass (`pytest`, `npm test`)
- [ ] Documentation updated
- [ ] Commit messages reference the issue
- [ ] No merge conflicts with `main`
- [ ] PR title includes issue number: "Feature: X (#N)"

---

## 🚫 What NOT to Do

- ❌ Don't commit to `main` directly
- ❌ Don't mix multiple issues in one branch
- ❌ Don't push without clear commit messages
- ❌ Don't skip tests
- ❌ Don't ignore code style
- ❌ Don't update version numbers (maintainers only)

---

## 🆘 Getting Help

-📖 Check [docs/](docs/) for guides
- 💬 Comment on issues for clarification
- 🐛 Found a bug? Create an issue with reproduction steps
- 💡 Have an idea? Start a discussion issue first

---

## 📞 Questions?

- Create an issue with label `question`
- Join discussions in existing issues
- Contact maintainers (see README.md)

---

**Thank you for contributing to SmartTourism! 🎉**
