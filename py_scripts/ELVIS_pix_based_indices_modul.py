import glob
import rasterio as rio
import numpy as np

# result lists pixel based
ndvi_pixel = []
ccci_pixel = []
gari_pixel = []
ndre_pixel = []
ndmi_pixel = []
ndwi_pixel = []
lci_pixel = []


# ndvi - Normalized Difference Vegetation Index


def ndvi_pix(band_8_nir_big, band_4_red):
    ndvi_pixel_res = (band_8_nir_big - band_4_red) / (band_8_nir_big + band_4_red)
    ndvi_pixel.append(ndvi_pixel_res)

    return ndvi_pixel

    # ccci - Canopy chlorophyll content index


def ccci_pix(band_8_nir_big, band_4_red, band_5_red_edge_1_sm):
    ccci_pixel_res = ((band_8_nir_big - band_5_red_edge_1_sm) / (band_8_nir_big + band_5_red_edge_1_sm)) / \
                     ((band_8_nir_big - band_4_red) / (band_8_nir_big + band_4_red))
    ccci_pixel.append(ccci_pixel_res)

    return ccci_pixel

    # gari - Green atmospherically resistant vegetation index


def gari_pix(band_8_nir_big, band_3_green, band_2_blue, band_4_red):
    gari_pixel_res = (band_8_nir_big - (band_3_green - (band_2_blue - band_4_red))) / \
                     (band_8_nir_big - (band_3_green + (band_2_blue - band_4_red)))
    gari_pixel.append(gari_pixel_res)

    return gari_pixel

    # ndre - normalized difference red-edge


def ndre_pix(band_7_red_edge_3_sm, band_5_red_edge_1_sm):
    ndre_pixel_res = (band_7_red_edge_3_sm - band_5_red_edge_1_sm) / \
                     (band_7_red_edge_3_sm + band_5_red_edge_1_sm)
    ndre_pixel.append(ndre_pixel_res)

    return ndre_pixel

    # ndmi - normalized difference moisture index


def ndmi_pix(band_8_nir_big, band_11_swir_1):
    ndmi_pixel_res = (band_8_nir_big - band_11_swir_1) / (band_8_nir_big + band_11_swir_1)
    ndmi_pixel.append(ndmi_pixel_res)

    return ndmi_pixel

    # ndwi - Normalized Difference Water Index


def ndwi_pix(band_3_green, band_8_nir_big):
    ndwi_pixel_res = (band_3_green - band_8_nir_big) / (band_3_green + band_8_nir_big)
    ndwi_pixel.append(ndwi_pixel_res)

    return ndwi_pixel

    #  Leaf Chlorophyll Index


def lci(band_8_nir_big, band_5_red_edge_1_sm, band_4_red):
    lci_pixel_res = (band_8_nir_big - band_5_red_edge_1_sm) / (band_8_nir_big + band_4_red)
    lci_pixel.append(lci_pixel_res)

    return lci_pixel


