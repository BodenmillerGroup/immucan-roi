import pandas as pd

from napping import NappingApplication
from napping.qt import NappingDialog, NappingViewer
from os import PathLike
from pathlib import Path
from qtpy.QtWidgets import QFileDialog
from typing import Optional, Union

from immucan_roi.qt import IMMUcanIMCWidget, IMMUcanROIWidget


class IMMUcanNappingApplication(NappingApplication):
    def __init__(self) -> None:
        super(IMMUcanNappingApplication, self).__init__()
        self._immucan_dir: Optional[Path] = None

    def reload_source_coords_and_update_and_save_transf_coords(self) -> None:
        current_source_coords = pd.read_csv(
            self._navigator.current_source_coords_file
        )
        if len(current_source_coords.index) > 0:
            self._current_source_coords = current_source_coords
        self._update_current_transf_coords()
        if not self._write_blocked and self._current_transf_coords is not None:
            with self._navigator.current_transf_coords_file.open(
                mode="wb", buffering=0
            ) as f:
                self._current_transf_coords.to_csv(f, mode="wb", index=False)
        self._current_widget.refresh()

    def _create_dialog(self) -> NappingDialog:
        file_dialog = QFileDialog(caption="Select IMMUcan directory")
        file_dialog.setFileMode(QFileDialog.FileMode.DirectoryOnly)
        while file_dialog.exec() != QFileDialog.DialogCode.Accepted:
            pass
        self._immucan_dir = Path(file_dialog.selectedFiles()[0])
        control_points_dir = self._immucan_dir / "points"
        joint_transform_dir = self._immucan_dir / "transforms"
        source_roi_dir = self._immucan_dir / "czi_rois"
        self._immucan_dir.mkdir(exist_ok=True, parents=True)
        control_points_dir.mkdir(exist_ok=True)
        joint_transform_dir.mkdir(exist_ok=True)
        source_roi_dir.mkdir(exist_ok=True)
        dialog = super(IMMUcanNappingApplication, self)._create_dialog()
        dialog.selection_mode = NappingDialog.SelectionMode.DIR
        dialog.matching_strategy = NappingDialog.MatchingStrategy.ALPHABETICAL
        dialog.source_img_path = self._immucan_dir / "czi"
        dialog.source_regex = None
        dialog.target_img_path = self._immucan_dir / "mcd"
        dialog.target_regex = None
        dialog.control_points_path = control_points_dir
        dialog.joint_transform_path = joint_transform_dir
        dialog.transform_type = NappingDialog.TransformType.AFFINE
        dialog.source_coords_path = source_roi_dir
        dialog.source_coords_regex = None
        dialog.transf_coords_path = self._immucan_dir / "mcd_rois"
        dialog.pre_transform_path = None
        dialog.post_transform_path = None
        dummy_source_rois = pd.DataFrame(columns=["Name", "X", "Y", "W", "H"])
        for source_img_file in dialog.source_img_path.iterdir():
            dummy_source_rois.to_csv(
                source_roi_dir / source_img_file.with_suffix(".csv").name,
                index=False,
            )
        return dialog

    def _create_source_viewer(
        self, img_file: Union[str, PathLike]
    ) -> NappingViewer:
        source_viewer = super(
            IMMUcanNappingApplication, self
        )._create_source_viewer(img_file)
        roi_layer = source_viewer.viewer.add_shapes(name="ROIs")
        source_viewer.viewer.layers.selection.active = roi_layer
        roi_widget = IMMUcanROIWidget(self, source_viewer.viewer)
        source_viewer.viewer.window.add_dock_widget(
            roi_widget, name="regions of interest"
        )
        assert self._immucan_dir is not None
        source_roi_dir = self._immucan_dir / "czi_rois"
        source_roi_dir.mkdir(exist_ok=True)
        roi_widget.roi_file = self._navigator.current_source_coords_file
        if roi_widget.roi_file.exists():
            roi_widget.load()
        roi_widget.save()
        source_viewer.viewer.layers.selection.active = (
            source_viewer.points_layer
        )
        return source_viewer

    def _create_target_viewer(
        self, img_file: Union[str, PathLike]
    ) -> NappingViewer:
        target_viewer = super(
            IMMUcanNappingApplication, self
        )._create_target_viewer(img_file)
        imc_widget = IMMUcanIMCWidget(self, target_viewer.viewer)
        target_viewer.viewer.window.add_dock_widget(
            imc_widget, name="imaging mass cytometry"
        )
        assert self._immucan_dir is not None
        target_roi_dir = self._immucan_dir / "mcd_rois"
        target_roi_dir.mkdir(exist_ok=True)
        return target_viewer
