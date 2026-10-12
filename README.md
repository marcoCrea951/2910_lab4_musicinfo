# MusicBrainz Discography Explorer

A Command Line app that interacts with the MusicBrainz API

# My first initial commit is my almost finished work, I need to add more flexibility with the output data

# I completely forgot that I needed to commit my history and I apologize. 


## How to Run
1. Ensure you have Python installed along with the `requests` library:
   ```bash
   pip install requests

2. Run the script from your terminal

python main.py

## Issues
The issues i encountered were connecting the ednpoints together so that it actually worked

I figured it out by just doing each function one by one then testing them

Another issue was making sure it all worked and flowed together

I had an issued that it would take the artist input and the album, but it would just prompt the user that it was fetching the data.

The fix was that I had to actaully print the data (i know, it took me like 30 min to realize)

But after that the only issue was the while loop, the fix was to get everything needed into the loop, I had some things outside the loop at first

Another issue I had was working on the see more feature. It is supposed to act when user presses m it shows another page of the albums. At first it would just show the same page if you clicked m

The fix was to remove my "top_albums = [:7]" and leave change it to batch_albums which allows the page to show 7 albums at a time on a page