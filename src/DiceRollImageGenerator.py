from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from random import randint

#TODO: Add py docStrings to classes and methods
class BoundedImage():
    def __init__(self, dieType: int, rollCount: int) -> None:
        self.acceptedDieTypes: tuple = (2, 4, 6, 8, 10, 12, 20)
        self.dieType = self._is_valid_dieType(dieType)
        self.rollCount = self._is_valid_roll_count(rollCount)
        self.imageBounds = (434, 204)
        self.imageFont = self._get_image_font()
        self.rollValues = self._create_roll_values()
        self.die_assets = self._get_required_assets()
        self.image = self._generate_die_image()
    
    def _is_valid_dieType(self, dieType: int):
        if dieType in self.acceptedDieTypes:
            return dieType
        else: 
            raise RollValueAndTypeError(f"Invalid die type passed: D{dieType} not accepted")
    
    def _is_valid_roll_count(self, rollCount: int):
        if rollCount >= 1 and rollCount <= 4:
            return rollCount
        else:
            raise RollValueAndTypeError(f"Invalid roll count passed. May only roll 1 to 4 die: {rollCount} passed")
    
    def _get_image_font(self):
        try:
            font = ImageFont.truetype("./Fonts/Mitr/Mitr-Regular.ttf", 32)
            return font
        except OSError:
            OSError("Font not detected")
    
    def _create_roll_values(self) -> list:
        rolls:list = []

        for i in range(0,self.rollCount):
            rolls.append(randint(1,self.dieType))

        return rolls
    
    def _get_required_assets(self):
        requiredRollAssets = set()
        assets: dict = {}

        for i in self.rollValues:
            requiredRollAssets.add(i)
        
        for j in requiredRollAssets:
            assets[j] = DieAsset(self.dieType, j)
                       
        return assets
    
    def _generate_die_image(self):
        baseImage = Image.new(mode="RGBA", size=self.imageBounds)
        textColor = (255, 255, 255)
        
        rollTypeHeaderText = f"Roll {self.rollCount}D{self.dieType}"
        rollTotalFooterText = f"Total: {sum(self.rollValues)}"
        
        #Starting, non-relative coordinates
        header_Y_coordinate = 5
        asset_X_coordinate_pointer = 10

        textGraphicCreator = ImageDraw.Draw(baseImage)

        #Get header and footer bounds used for relative positioning
        _, _, headerRight, headerBottom = textGraphicCreator.textbbox((0,0), text=rollTypeHeaderText, font=self.imageFont)
        _, _, footerRight, _ = textGraphicCreator.textbbox((0,0), text=rollTotalFooterText, font=self.imageFont)

        #Calculate relative coordinates for image header and image assets
        #image footer Y coordinate will be calculated based on the maximum asset height
        header_centered_X_coordinate = (self.imageBounds[0] - headerRight) / 2
        footer_centered_X_coordinate = (self.imageBounds[0] - footerRight) / 2
        asset_Y_coordinate = header_Y_coordinate + headerBottom + 10

        #Draws image header text
        textGraphicCreator.text((header_centered_X_coordinate, header_Y_coordinate), rollTypeHeaderText, font=self.imageFont, fill=textColor)

        #Paste asset images into the baseImage, assetsMaxHeight used in footer y coordinate calculation
        assetsMaxHeight = 0
        for i in self.rollValues:
            baseImage.paste(self.die_assets[i].getImage(), (asset_X_coordinate_pointer, asset_Y_coordinate))
            asset_X_coordinate_pointer += self.die_assets[i].getWidth() + 10

            if assetsMaxHeight < self.die_assets[i].getHeight():
                assetsMaxHeight = self.die_assets[i].getWidth()
        
        #Calculate footer Y coordinate and draw
        footer_Y_coordinate = asset_Y_coordinate + assetsMaxHeight + 10
        textGraphicCreator.text((footer_centered_X_coordinate, footer_Y_coordinate), rollTotalFooterText, font=self.imageFont, fill=textColor)

        return baseImage
    
    def getImage(self):
        return self.image
    
    def getByteArray(self):
        byteArray = BytesIO()
        self.image.save(byteArray, format="PNG")
        return byteArray
    
    def toString(self):
        return f"Rolled {self.rollCount}D{self.dieType}: {str(self.rollValues)}"
    
    def save(self, filePath: str):
        self.image.save(fp=filePath)
        return True

    
    def close(self):
        for i in self.die_assets:
            self.die_assets[i].close()
        self.image.close()
        pass




class DieAsset():
    def __init__(self, dieType:int, rollValue:int) -> None:
        self.dieType = dieType
        self.rollValue = rollValue
        self.image_asset = self._open_die_asset()
    
    def _open_die_asset(self) -> Image:
        try:
            assetImage = Image.open(f"./Assets/D{self.dieType}_{self.rollValue}.png")
            return assetImage
        except FileNotFoundError:
            FileNotFoundError(f"Requested file was not found in the Assets directory: D{self.dieType}_{self.rollValue}.png")

    def toString(self):
        return f"D{self.dieType}_{self.rollValue}.png"

    def getImage(self):
        return self.image_asset
    
    def getWidth(self):
        return self.image_asset._size[0]
    
    def getHeight(self):
        return self.image_asset._size[1]
    
    def close(self):
        self.image_asset.close()
        pass

class RollValueAndTypeError(Exception):
    """
    Error class used to validate key image generation factors. A RollValueAndTypeError is raised when the die type or die roll values
    don't meet the expected bounds.

    :inherit Exception:
    """
    def __init__(self, msg="Invalid die entry") -> None:
        self.msg = msg
        super().__init__(self.msg)