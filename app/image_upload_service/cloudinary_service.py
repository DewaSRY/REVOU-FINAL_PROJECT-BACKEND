"""_summary_
"""

from dotenv import load_dotenv
import cloudinary
import os


load_dotenv()

cloudinary_instance = cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
    secure=True,
)
