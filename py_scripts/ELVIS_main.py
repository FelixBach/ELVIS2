from py_scripts import ELVIS_field_indices_modul, ELVIS_pix_based_indices_modul, ELVIS_date_based_subsets
from datetime import datetime

start_time = datetime.now()


def main():
    # input and output paths

    # inpath like "C:/your/path/input/"
    inpath = "C:/402_praxis/xx_04_data/S2/FRIEN/"  # input path, store .shp ,raster and csv-files in the same input
    # folder

    outpath_date_based_subsets = "C:/402_praxis/processed/sen2_scenes/date_based/"
    # outpath like "C:/your/path/output_date_based/"

    outpath_pix_res = "C:/402_praxis/processed/pix_based_indices/all/"

    outpath_res_csv = "C:/402_praxis/processed/indices_csv/update/"

    # specify extensions
    shp_extension = '*.shp'
    ras_extension = '*.tif'
    csv_extension = '*.csv'

    # search for and subset cloudless images
    ELVIS_date_based_subsets.date_subset(inpath, outpath_date_based_subsets, csv_extension, ras_extension,
                                         shp_extension)

    # calculating the different indices with a field based and pixel based approach
    # field based function creates mean/median for each field and gives an csv-file as output
    ELVIS_field_indices_modul.indices_field_based(outpath_date_based_subsets, outpath_res_csv, csv_extension)

    # pixel based function creates for each indice an tif
    # manche parameter müssen manuell im folgenden Modul geändert werden
    ELVIS_pix_based_indices_modul.pixel_based_ratio(outpath_date_based_subsets, outpath_pix_res, ras_extension)

    end_time = datetime.now()
    print("end-time = ", end_time - start_time, "Hr:min:sec")


# main func
if __name__ == '__main__':
    main()
