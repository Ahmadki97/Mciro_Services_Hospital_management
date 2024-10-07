import cloudinary
import cloudinary.uploader
from Helper_Auth.loghandler import logger
from dotenv import load_dotenv
import os 


load_dotenv('.env')
async def uploadPhoto(file):
    try:
        cloudinary.config(
            cloud_name = os.getenv('CLOUD_NAME'),
            api_key = os.getenv('CLOUD_API_KEY'),
            api_secret = os.getenv('CLOUD_API_SECRET'),
            secure = True
        )
        upload_result = cloudinary.uploader.upload(file=file)
        file_url = upload_result['url']
        return file_url 
    except Exception as err:
        logger.error(f"Error in cloudinary uploadPhoto() Method: {err}")
        return("Error Uploading The file")