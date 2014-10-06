#!/usr/bin/python2
# GPLv3

import sys, lilv
uri = sys.argv[1]

world = lilv.World()
world.load_all()

plugin = world.get_all_plugins().get_by_uri(world.new_uri(uri))

def lilv_foreach(collection, func):
    l = []
    itr = collection.begin()
    while itr:
        yield func(collection.get(itr))
        itr = collection.next(itr)

# Get basic plugin info
print plugin.get_uri().as_string()
print ""
print "\tClass:\t\t\t%s" % plugin.get_class().get_label().as_string()
print "\tAuthor:\t\t\t%s" % plugin.get_author_name().as_string()
print "\tAuthor Email:\t\t%s" % plugin.get_author_email().as_string()
print "\tHas latency:\t\t%s" % ("yes" if plugin.has_latency() else "no")
print "\tBundle:\t\t\t%s" % plugin.get_bundle_uri().as_string()
print "\tBinary:\t\t\t%s" % plugin.get_library_uri().as_string()

data_uris = list(lilv_foreach(plugin.get_data_uris(), lambda uri: uri.as_string()))
print "\tData URIs:\t\t%s" % data_uris[0]
for uri in data_uris[1:]:
    print "\t\t\t\t%s" % uri

required_features = list(lilv_foreach(plugin.get_required_features(), lambda uri: uri.as_string()))
print "\tRequired Features:\t%s" % required_features[0]
for uri in required_features[1:]:
    print "\t\t\t\t%s" % uri

opt_features = list(lilv_foreach(plugin.get_optional_features(), lambda uri: uri.as_string()))
print "\tOptional Features:\t%s" % opt_features[0]
for uri in required_features[1:]:
    print "\t\t\t\t%s" % uri

# Presets
preset_uri = lilv.Node(world.new_uri("http://lv2plug.in/ns/ext/presets#Preset"))
label_uri = world.new_uri(lilv.LILV_NS_RDFS + "label")
psets = plugin.get_related(preset_uri)

if psets.size():
    def print_preset(pset):
        world.load_resource(pset.me)
        nodes = world.find_nodes(pset.me, label_uri, None)
        def print_label(node):
            print "\t\t%s" % node.as_string()
        list(lilv_foreach(nodes, print_label)) # list() will force the generator

    print "\tPresets:"
    list(lilv_foreach(psets, print_preset)) # list() will force the generator

# Ports information
for idx in range(plugin.get_num_ports()):
    port = plugin.get_port_by_index(idx)
    print "\n\tPort %d" % idx
    p_types = list(lilv_foreach(lilv.Nodes(port.get_classes()), lambda typ: typ.as_string()))
    print "\t\tType:\t%s" % p_types[0]
    for typ in p_types[1:]:
        print "\t\t\t%s" % typ
    print "\t\tSymbol:\t%s" % lilv.Node(port.get_symbol()).as_string()
    print "\t\tName:\t%s" % lilv.Node(port.get_name()).as_string()


