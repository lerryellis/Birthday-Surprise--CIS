import webbrowser
import os
import subprocess
import tempfile
import time

# 1. The HTML with CSS and a JS Countdown
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Surprise!</title>
    <style>
        body { 
            background: #0f0c29; 
            background: linear-gradient(to bottom, #24243e, #302b63, #0f0c29);
            color: white; 
            text-align: center; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        h1 { font-size: 4rem; margin-bottom: 10px; color: #f1c40f; text-shadow: 0 0 20px #f1c40f; }
        .cake { font-size: 100px; margin: 20px; }
        .timer-box { font-size: 1.5rem; background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; }
        #countdown { font-size: 3rem; color: #e74c3c; font-weight: bold; }
    </style>
</head>
<body>
    <div class="cake">🎂</div>
    <h1>Happy 45th Birthday!</h1>
    <p style="font-size: 1.5rem;">Level 45 Unlocked! System recalibrating...</p>
    
    <div class="timer-box">
        PC Self-Destruct (Nap Mode) in:<br>
        <span id="countdown">10</span>
    </div>

    <script>
        let seconds = 10;
        const display = document.getElementById('countdown');
        const interval = setInterval(() => {
            seconds--;
            display.innerText = seconds;
            if (seconds <= 0) clearInterval(interval);
        }, 1000);
    </script>
</body>
</html>
"""

def start_surprise():
    # Create a temp HTML file
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "birthday.html")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Open the browser
    webbrowser.open(f"file://{file_path}")

    # 2. Trigger Windows Shutdown Command
    # /s = shutdown, /t 10 = 10 second delay
    # We use 10 seconds here to match your HTML timer
    subprocess.run(["shutdown", "/s", "/t", "10"])

if __name__ == "__main__":
    start_surprise()
    
    