@echo off
echo.
echo ========================================
echo QUANTLET AUTOMATED SUBMISSION
echo ========================================
echo.
set /p TOKEN="Paste your GitHub token (ghp_...): "
echo.
echo Starting automated submission...
echo.
python quantlet_auto_submit.py --token %TOKEN%
echo.
pause