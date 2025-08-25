@echo off
echo.
echo ==========================================
echo QUANTLET QUICK SUBMISSION
echo ==========================================
echo.
echo This will help you submit to QuantLet.
echo.
echo STEP 1: Get a GitHub Token
echo ---------------------------
echo 1. Open browser to: https://github.com/settings/tokens
echo 2. Click "Generate new token (classic)"
echo 3. Name it: QuantLet
echo 4. Select: [x] repo
echo 5. Copy the token (starts with ghp_)
echo.
start https://github.com/settings/tokens
echo.
pause

echo.
echo STEP 2: Create Repository
echo -------------------------
echo Opening GitHub to create repository...
echo.
echo Repository name: QuantLet_NLP_Introduction
echo Make it PUBLIC
echo Do NOT initialize with README
echo.
start https://github.com/new
echo.
echo Press any key after creating the repository...
pause

echo.
echo STEP 3: Push Your Code
echo ----------------------
echo.
set /p USERNAME="Enter your GitHub username: "

git remote remove origin 2>nul
git remote add origin https://github.com/%USERNAME%/QuantLet_NLP_Introduction.git
git push -u origin master

echo.
echo STEP 4: Submit to QuantLet
echo --------------------------
echo.
echo Opening QuantLet issues page...
echo Create a new issue with the content from quantlet_issue_template.md
echo.
start https://github.com/QuantLet/Styleguide-and-FAQ/issues/new
start quantlet_issue_template.md
echo.
echo ==========================================
echo SUBMISSION COMPLETE!
echo ==========================================
echo.
echo Your repository: https://github.com/%USERNAME%/QuantLet_NLP_Introduction
echo.
pause