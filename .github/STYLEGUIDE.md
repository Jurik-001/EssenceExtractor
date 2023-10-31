# Style Guide for EssenceExtractor Project

Welcome to the EssenceExtractor project! We are thrilled to have you here. This document outlines the coding conventions, styling rules, and best practices to follow when contributing to this project. For areas not explicitly covered in this document, we refer to the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) and [Google’s Markdown Style Guide](https://google.github.io/styleguide/docguide/).

## Table of Contents

- [Python Style Guide](#python-style-guide)
  - [Code Formatting](#code-formatting)
  - [Naming Conventions](#naming-conventions)
  - [Comments and Docstrings](#comments-and-docstrings)
  - [Imports](#imports)
  - [Error Handling](#error-handling)
  - [Testing](#testing)
- [Markdown Style Guide](#markdown-style-guide)
  - [Headers](#headers)
  - [Lists](#lists)
  - [Links and Images](#links-and-images)
  - [Code](#code)
- [Commit Messages](#commit-messages)

## Python Style Guide

Follow the conventions and styling rules outlined here for Python code. For details not covered in this section, refer to the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

### Code Formatting

🛠 **Tools**: Use [Black](https://black.readthedocs.io/) for auto-formatting. Ensure that you run it before submitting your code.

📏 **Line Length**: Keep lines to a maximum of 79 characters for code, and 72 for comments and docstrings.

🛠 **Indentation**: Use 4 spaces per indentation level.

### Naming Conventions

👔 **Variables, Functions, and Constants**: Follow the naming conventions and guidelines provided in the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#316-naming).

### Comments and Docstrings

💬 **Inline Comments**: Use them sparingly and ensure they are necessary and add value.

📜 **Docstrings**: Follow the conventions for docstrings as per the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

### Imports

📥 **Import Order**: Standard library imports, followed by third-party imports, followed by local application imports. Each group should be sorted alphabetically.

🚫 **Wildcard Imports**: Avoid using wildcard imports (`from module import *`).

### Error Handling

🚫 **Bare Excepts**: Avoid using bare except statements. Instead, catch specific exceptions.

💬 **Include Error Messages**: When catching exceptions, include an error message to explain what went wrong.

### Testing

✅ **Write Tests**: Ensure that new features or changes include appropriate tests.

✅ **Use `pytest`**: Write your tests using the `pytest` framework.

## Markdown Style Guide

For Markdown files and documentation, refer to [Google’s Markdown Style Guide](https://google.github.io/styleguide/docguide/). Below are some additional specific guidelines for our project.

### Headers

📏 **Use `#` for Headers**: Use `#` followed by a space for headers. Use `##` for subheaders, and so on.

### Lists, Links, Images, and Code

Follow the conventions outlined in [Google’s Markdown Style Guide](https://google.github.io/styleguide/docguide/).

## Commit Messages

✉️ **Use the Imperative**: Write commit messages in the imperative mood.

📜 **Be Descriptive**: Make sure your commit messages clearly describe the changes made.

---

By adhering to this style guide and the referenced Google style guides, we ensure a consistent and professional codebase. Happy coding! 🚀