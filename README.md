# Songsterr-Printer

Print and download sheet music from Songsterr. No downloads - just a single command in your browser.
Inspired by https://github.com/AnsonLai/MuseScore-Printer.

## Usage

1. Open a Songsterr song (i.e. https://www.songsterr.com/a/wsa/ice-nine-kills-funeral-derangements-drum-tab-s499336).
2. Open Inspect Element (Ctrl+Shift+I on Chrome).
3. Copy and paste the following line of code into the console (second tab on Chrome) (see ./originalCode.js for the actual code)
```js
eval(await (await fetch("https://raw.githubusercontent.com/GreenJon902/Songsterr-Printer/refs/heads/main/originalCode.js")).text())
```
4. Enjoy! (it may take a couple of seconds if the score is very long.)

Please note that you can print as PDF if you want to just download and save your music. There are options in the print dialog to remove the unsightly URL and date headers/footers as well.
