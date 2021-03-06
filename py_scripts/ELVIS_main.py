from py_scripts import ELVIS_field_indices_modul, ELVIS_pix_based_indices_modul, ELVIS_date_based_subsets
from datetime import datetime

start_time = datetime.now()


def main():
    ######################################
    # define input and output paths only in this part

    # input path, store .shp ,raster and csv-files in the same input folder
    # inpath like "C:/your/path/input/"
    inpath = "C:/402_praxis/xx_04_data/S2/FRIEN/"
    # inpath = "C:/Users/Max/Desktop/GEO402/processed/inpath/"

    # outpath like "C:/your/path/output_date_based/"
    outpath_date_based_subsets = "C:/402_praxis/processed/sen2_scenes/date_based/"
    # outpath_date_based_subsets = "C:/Users/Max/Desktop/GEO402/processed/outpath/outpath_date_based_subsets/"

    # outpath like "C:/your/path/pix_based_indices/"
    outpath_pix_res = "C:/402_praxis/processed/pix_based_indices/all/"
    # outpath_pix_res = "C:/Users/Max/Desktop/GEO402/processed/outpath/pix_based"

    # outpath like "C:/your/path/indices_csv/"
    outpath_res_csv = "C:/402_praxis/processed/indices_csv/update/new_res_lci/"
    # outpath_res_csv = "C:/Users/Max/Desktop/GEO402/processed/outpath/csv_indizes/"

    ######################################
    # specify extensions
    shp_extension = '*.shp'
    ras_extension = '*.tif'
    csv_extension = '*.csv'

    # search for and subset cloudless images

    # notification
    # print(f"\n Start creating subsets. \n")
    # ELVIS_date_based_subsets.date_subset(inpath, outpath_date_based_subsets, csv_extension, ras_extension,
    #                                      shp_extension)

    # calculating the different indices with a field based and pixel based approach
    # field based function creates mean/median for each field and gives an csv-file as output

    # notification
    print(f"\n Start calculating field based indices and writing result csv's. \n")
    ELVIS_field_indices_modul.indices_field_based(inpath, outpath_date_based_subsets, outpath_res_csv, ras_extension,
                                                  shp_extension, csv_extension)

    # pixel based function creates for each indice an tif
    # notification
    # print(f"\n Start calculating pixel based ratios. \n")
    # ELVIS_pix_based_indices_modul.pixel_based_ratio(outpath_date_based_subsets, outpath_pix_res, ras_extension)

    end_time = datetime.now()
    print(f"\n end-time =", end_time - start_time, "Hr:min:sec \n")


# main func
if __name__ == '__main__':
    main()
