#!/usr/bin/env python3
"""
MCP Server that provides team coding standards as a markdown resource.
"""

from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Team Coding Standards Server")

# Coding standards content as markdown
CODING_STANDARDS_CONTENT = """# Team Coding Standards

## General Principles

### Code Quality
- Write clean, readable, and maintainable code
- Follow the principle of least surprise
- Prefer explicit over implicit
- Keep functions and classes focused on a single responsibility
- Use meaningful names for variables, functions, and classes

### Documentation
- Write clear, concise docstrings for all public functions and classes
- Include type hints for function parameters and return values
- Maintain up-to-date README files for all projects
- Document complex algorithms and business logic inline

## Language-Specific Standards

### Python
- Follow PEP 8 style guidelines
- Use type hints consistently
- Prefer f-strings for string formatting
- Use list/dict comprehensions when they improve readability
- Import order: standard library, third-party, local imports
- Maximum line length: 88 characters (Black formatter standard)
- Use `pathlib` for file path operations
- Prefer `dataclasses` or `pydantic` models for structured data

### JavaScript/TypeScript
- Use TypeScript for all new projects
- Follow ESLint and Prettier configurations
- Use `const` by default, `let` when reassignment is needed
- Prefer arrow functions for callbacks and short functions
- Use async/await over Promise chains
- Implement proper error handling with try/catch blocks
- Use meaningful variable names (avoid abbreviations)

### SQL
- Use uppercase for SQL keywords (SELECT, FROM, WHERE, etc.)
- Use snake_case for table and column names
- Always use explicit JOIN syntax
- Include proper indexing strategies
- Use parameterized queries to prevent SQL injection
- Format complex queries with proper indentation

## Git Workflow

### Commit Messages
- Use conventional commit format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Keep subject line under 50 characters
- Use imperative mood ("Add feature" not "Added feature")
- Include body for complex changes explaining why, not what

### Branch Naming
- Use descriptive branch names: `feature/user-authentication`
- Prefixes: `feature/`, `bugfix/`, `hotfix/`, `chore/`
- Use kebab-case for branch names
- Delete branches after merging

### Pull Requests
- Write clear PR titles and descriptions
- Include screenshots for UI changes
- Request appropriate reviewers
- Ensure CI/CD checks pass before merging
- Squash commits when merging to maintain clean history

## Code Review Guidelines

### For Authors
- Keep PRs small and focused (< 400 lines when possible)
- Self-review your code before requesting review
- Provide context and reasoning in PR description
- Respond to feedback promptly and professionally
- Test your changes thoroughly

### For Reviewers
- Review within 24 hours when possible
- Focus on logic, security, and maintainability
- Provide constructive feedback with suggestions
- Approve when code meets standards, even if not perfect
- Use "Request Changes" sparingly and with clear reasoning

## Testing Standards

### Unit Tests
- Aim for 80%+ code coverage
- Write tests before or alongside code (TDD/BDD)
- Use descriptive test names that explain the scenario
- Follow AAA pattern: Arrange, Act, Assert
- Mock external dependencies appropriately

### Integration Tests
- Test critical user journeys end-to-end
- Use realistic test data
- Ensure tests are deterministic and repeatable
- Clean up test data after each test

### Test Organization
- Keep tests close to the code they test
- Use consistent naming conventions
- Group related tests in describe/context blocks
- Maintain test fixtures and utilities

## Security Guidelines

### General Security
- Never commit secrets, API keys, or passwords
- Use environment variables for configuration
- Implement proper authentication and authorization
- Validate and sanitize all user inputs
- Use HTTPS for all external communications
- Keep dependencies up to date

### Data Protection
- Follow GDPR/privacy regulations
- Implement proper data encryption at rest and in transit
- Use secure session management
- Log security events appropriately
- Implement proper backup and recovery procedures

## Performance Guidelines

### General Performance
- Profile before optimizing
- Focus on algorithmic improvements first
- Cache expensive operations appropriately
- Use database indexes effectively
- Implement proper pagination for large datasets

### Frontend Performance
- Optimize images and assets
- Implement lazy loading for non-critical content
- Minimize bundle sizes
- Use CDNs for static assets
- Implement proper caching strategies

### Backend Performance
- Use connection pooling for databases
- Implement proper rate limiting
- Use asynchronous processing for heavy operations
- Monitor and log performance metrics
- Implement proper error handling and timeouts

## Deployment and DevOps

### CI/CD
- Automate testing and deployment pipelines
- Use infrastructure as code (Terraform, CloudFormation)
- Implement proper staging environments
- Use feature flags for gradual rollouts
- Monitor deployment success and rollback capabilities

### Monitoring
- Implement comprehensive logging
- Use structured logging (JSON format)
- Monitor application metrics and alerts
- Implement health checks for all services
- Use distributed tracing for microservices

## Code Organization

### Project Structure
- Use consistent directory structures across projects
- Separate concerns (models, views, controllers, services)
- Keep configuration files in a dedicated directory
- Use meaningful file and directory names
- Maintain clean separation between business logic and framework code

### Dependency Management
- Pin dependency versions in production
- Regularly update dependencies
- Use virtual environments (Python) or package-lock files (Node.js)
- Document system requirements clearly
- Avoid unnecessary dependencies

## Communication and Collaboration

### Team Communication
- Use clear, professional communication
- Document decisions and architectural choices
- Share knowledge through code reviews and pair programming
- Maintain team coding standards documentation
- Conduct regular retrospectives and improvements

### Knowledge Sharing
- Write technical documentation for complex systems
- Create runbooks for operational procedures
- Share learnings through team presentations
- Maintain architectural decision records (ADRs)
- Contribute to team knowledge base

---

*Last updated: January 2025*
*Version: 1.0*

These standards are living documents and should be updated as our team and technology stack evolves.
"""

