# Contributing Guide

## Welcome! 👋

Thank you for your interest in contributing to MiPortafolio. This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the work, not the person
- Help others learn and grow

## Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_USERNAME/MiPortafolio.git
cd MiPortafolio
git remote add upstream https://github.com/Harp-Andres/MiPortafolio.git
```

### 2. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
# or for bug fixes:
git checkout -b bugfix/issue-description
```

### 3. Set Up Development Environment
```bash
pnpm install
pnpm -C apps/web dev  # In one terminal
# (other app setup in another terminal)
```

## Development Workflow

### Branching Strategy

- `main` - Production-ready code (protected)
- `develop` - Development branch (if used)
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `refactor/*` - Code improvements

### Commit Standards

```bash
# Use conventional commits
git commit -m "type(scope): description"

# Types: feat, fix, docs, style, refactor, test, chore
# Examples:
# - feat(web): add dark mode toggle
# - fix(api): resolve authentication issue
# - docs(setup): update installation guide
# - refactor(core): simplify utility functions
```

### Pull Request Process

1. **Ensure branch is up-to-date**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests and checks**
   ```bash
   # Frontend
   pnpm -C apps/web test
   pnpm -C apps/web build
   
   # Backend
   pnpm -C apps/api test
   pnpm -C apps/api lint
   ```

3. **Create Pull Request**
   - Use descriptive title
   - Reference related issues (#123)
   - Describe changes and reasoning
   - Add before/after screenshots if UI changes

4. **Address Review Feedback**
   - Make requested changes
   - Respond to comments
   - Push updates (forces push only if necessary)

## Code Standards

### TypeScript/React (Frontend)
```typescript
// Use TypeScript for all .ts and .tsx files
// Follow ESLint and Prettier configuration
// Use functional components with hooks
// Add proper type annotations

interface UserProps {
  id: string;
  name: string;
  onSelect?: (id: string) => void;
}

export const UserCard: React.FC<UserProps> = ({ id, name, onSelect }) => {
  return (
    <div onClick={() => onSelect?.(id)}>
      {name}
    </div>
  );
};
```

### Python (Backend/Agent)
```python
# Use Python 3.11+ features
# Follow PEP 8 with Black formatting
# Use type hints for all functions
# Add docstrings to classes and functions

from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    """User model for API responses."""
    id: str
    name: str
    email: Optional[str] = None

def get_user(user_id: str) -> Optional[User]:
    """Retrieve a user by ID."""
    # Implementation
    pass
```

## Testing Requirements

### Frontend
```bash
# Unit tests
pnpm -C apps/web test

# E2E tests
pnpm -C apps/web test:e2e

# Coverage
pnpm -C apps/web test:coverage
```

### Backend
```bash
# Run tests
pnpm -C apps/api test

# With coverage
pnpm -C apps/api test:coverage
```

### Agent
```bash
cd agent
pytest tests/
pytest --cov=agent tests/
```

## Documentation

- Update docs/ for user-facing changes
- Add code comments for complex logic
- Update CHANGELOG if applicable
- Include JSDoc/docstrings in code

## Performance Considerations

- Keep bundle size minimal
- Optimize API requests
- Use efficient algorithms
- Profile before optimizing

## Security Guidelines

- Never commit secrets or credentials
- Review dependencies for vulnerabilities
- Use environment variables for sensitive data
- Follow OWASP best practices

## Release Process

1. Version bump (semver)
2. Update CHANGELOG.md
3. Create release commit
4. Tag release
5. Create GitHub Release
6. Deploy to production

## Getting Help

- **Questions**: Open a Discussion
- **Bugs**: Open an Issue with reproducible example
- **Features**: Open an Issue with use case
- **Chat**: Check GitHub Discussions

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in project

## Additional Resources

- [Project Setup](./SETUP.md)
- [Architecture](./MONOREPO_ARCHITECTURE.md)
- [API Documentation](./API.md)
- [Development Notes](./../.dev-docs/)

Thank you for contributing! 🎉
