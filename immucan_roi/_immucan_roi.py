import pandas as pd
import sys

from napari_imc import IMCWidget
from napping import NappingApplication
from napping.qt import NappingDialog, NappingViewer
from os import PathLike
from pathlib import Path
from qtpy.QtWidgets import QFileDialog, QMessageBox
from typing import Optional, Union

from ._immucan_roi_widget import IMMUcanROIWidget


class IMMUcanNappingApplication(NappingApplication):
    def __init__(self) -> None:
        super(IMMUcanNappingApplication, self).__init__()
        self._immucan_dir: Optional[Path] = None

    def reload_source_coords_and_update_and_save_transf_coords(self) -> None:
        current_source_coords = pd.read_csv(self._navigator.current_source_coords_file)
        if len(current_source_coords.index) > 0:
            self._current_source_coords = current_source_coords
        self._update_current_transf_coords()
        if not self._write_blocked and self._current_transf_coords is not None:
            with self._navigator.current_transf_coords_file.open(
                mode="wb", buffering=0
            ) as f:
                self._current_transf_coords.to_csv(f, mode="wb", index=False)
        if self._current_widget is not None:
            self._current_widget.refresh()

    def _create_dialog(self) -> NappingDialog:
        file_dialog = QFileDialog(caption="Select IMMUcan directory")
        file_dialog.setFileMode(QFileDialog.FileMode.DirectoryOnly)
        if file_dialog.exec() != QFileDialog.DialogCode.Accepted:
            sys.exit(1)
        self._immucan_dir = Path(file_dialog.selectedFiles()[0])
        source_img_dir = self._immucan_dir / "czi"
        if not source_img_dir.exists():
            QMessageBox.critical(
                None,
                "Directory not found",
                "The 'czi' sub-directory does not exist",
            )
            sys.exit(1)
        target_img_dir = self._immucan_dir / "mcd"
        if not target_img_dir.exists():
            QMessageBox.critical(
                None,
                "Directory not found",
                "The 'mcd' sub-directory does not exist",
            )
            sys.exit(1)
        control_points_dir = self._immucan_dir / "control_points"
        control_points_dir.mkdir(exist_ok=True)
        joint_transform_dir = self._immucan_dir / "transforms"
        joint_transform_dir.mkdir(exist_ok=True)
        source_coords_dir = self._immucan_dir / "czi_rois"
        source_coords_dir.mkdir(exist_ok=True)
        transf_coords_dir = self._immucan_dir / "mcd_rois"
        transf_coords_dir.mkdir(exist_ok=True)
        empty_source_rois = pd.DataFrame(columns=["Name", "X", "Y", "W", "H"])
        for source_img_file in source_img_dir.iterdir():
            source_coords_file_name = source_img_file.with_suffix(".csv").name
            source_coords_file = source_coords_dir / source_coords_file_name
            if not source_coords_file.exists():
                empty_source_rois.to_csv(source_coords_file, index=False)
        dialog = super(IMMUcanNappingApplication, self)._create_dialog()
        dialog.selection_mode = NappingDialog.SelectionMode.DIR
        dialog.matching_strategy = NappingDialog.MatchingStrategy.ALPHABETICAL
        dialog.source_img_path = source_img_dir
        dialog.source_regex = None
        dialog.target_img_path = target_img_dir
        dialog.target_regex = None
        dialog.control_points_path = control_points_dir
        dialog.joint_transform_path = joint_transform_dir
        dialog.transform_type = NappingDialog.TransformType.AFFINE
        dialog.source_coords_path = source_coords_dir
        dialog.source_coords_regex = None
        dialog.transf_coords_path = transf_coords_dir
        dialog.pre_transform_path = None
        dialog.post_transform_path = None
        return dialog

    def _create_source_viewer(self, img_file: Union[str, PathLike]) -> NappingViewer:
        assert self._immucan_dir is not None
        source_roi_dir = self._immucan_dir / "czi_rois"
        source_roi_dir.mkdir(exist_ok=True)
        source_viewer = super(IMMUcanNappingApplication, self)._create_source_viewer(
            img_file
        )
        immucan_roi_layer = source_viewer.viewer.add_shapes(name="ROIs")
        IMMUcanROIWidget.initialize_immucan_roi_layer(
            immucan_roi_layer, self._navigator.current_source_coords_file
        )
        immucan_roi_widget = IMMUcanROIWidget(
            self, source_viewer.viewer, immucan_roi_layer
        )
        source_viewer.viewer.window.add_dock_widget(
            immucan_roi_widget, name="regions of interest"
        )
        source_viewer.viewer.layers.selection.active = immucan_roi_layer
        if immucan_roi_widget.roi_file.exists():
            immucan_roi_widget.load_roi_file()
        else:
            immucan_roi_widget.save_roi_file()
        source_viewer.viewer.layers.selection.active = source_viewer.points_layer
        return source_viewer

    def _create_target_viewer(self, img_file: Union[str, PathLike]) -> NappingViewer:
        assert self._immucan_dir is not None
        target_roi_dir = self._immucan_dir / "mcd_rois"
        target_roi_dir.mkdir(exist_ok=True)
        target_viewer = super(IMMUcanNappingApplication, self)._create_target_viewer(
            img_file
        )
        imc_widget = IMCWidget(target_viewer.viewer)
        target_viewer.viewer.window.add_dock_widget(
            imc_widget, name="imaging mass cytometry"
        )
        target_viewer.viewer.layers.selection.active = target_viewer.points_layer
        return target_viewer
