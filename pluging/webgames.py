from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

@Client.on_message(filters.command(["webgames"]))
async def webgames_handler(client, message: Message):
    await message.reply(
        "**🎮 Play Browser Games Now!**\n\nClick any button below to launch the game in your browser.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🧠 Brain Out", url="https://poki.com/en/g/brain-test-tricky-puzzles")],
            [InlineKeyboardButton("🕹️ Retro Bowl", url="https://poki.com/en/g/retro-bowl")],
            [InlineKeyboardButton("🎯 Stick Merge", url="https://poki.com/en/g/stick-merge")],
            [InlineKeyboardButton("🧟‍♂️ Zombie Derby", url="https://poki.com/en/g/zombie-derby-pixel-survival")],
            [InlineKeyboardButton("👻 Horror Tale", url="https://poki.com/en/g/horror-tale")],
            [InlineKeyboardButton("🏎️ Smash Karts", url="https://poki.com/en/g/smash-karts")],
            [InlineKeyboardButton("♟️ Chess Online", url="https://www.chess.com/play/online")],
            [InlineKeyboardButton("🧩 The Impossible Quiz", url="https://poki.com/en/g/the-impossible-quiz")],
            [InlineKeyboardButton("💣 Minesweeper", url="https://minesweeper.online")],
            [InlineKeyboardButton("🧙‍♂️ Dark Runner", url="https://poki.com/en/g/dark-runner")],
        ])
    )
