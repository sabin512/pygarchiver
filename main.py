#!/usr/bin/python3
from optparse import OptionParser
import tarfile
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

import arcengine

class PygWindow(Gtk.Window):

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
        filechooser.add_filter(self.build_lzma_filter())
        answer = filechooser.run()
        if answer == Gtk.ResponseType.CANCEL:
            return
        
        filename = filechooser.get_filename()
        self.open_file(filename)

    def open_file(self, filename):
        self.clear_entries()
        self.engine.load_file(filename) 
        self.show_entries(self.engine.get_entries())
        self.extract_button.set_sensitive(True)

    def build_lzma_filter(self):
        lzmafilter = Gtk.FileFilter()
        lzmafilter.set_name('Tar LZMA')
        lzmafilter.add_mime_type('application/x-xz')
        return lzmafilter

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

def main():
    usage = 'Usage: %prog [options]'
    parser = OptionParser(usage)
    parser.add_option('-f','--file',dest='filename',
                      help='Open the given archive')
    (options,args) = parser.parse_args()

    pyg_window = PygWindow() 
    pyg_window.connect('delete-event', Gtk.main_quit)
    pyg_window.show_all()
    if options.filename:
        pyg_window.open_file(options.filename)
    Gtk.main()


if __name__ == '__main__':
    main()
