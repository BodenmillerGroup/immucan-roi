from typing import TYPE_CHECKING, Optional

from napari.layers import Shapes
from napari.viewer import Viewer
from napari_roi import ROIWidget
from qtpy.QtWidgets import QWidget

if TYPE_CHECKING:
    from immucan_roi import IMMUcanNappingApplication


class IMMUcanROIWidget(ROIWidget):
    def __init__(
        self,
        app: "IMMUcanNappingApplication",
        viewer: Viewer,
        immucan_roi_layer: Shapes,
        parent: Optional[QWidget] = None,
    ) -> None:
        super(IMMUcanROIWidget, self).__init__(viewer, parent=parent)
        self._app = app
        self._immucan_roi_layer = immucan_roi_layer

    def save_roi_file(self) -> None:
        super(IMMUcanROIWidget, self).save_roi_file()
        immucan_roi_layer = getattr(self, "_immucan_roi_layer", None)
        if immucan_roi_layer is not None and self._roi_layer == immucan_roi_layer:
            self._app.reload_source_coords_and_update_and_save_transf_coords()

    def _on_roi_layer_changed(self, old_roi_layer: Optional[Shapes]) -> None:
        self._roi_origin_combo_box.setEnabled(True)
        super(IMMUcanROIWidget, self)._on_roi_layer_changed(old_roi_layer)
        immucan_roi_layer = getattr(self, "_immucan_roi_layer", None)
        if immucan_roi_layer is not None and self._roi_layer == immucan_roi_layer:
            self._roi_origin_combo_box.setEnabled(False)

    def _refresh_save_widget(self) -> None:
        self._roi_file_line_edit.setEnabled(True)
        self._autosave_roi_file_check_box.setEnabled(True)
        super(IMMUcanROIWidget, self)._refresh_save_widget()
        immucan_roi_layer = getattr(self, "_immucan_roi_layer", None)
        if immucan_roi_layer is not None and self._roi_layer == immucan_roi_layer:
            self._roi_file_line_edit.setEnabled(False)
            self._autosave_roi_file_check_box.setEnabled(False)
