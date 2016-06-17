#!/usr/bin/python3
import tarfile
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

import arcengine

class MainWindow(Gtk.Window):

    def __init__(self):
        self.engine = arcengine.ArcEngine()
        self.filelist = Gtk.ListBox()

        Gtk.Window.__init__(self, title='PyGArchiver')
        self.set_size_request(640,400)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        self.add(vbox)
        toolbar = Gtk.Toolbar(toolbar_style=Gtk.ToolbarStyle.BOTH_HORIZ) 
        vbox.pack_start(toolbar, False, False, 0)

        open_button = Gtk.ToolButton.new(label='Open...')
        open_button.connect('clicked', self.on_open_clicked)
        toolbar.insert(open_button, 0)

        self.extract_button = Gtk.ToolButton.new(label='Extract To...')
        self.extract_button.set_sensitive(False)
        self.extract_button.connect('clicked', self.on_extract_clicked)
        toolbar.insert(self.extract_button, 1)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.filelist)
        vbox.pack_start(scrolled_window, True, True, 0)

    def on_open_clicked(self, button):
        filechooser = Gtk.FileChooserNative.new('Select an archive',
                self,
                Gtk.FileChooserAction.OPEN)
        answer = filechooser.run()
        if answer == Gtk.ResponseType.CANCEL:
            return
        
        self.clear_entries()
        filename = filechooser.get_filename()
        print('User selected: ' + filename) 
        self.engine.load_file(filename) 
        self.show_entries(self.engine.get_entries())
        self.extract_button.set_sensitive(True)

    def on_extract_clicked(self, button):
        filechooser = Gtk.FileChooserNative.new('Select a destination',
            self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            '_Extract',
            '_Cancel')
        answer = filechooser.run()
        if answer == Gtk.ResponseType.CANCEL:
            return

        filename = filechooser.get_filename()
        print('User chose to extract to ' + filename)
        self.engine.extract_to(filename)
        
    def show_entries(self, tar_entries):
        for tarinfo in tar_entries:
            self.show_entry(tarinfo)
        self.filelist.show_all()

    def show_entry(self, tarinfo):
        row = Gtk.Label(label=tarinfo.name)
        row.set_halign(Gtk.Align.START)
        self.filelist.add(row)

    def clear_entries(self):
        for row in self.filelist.get_children():
            self.filelist.remove(row)

win = MainWindow() 
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
