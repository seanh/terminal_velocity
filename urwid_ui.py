"""A console user interface for Terminal Velocity.

Implemented using the console user interface library urwid.

"""
import os
import subprocess

import urwid

import notebook


def system(cmd):
    """Execute a system command in a subshell and return the exit status."""

    p = subprocess.Popen(cmd, shell=True)
    return os.waitpid(p.pid, 0)[1]


# TODO: This widget will have to get smarter to implement note renaming.
# TODO: Make it so I don't have to wrap these widgets in AttrMaps.
class NoteWidget(urwid.Text):

    def __init__(self, note):
        self.note = note
        return super(NoteWidget, self).__init__(note.title)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class AutocompleteWidget(urwid.Edit):
    """A text editing widget with autocomplete support.

    If you set the .autocomplete_text attribute, it will be shown to the user
    as an autocomplete suggestion.

    Also has a .fakefocus attribute that, if set to True, makes the widget
    look like it has the keyboard focus even when it doesn't.

    """
    def __init__(self, *args, **kwargs):
        self.fakefocus = True
        self.autocomplete_text = None
        return super(AutocompleteWidget, self).__init__(*args, **kwargs)

    def render(self, size, focus=False):
        return super(AutocompleteWidget, self).render(size, self.fakefocus)

    def get_text(self):
        result = super(AutocompleteWidget, self).get_text()
        typed_text = result[0]

        if (not self.autocomplete_text) or (not typed_text):
            return result

        # Show the typed text followed by the autocomplete suggestion in a
        # different style.
        text_to_show = typed_text + self.autocomplete_text[len(typed_text):]
        attrs = [('search', len(typed_text)),
                ('autocomplete', len(text_to_show) - len(typed_text))]
        return (text_to_show, attrs)


class NoteFilterListBox(urwid.ListBox):
    """A filterable list of notes from a notebook."""

    def __init__(self):
        self.list_walker = urwid.SimpleFocusListWalker([])
        self.widgets = {}  # NoteWidget cache.
        super(NoteFilterListBox, self).__init__(self.list_walker)

    def filter(self, matching_notes):
        """Filter this listbox to show only widgets for matching notes."""

        # Get NoteWidgets for each of the matching Notes, retreive the
        # NoteWidgets from the NoteWidget cache if possible, if not create new
        # ones and add them to the cache.
        matching_widgets = []
        for note in matching_notes:
            widget = self.widgets.get(note.abspath)
            if widget:
                matching_widgets.append(widget)
            else:
                widget = urwid.AttrMap(NoteWidget(note), "list nofocus",
                        "list focus")
                self.widgets[note.abspath] = widget
                matching_widgets.append(widget)

        # Remove widgets from list_walker that don't match the query.
        widgets_to_remove = []
        for widget in self.list_walker:
            if widget not in matching_widgets:
                widgets_to_remove.append(widget)
        for widget in widgets_to_remove:
            self.list_walker.remove(widget)

        # Add widgets to list_walker if they match the query and aren't already
        # in list_walker.
        for widget in matching_widgets:
            if widget not in self.list_walker:
                self.list_walker.append(widget)

    def focus_note(self, note):
        """Focus the widget for the given note."""

        for widget in self.list_walker:
            if widget.base_widget.note == note:
                self.list_walker.set_focus(self.list_walker.index(widget))
                break


class MainFrame(urwid.Frame):
    """The topmost urwid widget."""

    def __init__(self):

        self.notebook = notebook.PlainTextNoteBook(
                "/home/seanh/Dropbox/Notes", "txt")

        self.suppress_filter = False
        self._selected_note = None

        self.search_box = AutocompleteWidget(wrap="clip")
        self.list_box = NoteFilterListBox()

        urwid.connect_signal(self.search_box, "change",
                self.on_search_box_changed)

        super(MainFrame, self).__init__(header=self.search_box,
                body=self.list_box, focus_part="header")

        # Add all the notes to the listbox.
        self.filter(self.search_box.edit_text)

    def get_selected_note(self):
        return self._selected_note

    def set_selected_note(self, note):
        """Select the given note.

        Make the note appear focused in the list box, and the note's title
        autocompleted in the search box.

        """
        self._selected_note = note

        if note:

            self.search_box.autocomplete_text = note.title

            # Focus the list box so the focused note will look selected.
            self.set_focus("body")

            # Tell list box to focus the note.
            self.list_box.focus_note(note)

        else:

            self.search_box.autocomplete_text = None

            # Unfocus the listbox so no list item widget will look selected.
            self.set_focus("header")

    selected_note = property(get_selected_note, set_selected_note)

    def quit(self):
        """Quit the app."""

        raise urwid.ExitMainLoop()

    def keypress(self, size, key):

        maxcol, maxrow = size

        if key in ["esc", "ctrl d"]:
            if self.selected_note:
                self.selected_note = None
                self.suppress_filter = True
                self.search_box.set_edit_text(self.search_box.edit_text)
                return None
            elif self.search_box.edit_text:
                self.search_box.set_edit_text("")
                return None
            else:
                self.quit()

        elif key in ["enter"]:
            if self.selected_note:
                system('{0} "{1}"'.format("vim",
                    self.selected_note.abspath))
            else:
                note = self.notebook.add_new(self.search_box.text)
                system('{0} "{1}"'.format("vim", note.abspath))
            self.filter(self.search_box.edit_text)
            return None

        elif key in ("up", "down", "page up", "page down"):
            self.set_focus("body")
            return super(MainFrame, self).keypress(size, key)

        elif key in ["ctrl q"]:
            # FIXME: Why doesn't this work? ctrl q doesn't seem to get here.
            self.quit()
            raise urwid.ExitMainLoop()

        else:
            return self.search_box.keypress((maxcol,), key)

    def filter(self, query):
        """Do the synchronised list box filter and search box autocomplete.

        """
        # Find all notes that match the typed text.
        matching_notes = self.notebook.search(query)

        # Tell the list box to show only the matching notes.
        self.list_box.filter(matching_notes)

        # Find the notes whose title begins with the typed text.
        autocompletable_matches = []
        if query:
            for note in matching_notes:
                if note.title.lower().startswith(query.lower()):
                    autocompletable_matches.append(note)

        # Select the first autocompletable note.
        if autocompletable_matches:
            self.selected_note = autocompletable_matches[0]
        else:
            self.selected_note = None

    def on_search_box_changed(self, edit, new_edit_text):
        if self.suppress_filter:
            self.suppress_filter = False
        else:
            self.filter(new_edit_text)

palette = [
    ('list nofocus', 'default', 'default', '', '', ''),
    ('list focus', 'black', 'brown', '', '', ''),
    ('search', 'default', 'default', '', '', ''),
    ('autocomplete', 'black', 'brown', '', '', ''),
    ]
frame = MainFrame()
loop = urwid.MainLoop(frame, palette)
loop.run()
