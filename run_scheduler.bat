@echo off
REM Run Monitoring Scheduler
REM This script runs daily automated monitoring
REM Press Ctrl+C to stop

echo.
echo ====================================
echo   MONITORING SYSTEM - DAILY SCHEDULER
echo ====================================
echo.
echo The scheduler will run monitoring at:
echo - 09:00 AM (Daily monitoring)
echo - 06:00 PM (Email report)
echo.
echo To customize times, edit scheduler.py
echo.
echo Press Ctrl+C to stop the scheduler
echo.

python scheduler.py

pause
