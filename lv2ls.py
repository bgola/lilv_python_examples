#!/usr/bin/python2
# GPLv3

import lilv

world = lilv.World()
world.load_all()

for plugin in world.get_all_plugins():
    print plugin.get_uri().as_string()


