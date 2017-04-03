#!/bin/python3
import gi
import subprocess
import time

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject


def main():

    builder = gtk.Builder()
    builder.add_from_file("main.ui")

    ## declarations
    # main window
    main = builder.get_object("main");
    box	= builder.get_object("box");
    menu = builder.get_object("menu");
    title = builder.get_object("title");
    kodi = builder.get_object("kodi");
    network = builder.get_object("network");
    restart	= builder.get_object("restart");
    update = builder.get_object("update");
    fix_label = builder.get_object("fix-label")
    # menu bar
    menu_file = builder.get_object("menu_file");
    menu_help = builder.get_object("menu_help");
    sub_file = builder.get_object("sub-file");
    menu_quit = builder.get_object("menu-quit");
    sub_help = builder.get_object("sub-help");
    menu_about = builder.get_object("menu-about");
    # about window
    about = builder.get_object("about");
    about_box = builder.get_object("about-box");
    about_ok = builder.get_object("about-ok");
    about_text = builder.get_object("about-text");
    license	= builder.get_object("license");
    # restart window
    restart_win = builder.get_object("restart-win");
    restart_box = builder.get_object("restart-box");
    restart_bbox = builder.get_object("restart-bbox");
    restart_ok = builder.get_object("restart-ok");
    restart_cancel = builder.get_object("restart-cancel");
    restart_text = builder.get_object("restart-text");

    ## buttons
    # misc
    main.connect('destroy', gtk.main_quit)
    menu_quit.connect('activate', gtk.main_quit)
    menu_about.connect('activate', show_widget, about)
    about.connect('destroy', hide_widget, about) # don't destroy the about window, just hide it
    # main window buttons
    kodi.connect('clicked', launch_kodi)
    network.connect('clicked', fix_net, fix_label)
    restart.connect('clicked', show_widget, restart_win)
    update.connect('clicked', check_updates, fix_label)
    # about window
    about_ok.connect('clicked', hide_widget, about)
    # restart window
    restart_ok.connect('clicked', restart_dev)
    restart_cancel.connect('clicked', hide_widget, restart_win)

    # thing to hide the fix label
    buttons = (kodi, restart, update) # network excluded for obvious reasons
    for button in buttons:
        button.connect('clicked', hide_widget, fix_label)
    gobject.timeout_add(5000, timeout_hide, fix_label)

    gtk.main()

def show_widget(widget, data):
    data.show()
def hide_widget(widget, data):
    data.hide()
def timeout_hide(label):
    gobject.timeout_add(5000, timeout_hide, label)
    # recursive timeout_add to keep it from self-destructing
    label.hide()

def launch_kodi(trash): # trash var to intercept widget signal emit
    subprocess.call(['kodi'])

def fix_net(widget, data):
    # TODO implement a search function maybe
    data.set_text("Fix applied.")
    data.show()
    #subprocess.call('sudo wpa_supplicant -iwlan0 -Dwext -c /etc/wpa_supplicant/wpa_supplicant.conf &'.split(' '))
    #subprocess.call(['sudo', 'dhcpcd'])

def restart_dev():
    subprocess.call(['reboot'])

def check_updates(widget, data):
    data.set_text("Checking for updates. Please wait.")
#   subprocess.call(['sudo', 'apt', '-y', 'update', '&&', 'sudo', 'apt', '-y', 'upgrade'])
    update_string = subprocess.check_output(['yaourt', '-Syu'])
    data.set_text(update)



if __name__ == '__main__':
     main()
