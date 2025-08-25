@echo off
echo ==========================================
echo BROWSER-BASED QUANTLET SUBMISSION
echo ==========================================
echo.
echo This will open 3 browser tabs to complete submission.
echo.
pause

echo.
echo STEP 1: Creating Repository
echo ---------------------------
echo A browser tab will open to create the repository.
echo.
echo IMPORTANT:
echo - Repository name: QuantLet_NLP_Introduction  
echo - Description: Natural Language Processing educational modules for QuantLet
echo - Make it PUBLIC
echo - Do NOT initialize with README
echo.
start https://github.com/new?name=QuantLet_NLP_Introduction&description=Natural+Language+Processing+educational+modules+for+QuantLet+platform&visibility=public
echo.
echo Press any key after creating the repository...
pause

echo.
echo STEP 2: Getting Push Command
echo -----------------------------
set /p USERNAME="Enter your GitHub username: "
echo.
echo Now push the code with these commands:
echo.
echo git remote remove origin
echo git remote add origin https://github.com/%USERNAME%/QuantLet_NLP_Introduction.git  
echo git push -u origin master
echo.
echo Running commands...
git remote remove origin 2>nul
git remote add origin https://github.com/%USERNAME%/QuantLet_NLP_Introduction.git
git branch -M master 2>nul
git push -u origin master
echo.
pause

echo.
echo STEP 3: Submit to QuantLet
echo --------------------------
echo Opening QuantLet issue page and your submission template...
echo.
echo Copy the content from the Notepad window that opens
echo and paste it into the issue form.
echo.
start https://github.com/QuantLet/Styleguide-and-FAQ/issues/new
notepad quantlet_issue_template.md
echo.
echo ==========================================
echo SUBMISSION COMPLETE!
echo ==========================================
echo.
echo Repository: https://github.com/%USERNAME%/QuantLet_NLP_Introduction
echo.
echo Next: QuantLet maintainers will review your submission
echo.
pause