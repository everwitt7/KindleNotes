"""
NOTE: Example Highlight:
Atomic Habits: Tiny Changes, Remarkable Results (James Clear)
- Your Highlight on Location 172-174 | Added on Friday, May 7, 2021 5:36:46 AM

By my junior year, I was voted team captain and at the end of the season, ...
==========

NOTE: Example Note:
Atomic Habits: Tiny Changes, Remarkable Results (James Clear)
- Your Note on Location 174 | Added on Friday, May 7, 2021 5:37:35 AM

You dont want to lift to get bigger you want to enjoy the habit and ...
==========

NOTE: Highlights and Notes follow the same structure:
line 1: Title = Atomic Habits: Tiny Changes, Remarkable Results (James Clear)
line 2: MetaData = Your Note/Highlight on Location 174 | Added on Friday, May 7, 2021 5:37:35 AM
    Location and Time (we can use time to try and remove duplicate notes and highlights)
line 3: blank
line 4: Note or Highlight

NOTE: the content preceding a note card is what you highlighted when you wrote the note.
To keep the structure of what you were thinking when you highlighted and took a note, you
want to combine these highlights and notes together 

NOTE: Duplicate Highlight Example:
Atomic Habits: Tiny Changes, Remarkable Results (James Clear)
- Your Highlight on Location 210-213 | Added on Friday, May 7, 2021 5:41:16 AM

The entrepreneur and investor Naval Ravikant has said
==========
Atomic Habits: Tiny Changes, Remarkable Results (James Clear)
- Your Highlight on Location 210-213 | Added on Friday, May 7, 2021 5:41:25 AM

The entrepreneur and investor Naval Ravikant has said, “To write a great book ...
==========

In this case we want to delete the previous highlight and replace it with the updated
one that contains more highlighted text. 

NOTE: Duplicate Note Example:
Atomic Habits: Tiny Changes, Remarkable Results (James Clear)
- Your Note on Location 583 | Added on Tuesday, May 11, 2021 5:44:11 AM

So how do you just change your identity whgaa if you always have 
==========
Atomic Habits: Tiny Changes, Remarkable Results (James Clear)
- Your Note on Location 583 | Added on Tuesday, May 11, 2021 5:45:02 AM

So how do you just change your identity whgaa if you always have  
something interesting is my mindseft to blisters is differen i now...
==========

In this case we want to delete the previous note, but we want to associate this
with the same highlight 

We can parse "May 11, 2021 5:44:11 AM" as a date, and then we will keep the most recent date.
To identify similar notes, we will only search the previous note - I rarely go back and update
highlights or notes, I do it immediatley after creating the first highlight/note

TODO: Add functionality for bookmars - I don't use these so I will not add this
TODO: Add unit tests to prove duplicates are removed
TODO: Add functionality for multiline notes where people use return (use ======== as EOL)
"""

from typing import Union
import argparse
from dataclasses import dataclass


@dataclass
class Metadata:
    """Class for note and highlight metadata"""

    # TODO: add date later if needed? everything is chronological sorted anyways...
    k_type: str
    loc: str

    def __str__(self) -> str:
        return f"type: {self.k_type}, loc: {self.loc}\n"


class Highlight:
    """Class to denote a kindle highlight"""

    def __init__(self, metadata: Metadata, content: str) -> None:
        self.metadata = metadata
        self.content = content

    def __str__(self) -> str:
        return f"meta: {self.metadata}content: {self.content}\n"


class Note:
    """Class to denote a kindle note"""

    # TODO: can add the highlight the note refers to, but it will have the same loc
    def __init__(self, metadata: Metadata, content: str) -> None:
        self.metadata = metadata
        self.content = content

    def __str__(self) -> str:
        return f"meta: {self.metadata}content: {self.content}\n"


def main() -> None:
    # read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--title",
        type=str,
        required=True,
        help="title of the book you want to extract",
    )
    args = parser.parse_args()
    title: str = args.title

    # NOTE: set this variable to the absolute path of your clippings
    clippings_path = "/Users/Everwitt/Desktop/My Clippings.txt"

    k_notes = parse_notes(clippings_path, title)
    write_notes(title, k_notes)


def parse_notes(path: str, title: str):
    """parse the My Clippings.txt file and create a list of Note & Highlight objects"""
    # update var to 3 if we run into desired title, otherwise subtract 1
    cur_line = 0
    cur_meta: Metadata
    meta_line = 3
    content_line = 1
    k_notes: list[Union[Highlight, Note]] = list()

    with open(path) as f:
        for line in f:
            if cur_line > 0:
                # capture the metadata in the Metadata data class
                if cur_line == meta_line:
                    # use this to get location
                    pipe_index = line.find("|")

                    # line[7] will either be N (Note) or H (Highlight)
                    if line[7] == "H":
                        # Location begins on line[20] to one index before |
                        k_type = "highlight"
                        loc = line[20 : pipe_index - 1]

                    elif line[7] == "N":
                        # Location begins on line[15] to one index before |
                        k_type = "note"
                        loc = line[15 : pipe_index - 1]

                    cur_meta = Metadata(k_type, loc)

                elif cur_line == content_line:
                    # remove trailing spaces
                    content = line.strip()

                    if cur_meta.k_type == "highlight":
                        # check if the previous highlight is a duplicate
                        if len(k_notes) > 0:
                            if isinstance(k_notes[-1], Highlight):
                                if k_notes[-1].content in content:
                                    k_notes.pop()
                        k_notes.append(Highlight(cur_meta, content))

                    elif cur_meta.k_type == "note":
                        # check if the previous note is a duplicate
                        if len(k_notes) > 0:
                            if isinstance(k_notes[-1], Note):
                                if (
                                    k_notes[-1].content in content
                                    or content in k_notes[-1].content
                                ):
                                    k_notes.pop()
                        k_notes.append(Note(cur_meta, content))

                # it is fine if cur_line goes neg, it will reset to 3 when it sees the right title
                cur_line -= 1

            # line contains trailing spaces
            elif title in line:
                # set cur_line to 3 to get metadata & content
                cur_line = 3

    return k_notes


def write_notes(title: str, notes: list[Union[Highlight, Note]]):
    """Create a title and iterate through Notes & Highlights list to create a markdown output"""
    # extract author from the title (could be unknown)
    paren_ind = title.rindex("(")
    author = title[paren_ind + 1 : -1]
    book = title[: paren_ind - 1]

    # get the number of highlights and notes
    num_highlights = len([h for h in notes if isinstance(h, Highlight)])
    num_notes = len(notes) - num_highlights

    # open and write the output file
    out_path = "/Users/Everwitt/Documents/Zettelkasten/KindleNotes"
    with open(f"{out_path}/{title}.md", "w") as f:
        # create the title, author, and number of highlights & notes
        f.write(f"# {book}\n")
        f.write("---\n")
        f.write(f"**Author:** {author}\n")
        f.write(f"**{num_highlights}** Highlights, **{num_notes}** Notes\n\n")
        f.write("---\n")

        for note in notes:
            f.write(f"- {note.content}\n\n")
            f.write(f"{note.metadata.k_type} @ loc. {note.metadata.loc}\n")


if __name__ == "__main__":
    main()
