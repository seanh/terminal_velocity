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


class SearchBoxWidget(urwid.Edit):

    def __init__(self, *args, **kwargs):
        self.fakefocus = True
        return super(SearchBoxWidget, self).__init__(*args, **kwargs)

    def render(self, size, focus=False):
        return super(SearchBoxWidget, self).render(size, self.fakefocus)


# TODO: This widget will have to get smarter to implement note renaming.
class NoteWidget(urwid.Text):

    def __init__(self, note):
        self.note = note
        return super(NoteWidget, self).__init__(note.title)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class NoteFilterListBox(urwid.ListBox):
    """A filterable list of notes from a notebook."""

    def __init__(self, notebook, query=None):
        """Initialise a NoteFilterListBox for the given NoteBook.

        This will create NoteWidgets for all the Notes in the given NoteBook.

        """
        if query is None:
            query = ""
        self.notebook = notebook
        self.list_walker = urwid.SimpleFocusListWalker([])
        self.widgets = {}  # NoteWidget cache.
        self.filter(query)
        super(NoteFilterListBox, self).__init__(self.list_walker)

    def filter(self, query):
        """Filter this NoteFilterListBox to show only notes that match query.

        """
        matching_notes = self.notebook.search(query)

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


class MainFrame(urwid.Frame):
    """The topmost urwid widget."""

    def __init__(self):
        self.notebook = notebook.PlainTextNoteBook(
                "/home/seanh/Dropbox/Notes", "txt")
        self.search_box = SearchBoxWidget()
        self.note_filter_list_box = NoteFilterListBox(self.notebook,
                query=self.search_box.text)
        urwid.connect_signal(self.search_box, "change",
                self.on_search_box_changed)
        super(MainFrame, self).__init__(header=self.search_box,
                body=self.note_filter_list_box, focus_part="header")

    def quit(self):
        """Quit the app."""
        raise urwid.ExitMainLoop()

    def keypress(self, size, key):

        maxcol, maxrow = size

        if key in ["esc"]:
            # Esc clears the search box, Esc again quits the app.
            if self.search_box.text:
                self.search_box.set_edit_text("")
                return None
            else:
                self.quit()

        elif key in ["ctrl d"]:
            # Deselect the selected note, if any.
            self.set_focus("header")
            return None

        elif key in ["enter"]:
            if self.note_filter_list_box.focus:
                system('{0} "{1}"'.format("vim",
                    self.note_filter_list_box.focus.base_widget.note.abspath))
            else:
                note = self.notebook.add_new(self.search_box.text)
                system('{0} "{1}"'.format("vim", note.abspath))
            self.note_filter_list_box.filter(self.search_box.text)
            return None

        elif key in ("up", "down", "page up", "page down"):
            self.focus_part = 'body'
            return super(MainFrame, self).keypress(size, key)

        elif key in ["ctrl q"]:
            # FIXME: Why doesn't this work? ctrl q doesn't seem to get here.
            self.quit()
            raise urwid.ExitMainLoop()

        else:
            return self.search_box.keypress((maxcol,), key)

    def on_search_box_changed(self, edit, new_edit_text):
        self.note_filter_list_box.filter(new_edit_text)

palette = [
    ('list nofocus', 'white', 'dark gray', '', 'black', 'g78'),
    ('list focus', 'black', 'light gray', '', 'black', 'g70'),
    ]
frame = MainFrame()
loop = urwid.MainLoop(frame, palette)
loop.run()
