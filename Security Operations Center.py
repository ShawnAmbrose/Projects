import os
import sys
import time
import re
import json
from collections import defaultdict
from datetime import datetime

LOG_FILE_PATH = "/var/log/auth.log"
ALERT_THRESHOLD = 5
TIME_WINDOW = 60

FAILED_SSH_REGEX = re.compile(r"Failed password for (invalid user )?(\S+) from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port")
ACCEPTED_SSH_REGEX = re.compile(r"Accepted password for (\S+) from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port")

failed_attempts_tracker = defaultdict(list)

def generate_incident_report(alert_type, source_ip, username, count, details):
    report = {
        "@timestamp": datetime.utcnow().isoformat() + "Z",
        "severity": "HIGH" if alert_type == "BRUTE_FORCE_ATTACK" else "MEDIUM",
        "event": {
            "category": "authentication",
            "type": alert_type,
            "description": details
        },
        "source": {
            "ip": source_ip,
            "user": username
        },
        "network": {
            "failed_attempts": count
        }
    }
    print(f"\n[ALERT - {report['severity']}] {datetime.now()} | {alert_type} detected from IP: {source_ip} (Target User: {username})")
    print(f"Details: {details}\n" + "-"*70)
    
    with open("siem_alerts.json", "a") as f:
        f.write(json.dumps(report) + "\n")

def process_log_line(line):
    current_time = time.time()
    
    failed_match = FAILED_SSH_REGEX.search(line)
    if failed_match:
        username = failed_match.group(2)
        ip_address = failed_match.group(3)
        
        failed_attempts_tracker[ip_address].append(current_time)
        
        failed_attempts_tracker[ip_address] = [
            t for t in failed_attempts_tracker[ip_address] if current_time - t <= TIME_WINDOW
        ]
        
        failure_count = len(failed_attempts_tracker[ip_address])
        if failure_count >= ALERT_THRESHOLD:
            generate_incident_report(
                alert_type="BRUTE_FORCE_ATTACK",
                source_ip=ip_address,
                username=username,
                count=failure_count,
                details=f"IP address exceeded threshold with {failure_count} failed login attempts within {TIME_WINDOW}s."
            )
            failed_attempts_tracker[ip_address].clear()
            
    success_match = ACCEPTED_SSH_REGEX.search(line)
    if success_match:
        username = success_match.group(1)
        ip_address = success_match.group(2)
        
        if username == "root":
            generate_incident_report(
                alert_type="UNAUTHORIZED_ROOT_ACCESS",
                source_ip=ip_address,
                username=username,
                count=1,
                details="Successful root access login established over SSH. Audit access privilege compliance."
            )

def monitor_log_stream():
    print(f"[*] Core SOC Engine Active. Monitoring system access rules on {LOG_FILE_PATH}...")
    
    if not os.path.exists(LOG_FILE_PATH):
        print(f"[!] Error: Target log file {LOG_FILE_PATH} not found. Ensure script is running with proper system privileges.")
        sys.exit(1)

    with open(LOG_FILE_PATH, "r") as f:
        f.seek(0, os.SEEK_END)
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            process_log_line(line)

if __name__ == "__main__":
    try:
        monitor_log_stream()
    except KeyboardInterrupt:
        print("\n[*] SOC Monitoring Engine shutdown cleanly.")