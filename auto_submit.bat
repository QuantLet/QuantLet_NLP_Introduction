@echo off
echo.
echo ========================================
echo QUANTLET AUTO-SUBMISSION TOOL
echo ========================================
echo.
echo This script will:
echo 1. Create GitHub repository
echo 2. Push your code
echo 3. Submit to QuantLet organization
echo.
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Install required packages if needed
echo Checking required packages...
pip show requests >nul 2>&1
if errorlevel 1 (
    echo Installing requests...
    pip install requests
)

pip show PyGithub >nul 2>&1
if errorlevel 1 (
    echo Installing PyGithub...
    pip install PyGithub
)

pip show gitpython >nul 2>&1
if errorlevel 1 (
    echo Installing gitpython...
    pip install gitpython
)

echo.
echo ========================================
echo GITHUB AUTHENTICATION REQUIRED
echo ========================================
echo.
echo You need a GitHub Personal Access Token.
echo.
echo To get one:
echo 1. Go to: https://github.com/settings/tokens
echo 2. Click "Generate new token (classic)"
echo 3. Name it: "QuantLet Submission"
echo 4. Select scopes: [x] repo, [x] workflow
echo 5. Click "Generate token"
echo 6. Copy the token (starts with ghp_)
echo.
set /p GITHUB_TOKEN="Paste your GitHub token here: "

if "%GITHUB_TOKEN%"=="" (
    echo ERROR: No token provided
    pause
    exit /b 1
)

echo.
echo Running QuantLet submission...
echo.

REM Run the Python script
python quantlet_auto_submit.py --token %GITHUB_TOKEN% --repo-name QuantLet_NLP_Introduction

if errorlevel 1 (
    echo.
    echo ========================================
    echo MANUAL STEPS REQUIRED
    echo ========================================
    echo.
    echo The automatic submission encountered an issue.
    echo Please complete manually:
    echo.
    echo 1. Create repository at: https://github.com/new
    echo    Name: QuantLet_NLP_Introduction
    echo.
    echo 2. Push code:
    echo    git remote add origin https://github.com/YOUR_USERNAME/QuantLet_NLP_Introduction.git
    echo    git push -u origin master
    echo.
    echo 3. Submit issue at: https://github.com/QuantLet/Styleguide-and-FAQ/issues
    echo    Use content from: quantlet_issue_template.md
    echo.
) else (
    echo.
    echo ========================================
    echo SUCCESS!
    echo ========================================
    echo.
    echo Your QuantLet submission is complete!
    echo Check your GitHub for the repository and issue.
    echo.
)

pause