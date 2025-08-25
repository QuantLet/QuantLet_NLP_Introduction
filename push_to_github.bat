@echo off
echo Pushing QuantLet NLP Introduction to GitHub...
echo.
echo Make sure you have created the repository on GitHub first:
echo Repository name: QuantLet_NLP_Introduction
echo.
pause

git remote -v
git push -u origin master

echo.
echo Repository pushed successfully!
echo View at: https://github.com/josterri/QuantLet_NLP_Introduction
pause