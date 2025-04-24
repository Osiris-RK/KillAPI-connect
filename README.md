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

