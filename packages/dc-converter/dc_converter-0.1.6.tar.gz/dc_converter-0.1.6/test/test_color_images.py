import os.path

from dc_converter.convert_folder import write_color_images, write_multi_view


def test_color():
    write_color_images(os.path.expanduser(
        '~/tmp/Tasse/Timo_Tasse_10-ergonomic-standing-2023-09-21T164305.097Z-DCG2202205001888/data.raw'))


def test_multi():
    write_multi_view(os.path.expanduser(
        '~/tmp/Tasse/Timo_Tasse_10-ergonomic-standing-2023-09-21T164305.097Z-DCG2202205001888/data.raw'), './data/multi.png')

    write_multi_view(os.path.expanduser(
        '~/deepcare/data-preperation/data/raw/sync/Timo_LB-empty-standing-2022-09-14T154738.746ZUTC-DCG2202200000001/data.raw'), './data/multi2.png')

