from pyrogram import Client, filters
from pyrogram.types import Message
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import os
import uuid

PDF_PREVIEW_LIMIT = 7  # Kitne pages ka preview bhejna hai

# 📚 /readpdf - Extract text
@Client.on_message(filters.command("readpdf") & filters.document)
async def read_pdf(client, message: Message):
    if not message.document.file_name.endswith(".pdf"):
        return await message.reply("❗ Sirf PDF files hi chalte hain.")

    download_path = f"downloads/{uuid.uuid4()}.pdf"
    await message.download(download_path)
    await message.reply("📥 PDF download ho gayi, extracting text...")

    try:
        with open(download_path, "rb") as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            if len(text) > 4000:
                text = text[:4000] + "\n\n...text trimmed..."
        await message.reply(f"📝 *Extracted Text:*\n\n{text}")
    except Exception as e:
        await message.reply("❌ Error reading PDF text.")
        print(f"[readpdf error] {e}")
    finally:
        os.remove(download_path)

# 🖼️ /previewpdf - Convert first few pages to images
@Client.on_message(filters.command("previewpdf") & filters.document)
async def preview_pdf(client, message: Message):
    if not message.document.file_name.endswith(".pdf"):
        return await message.reply("❗ Yeh command sirf PDF ke liye hai.")

    download_path = f"downloads/{uuid.uuid4()}.pdf"
    await message.download(download_path)
    await message.reply("📥 PDF download ho gayi, making preview...")

    try:
        images = convert_from_path(download_path, first_page=1, last_page=PDF_PREVIEW_LIMIT)
        for i, image in enumerate(images):
            temp_img_path = f"downloads/{uuid.uuid4()}.jpg"
            image.save(temp_img_path, "JPEG")
            await client.send_photo(message.chat.id, photo=temp_img_path, caption=f"📄 Page {i + 1}")
            os.remove(temp_img_path)
    except Exception as e:
        await message.reply("❌ PDF preview fail ho gaya.")
        print(f"[previewpdf error] {e}")
    finally:
        os.remove(download_path)
