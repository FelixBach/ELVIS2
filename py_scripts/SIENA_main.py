from py_scripts import SIENA_createsubset, SIENA_data_import, SIENA_field_indices, \
    SIENA_pix_based_indices, SIENA_date_based_subsets, SIENA_subset
from datetime import datetime
import os

start_time = datetime.now()


def main():
    ######################################
    # input and output paths

    # path like "C:/your/path/input/"
    path = "C:/SIENA/data/"  # input path, store .shp and raster in the same input folder

    # specify extensions
    shp_extension = '*.shp'
    ras_extension = '*.tif'
    csv_extension = '*.csv'

    ######################################

    folder_subsets = "subsets/"
    folder_csv_files = "csv/"

    subset_path = os.path.join(path, folder_subsets)
    # if not os.path.isdir(folder_csv_files):
    #     csv_path = os.path.join(path, folder_csv_files)
    #     os.makedirs(csv_path)
    # else:
    #     print(f"Folder exists")

    # subsetting simple
    SIENA_subset.subset(path, subset_path, shp_extension, ras_extension)

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
