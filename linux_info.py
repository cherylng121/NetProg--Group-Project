import subprocess

def run():
    print("--- LINUX SYSTEM INFORMATION ---")
    print("\n[Hostname]")
    subprocess.run(["hostname"])
    print("\n[Current Date and Time]")
    subprocess.run(["date"])
    print("\n[CPU Information]")
    subprocess.run(["lscpu"])
    print("\n[Memory Usage]")
    subprocess.run(["free", "-h"])
    print("\n[Disk Usage]")
    subprocess.run(["df", "-h", "/"])
    print("\n[Logged-in Users]")
    subprocess.run(["who"])
    print("\n[Top 5 Running Processes by CPU Usage]")
    subprocess.run("ps -eo pid,comm,%cpu --sort=-%cpu | head -n 6", shell=True)
    print("\n--------------------------------")