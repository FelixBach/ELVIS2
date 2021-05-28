import os
import glob
import fiona
import rasterio
import rasterio.mask
from rasterio.mask import mask


def subset(path, subset_path, shp_extension, ras_extension):
    shp_list = []
    for shp in glob.glob(os.path.join(path, shp_extension)):
        shp_list.append(shp)
    shp_list = [w.replace('\\', '/') for w in shp_list]
    shp_names = [str("_") + w[len(path):-(len(shp_extension) - 1)] for w in shp_list]

    raster_list = []
    for ras in glob.glob(os.path.join(path, ras_extension)):
        raster_list.append(ras)
    raster_list = [w.replace('\\', '/') for w in raster_list]
    raster_names = [w[len(path):-(len(ras_extension) - 1)] for w in raster_list]

    if len(raster_list) == 1:
        print(str(len(raster_list)) + str(" raster-file found"))
    else:
        print(str(len(raster_list)) + str(" raster-files found \n "))

    if len(shp_list) == 1:
        print(str(len(shp_list)) + str(" .shp-file found") + str("\n"))
    else:
        print(str(len(shp_list)) + str(" .shp-files found") + str("\n"))

    if not os.path.isdir(subset_path):
        os.makedirs(subset_path)
    else:
        print(f"Folder exists")

    for i, shp in enumerate(shp_list):
        with fiona.open(shp, "r") as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]

            for j, ras in enumerate(raster_list):
                for scene in raster_list:
                    with rasterio.open(ras, "r") as src:
                        out_image, out_transform = mask(src, shapes, crop=True)
                        out_meta = src.meta

                        out_meta.update({"driver": "GTiff",
                                         "height": out_image.shape[1],
                                         "width": out_image.shape[2],
                                         "transform": out_transform})

                        ras_path = f"{subset_path}{raster_names[j]}{shp_names[i]}{ras_extension[1:]}"

                        with rasterio.open(ras_path, "w", **out_meta) as dest:
                            dest.write(out_image)
                        # print(f"Processing")

    # number of created subsets
    subset_count = (i + 1) * (j + 1)
    if len(shp_list) * len(raster_list) == subset_count:
        print(f"Done. \n{subset_count} subsets created")
