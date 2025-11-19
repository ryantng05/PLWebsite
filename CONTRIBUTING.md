# Contributing to Premier League Match Predictor

First off, thank you for considering contributing to Premier League Match Predictor! It's people like you that make this project better for everyone.

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## 🎯 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if applicable**
- **Include your environment details** (OS, Python version, Node version, etc.)

**Bug Report Template:**
```markdown
### Description
[Clear description of the bug]

### Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

### Expected Behavior
[What you expected to happen]

### Actual Behavior
[What actually happened]

### Environment
- OS: [e.g., Windows 11, macOS 14]
- Python: [e.g., 3.11.5]
- Node: [e.g., 20.10.0]
- Browser: [e.g., Chrome 120]

### Screenshots
[If applicable]
```

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternatives you've considered**

### 🔨 Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Commit your changes** with clear commit messages
6. **Push to your fork** and submit a pull request

## 💻 Development Setup

### Backend Setup

```bash
cd pl_predictor_backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup

```bash
cd pl_predictor_frontend
npm install
npm run dev
```

### Database Setup

```bash
docker-compose up -d postgres
cd pl_predictor_backend
python manage.py import_csv_data ../matches.csv
```

## 📝 Coding Standards

### Python (Backend)

- Follow **PEP 8** style guide
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Maximum line length: **88 characters** (Black formatter)
- Use **meaningful variable names**

**Example:**
```python
def calculate_team_form(matches: List[Match], window: int = 5) -> float:
    """
    Calculate team form based on recent matches.
    
    Args:
        matches: List of recent matches
        window: Number of matches to consider (default: 5)
    
    Returns:
        Float representing team form score (0-1)
    """
    if not matches:
        return 0.0
    
    # Implementation here
    pass
```

### TypeScript (Frontend)

- Use **TypeScript** for all new files
- Follow **Airbnb style guide**
- Use **functional components** with hooks
- Write **interface definitions** for props
- Use **meaningful component names**

**Example:**
```typescript
interface TeamStatsProps {
  teamId: number;
  showRecent?: boolean;
}

export default function TeamStats({ teamId, showRecent = true }: TeamStatsProps) {
  const [stats, setStats] = useState<TeamStats | null>(null);
  
  // Implementation here
  
  return (
    <div className="team-stats">
      {/* JSX here */}
    </div>
  );
}
```

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Formatting, missing semicolons, etc
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Maintenance tasks

**Example:**
```
feat(predictions): add confidence score visualization

- Add progress bars for win/draw/loss probabilities
- Update PredictionCard component styling
- Add formatPercentage utility function

Closes #42
```

## 🧪 Testing

### Backend Tests

```bash
cd pl_predictor_backend
python manage.py test
```

Write tests for:
- All API endpoints
- ML model predictions
- Data processing functions
- Database models

### Frontend Tests

```bash
cd pl_predictor_frontend
npm test
```

Write tests for:
- Component rendering
- User interactions
- API integration
- State management

## 📚 Documentation

- Update the README.md if you change functionality
- Add JSDoc/docstrings to new functions
- Update API documentation for endpoint changes
- Add inline comments for complex logic
- Update the CHANGELOG.md

## 🔍 Code Review Process

1. **Automated checks** must pass (linting, tests)
2. **At least one maintainer** must review the PR
3. **All conversations** must be resolved
4. **Branch must be up-to-date** with main
5. **Documentation** must be updated if needed

### What We Look For

- **Correctness**: Does the code work as intended?
- **Design**: Is the code well-structured?
- **Readability**: Is the code easy to understand?
- **Testing**: Are there adequate tests?
- **Documentation**: Are changes documented?
- **Performance**: Are there any performance concerns?

## 🎨 Style Guide

### File Naming

**Python:**
- `snake_case.py` for modules
- `PascalCase` for classes
- `snake_case` for functions and variables

**TypeScript:**
- `PascalCase.tsx` for components
- `camelCase.ts` for utilities
- `PascalCase` for interfaces/types
- `camelCase` for functions and variables

### Project Structure

```
New Backend Feature:
pl_predictor_backend/
└── predictions/
    ├── models.py          # Add model if needed
    ├── serializers.py     # Add serializer
    ├── views.py           # Add view
    ├── urls.py            # Add URL pattern
    └── tests/             # Add tests
        └── test_feature.py

New Frontend Component:
pl_predictor_frontend/
└── src/
    ├── components/
    │   └── NewComponent.tsx
    ├── lib/
    │   └── newUtility.ts
    └── app/
        └── page.tsx       # Update if needed
```

## 🚀 Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create a release branch
4. Test thoroughly
5. Merge to main
6. Tag the release
7. Deploy to production

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: For security issues only

## 🙏 Recognition

Contributors will be:
- Added to the Contributors section
- Mentioned in release notes
- Given credit in commit messages

Thank you for contributing! 🎉

