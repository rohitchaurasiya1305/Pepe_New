from datetime import datetime
import html
import os

# Global log storage
allLogs = []

# ---------------------------
# Write log function
# ---------------------------
def write_log(message, level="INFO"):
    currentTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    finalMessage = f"{currentTime} [{level}] - {message}"

    print(finalMessage)
    allLogs.append(finalMessage)


# ---------------------------
# Save logs to HTML
# ---------------------------
def save_logs_html(index,LOG_FOLDER):
    # Ensure folder exists
    os.makedirs(LOG_FOLDER, exist_ok=True)

    # Create dynamic file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logFilePath = os.path.join(LOG_FOLDER, f"Processlogs_{index+1}_{timestamp}.html")

    htmlContent = """
    <html>
    <head>
        <title>marketPlace Logs</title>
        <style>
            body { font-family: Arial; background-color: #f4f4f4; }
            h2 { color: #333; }
            p { background: #fff; padding: 8px; border-left: 4px solid #4CAF50; }
            .ERROR { border-left: 4px solid red; }
        </style>
    </head>
    <body>
    """

    htmlContent += "<h2>marketPlace Process Logs</h2>"

    for log in allLogs:
        safe_log = html.escape(log)

        # Highlight ERROR logs
        if "[ERROR]" in log:
            htmlContent += f"<p class='ERROR'>{safe_log}</p>"
        else:
            htmlContent += f"<p>{safe_log}</p>"

    htmlContent += """
    </body>
    </html>
    """

    try:
        with open(logFilePath, "w", encoding="utf-8") as file:
            file.write(htmlContent)

        print(f"Logs saved successfully: {logFilePath}")

    except PermissionError:
        print("Log file is open. Please close it and retry.")
