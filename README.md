# art-display

Created to display my art so I can record to OBS Studio.

Python program to display the images in the images directory while playing the audio files in the audio directory
Easiest way to start is just download the latest release and extract with directories to whatever location you like. Run the Python file or .EXE file.

Place your images (1080p) in the images directory
Place your audio files in the audio directory

Several functions built in to add some effects. Add the keyword to the image filename in order to add the effect.

Effect keywords: RAIN, SNOW, BLIZZARD, SPECIAL, FIREFLY, WAVE, FIREWORKS

ADDED TEXT;(font_size);(Message to display) Effect - Example Filename: flying_bird TEXT;20;Happy Birthday!.jpg will display Happy Birthday! in the size 20 font

LEFT and RIGHT cursor keys will move forward and backwards through the images.

UP and DOWN cursor keys will select the next or previous audio file.

Either run with 'python ss93.py' if your have python installed or by the executable file.

Images are currently set to display every 15 seconds but can be easily changed in the program. Line 315    if time.time() - image_change_timer > 15:

If you are interested in my art, you can reach out to me at: https://www.deviantart.com/jdc4429/gallery

Also check out https://www.youtube.com/@JEFFCARLETON

