@echo off
setlocal

title AI News Recommendation

echo ==========================================
echo       AI NEWS RECOMMENDATION SYSTEM
echo ==========================================
echo.

REM Go to the folder where run.bat is located
cd /d "%~dp0"

REM ------------------------------------------------
REM Check Python
REM ------------------------------------------------

python --version >nul 2>&1

if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo.
    echo Install Python 3.10+ and try again.
    pause
    exit /b 1
)

echo Python:
python --version
echo.

REM ------------------------------------------------
REM Create virtual environment
REM ------------------------------------------------

if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv

    if errorlevel 1 (
        echo ERROR: Could not create virtual environment.
        pause
        exit /b 1
    )
)

REM ------------------------------------------------
REM Activate virtual environment
REM ------------------------------------------------

call "venv\Scripts\activate.bat"

echo.
echo Virtual environment activated.
echo.

REM ------------------------------------------------
REM Install dependencies
REM ------------------------------------------------

if exist "requirements.txt" (
    echo Installing requirements.txt...
    python -m pip install -r requirements.txt
) else if exist "requirement.txt" (
    echo Installing requirement.txt...
    python -m pip install -r requirement.txt
) else if exist "AI_NEWS\requirements.txt" (
    echo Installing AI_NEWS\requirements.txt...
    python -m pip install -r AI_NEWS\requirements.txt
) else if exist "AI_NEWS\requirement.txt" (
    echo Installing AI_NEWS\requirement.txt...
    python -m pip install -r AI_NEWS\requirement.txt
) else (
    echo WARNING: No requirements file found.
)

echo.
echo ==========================================
echo Starting backend...
echo ==========================================
echo.

REM ------------------------------------------------
REM Prepare frontend files for local backend serving
REM ------------------------------------------------

if not exist "api\Backend.py" (
    echo ERROR: api\Backend.py was not found.
    pause
    exit /b 1
)

if not exist "AI_NEWS\index.html" (
    echo ERROR: AI_NEWS\index.html was not found.
    pause
    exit /b 1
)

echo Preparing frontend files...
copy /y "AI_NEWS\index.html" "api\NEWS.html" >nul
copy /y "AI_NEWS\Live_action.js" "api\Live_action.js" >nul
copy /y "AI_NEWS\Stylish_NEWS.css" "api\Stylish_NEWS.css" >nul

REM ------------------------------------------------
REM Start Flask/Python backend
REM ------------------------------------------------

start "AI News Backend" cmd /k "cd /d ""%~dp0api"" && ""%~dp0venv\Scripts\python.exe"" Backend.py"

REM ------------------------------------------------
REM Wait for backend to start and open app
REM ------------------------------------------------

echo Waiting for backend to start...
timeout /t 4 /nobreak >nul
start "" "http://localhost:5000/NEWS.html"

echo.
echo ==========================================
echo AI NEWS APPLICATION STARTED
echo ==========================================
echo.
echo Frontend:
echo http://localhost:5000/NEWS.html
echo.
echo Backend:
echo Running in a separate terminal on http://localhost:5000
echo.
echo Do not close the backend terminal.
echo.

pause