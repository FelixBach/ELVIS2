import glob
import numpy as np
import rasterio as rio
import csv

# initial list for the result
subset_list_4 = []
subset_list_47 = []
subset_list_50 = []
subset_list_51 = []


# result lists for field mean/median
ndvi_mean = []
ndvi_median = []
arvi_mean = []
arvi_median = []
ccci_mean = []
ccci_median = []
gari_mean = []
gari_median = []
ndre_mean = []
ndre_median = []
savi_mean = []
savi_median = []
siwsi_mean = []
siwsi_median = []


# func for calc mean/median field indices
def indices_field_based(outpath_date_based_subsets, outpath_res_csv, csv_extension):
    # new list for subsets
    subset_list = []

    # searching for subsets as input
    for name in glob.glob(str(outpath_date_based_subsets) + str('*_4.tif')):
        subset_list.append(name)
    subset_list = [w.replace('\\', '/') for w in subset_list]
    print(str(len(subset_list)) + str(" subsets found"))

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

        np.seterr(divide='ignore', invalid='ignore')

        # ndvi
        ndvi_mean_field = (np.nanmean(band_8_nir_big) - np.nanmean(band_4_red)) / \
                          (np.nanmean(band_8_nir_big) + np.nanmean(band_4_red))

        ndvi_median_field = (np.nanmedian(band_8_nir_big) - np.nanmedian(band_4_red)) / \
                            (np.nanmedian(band_8_nir_big) + np.nanmedian(band_4_red))

        ndvi_mean.append(ndvi_mean_field)
        ndvi_median.append(ndvi_median_field)

        # arvi
        arvi_mean_field = (np.nanmean(band_8_nir_big) - (
                np.nanmean(band_4_red) - 1 * (np.nanmean(band_2_blue) - np.nanmean(band_4_red)))) / \
                          (np.nanmean(band_8_nir_big) + (
                                  np.nanmean(band_4_red) - 1 * (np.nanmean(band_2_blue) - np.nanmean(band_4_red))))

        arvi_median_field = (np.nanmedian(band_8_nir_big) - (
                np.median(band_4_red) - 1 * (np.nanmedian(band_2_blue) - np.nanmedian(band_4_red)))) / \
                            (np.nanmean(band_8_nir_big) + (
                                    np.nanmedian(band_4_red) - 1 * (
                                    np.nanmedian(band_2_blue) - np.nanmedian(band_4_red))))

        arvi_mean.append(arvi_mean_field)
        arvi_median.append(arvi_median_field)

        # ccci
        ccci_mean_field = ((np.nanmean(band_8_nir_big) - np.nanmean(band_5_red_edge_1_sm)) /
                           (np.nanmean(band_8_nir_big) + np.nanmean(band_5_red_edge_1_sm))) / \
                          ((np.nanmean(band_8_nir_big) - np.nanmean(band_4_red)) /
                           (np.nanmean(band_8_nir_big) + np.nanmean(band_4_red)))
        ccci_median_field = ((np.nanmedian(band_8_nir_big) - np.nanmedian(band_5_red_edge_1_sm)) /
                             (np.nanmedian(band_8_nir_big) + np.nanmedian(band_5_red_edge_1_sm))) / \
                            ((np.nanmedian(band_8_nir_big) - np.nanmedian(band_4_red)) /
                             (np.nanmedian(band_8_nir_big) + np.nanmedian(band_4_red)))

        ccci_mean.append(ccci_mean_field)
        ccci_median.append(ccci_median_field)

        # gari
        gari_mean_field = (np.nanmean(band_8_nir_big) - (
                np.nanmean(band_3_green) - (np.nanmean(band_2_blue) - np.nanmean(band_4_red)))) / \
                          (np.nanmean(band_8_nir_big) - (
                                  np.nanmean(band_3_green) + (np.nanmean(band_2_blue) - np.nanmean(band_4_red))))
        gari_median_field = (np.nanmedian(band_8_nir_big) - (
                np.nanmedian(band_3_green) - (np.nanmedian(band_2_blue) - np.nanmedian(band_4_red)))) / \
                            (np.nanmedian(band_8_nir_big) - (
                                    np.nanmedian(band_3_green) + (
                                    np.nanmedian(band_2_blue) - np.nanmedian(band_4_red))))

        gari_mean.append(gari_mean_field)
        gari_median.append(gari_median_field)

        # ndre

        ndre_mean_field = (np.nanmean(band_7_red_edge_3_sm) - np.nanmean(band_5_red_edge_1_sm)) / \
                          (np.nanmean(band_7_red_edge_3_sm) + np.nanmean(band_5_red_edge_1_sm))
        ndre_median_field = (np.nanmedian(band_7_red_edge_3_sm) - np.nanmedian(band_5_red_edge_1_sm)) / \
                            (np.nanmedian(band_7_red_edge_3_sm) + np.nanmedian(band_5_red_edge_1_sm))

        ndre_mean.append(ndre_mean_field)
        ndre_median.append(ndre_median_field)

        # savi
        savi_mean_field = 1.5 * ((np.nanmean(band_8_nir_big) - np.nanmean(band_4_red)) /
                                 (np.nanmean(band_8_nir_big) + np.nanmean(band_4_red) + 0.5))
        savi_median_field = 1.5 * ((np.nanmedian(band_8_nir_big) - np.nanmedian(band_4_red)) /
                                   (np.nanmedian(band_8_nir_big) + np.nanmedian(band_4_red) + 0.5))

        savi_mean.append(savi_mean_field)
        savi_median.append(savi_median_field)

        # siwsi
        siwsi_mean_field = (np.nanmean(band_8a_nir_sm) - np.nanmean(band_11_swir_1)) / \
                           (np.nanmean(band_8a_nir_sm) + np.nanmean(band_11_swir_1))
        siwsi_median_field = (np.nanmedian(band_8a_nir_sm) - np.nanmedian(band_11_swir_1)) / \
                             (np.nanmedian(band_8a_nir_sm) + np.nanmedian(band_11_swir_1))

        siwsi_mean.append(siwsi_mean_field)
        siwsi_median.append(siwsi_median_field)

        if (i + 1) == (len(subset_list)):
            with open(str(outpath_res_csv) + "fid_4" + csv_extension[1:], 'w',
                      encoding="UTF-8", newline='') as myfile:
                wr = csv.writer(myfile)
                wr.writerow(("ndvi_mean", "ndvi_median", "arvi_mean", "arvi_median", "ccci_mean", "ccci_median",
                             "gari_mean", "gari_median", "ndre_mean", "ndre_median", "savi_mean", "savi_median",
                             "siwsi_mean", "siwsi_median"))
                wr.writerows(zip(ndvi_mean, ndvi_median, arvi_mean, arvi_median,  ccci_mean, ccci_median, gari_mean,
                                 gari_median, ndre_mean, ndre_median, savi_mean, savi_median, siwsi_mean,
                                 siwsi_median))

    return print("done")
