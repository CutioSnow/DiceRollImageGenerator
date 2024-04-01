from DiceRollImageGenerator import BoundedImage
from PIL import Image #Only need to import if using the BoundedImage.getImage() method
from io import BytesIO #Only need to import if using the BoundedImage.getByteArray() method

#Recommended use case
if __name__=="__main__":
    # To generate a Bounded (434px by 204px) image
    dieImage = BoundedImage(dieType=6,rollCount=4)

    # If the program requires unique image transformations, you can call the getImage() method
    # to access the PIL Image directly in memory
    imagePointer: Image = dieImage.getImage()

    # Save generated image to hard disk with save method, must provide a valid file path
    dieImage.save("test2.png")

    # To avoid saving the image to hard disk you can access the image as a Byte array via the getByteArray() method
    imageByteArray: BytesIO = dieImage.getByteArray()
    # In discord.py you can embed an image using a Byte array as a discord attachment file, for example:
    #   embed = discord.Embed()
    #   imageFile = discord.File(fp=imageByteArray, filename="rollImage.png")
    #   embed.set_image(url="attachment://rollImage.png")

    # Closing the BoundedImage will close all associated image files
    # Note: this will also close imagePointer and imageByteArray in this use case
    dieImage.close()