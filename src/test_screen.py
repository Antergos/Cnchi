from gi.repository import Gtk, GLib

def _(txt):
    return txt

def get_screen(screen_name, params):
    screen = None
    if screen_name == "DesktopAsk":
        import desktop
        screen = desktop.DesktopAsk(params)
    elif screen_name == "Check":
        import check
        screen = check.Check(params)
    elif screen_name == "Timezone":
        import timezone
        screen = timezone.Timezone(params)
    elif screen_name == "Wireless":
        import wireless
        screen = wireless.Wireless(params)
    elif screen_name == "Welcome":
        import welcome
        screen = welcome.Welcome(params)
    elif screen_name == "UserInfo":
        import user_info
        screen = user_info.UserInfo(params)
    elif screen_name == "Location":
        import location
        screen = location.Location(params)
    elif screen_name == "Language":
        import language
        screen = language.Language(params)
    elif screen_name == "Keymap":
        import keymap
        screen = keymap.Keymap(params)
    elif screen_name == "Features":
        import features
        screen = features.Features(params)
    return screen

def run(screen_name):
    window = Gtk.Window()
    window.connect('destroy', Gtk.main_quit)
    window.set_size_request(600, 500)
    window.set_border_width(12)
    params = {}
    params['title'] = "Cnchi"
    params['ui_dir'] = "/usr/share/cnchi/ui"
    params['disable_tryit'] = False
    import config
    settings = config.Settings()
    settings.set('data', '/usr/share/cnchi/data')
    from desktop_environments import DESKTOPS
    settings.set('desktops', DESKTOPS)
    params['settings'] = settings
    params['forward_button'] = Gtk.Button.new()
    params['backwards_button'] = Gtk.Button.new()
    params['main_progressbar'] = Gtk.ProgressBar.new()
    params['header'] = Gtk.HeaderBar.new()
    params['testing'] = True
    screen = get_screen(screen_name, params)
    if screen != None:
        window.add(screen)
        window.show_all()
        Gtk.main()
    else:
        print("Unknown screen")
