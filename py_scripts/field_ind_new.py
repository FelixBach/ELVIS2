import glob
from os.path import join
import numpy as np
import rasterio as rio
import csv
from py_scripts import ELVIS_data_import_modul

# result lists for field mean/median
ndvi_mean = []
ndvi_median = []


# func for calc mean/median field indices
def indices_field_based(outpath_date_based_subsets, outpath_res_csv, csv_extension, inpath, shp_extension,
                        ras_extension):
    # new list for subsets
    subset_list = []
    # shp_names = ELVIS_data_import_modul.shp_names(inpath, shp_extension)

    shp_list = []
    # searching .shp-files
    for shp in glob.glob(join(inpath, shp_extension)):
        shp_list.append(shp)
    shp_list = [w.replace('\\', '/') for w in shp_list]
    shp_names = [str("_") + w[len(inpath):-(len(shp_extension) - 1)] for w in shp_list]

    print(shp_names)
    # TODO index wird noch nicht richtig berechnet, aber liste mit subsets wird erstellt und wieder geleert
    # berechnung einfügen und Ausgabe von csv-Dateien
    i = 0
    print("glob")
    print(len(shp_names))
    while i < len(shp_names):
        for name in glob.glob(str(outpath_date_based_subsets) + str("*") + shp_names[i] + ras_extension[1:]):
            subset_list.append(name)
            subset_list = [w.replace('\\', '/') for w in subset_list]
            # print(subset_list)
            # j = 0
            # for j, subset in enumerate(subset_list):
            #     with rio.open(subset_list[j]) as src:
            #         band_4_red = src.read(4)
            #     with rio.open(subset_list[j]) as src:
            #         band_8_nir_big = src.read(8)
            #
            #     np.seterr(divide='ignore', invalid='ignore')
            #
            #     # ndvi
            #     ndvi_mean_field = (np.nanmean(band_8_nir_big) - np.nanmean(band_4_red)) / \
            #                       (np.nanmean(band_8_nir_big) + np.nanmean(band_4_red))
            #
            #     ndvi_median_field = (np.nanmedian(band_8_nir_big) - np.nanmedian(band_4_red)) / \
            #                         (np.nanmedian(band_8_nir_big) + np.nanmedian(band_4_red))
            #
            #     ndvi_mean.append(ndvi_mean_field)
            #     ndvi_median.append(ndvi_median_field)
            #     print(ndvi_mean)
            #     print(ndvi_median)
            #
            #     j = j + 1
            #
            #     if (j + 1) == (len(subset_list)):
            #         with open(str(outpath_res_csv) + shp_names[i] + csv_extension[1:], 'w',
            #                   encoding="UTF-8", newline='') as myfile:
            #             wr = csv.writer(myfile)
            #             wr.writerow(("ndvi_mean", "ndvi_median"))
            #             wr.writerows(zip(ndvi_mean, ndvi_median))

        i = i + 1
        print(len(subset_list))
        subset_list.clear()
        print(len(subset_list))

    return print("done")


inpath = "C:/402_praxis/xx_04_data/S2/FRIEN/"
outpath_date_based_subsets = "C:/402_praxis/processed/sen2_scenes/date_based/"
outpath_res_csv = "C:/402_praxis/processed/indices_csv/update/"
csv_extension = '*.csv'
shp_extension = '*.shp'
ras_extension = '*.tif'

indices_field_based(outpath_date_based_subsets, outpath_res_csv, csv_extension, inpath, shp_extension, ras_extension)
