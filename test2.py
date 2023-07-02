import telebot
from telebot import types
import requests
from PIL import Image
from io import BytesIO
from transformers import BlipProcessor, BlipForConditionalGeneration

# Initialize the Telegram bot
bot_token = "6263151783:AAEQM3avoTLWQdqUMenhEsFFHUgggOCnSbg"
bot = telebot.TeleBot(bot_token)

# Load the image captioning model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Welcome to the Image Captioning Bot! Send me an image and I'll generate a caption for it.",
    )


@bot.message_handler(content_types=["photo"])
def handle_image(message):
    try:
        # Get the image file ID
        file_id = message.photo[-1].file_id
        # Get the file path
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        # Download the image
        image_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content)).convert("RGB")

        # Perform image captioning
        captions = generate_captions(image)
        caption_text = "".join(captions)

        # Send the caption as a message
        bot.reply_to(message, caption_text)
    except Exception as e:
        print(e)
        bot.reply_to(message, "Oops! Something went wrong. Please try again.")


def generate_captions(image):
    inputs = processor(image, return_tensors="pt")
    outputs = model.generate(**inputs)
    captions = processor.decode(outputs[0], skip_special_tokens=True)
    return [caption for caption in captions]


# Start the bot
bot.polling()


# 6263151783:AAEQM3avoTLWQdqUMenhEsFFHUgggOCnSbg"
