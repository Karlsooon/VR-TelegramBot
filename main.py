# import telebot
# # from telebot import types
# from transformers import ViTImageProcessor, AutoTokenizer
# from transformers import VisionEncoderDecoderModel
# import torch
# from PIL import Image
# import requests
# from io import BytesIO

# # Initialize the Telegram bot
# bot_token = "6263151783:AAEQM3avoTLWQdqUMenhEsFFHUgggOCnSbg"
# bot = telebot.TeleBot(bot_token)

# # Load the image-to-text model and components
# model = VisionEncoderDecoderModel.from_pretrained(
#     "nlpconnect/vit-gpt2-image-captioning"
# )
# feature_extractor = ViTImageProcessor.from_pretrained(
#     "nlpconnect/vit-gpt2-image-captioning"
# )
# tokenizer = AutoTokenizer.from_pretrained('nlpconnect/vit-gpt2-image-captioning')

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)

# # Set the maximum length and number of beams for caption generation
# max_length = 16
# num_beams = 4
# gen_kwargs = {"max_length": max_length, "num_beams": num_beams}


# @bot.message_handler(commands=["start"])
# def start(message):
#     bot.reply_to(
#         message,
#         "Welcome to the Image Captioning Bot! Send me an ima"
#         + "ge and I'll generate a caption for it.",
#     )


# @bot.message_handler(content_types=["photo"])
# def handle_image(message):
#     try:
#         # Get the image file ID
#         file_id = message.photo[-1].file_id
#         # Get the file path
#         file_path = bot.get_file(file_id).file_path
#         # Download the image
#         image_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
#         response = requests.get(image_url)
#         image = Image.open(BytesIO(response.content))

#         # Convert image to RGB if needed
#         if image.mode != "RGB":
#             image = image.convert("RGB")

#         # Perform image captioning
#         captions = predict_step([image])
#         caption_text = " ".join(captions)

#         # Send the caption as a message
#         bot.reply_to(message, caption_text)
#     except Exception as e:
#         print(e)
#         bot.reply_to(message, "Oops! Something went wrong. Please try again.")


# def predict_step(images):
#     pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
#     pixel_values = pixel_values.to(device)

#     output_ids = model.generate(pixel_values, **gen_kwargs)

#     preds = tokenizer.batch_decode(output_ids[0], skip_special_tokens=True)
#     preds = [pred.strip() for pred in preds]
#     return preds


# # Start the bot
# bot.polling()
