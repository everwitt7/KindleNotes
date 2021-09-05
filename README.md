# KindleNotes

This program transforms the raw text from "My Clippings.txt" of the kindle into Markdown. It removes duplicate entries (which happens when you extend a highlight or edit a note). I created this because I wanted to read a book, export my highlights and notes into some organized file, then go through my notes/highlights and insert them into my zettelkasten, which lives in Obsidian.

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py --title "{Name of Book Title}"
```
