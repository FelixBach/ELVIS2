from py_scripts import ELVIS_field_indices_modul, ELVIS_pix_based_indices_modul, ELVIS_date_based_subsets, \
    ELVIS_simple_subset
from datetime import datetime

start_time = datetime.now()


def main():
    # input and output paths

    # inpath like "C:/your/path/input/"
    inpath = "C:/402_praxis/xx_04_data/S2/FRIEN/"  # input path, store .shp ,raster and csv-files in the same input
    # folder

    # outpath like "C:/your/path/output/"
    outpath_subsets = "C:/402_praxis/processed/sen2_scenes/fid_based/test/"  # path from the output folder

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
    ELVIS_date_based_subsets.date_subset(inpath, outpath_date_based_subsets, csv_list, shp_list, raster_list,
                                         csv_extension, ras_extension, shp_extension)

    # subsetting simple
    ELVIS_simple_subset.simple_subset(inpath, outpath_subsets, shp_extension, ras_extension, shp_list, raster_list)

    # calculating the different indices with a field based and pixel based approach
    # field based function creates mean/median for each field/croptype and gives an csv-file as output
    subset_list = ELVIS_field_indices_modul.subset_import(subset_list, outpath_date_based_subsets)
    ELVIS_field_indices_modul.indices_field_based(subset_list)

    # pixel based function creates for each indice an tif
    # manche parameter müssen manuell im folgenden Modul geändert werden
    ELVIS_pix_based_indices_modul.pixel_based_ratio(subset_list_pix)

    end_time = datetime.now()
    print("end-time = ", end_time - start_time, "Hr:min:sec")


# main func
if __name__ == '__main__':
    main()
