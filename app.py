from defusedxml.ElementTree import parse
from xml.etree.ElementTree import SubElement


tree = parse("madrix.mpx")
root = tree.getroot()

maxaddr = {}

for fixture in root.iter("fixture"):
    settings = fixture.find("fixture_settings")
    universe = settings.find("dmx_universe")
    if universe is None:
        universenum = 1
    else:
        universenum = int(universe.get("value"))
    channel = settings.find("dmx_channel")
    if channel is None:
        channelnum = 0
    else:
        channelnum = int(channel.get("value"))
    maxaddr[universenum] = max(channelnum, maxaddr.get(universenum, 0))
print(maxaddr)

for fixture in root.iter("fixture"):
    settings = fixture.find("fixture_settings")
    universe = settings.find("dmx_universe")
    if universe is None:
        universenum = 1
    else:
        universenum = int(universe.get("value"))
    channel = settings.find("dmx_channel")
    if channel is None:
        channelnum = 0
    else:
        channelnum = int(channel.get("value"))
    newchannel = maxaddr[universenum] - channelnum
    if newchannel == 0:
        settings.remove(channel)
    elif channel is None:
        SubElement(settings, "dmx_channel", attrib={"value": str(newchannel)})
    else:
        channel.set("value", str(newchannel))

tree.write("new.mpx", encoding="UTF-8", xml_declaration=True)
