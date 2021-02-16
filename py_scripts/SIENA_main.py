from py_scripts import SIENA_field_indices_modul, SIENA_pix_based_indices_modul, SIENA_date_based_subsets, \
    SIENA_simple_subset, SIENA_data_import_modul
from datetime import datetime

start_time = datetime.now()


def main():
    # input and output paths

    # inpath like "C:/your/path/input/"
    # input path, store .shp ,raster and csv-files in the same input folder
    inpath = "C:/402_praxis/xx_04_data/S2/FRIEN_subset/"

    # outpath like "C:/your/path/output/"
    # path from the output folder for simple.subset function
    outpath_subsets = "C:/402_praxis/test_path/subsets/"

    # outpath like "C:/your/path/output_date_based/"
    # not needed if you dont have csv files with some dates
    # outpath_date_based_subsets = "C:/402_praxis/test_path/date_subsets/"

    # outpath like "C:/your/path/pix_based/
    # results
    outpath_pix_res = "C:/402_praxis/test_path/pix_res/"

    outpath_indices_csv = "C:/402_praxis/test_path/indices_csv/"

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

    # SIENA_simple_subset.simple_subset(inpath, outpath_subsets, shp_extension, ras_extension, shp_list, raster_list)

    # calculating the different indices with a field based and pixel based approach
    # field based function creates mean/median for each field/croptype and gives an csv-file as output
    # subset_list = ELVIS_field_indices_modul.subset_import(subset_list, outpath_subsets, ras_extension, inpath,
    #                                                       shp_extension)
    # SIENA_field_indices_modul.subset_import(subset_list, outpath_subsets, ras_extension, inpath, shp_extension,
    #                                         outpath_indices_csv, csv_extension)


    # SIENA_field_indices_modul.indices_field_based(outpath_indices_csv, subset_list, outpath_subsets, ras_extension,
    #                                               inpath, shp_extension, csv_extension)

    SIENA_field_indices_modul.indi_test(outpath_indices_csv, subset_list, outpath_subsets, ras_extension, inpath,
                                        shp_extension, csv_extension)
    # SIENA_field_indices_modul.indi_test(subset_list, outpath_subsets, ras_extension, inpath, shp_extension,
    #                                    outpath_indices_csv, csv_extension)

    # pixel based function creates for each indice an tif
    # manche parameter müssen manuell im folgenden Modul geändert werden
    # SIENA_pix_based_indices_modul.pixel_based_ratio(subset_list_pix, outpath_subsets, outpath_pix_res, ras_extension)

    end_time = datetime.now()
    print("end-time = ", end_time - start_time, "Hr:min:sec")


# main func
if __name__ == '__main__':
    main()
