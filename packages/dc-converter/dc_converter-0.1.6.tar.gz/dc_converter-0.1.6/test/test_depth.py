from dc_converter.convert_folder import convert_depth_file_target


def test_depth_target():
    convert_depth_file_target(
        './data/data.raw',
        './data/depth.tiff')
