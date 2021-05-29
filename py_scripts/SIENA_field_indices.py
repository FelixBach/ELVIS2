import glob
import numpy as np
import rasterio as rio
import csv
import os

# result lists for field mean/median
ari_mean = []
ari_median = []
ari_sd = []
ccci_mean = []
ccci_median = []
ccci_sd = []
evi_mean = []
evi_median = []
evi_sd = []
evi2_mean = []
evi2_median = []
evi2_sd = []
gari_mean = []
gari_median = []
gari_sd = []
gndvi_mean = []
gndvi_median = []
gndvi_sd = []
lci_mean = []
lci_median = []
lci_sd = []
mari_mean = []
mari_median = []
mari_sd = []
msi_mean = []
msi_median = []
msi_sd = []
ndci_mean = []
ndci_median = []
ndci_sd = []
ndmi_mean = []
ndmi_median = []
ndmi_sd = []
ndre_mean = []
ndre_median = []
ndre_sd = []
ndvi_mean = []
ndvi_median = []
ndvi_sd = []
ndwi_mean = []
ndwi_median = []
ndwi_sd = []
sipi_mean = []
sipi_median = []
sipi_sd = []



def field_based(path, folder_subsets, folder_csv_files, ras_extension, shp_extension, csv_extension):
    if not os.path.isdir(path + folder_csv_files):
        csv_path = os.path.join(path, folder_csv_files)
        os.makedirs(csv_path)
        print(f"CSV output folder created \n")
    else:
        print(f"CSV output folder exists \n")

    # new list for subsets
    subset_list = []
    shp_list = []

    # searching .shp-files
    for shp in glob.glob(path + shp_extension):
        shp_list.append(shp)
    shp_list = [w.replace('\\', '/') for w in shp_list]
    shp_names = [str("_") + w[len(path):-(len(shp_extension) - 1)] for w in shp_list]

    for i, shp in enumerate(shp_names):
        for name in glob.glob(path + folder_subsets + str("*") + shp_names[i] + ras_extension[1:]):
            subset_list.append(name)
            subset_list = [w.replace('\\', '/') for w in subset_list]
            subset_names = [w[len(path + folder_subsets):-(len(ras_extension) - 1)] for w in subset_list]

        for j, subset in enumerate(subset_list):
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

            # ari
            ari_mean_field = (1 / np.nanmean(band_3_green)) - (1 / np.nanmean(band_5_red_edge_1_sm))
            ari_median_field = (1 / np.nanmedian(band_3_green)) - (1 / np.nanmedian(band_5_red_edge_1_sm))
            ari_mean.append(ari_mean_field)
            ari_median.append(ari_median_field)
            ari_f_sd = np.nanstd((1 / band_3_green) - (1 / band_5_red_edge_1_sm))
            ari_sd.append(ari_f_sd)

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

            # evi
            evi_mean_field = ((2.5 * (np.nanmean(band_8_nir_big) - np.nanmean(band_4_red))) /
                              ((np.nanmean(band_8_nir_big) + 6 * np.nanmean(band_4_red) - 7.5 *
                                np.nanmean(band_2_blue)) + 1))
            evi_median_field = ((2.5 * (np.nanmedian(band_8_nir_big) - np.nanmedian(band_4_red))) /
                                ((np.nanmedian(band_8_nir_big) + 6 * np.nanmedian(band_4_red) - 7.5 *
                                  np.nanmedian(band_2_blue)) + 1))
            evi_mean.append(evi_mean_field)
            evi_median.append(evi_median_field)
            evi_f_sd = np.nanstd(((2.5 * (band_8_nir_big - band_4_red)) / ((band_8_nir_big + 6 * band_4_red - 7.5 *
                                                                            band_2_blue) + 1)))
            evi_sd.append(evi_f_sd)

            # evi2
            evi2_mean_field = (2.4 * (np.nanmean(band_8_nir_big) - np.nanmean(band_3_green))) / \
                              (np.nanmean(band_8_nir_big) + np.nanmean(band_4_red) + 1)
            evi2_median_field = (2.4 * (np.nanmedian(band_8_nir_big) - np.nanmedian(band_3_green))) / \
                                (np.nanmedian(band_8_nir_big) + np.nanmedian(band_4_red) + 1)
            evi2_mean.append(evi2_mean_field)
            evi2_median.append(evi2_median_field)
            evi2_f_sd = np.nanstd((2.4 * (band_8_nir_big - band_3_green)) / (band_8_nir_big + band_4_red + 1))
            evi2_sd.append(evi2_f_sd)

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

            # gndvi
            gndvi_mean_field = (np.nanmean(band_8_nir_big) - np.nanmean(band_3_green)) / \
                               (np.nanmean(band_8_nir_big) + np.nanmean(band_3_green))

            gndvi_median_field = (np.nanmedian(band_8_nir_big) - np.nanmedian(band_3_green)) / \
                                 (np.nanmedian(band_8_nir_big) + np.nanmedian(band_3_green))

            gndvi_mean.append(gndvi_mean_field)
            gndvi_median.append(gndvi_median_field)

            gndvi_f_sd = np.nanstd((band_8_nir_big - band_3_green) / (band_8_nir_big + band_3_green))
            gndvi_sd.append(gndvi_f_sd)

            # lci - leaf chlorophyll index
            lci_mean_field = (np.nanmean(band_8_nir_big) - np.nanmean(band_5_red_edge_1_sm)) / \
                             (np.nanmean(band_8_nir_big) + np.nanmean(band_4_red))
            lci_median_field = (np.nanmedian(band_8_nir_big) - np.nanmedian(band_5_red_edge_1_sm)) / \
                               (np.nanmedian(band_8_nir_big) + np.nanmedian(band_4_red))

            lci_mean.append(lci_mean_field)
            lci_median.append(lci_median_field)

            lci_f_sd = np.nanstd((band_8_nir_big - band_5_red_edge_1_sm) / (band_8_nir_big + band_4_red))
            lci_sd.append(lci_f_sd)

            # mari
            mari_mean_field = (((1 / np.nanmean(band_3_green)) - (1 / np.nanmean(band_5_red_edge_1_sm))) *
                               np.nanmean(band_7_red_edge_3_sm))
            mari_median_field = (((1 / np.nanmedian(band_3_green)) - (1 / np.nanmedian(band_5_red_edge_1_sm))) *
                                 np.nanmedian(band_7_red_edge_3_sm))
            mari_mean.append(mari_mean_field)
            mari_median.append(mari_median_field)
            mari_f_sd = np.nanstd(((1 / band_3_green) - (1 / band_5_red_edge_1_sm)) * band_7_red_edge_3_sm)
            mari_sd.append(mari_f_sd)

            # msi
            msi_mean_field = np.nanmean(band_11_swir_1) / np.nanmean(band_8_nir_big)
            msi_median_field = np.nanmedian(band_11_swir_1) / np.nanmedian(band_8_nir_big)
            msi_mean.append(msi_mean_field)
            msi_median.append(msi_median_field)
            msi_f_sd = np.nanstd(band_11_swir_1 / band_8_nir_big)
            msi_sd.append(msi_f_sd)

            # ndci
            ndci_mean_field = (np.nanmean(band_5_red_edge_1_sm) - np.nanmean(band_4_red)) / \
                              (np.nanmean(band_5_red_edge_1_sm) + np.nanmean(band_4_red))
            ndci_median_field = (np.nanmedian(band_5_red_edge_1_sm) - np.nanmedian(band_4_red)) / \
                                (np.nanmedian(band_5_red_edge_1_sm) + np.nanmedian(band_4_red))
            ndci_mean.append(ndci_mean_field)
            ndci_median.append(ndci_median_field)
            ndci_f_sd = np.nanstd((band_5_red_edge_1_sm - band_4_red) / (band_5_red_edge_1_sm + band_4_red))
            ndci_sd.append(ndci_f_sd)

            # ndmi - normalized difference moisture index
            ndmi_mean_field = (np.nanmean(band_8_nir_big) - np.nanmean(band_11_swir_1)) / \
                              (np.nanmean(band_8_nir_big) + np.nanmean(band_11_swir_1))
            ndmi_median_field = (np.nanmedian(band_8_nir_big) - np.nanmedian(band_11_swir_1)) / \
                                (np.nanmedian(band_8_nir_big) + np.nanmedian(band_11_swir_1))

            ndmi_mean.append(ndmi_mean_field)
            ndmi_median.append(ndmi_median_field)

            ndmi_f_sd = np.nanstd((band_8_nir_big - band_11_swir_1) / (band_8_nir_big + band_11_swir_1))
            ndmi_sd.append(ndmi_f_sd)

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

            # ndvi
            ndvi_mean_field = (np.nanmean(band_8_nir_big) - np.nanmean(band_4_red)) / \
                              (np.nanmean(band_8_nir_big) + np.nanmean(band_4_red))

            ndvi_median_field = (np.nanmedian(band_8_nir_big) - np.nanmedian(band_4_red)) / \
                                (np.nanmedian(band_8_nir_big) + np.nanmedian(band_4_red))

            ndvi_mean.append(ndvi_mean_field)
            ndvi_median.append(ndvi_median_field)

            ndvi_f_sd = np.nanstd((band_8_nir_big - band_4_red) / (band_8_nir_big + band_4_red))
            ndvi_sd.append(ndvi_f_sd)

            # ndwi
            ndwi_mean_field = (np.nanmean(band_3_green) - np.nanmean(band_8_nir_big)) / \
                              (np.nanmean(band_3_green) + np.nanmean(band_8_nir_big))
            ndwi_median_field = (np.nanmedian(band_3_green) - np.nanmedian(band_8_nir_big)) / \
                                (np.nanmedian(band_3_green) + np.nanmedian(band_8_nir_big))

            ndwi_mean.append(ndwi_mean_field)
            ndwi_median.append(ndwi_median_field)

            ndwi_f_sd = np.nanstd((band_3_green - band_8_nir_big) / (band_3_green + band_8_nir_big))
            ndwi_sd.append(ndwi_f_sd)

            # SIPI1
            sipi_mean_field = (np.nanmean(band_8_nir_big) - np.nanmean(band_1_coast)) / \
                              (np.nanmean(band_8_nir_big) + np.nanmean(band_4_red))
            sipi_median_field = (np.nanmedian(band_8_nir_big) - np.nanmedian(band_1_coast)) / \
                                (np.nanmedian(band_8_nir_big) + np.nanmedian(band_4_red))
            sipi_mean.append(sipi_mean_field)
            sipi_median.append(sipi_median_field)
            sipi_f_sd = np.nanstd((band_8_nir_big - band_1_coast) / (band_8_nir_big + band_4_red))
            sipi_sd.append(sipi_f_sd)

        with open(path + folder_csv_files + shp_names[i][1:] + csv_extension[1:], 'w',
                  encoding="UTF-8", newline='') as file:
            wr = csv.writer(file)
            wr.writerow(("subset_names", "ari_mean", "ari_median", "ari_sd",  "ccci_mean", "ccci_median", "ccci_sd",
                         "evi_mean", "evi_median", "evi_sd", "evi2_mean", "evi2_median", "evi2_sd", "gari_mean",
                         "gari_median", "gari_sd", "gndvi_mean", "gndvi_median", "gndvi_sd", "lci_mean", "lci_median",
                         "lci_sd", "mari_mean", "mari_median", "mari_sd",
                         "msi_mean", "msi_median", "msi_sd", "ndci_mean", "ndci_median", "ndci_sd", "ndmi_mean",
                         "ndmi_median", "ndmi_sd", "ndre_mean", "ndre_median", "ndre_sd", "ndvi_mean", "ndvi_median",
                         "ndvi_sd", "ndwi_mean", "ndwi_median", "ndwi_sd", "sipi_mean", "sipi_median", "sipi_sd"))
            wr.writerows(zip(subset_names, ari_mean, ari_median, ari_sd, ccci_mean, ccci_median, ccci_sd, evi_mean,
                             evi_median, evi_sd, evi2_mean, evi2_median, evi2_sd, gari_mean, gari_median, gari_sd,
                             gndvi_mean, gndvi_median, gndvi_sd, lci_mean, lci_median, lci_sd, mari_mean, mari_median,
                             mari_sd, msi_mean, msi_median, msi_sd, ndci_mean,
                             ndci_median, ndci_sd, ndmi_mean, ndmi_median, ndmi_sd, ndre_mean, ndre_median, ndre_sd,
                             ndvi_mean, ndvi_median, ndvi_sd, ndwi_mean, ndwi_median, ndwi_sd, sipi_mean, sipi_median,
                             sipi_sd))

        # clearing indices lists
        ari_mean.clear()
        ari_median.clear()
        ari_sd.clear()
        ccci_mean.clear()
        ccci_median.clear()
        ccci_sd.clear()
        evi_mean.clear()
        evi_median.clear()
        evi_sd.clear()
        evi2_mean.clear()
        evi2_median.clear()
        evi2_sd.clear()
        gari_mean.clear()
        gari_median.clear()
        gari_sd.clear()
        gndvi_mean.clear()
        gndvi_median.clear()
        gndvi_sd.clear()
        lci_mean.clear()
        lci_median.clear()
        lci_sd.clear()
        mari_mean.clear()
        mari_median.clear()
        mari_sd.clear()
        msi_mean.clear()
        msi_median.clear()
        msi_sd.clear()
        ndci_mean.clear()
        ndci_median.clear()
        ndci_sd.clear()
        ndmi_mean.clear()
        ndmi_median.clear()
        ndmi_sd .clear()
        ndre_mean.clear()
        ndre_median.clear()
        ndre_sd.clear()
        ndvi_mean.clear()
        ndvi_median.clear()
        ndvi_sd.clear()
        ndwi_mean.clear()
        ndwi_median.clear()
        ndwi_sd.clear()
        sipi_mean.clear()
        sipi_median.clear()
        sipi_sd.clear()

        # clearing subset list
        subset_list.clear()

    return print("Field indices calculated for each subset")
