import fiona
import rasterio
import rasterio.mask
from rasterio.mask import mask


def subs(shp_list, shp_names, raster_list, raster_names, ras_extension, outpath_subsets):
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

                        ras_path = f"{outpath_subsets}{raster_names[j]}{shp_names[i]}{ras_extension[1:]}"

                        with rasterio.open(ras_path, "w", **out_meta) as dest:
                            dest.write(out_image)

    # number of created subsets
    subset_count = (i + 1) * (j + 1)
    if len(shp_list) * len(raster_list) == subset_count:
        print(f"Done. \n{subset_count} subsets created")
