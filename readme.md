
# Rumi.py
My side project - trying out more stuff in Python. 

As a fan of the Rummikub board game, I wanted to recreate and enchance 
the experience. My final goal is to provide API that would be able to receive 
a picture of a table full of rumi tiles and the users own tiles, and then calculate
the best possible way of playing your hand. That goal requires modeling all the game logic,
processing given images, and then running the calculations for the best outcome.

As far I am at the first step, recreating the game's logic in code.
To be able to test it, I am also working on command line interface.

Components:
- rumi_api.py - game logic 
- rumi_cli.py - CLI client
- rumi_gui.py - GUI client 
- rumi_photo_ai.py - photo processing



## Run

Only CLI available for now.

```bash
  python3 rumi_cli.py
```


