# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "kitty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "t", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window",),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "Return", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("wpctl set-volume -l 1.4 @DEFAULT_AUDIO_SINK@ 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("wpctl set-volume -l 1.4 @DEFAULT_AUDIO_SINK@ 5%-")),
    Key([], "XF86AudioMute", lazy.spawn("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key(["control"], "space", lazy.spawn('playerctl --player=musikcube,%any play-pause')),
    Key(["control"], "j", lazy.spawn('playerctl --player=musikcube,%any previous')),
    Key(["control"], "k", lazy.spawn('playerctl --player=musikcube,%any next')),
    Key([mod], "Escape", lazy.spawn("/home/evie/.config/scripts/lock.sh", shell=True)),
    Key([mod], "space", lazy.spawn("bemenu-run --fn 'FiraCode Nerd Font Mono Normal Medium 11' --margin 780 --center --list 11 down --binding vim --vim-esc-exits --tb #272727 --tf #ebdbb2 --fb #272727 --ff #ebdbb2 #ebdbb2 --nb #272727 --nf #ebdbb2 --hb #272727 --hf #8ec07b --sb #272727 --sf #8ec07b --ab #272727 --af #ebdbb2 --border 2 --bdr #ebdbb2 --border-radius 11 --fixed-height"), desc="menu"),
    Key([mod], "b", lazy.spawn("firefox"), desc="browser"),
    Key([], "Print", lazy.spawn("/home/evie/.config/scripts/screenshot.sh", shell=True)),
    Key([mod], "Print", lazy.spawn("/home/evie/.config/scripts/iscreenshot.sh", shell=True)),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.MonadTall(
                     border_focus="#ebdbb2", 
                     border_normal="#272727",
                     ratio=0.57,
                     margin=0,
                     single_border_width=0,
                     border_width=2,
                     ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    #layout.Matrix(),
    #        border_focus="#55ff55",
    #        border_normal="#000000",
    #        single_border_width=0,
    #        border_width=2,    
    #        ),
    # layout.Columns(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="FiraCode Nerd Font Propo Medium",
    fontsize=16,
    padding=11,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method='block',
                    block_highlight_text_color='000000',
                    borderwidth=2,
                    margin=3,
                    padding=2,
                    active='ebdbb2',
                    inactive='928373',
                    this_current_screen_border='ebdbb2',
                    this_screen_border='ebdbb2',
                    hide_unused=False,
                    rounded=True,
                    ),
                widget.CurrentLayout(
                    foreground='ebdbb2'
                    ),
                widget.Prompt(
                    foreground='ebdbb2',
                    ),
                widget.WindowName(
                    max_chars=30,
                    foreground='ebdbb2'
                    ),
                widget.Mpris2(
                    foreground='b8ba25',
                    poll_interval=3
                    ),
                widget.Notify(
                    default_timeout=7,
                    default_timeout_low=7,
                    foreground='b8ba25',
                    foreground_low='b8ba25',
                    foreground_urgent='fb4833'
                    ),
              widget.Clock(
                    format="%d/%m/%Y // %T",
                    foreground='83a597'
                    ),
               widget.PulseVolume(
                    #emoji_list=['󰝟', '󰕿', '󰖀', '󰕾'],
                    #emoji=True,
                    unmute_format='󰕾 {volume}%',
                    mute_format='󰝟 x',
                    foreground='d3859a',
                    ),
                widget.Wlan(
                    interface='wlp1s0',
                    format='󰖩 {percent:2.0%}',
                    foreground='d65c0d'
                    ),
                #widget.CPU(
                #    format=' {freq_current}GHz {load_percent}%',
                #    foreground='ebdbb2'
                #    ),
                widget.Memory(
                    measure_mem='G',
                    format=' {MemUsed:0.1f}G/{MemTotal:0.1f}G',
                    foreground='fabc2e'
                    ),
                widget.Battery(
                    update_interval=3,
                    show_short_text=False,
                    format='{char} {percent:2.0%} {hour:d}:{min:02d}',
                    discharge_char='',
                    charge_char='',
                    full_char='󰣇',
                    foreground='689d69',
                    low_foreground='fb4833',
                    low_percentage=0.35
                    ),
            ],
            33,
            background="#181818",
            opacity=1.0,
            margin=[0, 0, 0, 0],
            # border_width=[0, 0, 4, 0],  # Draw top and bottom borders, NESW
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        #wallpaper = '~/wallpapers/gits0.png',
        #wallpaper_mode = 'fill',
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
floats_kept_above = True
cursor_warp = True
floating_layout = layout.Floating(
    border_focus='ebdbb2',
    border_normal='272727',
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

wmname = "qtile"
