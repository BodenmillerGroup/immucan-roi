# immucan-roi

IMMUcan ROI selection using napping, napari-imc and napari-roi

## Installation

To install the latest version of `immucan-roi`:

    pip install git+https://github.com/BodenmillerGroup/immucan-roi.git

To install a specific version (e.g. `v0.1.0`) of `immucan-roi`:

    pip install git+https://github.com/BodenmillerGroup/immucan-roi.git@v0.1.0

At the time of writing, `immucan-roi` only works with the latest `main` version of napari (>0.4.12, unreleased). To install the latest `main` version of napari from GitHub:

    pip install --upgrade "git+https://github.com/napari/napari"

## Usage

1. Run `immucan-roi`, select your IMMUcan folder containing `czi` and `mcd` subdirectories and accept the proposed settings
2. With the `Control points` layers selected, choose enough (>3) control points in both images to create an accurate transform
3. With the `ROIs` layer selected and the `autosave` option active, draw/specify the desired regions of interests (ROIs) on the slidescanner image

Note: Due to a bug in napari, `immucan-roi` may crash when adding ROIs. As a workaround, manually add a Shapes layer to the IMC window and ensure to activate this layer whenever working on the `ROIs` layer in the slidescanner window.

## Authors

Created and maintained by Jonas Windhager [jonas.windhager@uzh.ch](mailto:jonas.windhager@uzh.ch)

## Contributing

[Contributing](https://github.com/BodenmillerGroup/immucan-roi/blob/main/CONTRIBUTING.md)

## Changelog

[Changelog](https://github.com/BodenmillerGroup/immucan-roi/blob/main/CHANGELOG.md)

## License

[MIT](https://github.com/BodenmillerGroup/immucan-roi/blob/main/LICENSE.md)
