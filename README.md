# DAILY ASTRO BOT #
## BY JAKOB ROSEN FOR ASTR 2030 ##

This bot can be found at https://twitter.com/dailyastrobot and provides a random galaxy each day, as well as the distance to that galaxy, and how long it would take humans to reach that galaxy at our current top speed for space travel.

The bot converts a speed in km/h into Mly/y using the following equation...
```math
{Mly \over y} = {km \over h} * {1.0577248071986049*10^{-19} {Mly \over km} \over 1.14155*10^{-4} {y \over h}}
```

Then, the time to the galaxy is given from the following equation...
```math
y = {distance \over speed} = {Mly \over {Mly \over y}}
```

The relativistic time is calculated by first calculated the time it would take from an outside observer, and then dividing that number by the lorentz factor, in order to get the time experienced by the traveler. This is done with the following equation...
```math
T = {T_O \over \gamma} = {Mly \over % of c} \sqrt{1-{v^2 \over c^2}}
```
