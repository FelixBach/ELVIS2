from os.path import join
import glob


def shp_files(inpath, shp_extension):
    shp_list = []
    # searching .shp-files
    for shp in glob.glob(join(inpath, shp_extension)):
        shp_list.append(shp)
    shp_list = [w.replace('\\', '/') for w in shp_list]

    return shp_list


def shp_names(inpath, shp_extension):
    shp_list = shp_files(inpath, shp_extension)
    shp_names = [str("_") + w[len(inpath):-(len(shp_extension) - 1)] for w in
                 shp_list]
    print(str("shape list: ") + str(shp_list))
    print(str("shp names: ") + str(shp_names))

    # number of .shp-files
    if len(shp_list) == 1:
        print(str(len(shp_list)) + str(" .shp-file found") + str("\n"))
    else:
        print(str(len(shp_list)) + str(" .shp-files found") + str("\n"))

    return shp_names


def raster_files(inpath, ras_extension):
    raster_list = []
    # searching raster files
    for ras in glob.glob(join(inpath, ras_extension)):
        raster_list.append(ras)
    raster_list = [w.replace('\\', '/') for w in raster_list]

    return raster_list


def raster_names(inpath, ras_extension):
    raster_list = raster_files(inpath, ras_extension)
    raster_names = [w[len(inpath):-(len(ras_extension) - 1)] for w in
                    raster_list]
    print(str("raster list: ") + str(raster_list))
    print(str("raster names: ") + str(raster_names))

    # number of raster-files
    if len(raster_list) == 1:
        print(str(len(raster_list)) + str(" raster-file found"))
    else:
        print(str(len(raster_list)) + str(" raster-files found \n "))

    return raster_names
