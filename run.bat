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
REM Start Flask/Python backend
REM ------------------------------------------------

if exist "AI_NEWS\app.py" (
    start "AI News Backend" cmd /k "cd /d "%~dp0AI_NEWS" && "%~dp0venv\Scripts\python.exe" app.py"
) else if exist "app.py" (
    start "AI News Backend" cmd /k ""%~dp0venv\Scripts\python.exe" app.py"
) else (
    echo ERROR: app.py was not found.
    pause
    exit /b 1
)

REM ------------------------------------------------
REM Wait for backend to start
REM ------------------------------------------------

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

REM ------------------------------------------------
REM Start frontend HTTP server
REM ------------------------------------------------

echo.
echo ==========================================
echo Starting frontend...
echo ==========================================
echo.

if exist "AI_NEWS\NEWS.html" (

    start "AI News Frontend" cmd /k "cd /d "%~dp0AI_NEWS" && "%~dp0venv\Scripts\python.exe" -m http.server 5500"

    timeout /t 2 /nobreak >nul

    start "" "http://localhost:5500/NEWS.html"

) else if exist "NEWS.html" (

    start "AI News Frontend" cmd /k "cd /d "%~dp0" && "%~dp0venv\Scripts\python.exe" -m http.server 5500"

    timeout /t 2 /nobreak >nul

    start "" "http://localhost:5500/NEWS.html"

) else (

    echo ERROR: NEWS.html was not found.
    pause
    exit /b 1

)

echo.
echo ==========================================
echo AI NEWS APPLICATION STARTED
echo ==========================================
echo.
echo Frontend:
echo http://localhost:5500/NEWS.html
echo.
echo Backend:
echo Running in a separate terminal.
echo.
echo Do not close the backend or frontend terminals.
echo.

pause