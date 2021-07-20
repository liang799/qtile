import os
import subprocess
import logging
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from typing import List  # noqa: F401

### VARIABLES ###
mod = "mod4"                                          
terminal = "gnome-terminal"                          
myConfig = "/home/james/.config/qtile/config.py"   

### MISC FUNCTIONS ###
# Brings all floating windows to the front
@lazy.function
def float_to_front(qtile):
    logging.info("bring floating windows to front")
    for group in qtile.groups:
        for window in group.windows:
            if window.floating:
                window.cmd_bring_to_front()

### KEYBINDS ###
keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", 
        lazy.layout.shuffle_down(),
        lazy.layout.section_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", 
        lazy.layout.shuffle_up(),
        lazy.layout.section_up(),
        desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), lazy.layout.shrink(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), lazy.layout.grow(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "m", lazy.layout.maximize(), desc='maximize'),

    Key([mod], "f", lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc='toggle floating'),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    #Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        #desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #Key([mod], "r", lazy.spawncmd(),
    #    desc="Spawn a command using a prompt widget"),


    # Sound
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 1- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 1+ unmute")),

    # backlight controls
    Key([], "XF86MonBrightnessUp", lazy.spawn("light -A 2")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("light -U 2")),

    # Screenshot
    Key([], "Print", lazy.spawn("scrot -e 'mv $f ~/Pictures/Screenshots/ 2>/dev/null'"), desc="Screenshot"),

    # dmenu
    Key([mod, "shift"], "Return", lazy.spawn("rofi -show drun"), desc="Find Desktop Apps"),
    Key([mod], "s", lazy.spawn("bash /home/james/dmscripts/switch"), desc="switch window"),
    Key([mod], "i", lazy.spawn("bash /home/james/dmscripts/dmsearch"), desc="Internet"),
    Key([mod, "shift"], "m", lazy.spawn("bash /home/james/dmscripts/dman"), desc="Man page"),
    Key([mod], "q", lazy.spawn("bash /home/james/dmscripts/dmkill"), desc="Q(uit) - kill"),
    Key([mod], "e", lazy.spawn("bash /home/james/dmscripts/dmconf"), desc="Edit config"),
    Key([mod], "p", lazy.spawn("bash /home/james/dmscripts/dmscrot"), desc="Print screen"),
    Key([mod], "a", lazy.spawn("bash /home/james/dmscripts/mpdmenu"), desc="Artist - music"),
    Key([mod], "y", lazy.spawn("ytfzf -D"), desc="Youtube"),
    Key([mod], "c", lazy.spawn("clipmenu"), desc="Clipboard manager"),

    # GUI browser
    Key([mod], "b", lazy.spawn("firefox"), desc="firefox"),
]

### GROUPS ###
groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

### DEFAULT THEME SETTINGS FOR LAYOUTS ###
layout_theme = {"border_width": 3,
                "margin": 10,
                "border_focus" : "#5e81ac",
                "border_normal": "#3b4252"
                }

### LAYOUTS ###
layouts = [
    layout.Columns(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Floating(**layout_theme)
]



colors = [["#282a36", "#282a36"], # Background                [0]
          ["#44475a", "#44475a"], # Current Line / Selection  [1]
          ["#f8f8f2", "#f8f8f2"], # Foreground                [2]
          ["#6272a4", "#6272a4"], # Comment                   [3]
          ["#8be9fd", "#8be9fd"], # Cyan                      [4]
          ["#50fa7b", "#50fa7b"], # Green                     [5]
          ["#ffb86c", "#ffb86c"], # Orange                    [6]
          ["#ff79c6", "#ff79c6"], # Pink                      [7]
          ["#bd93f9", "#bd93f9"], # Purple                    [8]
          ["#ff5555", "#ff5555"], # Red                       [9]
          ["#0000ff", "#0000ff"], # blue                      [10]
          ["#f1fa8c", "#f1fa8c"]] # Yellow                    [11]


widget_defaults = dict(
    font='FiraCode Medium',
    fontsize=12,
	foreground=colors[2],
    padding=2,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(background=colors[1]),
                widget.Spacer(length=5, background=colors[0]),
                widget.GroupBox(background=colors[0], this_current_screen_border=colors[1], this_screen_border=colors[6], active=colors[4], inactive=colors[3]),
                widget.Spacer(length=5, background=colors[0]),
                widget.WindowName(padding=690, max_chars=17),
		widget.Volume(background=colors[0], foreground=colors[4],fmt='  Vol: {}'),
                #widget.CPU(background=colors[1], format='  CPU: {freq_current}GHz {load_percent}%'),
                widget.Clock(format='  %a,  %I:%M %p ', background=colors[0], foreground=colors[6]),
                widget.Systray(background = colors[0], padding = 5),
            ],
            20,
			background=colors[0],
        ),
    ),

    Screen(
    ),

]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'tor'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"



### STARTUP APPLICATIONS ###
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
