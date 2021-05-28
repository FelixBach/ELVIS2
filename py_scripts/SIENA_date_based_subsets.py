from os.path import join
import glob
import fiona
import rasterio
import rasterio.mask
# import pandas as pd


def date_subset(inpath, outpath_date_based_subsets, csv_list, shp_list, raster_list, csv_extension, ras_extension,
         shp_extension):

    # search for csv files from the inpath and cut them
    for file in glob.glob(join(inpath, csv_extension)):
        csv_list.append(file)
    csv_list = [w.replace('\\', '/') for w in csv_list]

    # searching .shp-files
    for shp in glob.glob(join(inpath, shp_extension)):
        shp_list.append(shp)
    shp_list = [w.replace('\\', '/') for w in shp_list]
    shp_names = [str("_") + w[len(inpath):-len(shp_extension) + 1] for w in shp_list]

    # number of .shp-files
    if len(shp_list) == 1:
        print(str(len(shp_list)) + str(" .shp-file found") + str("\n"))
    else:
        print(str(len(shp_list)) + str(" .shp-files found") + str("\n"))

    # searching raster files
    for ras in glob.glob(join(inpath, ras_extension)):
        raster_list.append(ras)
    raster_list = [w.replace('\\', '/') for w in raster_list]

    # number of raster-files
    if len(raster_list) == 1:
        print(str(len(raster_list)) + str(" raster-file found"))
    else:
        print(str(len(raster_list)) + str(" raster-files found \n "))

    # search for raster dates
    raster_list_dates = []

    for ras in glob.glob(join(inpath, ras_extension)):
        raster_list_dates.append(ras)

    raster_list_dates = [w.replace('\\', '/') for w in raster_list_dates]
    raster_dates = [w[len(inpath):-18] for w in raster_list_dates]

    # Use glob module to return all csv files under root directory. Create DF.
    files = pd.DataFrame([file for file in glob.glob(join(inpath, csv_extension))], columns=["fullpath"])

    # Split the full path into directory and filename
    files_split = files['fullpath'].str.rsplit("\\", 1, expand=True).rename(columns={0: 'path', 1: 'filename'})

    # Join these into one DataFrame
    files = files.join(files_split)

    # Iterate over unique filenames; read CSVs, concat DFs, save file
    i_shp = 0

    for f in files['filename'].unique():
        paths = files[files['filename'] == f]['fullpath']  # Get list of fullpaths from unique filenames
        dfs = [pd.read_csv(path, decimal='.', index_col=False) for path in
               paths]  # Get list of dataframes from CSV file paths
        concat_df = pd.concat(dfs)  # Concat dataframes into one
        compare_dates_df = concat_df  # saving original date and time in a csv file
        compare_dates_df.to_csv(str(outpath_date_based_subsets) + str("/") + str("date_") + str(f), index=False,
                                header=False)
        concat_df.replace(to_replace=[":", '\.', '-'],
                          value="", regex=True, inplace=True)
        concat_df.replace(to_replace=" ",
                          value="T", regex=True, inplace=True)
        temp = pd.DataFrame(raster_dates, columns=["date"])
        compare_df = temp.merge(concat_df, how='inner', indicator=False)
        compare_df_names = pd.DataFrame.copy(compare_df)
        compare_df['date'] = str(inpath) + compare_df['date'].astype(str) + str("_resamp_subset.tif")
        compare_df.to_csv(str(outpath_date_based_subsets) + str("/") + str(f), index=False,
                          header=False)  # Save dataframe
        print(len(compare_df), "matches between your", len(raster_dates), "input-tifs and the", len(concat_df),
              "cloudfree-dates for the dataset", str(f),
              "were found.\nYou can find the resulting .csv-file for each FID in your outpath.\n")
        print(f)

        '''
        # iterate over .shp-files
        with fiona.open(shp_list[i_shp], "r") as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]
            i_ras = 0  # iterate over raster files
            while i_ras < len(compare_df):
                for scene in compare_df:
                    compare_list = compare_df.values.tolist()  # write dataframe values to list
                    compare_list = [item for items in compare_list for item in items]  # flatten the list
                    compare_list_names = compare_df_names.values.tolist()
                    compare_list_names = [item for items in compare_list_names for item in items]
                    with rasterio.open(compare_list[i_ras], "r") as src:
                        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                        out_meta = src.meta

                        out_meta.update({"driver": "GTiff",
                                         "height": out_image.shape[1],
                                         "width": out_image.shape[2],
                                         "transform": out_transform})

                        with rasterio.open(str(outpath_date_based_subsets) + str(compare_list_names[i_ras]) +
                                           str(shp_names[i_shp]) + str(ras_extension[1:]), "w", **out_meta) as dest:
                            dest.write(out_image)
                        if i_ras == 1:
                            print(i_ras, "Image created.")
                        else:
                            print(i_ras, "Images created.")
                        i_ras = i_ras + 1
        i_shp = i_shp + 1

        # number of created subsets
        subset_count = i_shp * i_ras
        if len(shp_list) * len(compare_list_names) == subset_count:
            print(str("Done. \n ") + str(subset_count) + str(" subsets created"))
        '''
