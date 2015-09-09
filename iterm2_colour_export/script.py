#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""iTerm2 Colour Export

Parses a binary iTerm2 plist preferences file and exports all profile and preset colour schemes to a directory.

Warren Moore
      @wamonite     - twitter
       \_______.com - web
warren____________/ - email
"""

from __future__ import print_function
import argparse
import sys
import biplist
import os

DEFAULT_PLIST = '~/Library/Preferences/com.googlecode.iterm2.plist'
COLOUR_NAME_LIST = [
    'Background Color',
    'Foreground Color',
    'Cursor Color',
    'Cursor Text Color',
    'Ansi 0 Color',
    'Ansi 1 Color',
    'Ansi 2 Color',
    'Ansi 3 Color',
    'Ansi 4 Color',
    'Ansi 5 Color',
    'Ansi 6 Color',
    'Ansi 7 Color',
    'Ansi 8 Color',
    'Ansi 9 Color',
    'Ansi 10 Color',
    'Ansi 11 Color',
    'Ansi 12 Color',
    'Ansi 13 Color',
    'Ansi 14 Color',
    'Ansi 15 Color'
]


class ScriptException(Exception):
    """Derived exception to throw simple error messages.
    """


def get_rgb_colour(colour_value_lookup):
    """Convert to integer RGB values to ignore rounding errors.
    """

    return (
        int(float(colour_value_lookup['Red Component']) * 255.0),
        int(float(colour_value_lookup['Green Component']) * 255.0),
        int(float(colour_value_lookup['Blue Component']) * 255.0)
    )


def match_profile_to_preset(profile_lookup, colour_preset_lookup):
    """Get a list of preset names that match the current profile colour scheme.
    """

    match_list = []
    for preset_name, preset_colours in colour_preset_lookup.iteritems():
        match = True
        for colour_name, colour_val in preset_colours.iteritems():
            if colour_name in profile_lookup:
                if get_rgb_colour(colour_val) != get_rgb_colour(profile_lookup[colour_name]):
                    match = False
                    break

        if match:
            match_list.append(preset_name)

    return match_list


def print_match_profiles(profile_list, colour_preset_lookup):
    """For each profile, print the list of colour presets it matches.
    """

    for profile_lookup in profile_list:
        match_list = match_profile_to_preset(profile_lookup, colour_preset_lookup)
        if match_list:
            print('profile (%s) matches (%s)' % (profile_lookup['Name'], ', '.join(match_list)))


def print_unused_presets(profile_list, colour_preset_lookup):
    unused_list = colour_preset_lookup.keys()
    for profile_lookup in profile_list:
        match_list = match_profile_to_preset(profile_lookup, colour_preset_lookup)
        for preset in match_list:
            if preset in unused_list:
                unused_list.remove(preset)

    for preset in unused_list:
        print("preset (%s) unused" % preset)


def make_directory(directory_name):
    """Check output directory, making it if necessary.
    """

    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

    elif not os.path.isdir(directory_name):
        raise ScriptException('directory not found (%s)' % directory_name)


def write_colour_plist(colour_lookup, export_name, colour_type_name, output_directory):
    """Write the colour scheme to a named file as a text plist.
    """

    make_directory(output_directory)

    export_directory_name = os.path.join(output_directory, colour_type_name)
    make_directory(export_directory_name)

    export_file_name = os.path.join(export_directory_name, '%s.itermcolors' % export_name)
    print('writing (%s) (%s) to (%s)' % (colour_type_name, export_name, export_file_name))

    output_colour_lookup = {}
    for colour_name in COLOUR_NAME_LIST:
        if colour_name in colour_lookup:
            output_colour_lookup[colour_name] = colour_lookup[colour_name]

    biplist.writePlist(output_colour_lookup, export_file_name, binary = False)


def export_colours(profile_list, colour_preset_lookup, output_directory):
    """Write the profile and preset colour schemes to the output directory.
    """

    if profile_list:
        for profile_lookup in profile_list:
            write_colour_plist(profile_lookup, profile_lookup['Name'], 'profile', output_directory)

    if colour_preset_lookup:
        for preset_name, colour_lookup in colour_preset_lookup.iteritems():
            write_colour_plist(colour_lookup, preset_name, 'preset', output_directory)


def parse_iterm_plist(plist_file_name, match_profiles = True, unused_presets = False, output_directory = None):
    """Parse the profile and preset colour schemes from the specified iTerm2 plist.
    """

    file_name = os.path.expanduser(plist_file_name)
    plist = biplist.readPlist(file_name)

    profile_list = plist.get('New Bookmarks', [])
    colour_preset_lookup = plist.get('Custom Color Presets', {})

    if unused_presets:
        print_unused_presets(profile_list, colour_preset_lookup)

    elif match_profiles:
        print_match_profiles(profile_list, colour_preset_lookup)

    if output_directory:
        export_colours(profile_list, colour_preset_lookup, output_directory)


def do_iterm2_colour_export():
    parser = argparse.ArgumentParser(
        description = 'iterm2_colour_export',
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-p', '--plist', default = DEFAULT_PLIST, help = 'input plist file')
    parser.add_argument('-n', '--no-match', action = 'store_false', help = 'do not show profiles that match presets')
    parser.add_argument('-u', '--unused', action = 'store_true', help = 'show presets that are not used by any profiles (implies -n)')
    parser.add_argument('-o', '--output-directory', help = 'output directory')
    args = parser.parse_args()

    parse_iterm_plist(
        args.plist,
        args.no_match,
        args.unused,
        args.output_directory
    )


def run():
    try:
        do_iterm2_colour_export()

    except ScriptException as e:
        print('Error:', e, file = sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    do_iterm2_colour_export()
