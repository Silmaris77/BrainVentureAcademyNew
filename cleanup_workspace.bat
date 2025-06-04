@echo off
echo Starting BrainVenture Academy Cleanup...

:: Create backup directory with timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (set mytime=%%a%%b)
set backup_dir=backup_cleanup_%mydate%_%mytime%
mkdir %backup_dir%
echo Created backup directory: %backup_dir%

:: Move test files
echo.
echo Moving test files...
mkdir %backup_dir%\test_files
for %%F in (test_*.py) do (
    echo Moving: %%F
    move %%F %backup_dir%\test_files\
)

:: Move debug files
echo.
echo Moving debug files...
mkdir %backup_dir%\debug_files
for %%F in (debug_*.py) do (
    echo Moving: %%F
    move %%F %backup_dir%\debug_files\
)

:: Move simple test files
echo.
echo Moving simple test files...
mkdir %backup_dir%\simple_test_files
for %%F in (simple_*.py) do (
    echo Moving: %%F
    move %%F %backup_dir%\simple_test_files\
)

:: Move quick test files
echo.
echo Moving quick test files...
mkdir %backup_dir%\quick_test_files
for %%F in (quick_*.py) do (
    echo Moving: %%F
    move %%F %backup_dir%\quick_test_files\
)

:: Move verification files
echo.
echo Moving verification files...
mkdir %backup_dir%\verification_files
for %%F in (verify_*.py) do (
    echo Moving: %%F
    move %%F %backup_dir%\verification_files\
)

:: Move final validation files
echo.
echo Moving final validation files...
mkdir %backup_dir%\final_validation_files
for %%F in (final_*.py) do (
    echo Moving: %%F
    move %%F %backup_dir%\final_validation_files\
)

:: Move utility migration files
echo.
echo Moving utility migration files...
mkdir %backup_dir%\utility_files
for %%F in (fix_*.py validate_*.py profile_simulation.py simulate_profile_logic.py) do (
    echo Moving: %%F
    move %%F %backup_dir%\utility_files\
)

:: Move admin dev files
echo.
echo Moving admin dev files...
mkdir %backup_dir%\admin_files
for %%F in (admin_test.py direct_badge_test.py badge_test_fix.py) do (
    echo Moving: %%F
    move %%F %backup_dir%\admin_files\
)

:: Move syntax check files
echo.
echo Moving syntax check files...
mkdir %backup_dir%\syntax_check_files
for %%F in (syntax_check.py check_app_health.py) do (
    echo Moving: %%F
    move %%F %backup_dir%\syntax_check_files\
)

:: Move documentation files
echo.
echo Moving documentation files...
mkdir %backup_dir%\docs
for %%F in (*.md) do (
    echo Moving: %%F
    move %%F %backup_dir%\docs\
)

:: Move special files
echo.
echo Moving special files...
mkdir %backup_dir%\special_files
move app.log %backup_dir%\special_files\
move main.py.broken %backup_dir%\special_files\
move course_map_integration_demo.html %backup_dir%\special_files\

:: Move backup files from views directory
echo.
echo Moving backup files from views...
mkdir %backup_dir%\views_backup
move views\*.backup %backup_dir%\views_backup\
move views\*_backup.py %backup_dir%\views_backup\
move views\*_fixed.py %backup_dir%\views_backup\
move views\*_new.py %backup_dir%\views_backup\

:: Cleanup pycache directories
echo.
echo Cleaning up __pycache__ directories...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

:: Complete
echo.
echo ========================================================
echo CLEANUP SUMMARY
echo ========================================================
echo Backup location: %backup_dir%
echo.
echo Core files kept:
echo   - main.py
echo   - requirements.txt
echo   - runtime.txt
echo   - run_app.py
echo   - users_data.json
echo   - views\ (core files)
echo   - utils\ (core files)
echo   - data\ (core files)
echo   - config\ (core files)
echo   - static\ (core files)
echo   - assets\ (core files)
echo.
echo Cleanup completed! Your workspace is now organized.
echo If you need any files back, they're safely stored in: %backup_dir%
echo.
echo Press any key to exit...
pause > nul
