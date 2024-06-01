from pic_scanner.gui.wrappers.file_collections import GUIFileCollection
from pic_scanner.common.types import ScannedImageCollection


class GUIScannedCollection(GUIFileCollection):
    def __init__(self, scanned_collection: ScannedImageCollection):
        if not isinstance(scanned_collection, ScannedImageCollection):
            raise TypeError('The `scanned_collection` attribute must be of type `ScannedImageCollection`.')

        super().__init_

        self.__scanned_collection = scanned_collection
