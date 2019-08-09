# WereWolfStatsGrabber
Uses tgwerewolf.com site to display last kills. Who and by who.

## How to setup?
Linux:
1. $git clone https://github.com/SPevSand/WereWolfStatsGrabber.git
2. $cd WereWolfStatsGrabber
3. $pip install -r requirements.txt
4. In the same directory put players.txt file with short names and IDs without spaces.  
  Syntax: name:id<br />Example:
  ```
  name1:123
  name2:456
  ```
5. $python start.py

Windows:
1. Download script
2. In the same directory put players.txt file with short names and IDs without spaces.  
  Syntax: name:id<br />Example:
  ```
  name1:123
  name2:456
  ```
3. Use python interpreter to launch

## Where do I get IDs of players?  
You can get it with @userinfobot

## Why it doesn't always shows recent kills?  
The script shows only the lastest changes on https://www.tgwerewolf.com/Stats/Player/*userid* site, which shows only the top kills. It takes time for the script to respond to newcome players.
