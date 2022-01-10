from napari.viewer import Viewer
from napari_roi import ROIWidget
from qtpy.QtWidgets import QWidget
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from immucan_roi import IMMUcanNappingApplication


class IMMUcanROIWidget(ROIWidget):
    def __init__(
        self,
        app: IMMUcanNappingApplication,
        viewer: Viewer,
        parent: Optional[QWidget] = None,
    ) -> None:
        super(IMMUcanROIWidget, self).__init__(viewer, parent=parent)
        self._app = app

    def save(self) -> None:
        super(IMMUcanROIWidget, self).save()
        self._app.reload_source_coords_and_update_and_save_transf_coords()
