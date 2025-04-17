from zapv2 import ZAPv2
import time

# Initialize the ZAP API client
zap = ZAPv2()

# Target Flask web app (adjust the URL based on your setup)
target_url = 'http://host.docker.internal:5000'  # Update to your Flask app's URL
print(f"Scanning {target_url}")

# Access the target website (this may be required to start the spider)
zap.urlopen(target_url)
time.sleep(2)  # Wait for the initial URL to be loaded

# Start the spider scan
print("Starting Spider scan...")
zap.spider.scan(target_url)

# Wait for spider scan to finish
while int(zap.spider.status) < 100:
    print(f"Spider scan progress: {zap.spider.status}%")
    time.sleep(5)

# Start the active scan (this is where the real security testing happens)
print("Starting Active scan...")
zap.ascan.scan(target_url)

# Wait for active scan to finish
while int(zap.ascan.status) < 100:
    print(f"Active scan progress: {zap.ascan.status}%")
    time.sleep(5)

# Generate the report in HTML format
print("Generating HTML report...")
with open("zap_report.html", "w") as report_file:
    report_file.write(zap.core.htmlreport())
