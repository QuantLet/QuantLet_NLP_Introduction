@echo off
echo Pushing to GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/josterri/QuantLet_NLP_Introduction.git
git branch -M master
git push -u origin master
echo.
echo Done! Repository: https://github.com/josterri/QuantLet_NLP_Introduction
pause