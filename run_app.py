import subprocess
import sys
import time

print("🚀 Uruchamiam aplikację BrainVenture Academy...")

try:
    # Uruchom streamlit w tle
    process = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "main.py", 
        "--server.port", "8501",
        "--server.headless", "true"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    print("Aplikacja uruchamia się...")
    time.sleep(3)
    
    # Sprawdź czy proces jest aktywny
    if process.poll() is None:
        print("✅ Aplikacja uruchomiona pomyślnie na http://localhost:8501")
        print("Możesz teraz przejść do przeglądarki i sprawdzić funkcjonalność.")
        
        # Czekaj na input użytkownika
        input("Naciśnij Enter aby zatrzymać aplikację...")
        process.terminate()
        print("Aplikacja zatrzymana.")
    else:
        print("❌ Błąd uruchamiania aplikacji")
        stdout, stderr = process.communicate()
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
        
except Exception as e:
    print(f"❌ Błąd: {e}")
