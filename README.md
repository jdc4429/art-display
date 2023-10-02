# art-display

Created this to display my art so I can record to OBS Studio or just play live.

Python program to display the images in the images directory while playing the audio files in the audio directory.
Easiest way to start is just download the latest release and extract with directories to whatever location you like. Run the Python file or .EXE file.

Place your .jpg images and .mp4 files (1080p) in the images directory and place your audio files (mp3 tested) in the audio directory when creating your own display or switching the music out for your favorites while watching my art.

Several functions built in to add some effects. Add the keyword to the image filename in order to add the effect.

Effect keywords: RAIN, SNOW, BLIZZARD, SPECIAL, FIREFLY, WAVE, FIREWORKS, BUBBLES, BUBBLEMAX, STARFIELD, HEARTMAX

ADDED TEXT;(font_size);(Message to display) Effect - Example Filename: flying_bird TEXT;20;Happy Birthday!.jpg will display Happy Birthday! in the size 20 font
(TEXT must be the last option used in the filename if using other effects)

LEFT and RIGHT cursor keys will move forward and backwards through the images.

UP and DOWN cursor keys will select the next or previous audio file.

F key used to toggle the filename off or on.

Images are currently set to display every 10 seconds but can be easily changed in the program. Change the 10 on the following line: if time.time() - image_change_timer > 10:

If you are interested in my art, you can reach out to me at: https://www.deviantart.com/jdc4429/gallery

Check out https://www.youtube.com/watch?v=4PaqgIELhJE for an example.

Free to use for individual use.  Any monetary use please contact for arrangements and permission. Copyright 2023.
