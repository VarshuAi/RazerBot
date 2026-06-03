<p align="center"><img src="https://telegra.ph/file/03dfb5cb80dc9921ed16f.jpg"></p>

<h4 align="center">
    A Telegram Powerful Group Managment Bot written in Python using Pyrogram and Telethon.
</h4>
<p align="center">
    <a href="https://t.me/Razer312Bot"> Ready-To-Use Bot </a> •
    <a href="about:blank"> Documentation </a> •
    <a href="https://t.me/Razer312Updates"> Update Channel </a> •
    <a href="https://t.me/Razer312Support"> Support Chat </a> 
</p>
    
# RΛZΞR Bot
#### RΛZΞR is a Telegram group managment bot made using Telethon and Pyrogram which makes it modern and faster than most of the exisitng Telegram Chat Managers.

#### RΛZΞR's features over other bots:
- Modern
- Fast
- Fully open-source
- Frequently updated
- Multi Language Support [Soon]
- Advanced Federation System With Buttons
- Advanced Api
- Smart Ai System
- Easy To Use

Can be found on Telegram as [@Razer312bot](https://t.me/Razer312Bot)

## Deployment
First Step!

Star ⭐ the repository!!
It really motivates me to continue this project further

> Click on buttons to expand!
<details>
<summary><b>Requirements</b></summary>
<br>
    
- [Python 3.9 - 3.12](https://www.python.org/downloads/)
- [Telegram API Key](https://docs.pyrogram.org/intro/setup#api-keys)
- [Telegram Bot Token](https://t.me/botfather)
- [MongoDB URI](https://telegra.ph/How-To-get-Mongodb-URI-04-06)

</details>

<details>
<summary><b>Deploy to Railway (Easiest)</b></summary>
<br>

To host RazerBot on Railway:
1. Click **New Project** on Railway.
2. Select **Deploy from GitHub repo** and choose this repository.
3. In your project settings, add a **PostgreSQL** database service (Railway automatically links the `DATABASE_URL` environment variable).
4. Go to the **Variables** tab of your bot service and add the following Environment Variables:
   * `API_ID` — Your Telegram API ID (integer)
   * `API_HASH` — Your Telegram API HASH (string)
   * `TOKEN` — Your Telegram Bot Token from @BotFather
   * `OWNER_ID` — Your Telegram ID (integer, Owner)
   * `OWNER_USERNAME` — Your Telegram Username (without @)
   * `MONGO_DB_URI` — Your MongoDB Connection String
5. Click **Deploy**. The bot will build and start polling automatically.
</details>

<details>
<summary><b>Deploy to VPS</b></summary>
<br>


```console
$ git clone https://github.com/LinuxGuy312/RazerBot.git
$ cd RazerBot
$ pip3 install -U -r requirements.txt
$ cp xconfig.py config.py
```
> Edit config.py with your values and then start bot with
```console
$ python3 -m Razerbot
```
</details>

## Contact & Support

- [Telegram Channel](https://t.me/Razer312Updates)
- [Telegram Support Group](https://t.me/Razer312Support)
- [Contact Owner](https://t.me/Razer_312) | [Second Account](https://t.me/WH0907)

## License

Distributed under the [GNU General Public License v3.0 License.](https://github.com/LinuxGuy312/RazerBot/blob/main/LICENSE) See `LICENSE.md` for more information.

## Acknowledgements

Special thanks to these amazing projects/people which/who help power RΛZΞR Bot:

- [R Λ Z Ξ R](https://t.me/Razer_312)
- [𝔼𝕣𝕖𝕟](https://t.me/WH0907)
