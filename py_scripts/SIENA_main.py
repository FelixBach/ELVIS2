from py_scripts import SIENA_createsubset, SIENA_data_import, SIENA_field_indices, \
    SIENA_pix_based_indices, SIENA_date_based_subsets, SIENA_subset
from datetime import datetime
import os

start_time = datetime.now()


def main():
    ######################################
    # input path
    # path like "C:/your_path/data/"
    path = "C:/SIENA/data/"  # input path, store .shp and raster in the same input folder

    # specify extensions
    shp_extension = '*.shp'
    ras_extension = '*.tif'
    csv_extension = '*.csv'

    ######################################

    folder_subsets = "subsets/"
    folder_csv_files = "csv/"
    folder_pixel_res = "pixel_res/"

    # SIENA_subset.subset(path, folder_subsets, shp_extension, ras_extension)

    # SIENA_field_indices.field_based(path, folder_subsets, folder_csv_files, ras_extension, shp_extension, csv_extension)

    SIENA_pix_based_indices.pixel_based(path, folder_pixel_res, folder_subsets, folder_pixel_res, ras_extension)

    end_time = datetime.now()
    print("end-time = ", end_time - start_time, "Hr:min:sec")


# main func
if __name__ == '__main__':
    main()
