Osiris
osiris75x
Online

KindPerspective — 4/20/2025 12:53 PM
That’s strange I see other Orgs use it without issues 
Osiris — 4/20/2025 12:53 PM
This is all we see
KindPerspective — 4/20/2025 12:54 PM
Monitoring is on?
Osiris — 4/20/2025 12:54 PM
I will try again later tonight hopefully
I tried it last night, I had monitoring on but don't think I had the overlay stuff active
And some of my users saying api subscribe doesn't show as an option for them.
KindPerspective — 4/20/2025 12:57 PM
Only admin subscribes channel
Everybody else just request key via button
I will update guide if its confusing
Osiris — 4/20/2025 12:58 PM
Ya it is a bit
And I don't see a request key button, is there a new version?
I'm very good at documentation if you want help lmk
KindPerspective — 4/20/2025 1:07 PM
here is our MD guide
you can edit it and i put it in bot
so maybe your user perspective will help make it more user firendly) 
# Killfeed API
`/api subscribe` - Subscribe to API update events either from a channel or via DM (Admin Only)
`/api unsubscribe` - Unsubscribe from API update events (Admin Only)
`/api show_key` - Show API key in a DM for privacy and tracking purposes, creates a new API key if none exists.
`/api killlog` - Show Killfeed log Panel for the current channel or in DM
`/api remove_user` - Remove user from API key database (Admin Only)
Expand
API guide.md
2 KB
Osiris — 4/20/2025 3:43 PM
If you want I have a GitHub acct and can edit it there with a PR .
I'm also a software engineer professionally
Osiris — 4/20/2025 4:12 PM
Working now!
Image
Osiris — 4/20/2025 9:00 PM
Is there a way to disable getting DMs from gunhead for every kill log message, but not disable the feed in the chat?
Osiris — 4/20/2025 9:27 PM
Here's the updated version, put several TODO comments that I suggest as developers you clarify
# Killfeed 
TODO: Short description of kill feed. List the type of events that killfeed will post.

# Killfeed Setup for Discord Admins

Before the killfeed can stream messages to your discord you must complete the following steps:
Expand
API guide-osiris-edit.md
4 KB
KindPerspective — 4/21/2025 3:08 AM
disable notification via button
Image
we will add pvp/pve switch to avoid spamming npc kills
KindPerspective — 4/21/2025 3:09 AM
will fill TODOs and add it
thank you 
Osiris — 4/21/2025 7:12 AM
Should add this to the documentation
KindPerspective — 3:36 AM
@Osiris app is open source now
https://github.com/Poekhavshiy/KillAPI-connect 
Osiris — 7:41 AM
Screenshots in the documentation look broken
Osiris — 7:55 AM
Also, I am thinking of forking this to add on some stuff
KindPerspective — 8:22 AM
Yes you can fork it
We currently looking for solution to build it without triggering windows defender
if you came up with idea it will be grate
windows defender going nuts when it sees something build with pyinstaller
btw what languages you work with?
Osiris — 8:24 AM
I will look into it.
Mostly Python right now but I've worked in Go, Java, Perl, JavaScript, a little C.
I'm a backend/data engineer professionally.
KindPerspective — 8:26 AM
after brainstorm we decided to try to make prototype on C++ just to see how it goes
Osiris — 8:26 AM
My goal with forking this is to store kill data in a database, and integrate it with my citizen-bot that I wrote for my org.
I wrote an awards cog and I want to auto assign awards based on kills because doing it manually had been a pita
My bot has 4 cogs, awards, orgs, citizens and one other very specific to my orgs mission.
Osiris — 8:28 AM
To get around the windows defender issue?
KindPerspective — 8:28 AM
yes mostly
but also we kinda looking toward integrating imgui in future
Osiris — 8:29 AM
Having to rewrite your app for this one issue seems terrible
Have you looked at how much code signing would cost?
KindPerspective — 8:31 AM
yep few hundred backs
also we tried nuitka and other common solutions
still triggers it
Osiris — 8:32 AM
Is that for any apps you would create or is it per app
KindPerspective — 8:34 AM
if you talking about key its per apps
but it expires afrer some time
Osiris — 8:35 AM
Oh ok
I asked ChatGTP it had some suggestions you could try.
I can try them out on the fork
KindPerspective — 8:37 AM
will be cool
thanks
﻿
# Killfeed 
TODO: Short description of kill feed. List the type of events that killfeed will post.

# Killfeed Setup for Discord Admins

Before the killfeed can stream messages to your discord you must complete the following steps:

1. Choose or create a channel for the killfeed.
2. Give Gunhead the following permissions to that channel:
- TODO: Devs: list permissions required
3. Subscribe the channel to events using `/api subscribe` in the channel
4. Show the killfeed panel in the channel using `/api killlog`

# Killfeed Instructions for Users

Killfeed reads the logs from Star Citizen and streams them to the subscribed channel.
Users must download and setup the killfeed client application as follows:

1. Download client app [here](https://github.com/Poekhavshiy/KillAPI-connect/releases/latest/download/KillAPi.connect.exe).
2. Start the app and make sure the path to your Star Citizen LIVE folder is entered in the app.
3. Click "Show Key" in the Killfeed panel or 
TODO: It's unclear how a first-time user gets an API key for the first time. Will 'show key' generate one?
4. Click "Start Monitoring".
5. A message with the text `KillAPI connected` should appear in the Killfeed log panel.

# Enabling Discord Overlay Notifications

Bot uses Discord's overlay notifications to display real-time killfeed updates in your DMs or channels. To ensure you receive these notifications, you need to enable the Discord overlay. Follow these steps:

1. Open Discord and go to **User Settings** (click the gear icon in the bottom-left corner).
2. Navigate to **Overlay** in the left sidebar (under "App Settings").
3. Toggle **Enable in-game overlay** to **ON**.
4. Ensure **Show overlay notifications** is enabled for your desired notification types (e.g., messages or mentions).
5. Save your changes.

[https://media.discordapp.net/attachments/1337838441349648414/1363304705085935666/image.png?ex=68058bf2&is=68043a72&hm=5ca6321e2df245b43d2f20ddf539d833414fa80d52115045f2c5a3afef8a760c&=&format=webp&quality=lossless]
Once enabled, you’ll see notifications like this when pve/pvp events occur:
[https://media.discordapp.net/attachments/1335643850844405947/1362899180737007696/image.png?ex=680563c6&is=68041246&hm=0c9e80dca12221f3116d0e09a9d9e30265a2c29feb71e68759755c27786a0b6e&=&format=webp&quality=lossless&width=1522&height=856]

**Note**: You must have notifications enabled for the bot’s messages (via the "Notifications" button in the Killlog panel) to receive these updates. Adjust your Discord notification settings if you don’t see them.

# Killfeed API Commands Reference
`/api subscribe` - Subscribe to API update events either from a channel or via DM (Admin Only)
`/api unsubscribe` - Unsubscribe from API update events (Admin Only)
`/api show_key` - Show API key in a DM for privacy and tracking purposes, creates a new API key if none exists.
`/api killlog` - Show Killfeed log Panel for the current channel or in DM
`/api remove_user` - Remove user from API key database (Admin Only)

TODO: there are two commands that show up that are not documented: `/apikey refresh` and `/apikey show`. Either document or remove the commands.
