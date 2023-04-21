# DAILY ASTRO BOT #
## BY JAKOB ROSEN FOR ASTR 2030 ##

This bot can be found at https://twitter.com/dailyastrobot and provides a random galaxy each day, as well as the distance to that galaxy, and how long it would take humans to reach that galaxy at our current top speed for space travel.

The bot converts a speed in km/h into Mly/y using the following equation...
$$ {Mly \over y} = {km \over h} * {1.0577248071986049*10^{-19} {Mly \over km} \over 1.14155*10^{-4} {y \over h}} $$

Then, the time to the galaxy is given from the following equation...
$$ y = {distance \over speed} = {Mly \over {Mly \over y}} $$