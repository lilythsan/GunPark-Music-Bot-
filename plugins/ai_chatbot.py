from pyrogram import Client, filters
from pyrogram.types import Message
from random import choice

# 🌟 Personality Responses
PERSONALITY_MODES = {
    "waifu": [
        "Hey senpai~ ❤️",
        "Missed you so much 🥺",
        "Should I stay forever? UwU",
        "Your waifu is here~",
        "Kya aapko hug chahiye? 🤗",
    ],
    "villain": [
        "Main tumhara ant hoon.",
        "Shikaar ko daudne ka mauka nahi milta.",
        "Jab mein aata hoon... roshni chali jaati hai.",
        "Tumne haar maan li, main baksh dunga.",
        "Andhera mera ghar hai.",
    ],
    "bff": [
        "Oyeee tu aa gaya! 😍",
        "Gossip timee!! ☕",
        "Selfie le na abhi! 😎",
        "Tumhare bina maza nahi aata 🤗",
        "Let's vibe together 💃",
    ],
    "ghost": [
        "Main deewar ke peechhe hoon... 👻",
        "Darwaza band mat karna...",
        "Tumne mujhe yaad kiya?",
        "Raat bhar sapno mein rahunga...",
        "Waqt ruk gaya... jab se main gaya.",
    ],
    "senpai": [
        "Kya aapko guidance chahiye, kouhai?",
        "Tumhara progress impressive hai.",
        "Good job, proud of you.",
        "Senpai notices everything.",
        "Next time, aur better karo.",
    ],
}

# 🎭 AI Chat Personality Handler
@Client.on_message(filters.command("chat"))
async def ai_chatbot_handler(client, message: Message):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.reply(
                "**🧠 Use format:** `/chat <mode>`\n\n**Available Modes:** `waifu`, `villain`, `bff`, `ghost`, `senpai`"
            )

        mode = args[1].strip().lower()
        if mode not in PERSONALITY_MODES:
            return await message.reply(
                f"❌ Mode `{mode}` nahi mila.\n\n**Try one of these:**\n`waifu`, `villain`, `bff`, `ghost`, `senpai`"
            )

        reply = choice(PERSONALITY_MODES[mode])
        await message.reply(f"**🎭 {mode.title()} Mode Activated:**\n\n{reply}")

    except Exception as e:
        await message.reply("⚠️ Kuch toh garbar ho gayi... please try again.")
        print(f"[AI ChatBot Error] - {e}")
