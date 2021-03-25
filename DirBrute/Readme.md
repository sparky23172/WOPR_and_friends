This program is designed to preform mass directory discovery via gobuster. This works by taking in a CSV of URLs and then attempts to check if a wordlist for directories. The output is then saved to a CSV organized by URL, Directory Name, Status Code.
The program will also look for a few basic file extensions (.csv,.db,.dbf,.log,.sql,.xml,.exe,.ppt,.pptx,.xls,.xlsx,.bak,.tmp,.doc,.docx,.txt,.pdf) by default.

Requirements:
* You will need to run this program on a Linux machine along with having Gobuster installed and in PATH.

Future Plans:
* Use goroutines to allow for faster results
* Changes to how the arguments function to allow for more customization

Example Commands:
* ./DirBrute.exe -I input.csv -O output.csv -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt 
* ./DirBrute.exe -I input.csv -O output.csv -w /usr/share/SecLists/Discovery/Web-Content/api/api-seen-in-wild.txt -x None
