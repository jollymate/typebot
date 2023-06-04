from pyrogram.errors import Forbidden, FloodWait, SlowmodeWait
from pyrogram.raw.functions.messages import CheckChatInvite
from pyrogram import Client, filters, enums
import asyncio
import random


api_id = 25983686
api_hash = "d49ffa3e2b617c66250b7f4c169d1cb9"
chance = list(range(1, 2))
app = Client(
    name="alice",
    api_id=api_id,
    api_hash=api_hash
)
asnwers = [
    'Да блин, опять сбилась!',
    'Помолчите, печатаю...',
    'Да сколько можно беспокоить!',
    'Обратно кошка залезла на стол и всё стёрла!',
    'Да хватит!',
    'Вы издеваетесь? Тише, пример сложный решаю...',
    'Опять переписывать фанфик, твою ж мать!',
    'Блин',
    'Не беспокойте! Скоро всё увидите, что я пишу!'
]

ignorelist = []

async def chat_join(client, msg):
    open_link = False
    is_channel = False
    is_link = False
    if msg[:13] == 'https://t.me/':
        if msg.find('+') == -1:
            msg = msg[13:]
            open_link = True
        is_link = True
    if is_link:
        if open_link:
            s = await client.get_chat(msg)
            if enums.ChatType.CHANNEL == s.type:
                is_channel = True
        else:
            s = await client.invoke(CheckChatInvite(hash=msg[14:]))
            is_channel = s.channel

        if is_channel:
            if not open_link:
                f = await client.join_chat(msg)
                g_chat_data = f.id
            else:
                g_chat_data = msg
            c = await client.get_chat(g_chat_data)
            await client.join_chat(c.linked_chat.id)
        else:
            await client.join_chat(msg)


@app.on_message(filters.all)
async def hello(client, message):
    chat_id = message.chat.id
    msg_id = message.id
    user = message.from_user
    if user:
        u_id = user.id
        first_name = user.first_name
        username = user.username
        msg = message.text
        ch = random.choice(chance)
        if message.mentioned:
            print("*"*50)
            s_chat = str(chat_id).replace('-', '').replace('100', '')
            ms_lnk = f"https://t.me/c/{s_chat}/{msg_id}"
            print("Ответ в сообщениях")
            print(f"От кого: [{u_id}]({username}){first_name}")
            print(f"Сообщение: {msg}\n{ms_lnk}")
            answ = random.choice(asnwers)
            if ch == 1:
                await client.send_message(chat_id, answ)
        is_link = False
        if chat_id > 0:
            await chat_join(client, msg)
        if ch == 1 and chat_id not in ignorelist:
            try:
                await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
            except Forbidden:
                ignorelist.append(chat_id)
            except SlowmodeWait as e:
                print(e)
                asyncio.sleep(e.value+2)
            except FloodWait as e:
                print(e)
                asyncio.sleep(e.value+2)

app.run()
