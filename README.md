# Songsterr-Printer

Print and download sheet music from Songsterr. No downloads - just a single command in your browser.
Inspired by https://github.com/AnsonLai/MuseScore-Printer.

## Usage

1. Open a Songsterr song (i.e. https://www.songsterr.com/a/wsa/ice-nine-kills-funeral-derangements-drum-tab-s499336).
2. Open Inspect Element (Ctrl+Shift+I on Chrome).
3. Choose the size you want to print by resizing Inspect Element pane (Hover your mouse over the line immediately to the right of the scroll bar in the middle of the screen. Your mouse should change to two horizontal arrows, click and drag horizontally do resize).
4. Copy and paste the following line of code into the console (second tab on Chrome) (see ./single.js for the actual code)
```js
eval(await (await fetch("https://raw.githubusercontent.com/GreenJon902/Songsterr-Printer/refs/heads/main/single.js")).text())
```
4. Enjoy! (it may take a couple of seconds if the score is very long.)

Please note that you can print as PDF if you want to just download and save your music. There are options in the print dialog to remove the unsightly URL and date headers/footers as well.

## Download multiple
If you want to download a whole album, then you'll want a spotify developer token/credentials (google it, it's not hard to). Also you'll need the spotify album id.
That should be about it, just run the multi.py file.
Oh you'll need to install the pip dependencies (at the top of the python file) too.
