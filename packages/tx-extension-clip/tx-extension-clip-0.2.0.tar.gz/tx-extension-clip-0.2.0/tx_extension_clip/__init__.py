from threatexchange.extensions.manifest import ThreatExchangeExtensionManifest

from tx_extension_clip.signal import CLIPSignal

TX_MANIFEST = ThreatExchangeExtensionManifest(
    signal_types=(CLIPSignal,),
)
