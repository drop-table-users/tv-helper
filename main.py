#!/usr/bin/python3
import gi
import subprocess
import time
import sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject

def main():

    try:
        if sys.platform != 'linux':
            raise RuntimeError("This application was developed for use on GNU/Linux or BSD only.")
    except RuntimeError:
        sys.exit(1)
    builder = gtk.Builder()
    builder.add_from_file("main.ui")

    ## declarations
    # main window
    main = builder.get_object("main");
    kodi = builder.get_object("kodi");
    network = builder.get_object("network");
    restart	= builder.get_object("restart");
    update = builder.get_object("update");
    fix_label = builder.get_object("fix-label")
    expand = builder.get_object("expander")
    update_text = builder.get_object("update-text")
    # menu bar
    menu_quit = builder.get_object("menu-quit");
    menu_about = builder.get_object("menu-about");
    # about window
    about = builder.get_object("about");
    about_ok = builder.get_object("about-ok");
    # restart window
    restart_win = builder.get_object("restart-win");
    restart_ok = builder.get_object("restart-ok");
    restart_cancel = builder.get_object("restart-cancel");

    ## buttons
    # misc
    main.connect('destroy', gtk.main_quit)
    menu_quit.connect('activate', gtk.main_quit)
    menu_about.connect('activate', show_widget, about)
    about.connect('destroy', hide_widget, about) # don't destroy the about window, just hide it
    main.set_icon_from_file("pepe.jpg")
    # main window buttons
    kodi.connect('clicked', launch_kodi)
    network.connect('clicked', fix_net, fix_label)
    restart.connect('clicked', show_widget, restart_win)
    update_tuple = (fix_label, update_text, expand)
    update.connect('clicked', check_updates, update_tuple)
    # about window
    about_ok.connect('clicked', hide_widget, about)
    # restart window
    restart_ok.connect('clicked', _restart_dev)
    restart_cancel.connect('clicked', hide_widget, restart_win)

    # thing to hide the fix label
    buttons = (kodi, restart, update) # network excluded for obvious reasons
    for button in buttons:
        button.connect('clicked', hide_widget, fix_label)
    gobject.timeout_add(5000, timeout_hide, fix_label)

    buttons = (kodi, network, restart)
    for button in buttons:
        button.connect('clicked', hide_widget, expand)

    gtk.main()

def show_widget(widget, data):
    data.show()

def hide_widget(widget, data):
    print("\ncalled by", widget)
    print ("request to hide", data)
    data.hide()

def timeout_hide(label):
    gobject.timeout_add(5000, timeout_hide, label)
    # recursive timeout_add to keep it from self-destructing
    label.hide()

def launch_kodi(trash): # trash var to intercept widget signal emit
    try:
        subprocess.call(['kodi'])
    except FileNotFoundError:
        print("Kodi is not installed. Go to Help→Install Kodi to fix this.")

def fix_net(widget, data):
    # TODO implement a search function maybe
    data.set_text("Fix applied.")
    data.show()
    subprocess.call('sudo wpa_supplicant -iwlan0 -Dwext -c /etc/wpa_supplicant/wpa_supplicant.conf &'.split(' '))
    subprocess.call(['sudo', 'dhcpcd'])

def _restart_dev(arg_catcher):
    subprocess.call(['reboot'])

def _update_textview(view, stream):
    view.get_buffer().insert_at_cursor(stream.communicate()[0].decode('utf-8'))
    return stream.poll() is None


def check_updates(widget, data):
    data[0].set_text("Checking for updates. Please wait.")
    data[0].show()
    data[2].show()
#    stream = subprocess.Popen('ping -c 3 google.com'.split(' '), stdout=subprocess.PIPE)
# that was for testing purposes only
    stream = subprocess.Popen('sudo apt update && sudo apt upgrade'.split(' '), stdout=subprocess.PIPE)

    gobject.timeout_add(100, _update_textview, data[1], stream)


if __name__ == '__main__':
     main()
