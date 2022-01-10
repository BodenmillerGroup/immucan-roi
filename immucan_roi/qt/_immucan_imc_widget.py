from napari.viewer import Viewer
from napari_imc import IMCWidget
from qtpy.QtWidgets import QWidget
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from immucan_roi import IMMUcanNappingApplication


class IMMUcanIMCWidget(IMCWidget):
    def __init__(
        self,
        app: IMMUcanNappingApplication,
        viewer: Viewer,
        parent: Optional[QWidget] = None,
    ) -> None:
        super(IMMUcanIMCWidget, self).__init__(viewer, parent=parent)
        self._app = app
