from threatexchange.extensions.manifest import ThreatExchangeExtensionManifest

from .signal import CLIPSignal

TX_MANIFEST = ThreatExchangeExtensionManifest(
    signal_types=(CLIPSignal),
)
