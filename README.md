# fore-river-twitter-bot
A twitter bot to tweet when the MA Fore River Bridge is raised and closed. Using the local news source [The Patriot Ledger](https://www.patriotledger.com/) as a datasource. The bot monitors a GMail address for email notifications from The Patriot Ledger and parses them for opening times. It tweets when it gets an opening scheduled and stores the information in memory to later tweet a reminder.

[Follow it on twitter!](https://twitter.com/ForeRiver_3A)

## Can you help?

I'm currently looking for a more reliable data source for bridge opening notifications. If you are aware of one, or know someone who might be aware of one, please reach out and let me know! DMs are open on twitter.

## Hosting

Currently the bot is hosted on a raspberry pi 3B in my home, using a `systemd` service to start on reboots. It logs to a local `logfile.txt` and to `stdout` for `journalctl`. I tried bringing this over into a docker container for the pi, but I'm stretching the pi between a few services and didn't want to stress it with more overhead. This system has been working well so far. I monitor errors on the system through email alerts from my logging function, but these don't notify me of system-wide crashes. I can usually pick up on system-wide crashes because of the other services that run on the pi.

## Possible Enhancements

- [ ] More persistent storage of reminders so they can be tweeted even if the app crashes
- [ ] Rewrite in Cython to learn more about Cython and to make the runtime lighter weight
- [ ] Store when the bridge is scheduled to open to look at fun stats and posisbly make a webapp to provide them to the locals
- [ ] Testing
- [ ] More reliable or first-party data source. (If you're looking at this and know someone at the MA DOT who could help with this, please contact me!)
- [X] Better logging, including sending emails on error
- [X] Better/more fault tolerant hosting for stability. Internet outages and power outages to this Pi has caused issues in the past.
