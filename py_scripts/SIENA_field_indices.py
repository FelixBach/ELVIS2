import glob
import numpy as np
import rasterio as rio
import csv

# result lists for field mean/median
ndvi_mean = []
ndvi_median = []
ndvi_sd = []
ccci_mean = []
ccci_median = []
ccci_sd = []
gari_mean = []
gari_median = []
gari_sd = []
ndre_mean = []
ndre_median = []
ndre_sd = []
siwsi_mean = []
siwsi_median = []
siwsi_sd = []
ndmi_mean = []
ndmi_median = []
ndmi_sd = []
ndwi_mean = []
ndwi_median = []
ndwi_sd = []
lci_mean = []
lci_median = []
lci_sd = []


# func for calc mean/median field indices
def indices_field_based(inpath, outpath_date_based_subsets, outpath_res_csv, ras_extension, shp_extension,
                        csv_extension):
    # new list for subsets
    subset_list = []
    shp_list = []
    # searching .shp-files
    for shp in glob.glob(inpath + shp_extension):
        shp_list.append(shp)
    shp_list = [w.replace('\\', '/') for w in shp_list]
    shp_names = [str("_") + w[len(inpath):-(len(shp_extension) - 1)] for w in shp_list]

    i = 0
    while i < len(shp_names):
        for name in glob.glob(str(outpath_date_based_subsets) + str("*") + shp_names[i] + ras_extension[1:]):
            subset_list.append(name)
            subset_list = [w.replace('\\', '/') for w in subset_list]

        j = 0
        while j < len(subset_list):
            with rio.open(subset_list[j]) as src:
                band_1_coast = src.read(1)
            with rio.open(subset_list[j]) as src:
                band_2_blue = src.read(2)
            with rio.open(subset_list[j]) as src:
                band_3_green = src.read(3)
            with rio.open(subset_list[j]) as src:
                band_4_red = src.read(4)
            with rio.open(subset_list[j]) as src:
                band_5_red_edge_1_sm = src.read(5)
            with rio.open(subset_list[j]) as src:
                band_6_red_edge_2_sm = src.read(6)
            with rio.open(subset_list[j]) as src:
                band_7_red_edge_3_sm = src.read(7)
            with rio.open(subset_list[j]) as src:
                band_8_nir_big = src.read(8)
            with rio.open(subset_list[j]) as src:
                band_8a_nir_sm = src.read(9)
            with rio.open(subset_list[j]) as src:
                band_9_vapour = src.read(10)
            with rio.open(subset_list[j]) as src:
                band_10_cirrus_cloud = src.read(11)
            with rio.open(subset_list[j]) as src:
                band_11_swir_1 = src.read(12)
            with rio.open(subset_list[j]) as src:
                band_12_swir_2 = src.read(13)

            np.seterr(divide='ignore', invalid='ignore')

            # ndvi
            ndvi_mean_field = (np.nanmean(band_8_nir_big) - np.nanmean(band_4_red)) / \
                              (np.nanmean(band_8_nir_big) + np.nanmean(band_4_red))

            ndvi_median_field = (np.nanmedian(band_8_nir_big) - np.nanmedian(band_4_red)) / \
                                (np.nanmedian(band_8_nir_big) + np.nanmedian(band_4_red))

            ndvi_mean.append(ndvi_mean_field)
            ndvi_median.append(ndvi_median_field)

            ndvi_f_sd = np.nanstd((band_8_nir_big - band_4_red) / (band_8_nir_big + band_4_red))
            ndvi_sd.append(ndvi_f_sd)

            # ccci
            ccci_mean_field = ((np.nanmean(band_8a_nir_sm) - np.nanmean(band_5_red_edge_1_sm)) /
                               (np.nanmean(band_8a_nir_sm) + np.nanmean(band_5_red_edge_1_sm))) / \
                              ((np.nanmean(band_8a_nir_sm) - np.nanmean(band_4_red)) /
                               (np.nanmean(band_8a_nir_sm) + np.nanmean(band_4_red)))
            ccci_median_field = ((np.nanmedian(band_8a_nir_sm) - np.nanmedian(band_5_red_edge_1_sm)) /
                                 (np.nanmedian(band_8a_nir_sm) + np.nanmedian(band_5_red_edge_1_sm))) / \
                                ((np.nanmedian(band_8a_nir_sm) - np.nanmedian(band_4_red)) /
                                 (np.nanmedian(band_8a_nir_sm) + np.nanmedian(band_4_red)))

            ccci_mean.append(ccci_mean_field)
            ccci_median.append(ccci_median_field)

            ccci_f_sd = np.nanstd((band_8_nir_big - band_5_red_edge_1_sm) / (band_8_nir_big + band_5_red_edge_1_sm) / \
                        ((band_8_nir_big - band_4_red) / (band_8_nir_big + band_4_red)))
            ccci_sd.append(ccci_f_sd)

            # gari
            gari_mean_field = (np.nanmean(band_8_nir_big) - (np.nanmean(band_3_green) - (np.nanmean(band_2_blue) -
                                                                                         np.nanmean(band_4_red)))) / \
                              (np.nanmean(band_8_nir_big) - (np.nanmean(band_3_green) + (np.nanmean(band_2_blue) -
                                                                                         np.nanmean(band_4_red))))

            gari_median_field = (np.nanmedian(band_8_nir_big) - (
                    np.nanmedian(band_3_green) - (np.nanmedian(band_2_blue) - np.nanmedian(band_4_red)))) / \
                                (np.nanmedian(band_8_nir_big) - (
                                        np.nanmedian(band_3_green) + (
                                        np.nanmedian(band_2_blue) - np.nanmedian(band_4_red))))

            gari_mean.append(gari_mean_field)
            gari_median.append(gari_median_field)

            gari_f_sd = np.nanstd((band_8_nir_big - (band_3_green - (band_2_blue - band_4_red))) / \
                        (band_8_nir_big - (band_3_green + (band_2_blue - band_4_red))))
            gari_sd.append(gari_f_sd)

            # ndre
            ndre_mean_field = (np.nanmean(band_8_nir_big) - np.nanmean(band_5_red_edge_1_sm)) / \
                              (np.nanmean(band_8_nir_big) + np.nanmean(band_5_red_edge_1_sm))
            ndre_median_field = (np.nanmedian(band_8_nir_big) - np.nanmedian(band_5_red_edge_1_sm)) / \
                                (np.nanmedian(band_8_nir_big) + np.nanmedian(band_5_red_edge_1_sm))

            ndre_mean.append(ndre_mean_field)
            ndre_median.append(ndre_median_field)

            ndre_f_sd = np.nanstd((band_7_red_edge_3_sm - band_5_red_edge_1_sm) / \
                        (band_7_red_edge_3_sm + band_5_red_edge_1_sm))
            ndre_sd.append(ndre_f_sd)

            # ndmi - normalized difference moisture index
            ndmi_mean_field = (np.nanmean(band_8_nir_big) - np.nanmean(band_11_swir_1)) / \
                              (np.nanmean(band_8_nir_big) + np.nanmean(band_11_swir_1))
            ndmi_median_field = (np.nanmedian(band_8_nir_big) - np.nanmedian(band_11_swir_1)) / \
                                (np.nanmedian(band_8_nir_big) + np.nanmedian(band_11_swir_1))

            ndmi_mean.append(ndmi_mean_field)
            ndmi_median.append(ndmi_median_field)

            ndmi_f_sd = np.nanstd((band_8_nir_big - band_11_swir_1) / (band_8_nir_big + band_11_swir_1))
            ndmi_sd.append(ndmi_f_sd)

            # ndwi
            ndwi_mean_field = (np.nanmean(band_3_green) - np.nanmean(band_8_nir_big)) / \
                              (np.nanmean(band_3_green) + np.nanmean(band_8_nir_big))
            ndwi_median_field = (np.nanmedian(band_3_green) - np.nanmedian(band_8_nir_big)) / \
                                (np.nanmedian(band_3_green) + np.nanmedian(band_8_nir_big))

            ndwi_mean.append(ndwi_mean_field)
            ndwi_median.append(ndwi_median_field)

            ndwi_f_sd = np.nanstd((band_3_green - band_8_nir_big) / (band_3_green + band_8_nir_big))
            ndwi_sd.append(ndwi_f_sd)

            # lci - leaf chlorophyll index
            lci_mean_field = (np.nanmean(band_8_nir_big) - np.nanmean(band_5_red_edge_1_sm)) / \
                             (np.nanmean(band_8_nir_big) + np.nanmean(band_4_red))
            lci_median_field = (np.nanmedian(band_8_nir_big) - np.nanmedian(band_5_red_edge_1_sm)) / \
                               (np.nanmedian(band_8_nir_big) + np.nanmedian(band_4_red))

            lci_mean.append(lci_mean_field)
            lci_median.append(lci_median_field)

            lci_f_sd = np.nanstd((band_8_nir_big - band_5_red_edge_1_sm) / (band_8_nir_big + band_4_red))
            lci_sd.append(lci_f_sd)

            j = j + 1

            #  exporting csv-files with results
            if j == (len(subset_list)):
                with open(str(outpath_res_csv) + shp_names[i][1:] + csv_extension[1:], 'w',
                          encoding="UTF-8", newline='') as file:
                    wr = csv.writer(file)
                    wr.writerow(("ndvi_mean", "ndvi_median", "ndvi_sd", "ccci_mean", "ccci_median", "ccci_sd",
                                 "gari_mean", "gari_median", "gari_sd", "ndre_mean", "ndre_median", "ndre_sd",
                                 "ndmi_mean", "ndmi_sd", "ndmi_median", "ndwi_mean", "ndwi_median", "ndwi_sd",
                                 "lci_mean", "lci_median", "lci_sd"))
                    wr.writerows(zip(ndvi_mean, ndvi_median, ndvi_sd, ccci_mean, ccci_median, ccci_sd, gari_mean,
                                     gari_median, gari_sd, ndre_mean, ndre_median, ndre_sd, ndmi_mean, ndmi_median,
                                     ndmi_sd, ndwi_mean, ndwi_median, ndwi_sd, lci_mean, lci_median, lci_sd))
        # clearing indices lists
        ndvi_median.clear()
        ndvi_mean.clear()
        ndvi_sd.clear()
        ccci_mean.clear()
        ccci_median.clear()
        ccci_sd.clear()
        gari_mean.clear()
        gari_median.clear()
        gari_sd.clear()
        ndre_mean.clear()
        ndre_median.clear()
        ndre_sd.clear()
        ndmi_mean.clear()
        ndmi_median.clear()
        ndmi_sd.clear()
        ndwi_mean.clear()
        ndwi_median.clear()
        ndwi_sd.clear()
        lci_mean.clear()
        lci_median.clear()
        lci_sd.clear()

        # clearing subset list
        subset_list.clear()

        i = i + 1

    return print("Field indices calculated for each subset")