@mcp.resource(
    uri="resource://coding-standards",
    name="Team Coding Standards",
    description="Comprehensive coding standards and best practices for our development team",
    mime_type="text/markdown",
    tags={"documentation", "standards", "guidelines"}
)
def get_coding_standards() -> str:
    """Returns the team's coding standards as a markdown document."""
    return CODING_STANDARDS_CONTENT

@mcp.resource(
    uri="standards://summary",
    name="Coding Standards Summary",
    description="A brief summary of key coding standards",
    mime_type="text/markdown",
    tags={"documentation", "summary"}
)
def get_standards_summary() -> str:
    """Returns a summary of the most important coding standards."""
    return """# Coding Standards Summary

## Quick Reference

### Code Quality
- Write clean, readable code with meaningful names
- Follow language-specific style guides (PEP 8 for Python, ESLint for JS/TS)
- Use type hints and proper documentation
- Keep functions focused on single responsibility

### Git Workflow
- Use conventional commits: `type(scope): description`
- Create descriptive branch names with prefixes
- Keep PRs small and focused
- Review code within 24 hours

### Testing
- Aim for 80%+ test coverage
- Write tests alongside code
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

### Security
- Never commit secrets
- Validate all user inputs
- Use HTTPS and proper authentication
- Keep dependencies updated

### Performance
- Profile before optimizing
- Cache expensive operations
- Use proper database indexing
- Monitor and log metrics

For complete details, see the full coding standards document.
"""

@mcp.resource(
    uri="standards://checklist/{language}",
    name="Language-Specific Checklist",
    description="Get a checklist for specific programming languages",
    mime_type="text/markdown",
    tags={"checklist", "language-specific"}
)
def get_language_checklist(language: str) -> str:
    """Returns a checklist for the specified programming language."""
    
    checklists = {
        "python": """# Python Code Review Checklist

## Style and Formatting
- [ ] Follows PEP 8 guidelines
- [ ] Line length ≤ 88 characters
- [ ] Proper import order (stdlib, third-party, local)
- [ ] Uses f-strings for string formatting
- [ ] Consistent use of quotes

## Type Hints and Documentation
- [ ] Type hints on function parameters and returns
- [ ] Docstrings for all public functions/classes
- [ ] Complex logic is commented
- [ ] README updated if needed

## Code Quality
- [ ] Functions have single responsibility
- [ ] Meaningful variable and function names
- [ ] Uses pathlib for file operations
- [ ] Proper exception handling
- [ ] No hardcoded values (use constants/config)

## Testing
- [ ] Unit tests written/updated
- [ ] Test coverage ≥ 80%
- [ ] Tests use descriptive names
- [ ] Mocks used for external dependencies
""",
        
        "javascript": """# JavaScript/TypeScript Code Review Checklist

## TypeScript Usage
- [ ] Uses TypeScript for new code
- [ ] Proper type definitions
- [ ] No 'any' types without justification
- [ ] Interfaces defined for complex objects

## Style and Formatting
- [ ] ESLint rules followed
- [ ] Prettier formatting applied
- [ ] Uses const/let appropriately
- [ ] Arrow functions for callbacks

## Code Quality
- [ ] Async/await over Promise chains
- [ ] Proper error handling (try/catch)
- [ ] Meaningful variable names
- [ ] Functions are pure when possible
- [ ] No console.log in production code

## Testing
- [ ] Unit tests written/updated
- [ ] Integration tests for critical paths
- [ ] Test files follow naming convention
- [ ] Mocks used appropriately
""",
        
        "sql": """# SQL Code Review Checklist

## Style and Formatting
- [ ] SQL keywords in UPPERCASE
- [ ] snake_case for table/column names
- [ ] Proper indentation for complex queries
- [ ] Explicit JOIN syntax used

## Performance
- [ ] Appropriate indexes considered
- [ ] Query performance analyzed
- [ ] LIMIT used for large result sets
- [ ] Efficient WHERE clauses

## Security
- [ ] Parameterized queries used
- [ ] No SQL injection vulnerabilities
- [ ] Proper access controls
- [ ] Sensitive data handling

## Best Practices
- [ ] Meaningful table/column names
- [ ] Proper foreign key constraints
- [ ] Transaction boundaries appropriate
- [ ] Error handling implemented
"""
    }
    
    language_lower = language.lower()
    if language_lower in checklists:
        return checklists[language_lower]
    else:
        available_languages = ", ".join(checklists.keys())
        return f"""# Language Not Found

The language '{language}' is not available in our checklist system.

Available languages: {available_languages}

Please use one of the available languages or request a new checklist to be added.
"""

if __name__ == "__main__":
    mcp.run()