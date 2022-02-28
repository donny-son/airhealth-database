layers = iface.mapCanvas().layers()
for layer in layers:
    layer.setSubsetString('"year" = \'2001\'')