# iterate over al files from folder and load bands
def pixel_based_ratio(outpath_date_based_subsets, outpath_pix_res, ras_extension):
    # new list for pixel-based results
    pix_subset_list = []

    # searching for input in file
    for name in glob.glob(outpath_date_based_subsets + str(ras_extension)):
        pix_subset_list.append(name)
    pix_subset_list = [w.replace('\\', '/') for w in pix_subset_list]
    pix_subset_name = [w[len(outpath_date_based_subsets):-(len(ras_extension) - 1)] for w in pix_subset_list]
    print(str(len(pix_subset_list)) + str(" subsets found"))

    for i, subset in enumerate(pix_subset_list):
        with rio.open(pix_subset_list[i]) as src:
            band_1_coast = src.read(1)
        with rio.open(pix_subset_list[i]) as src:
            band_2_blue = src.read(2)
        with rio.open(pix_subset_list[i]) as src:
            band_3_green = src.read(3)
        with rio.open(pix_subset_list[i]) as src:
            band_4_red = src.read(4)
        with rio.open(pix_subset_list[i]) as src:
            band_5_red_edge_1_sm = src.read(5)
        with rio.open(pix_subset_list[i]) as src:
            band_6_red_edge_2_sm = src.read(6)
        with rio.open(pix_subset_list[i]) as src:
            band_7_red_edge_3_sm = src.read(7)
        with rio.open(pix_subset_list[i]) as src:
            band_8_nir_big = src.read(8)
        with rio.open(pix_subset_list[i]) as src:
            band_8a_nir_sm = src.read(9)
        with rio.open(pix_subset_list[i]) as src:
            band_9_vapour = src.read(10)
        with rio.open(pix_subset_list[i]) as src:
            band_10_cirrus_cloud = src.read(11)
        with rio.open(pix_subset_list[i]) as src:
            band_11_swir_1 = src.read(12)
        with rio.open(pix_subset_list[i]) as src:
            band_12_swir_2 = src.read(13)

            # ignoring division by zero
            np.seterr(divide='ignore', invalid='ignore')

            ndvi_pix(band_8_nir_big, band_4_red)
            ccci_pix(band_8_nir_big, band_4_red, band_5_red_edge_1_sm)
            gari_pix(band_8_nir_big, band_3_green, band_2_blue, band_4_red)
            ndre_pix(band_7_red_edge_3_sm, band_5_red_edge_1_sm)
            ndmi_pix(band_8a_nir_sm, band_11_swir_1)
            ndwi_pix(band_3_green, band_8_nir_big)
            lci(band_8_nir_big, band_5_red_edge_1_sm, band_4_red)

            with rio.open(pix_subset_list[i]) as src:
                ras_data = src.read()
                ras_meta = src.profile

            # make any necessary changes to raster properties, e.g.:
            ras_meta.update(count=1,
                            dtype=rio.float32,
                            nodata=0)

            with rio.open(outpath_pix_res + str(pix_subset_name[i]) + str('_NDVI_sb') + str('.tif'), 'w',
                          **ras_meta) as dst:
                dst.write(ndvi_pixel[i], 1)
                # print(pix_subset_name[i] + str("_NDVI"), str(".tif"), str("created"))

            with rio.open(outpath_pix_res + str(pix_subset_name[i]) + str('_CCCI_sb') + str('.tif'), 'w',
                          **ras_meta) as dst:
                dst.write(ccci_pixel[i], 1)
                # print(pix_subset_name[i] + str("_CCCI"), str(".tif"), str("created"))

            with rio.open(outpath_pix_res + str(pix_subset_name[i]) + str('_GARI_sb') + str('.tif'), 'w',
                          **ras_meta) as dst:
                dst.write(gari_pixel[i], 1)
                # print(pix_subset_name[i] + str("_GARI"), str(".tif"), str("created"))

            with rio.open(outpath_pix_res + str(pix_subset_name[i]) + str('_NDRE_sb') + str('.tif'), 'w',
                          **ras_meta) as dst:
                dst.write(ndre_pixel[i], 1)
                # print(pix_subset_name[i] + str("_NDRE"), str(".tif"), str("created"))

            with rio.open(outpath_pix_res + str(pix_subset_name[i]) + str("_NDMI_sb") + str(".tif"), "w",
                          **ras_meta) as dst:
                dst.write(ndmi_pixel[i], 1)
                # print(pix_subset_name[i], str("_NDMI"), str(".tif"), str("created"))

            with rio.open(outpath_pix_res + str(pix_subset_name[i]) + str("_NDWI_sb") + str(".tif"), "w",
                          **ras_meta) as dst:
                dst.write(ndwi_pixel[i], 1)
                # print(pix_subset_name[i], str("_NDWI"), str(".tif"), str("created"))

            with rio.open(outpath_pix_res + str(pix_subset_name[i]) + str("_CVI_sb") + str(".tif"), "w",
                          **ras_meta) as dst:
                dst.write(lci_pixel[i], 1)
                # print(pix_subset_name[i], str("_CVI"), str(".tif"), str("created"))
