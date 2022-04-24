# fore-river-twitter-bot
A twitter bot to tweet when the MA Fore River Bridge is raised and closed. Using the local news source [The Patriot Ledger](https://www.patriotledger.com/) as a datasource. The bot monitors a GMail address for email notifications from The Patriot Ledger and parses them for opening times. It tweets when it gets an opening scheduled and stores the information in memory to later tweet a reminder.

[Follow it on twitter!](https://twitter.com/ForeRiver_3A)

## Hosting

Currently the bot is hosted on a raspberry pi 3B in my home, running with [daemon tools'](https://cr.yp.to/daemontools.html) [supervise](https://cr.yp.to/daemontools/supervise.html) for some better fault tolerance. I tried using a docker image, but my Pi is already overloaded between this and some other services I have on it, so the overhead for Docker wasn't worth it. Supervise was a nice alternative that will restart the service when it fails.

## Possible Enhancements

- [ ] More persistent storage of reminders so they can be tweeted even if the app crashes
- [ ] Rewrite in Cython to learn more about Cython and to make the runtime lighter weight
- [ ] Store when the bridge is scheduled to open to look at fun stats and posisbly make a webapp to provide them to the locals
- [ ] More reliable or first-party data source. (If you're looking at this and know someone at the MA DOT who could help with this, please contact me!)
- [X] Better logging
- [X] Better/more fault tolerant hosting for stability. Internet outages and power outages to this Pi has caused issues in the past.
