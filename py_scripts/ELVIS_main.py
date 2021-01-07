from py_scripts import ELVIS_createsubset_modul, ELVIS_data_import_modul, ELVIS_field_indices_modul, \
    ELVIS_pix_based_indices_modul, ELVIS_date_based_subsets
from datetime import datetime

start_time = datetime.now()


def main():
    # input and output paths

    # inpath like "C:/your/path/input/"
    inpath = "C:/402_praxis/xx_04_data/S2/FRIEN/"  # input path, store .shp ,raster and csv-files in the same input
    # folder

    # outpath like "C:/your/path/output/"
    outpath_subsets = "C:/402_praxis/processed/sen2_scenes/fid_based/"  # path from the output folder

    outpath_date_based_subsets = "C:/402_praxis/processed/sen2_scenes/date_based/"
    # outpath like "C:/your/path/output_date_based/"

    outpath_res_csv = "C:/402_praxis/processed/sen2_scenes/indices_csv/"

    # specify extensions
    shp_extension = '*.shp'
    ras_extension = '*.tif'
    csv_extension = '*.csv'

    # initial lists
    subset_list = []
    subset_list_pix = []
    shp_list = []
    raster_list = []
    csv_list = []

    # search for and subset cloudless images
    # only use this function if you have some csv-files
    # subset your raster-files with information from a csv-file
    # ELVIS_date_based_subsets.date_subset(inpath, outpath_date_based_subsets, csv_list, shp_list, raster_list,
    #                                      csv_extension, ras_extension, shp_extension)

    # if you just want to subset all your raster-files, you should activate the following functions in line 41, 42, 45
    # 46 and 51

    # create shp_list and shp names
    shp_list = ELVIS_data_import_modul.shp_files(inpath, shp_extension)
    shp_names = ELVIS_data_import_modul.shp_names(inpath, shp_extension)

    # create raster_list and raster names
    raster_list = ELVIS_data_import_modul.raster_files(inpath, ras_extension)
    raster_names = ELVIS_data_import_modul.raster_names(inpath, ras_extension)

    # subsetting all files
    # ELVIS_createsubset_modul.subs(shp_list, shp_names, raster_list, raster_names, ras_extension, outpath_subsets)

    # calculating the different indices with a field based and pixel based approach
    # field based function creates mean/median for each field/croptype and gives an csv-file as output
    # subset_list = ELVIS_field_indices_modul.subset_import(subset_list, outpath_date_based_subsets)
    # ELVIS_field_indices_modul.indices_field_based(subset_list)

    # pixel based function creates for each indice an tif
    # manche parameter müssen manuell im folgenden Modul geändert werden
    # ELVIS_pix_based_indices_modul.pixel_based_ratio(subset_list_pix)

    end_time = datetime.now()
    print("end-time = ", end_time - start_time, "Hr:min:sec")


# main func
if __name__ == '__main__':
    main()
