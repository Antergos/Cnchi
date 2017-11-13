import gi

gi.require_versions({
    'Gtk': '3.0',
})

from gi.repository import (
    Gtk,
    Gdk,
    GObject,
)

from .controller import GTKController
