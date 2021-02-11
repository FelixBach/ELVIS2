import glob
import rasterio as rio
import numpy as np

subset_list = []
ras_ex = '*.tif'

# result list pixel based
ndvi_pixel = []
arvi_pixel = []
ccci_pixel = []
gari_pixel = []
ndre_pixel = []
savi_pixel = []
siwsi_pixel = []


def sublist(subset_list, outpath_date_based_subsets):
    # searching for input in file
    for name in glob.glob(outpath_date_based_subsets+str('*.tif')):
        subset_list.append(name)
    subset_list = [w.replace('\\', '/') for w in subset_list]
    subset_name = [w[len(outpath_date_based_subsets):-(len(ras_ex) - 1)] for w in subset_list]
    print(str(len(subset_list)) + str(" subsets found"))

    return subset_list, subset_name


def ndvi_pix(band_8_nir_big, band_4_red):
    ndvi_pixel_res = (band_8_nir_big - band_4_red) / \
                     (band_8_nir_big + band_4_red)
    ndvi_pixel.append(ndvi_pixel_res)

    return ndvi_pixel


def arvi_pix(band_8_nir_big, band_4_red, band_2_blue):
    arvi_pixel_res = (band_8_nir_big - (band_4_red - 1 * (band_2_blue - band_4_red))) / \
                     (band_8_nir_big + (band_4_red - 1 * (band_2_blue - band_4_red)))
    arvi_pixel.append(arvi_pixel_res)

    return arvi_pixel


def ccci_pix(band_8_nir_big, band_4_red, band_5_red_edge_1_sm):
    ccci_pixel_res = ((band_8_nir_big - band_5_red_edge_1_sm) / (band_8_nir_big + band_5_red_edge_1_sm)) / \
                     ((band_8_nir_big - band_4_red) / (band_8_nir_big + band_4_red))
    ccci_pixel.append(ccci_pixel_res)

    return ccci_pixel


def gari_pix(band_8_nir_big, band_3_green, band_2_blue, band_4_red):
    gari_pixel_res = (band_8_nir_big - (band_3_green - (band_2_blue - band_4_red))) / \
                     (band_8_nir_big - (band_3_green + (band_2_blue - band_4_red)))
    gari_pixel.append(gari_pixel_res)

    return gari_pixel


def ndre_pix(band_7_red_edge_3_sm, band_5_red_edge_1_sm):
    ndre_pixel_res = (band_7_red_edge_3_sm - band_5_red_edge_1_sm) / \
                     (band_7_red_edge_3_sm + band_5_red_edge_1_sm)
    ndre_pixel.append(ndre_pixel_res)

    return ndre_pixel


def savi_pix(band_8_nir_big, band_4_red):
    savi_pixel_res = 1.5 * ((band_8_nir_big - band_4_red) /
                            (band_8_nir_big + band_4_red + 0.5))
    savi_pixel.append(savi_pixel_res)

    return savi_pixel


def siwsi_pix(band_8a_nir_sm, band_11_swir_1):
    siwsi_pixel_res = (band_8a_nir_sm - band_11_swir_1) / (band_8a_nir_sm + band_11_swir_1)
    siwsi_pixel.append(siwsi_pixel_res)

    return siwsi_pixel


# iterate over al files from folder and load bands
def pixel_based_ratio(subset_list, outpath_date_based_subsets, outpath_pix_res):
    subset_list, subset_name = sublist(subset_list, outpath_date_based_subsets)
    for i, subset in enumerate(subset_list):
        with rio.open(subset_list[i]) as src:
            band_1_coast = src.read(1)
        with rio.open(subset_list[i]) as src:
            band_2_blue = src.read(2)
        with rio.open(subset_list[i]) as src:
            band_3_green = src.read(3)
        with rio.open(subset_list[i]) as src:
            band_4_red = src.read(4)
        with rio.open(subset_list[i]) as src:
            band_5_red_edge_1_sm = src.read(5)
        with rio.open(subset_list[i]) as src:
            band_6_red_edge_2_sm = src.read(6)
        with rio.open(subset_list[i]) as src:
            band_7_red_edge_3_sm = src.read(7)
        with rio.open(subset_list[i]) as src:
            band_8_nir_big = src.read(8)
        with rio.open(subset_list[i]) as src:
            band_8a_nir_sm = src.read(9)
        with rio.open(subset_list[i]) as src:
            band_9_vapour = src.read(10)
        with rio.open(subset_list[i]) as src:
            band_10_cirrus_cloud = src.read(11)
        with rio.open(subset_list[i]) as src:
            band_11_swir_1 = src.read(12)
        with rio.open(subset_list[i]) as src:
            band_12_swir_2 = src.read(13)

            # ignoring division by zero
            np.seterr(divide='ignore', invalid='ignore')

            # you can select ONLY ONE of these ratios for a pixel based result
            # you have to change manually the calculated indices
            # also important YOU have to change line 178 to the right indice and also some path changes in in line 173

            ndvi_pix(band_8_nir_big, band_4_red)
            arvi_pix(band_8_nir_big, band_4_red, band_2_blue)
            ccci_pix(band_8_nir_big, band_4_red, band_5_red_edge_1_sm)
            gari_pix(band_8_nir_big, band_3_green, band_2_blue, band_4_red)
            ndre_pix(band_7_red_edge_3_sm, band_5_red_edge_1_sm)
            savi_pix(band_8_nir_big, band_4_red)
            siwsi_pix(band_8a_nir_sm, band_11_swir_1)

            with rio.open(subset_list[i]) as src:
                ras_data = src.read()
                ras_meta = src.profile

            # make any necessary changes to raster properties, e.g.:
            ras_meta.update(count=1,
                            dtype=rio.float32,
                            nodata=0)

            with rio.open(outpath_pix_res + str(subset_name[i]) + str('_NDVI_sb') +
                    str('.tif'), 'w', **ras_meta) as dst:
                dst.write(ndvi_pixel[i], 1)

            with rio.open(outpath_pix_res + str(subset_name[i]) + str('_ARVI_sb') +
                    str('.tif'), 'w', **ras_meta) as dst:
                dst.write(arvi_pixel[i], 1)

            with rio.open(outpath_pix_res + str(subset_name[i]) + str('_CCCI_sb') +
                    str('.tif'), 'w', **ras_meta) as dst:
                dst.write(ccci_pixel[i], 1)

            with rio.open(outpath_pix_res + str(subset_name[i]) + str('_GARI_sb') +
                    str('.tif'), 'w', **ras_meta) as dst:
                dst.write(gari_pixel[i], 1)

            with rio.open(outpath_pix_res + str(subset_name[i]) + str('_NDRE_sb') +
                    str('.tif'), 'w', **ras_meta) as dst:
                dst.write(ndre_pixel[i], 1)

            with rio.open(outpath_pix_res + str(subset_name[i]) + str('_SAVI_sb') +
                    str('.tif'), 'w', **ras_meta) as dst:
                dst.write(savi_pixel[i], 1)

            with rio.open(outpath_pix_res + str(subset_name[i]) + str('_SIWSI_sb') +
                    str('.tif'), 'w', **ras_meta) as dst:
                dst.write(siwsi_pixel[i], 1)
