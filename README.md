# EasyJournal - Academic Journal Submission System

![EasyJournal Logo](generated-icon.png)

## EasyJournal: A Practical Publishing Experiment

EasyJournal was created as an experimental publishing platform built by a publishing expert (with a bit of AI help and no engineers involved). It's designed to get your journal online quickly—in a very short time—without any headaches or heavy costs.

To be clear, the underlying code isn't perfect—it's an experimental prototype, not industrial-strength software. But it works, and it's free for anyone who wants to try it out.

### What I've learned:
AI can accelerate the initial build dramatically. However, turning AI-generated prototypes into scalable, robust software still requires traditional engineering expertise.

For more information see https://robotscooking.com

---

A sophisticated academic journal submission platform leveraging intelligent technology to optimize the research publication workflow.

## Repository Information

- **GitHub Repository**: [https://github.com/Shippies-org/easyjournal-py](https://github.com/Shippies-org/easyjournal-py)

## Project Overview

EasyJournal is a comprehensive platform designed to streamline the academic publishing process while maintaining the highest standards of peer review and editorial integrity. Our system provides tools for:

- Article submissions and tracking
- Peer review management
- Editorial workflows
- Publication and issue management
- Analytics and reporting
- User role management (Author, Reviewer, Editor, Admin)

## Key Features

- **Modular Architecture**: Built with Flask blueprint architecture for maintainability and extensibility
- **Role-Based Access Control**: Different interfaces for authors, reviewers, editors, and administrators
- **Complete Submission Workflow**: From initial submission to final publication
- **Comprehensive Admin Controls**: Including user management, issue creation, and system settings
- **Performance Optimized**: Efficient request handling and database queries for improved response times
- **Analytics Capabilities**: Track site usage, article views, and other important metrics
- **Extensive Branding Customization**: Tailor the system to match your journal's identity
- **GDPR Compliance**: User data management with consent tracking and data portability

## Technology Stack

- **Backend**: Python with Flask framework
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: Bootstrap CSS framework with responsive design
- **Container Support**: Docker configuration for easy deployment

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/Shippies-org/easyjournal-py.git
   cd easyjournal-py
   ```

2. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit `.env` as needed (default values work for most users)

3. Install and run with options below
   
### Option 1: Docker Deployment (Recommended)

EasyJournal includes a fully configured Docker setup for easy deployment:

```bash
# Build and start the application with PostgreSQL database
docker-compose up -d

# Check logs if needed
docker-compose logs -f app

# Stop all containers
docker-compose down
```

The application will be available at http://localhost:5000 with these default credentials:
- Admin: admin@example.com / adminpassword
- Editor: editor@example.com / editorpassword
- Reviewer: reviewer@example.com / reviewerpassword
- Author: author@example.com / authorpassword

### Option 2: Local Installation

For development or customization:

```bash
# Install dependencies
bash setup/install_dependencies.sh

# Start the application
python main.py
```

The application will be available at http://localhost:5000

## Documentation

- [Installation Guide](INSTALL.md) - Complete installation instructions
- [Performance Optimization](PERFORMANCE.md) - Details on performance tuning
- [Development Guide](DEVELOPMENT.md) - Information for developers
- [Scaling Guide](SCALING.md) - Guidance for scaling to larger deployments

## Contribution

We welcome contributions to EasyJournal! Please feel free to submit issues and pull requests to the GitHub repository.

## Other Open-Source Journal Platforms

- [Open Journal Systems (OJS)](https://pkp.sfu.ca/software/ojs/) – Widely adopted journal management and publishing platform.
- [Janeway](https://janeway.systems/) – Modern, modular open-source publishing platform.
- [Kotahi](https://kotahi.community/) – Flexible, microservices-based publishing infrastructure supporting diverse workflows.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

Copyright (c) 2025 Adam Hyde