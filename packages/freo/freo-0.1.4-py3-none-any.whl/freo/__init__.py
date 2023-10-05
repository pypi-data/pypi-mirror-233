from pathlib import Path

# Specify the file name and path to your desktop
desktop_path = Path("~/Downloads").expanduser()  
file_name = "hacker-was-here.txt"
file_path = desktop_path / file_name


file_path.write_text("Hello, developer!\nThis could have been malware.")



