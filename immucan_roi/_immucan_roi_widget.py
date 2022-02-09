from napari.layers import Shapes
from napari.viewer import Viewer
from napari_roi import ROIWidget, ROIOrigin
from napari_roi.qt import ROILayerAccessor
from os import PathLike
from pathlib import Path
from qtpy.QtWidgets import QWidget
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from immucan_roi import IMMUcanNappingApplication


class IMMUcanROIWidget(ROIWidget):
    @staticmethod
    def initialize_immucan_roi_layer(
        immucan_roi_layer: Shapes, immucan_roi_file: Union[str, PathLike]
    ) -> None:
        immucan_roi_layer_accessor = ROILayerAccessor(immucan_roi_layer)
        immucan_roi_layer_accessor.roi_origin = ROIOrigin.BOTTOM_RIGHT
        immucan_roi_layer_accessor.roi_file = Path(immucan_roi_file)
        immucan_roi_layer_accessor.autosave_roi_file = True

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
        if self._roi_layer == self.immucan_roi_layer:
            self._app.reload_source_coords_and_update_and_save_transf_coords()

    def _on_roi_layer_changed(self, old_roi_layer: Optional[Shapes]) -> None:
        super(IMMUcanROIWidget, self)._on_roi_layer_changed(old_roi_layer)
        immucan_roi_layer = getattr(self, "_immucan_roi_layer", None)
        self._roi_origin_combo_box.setEnabled(
            immucan_roi_layer is not None and self._roi_layer != immucan_roi_layer
        )

    def _refresh_save_widget(self) -> None:
        super(IMMUcanROIWidget, self)._refresh_save_widget()
        immucan_roi_layer = getattr(self, "_immucan_roi_layer", None)
        if immucan_roi_layer is not None and self._roi_layer == immucan_roi_layer:
            self._roi_file_line_edit.setEnabled(False)
            self._autosave_roi_file_check_box.setEnabled(False)
        else:
            pass  # skipped intentionally (already set in _refresh_save_widget)
