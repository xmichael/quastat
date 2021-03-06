# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 14:29:09 2012

@author: polaris
"""
import pylab
import sys
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.colors as cl


def ra2theta(ra):
    """ Convert Right Ascention to Θ

    :param Array d: Declination as array[3] in degrees,mins,seconds
    :return: Returns float Θ
    """
    theta = (ra[0] + ra[1] / 60.0 + ra[2] / 3600.0) * 180.0 / 12.0
    return theta


def d2phi(d):
    """ Convert Declination to Φ

    :param Array d: Declination as array[3] of Hours, Minutes, Seconds
    :return: Returns float Φ
    """
    if d[0] >= 0:
        phi = d[0] + d[1] / 60.0 + d[2] / 3600.0
    elif d[0] < 0:
        phi = d[0] - d[1] / 60.0 - d[2] / 3600.0
    else:
        print("d2phi conversion error")
        sys.exit(1)
    return phi


def parse(fname):
    """ Parse Verocat CSV file and return a list of arrays as
    [names..], [Ras...], [Ds...], [Zs..], [Lons..], [Lats..], [Φs..], [Θs..]
    """
    (names, ras, ds, zs, lons, lats, fis, thetas) = (
        [], [], [], [], [], [], [], [])
    linenum = 0
    with open(fname) as f:
        try:
            # skip header
            [f.readline() for i in range(5)]
            linenum = 5
            while True:
                linenum = linenum + 1
                line = f.readline()
                if (line == ""):  # EOF
                    break
                l = line.split("|")
                # sanity checks
                # some redshifts are optional! Ignore empty ones
                if l[4].strip() == "":
                    continue
                # parse -- strip spaces and convert to floats
                names.append(l[1].strip())
                ra = [float(x) for x in l[2].strip().split(" ")]
                d = [float(x) for x in l[3].strip().split(" ")]
                ras.append(ra)
                ds.append(d)

                # My calculation of RAs and Ds to degrees φ,θ:
                thetas.append(ra2theta(ra))
                fis.append(d2phi(d))

                zs.append(float(l[4]))
                lons.append(float(l[5]))
                lats.append(float(l[6]))
        except Exception as e:
            print("Parse Error -- ", e.message)
            print("Cuprit line was at ", str(linenum), " -- ", str(l))
        return (names, ras, ds, zs, lons, lats, fis, thetas)


def scatterplot(x, y, xlabel, ylabel, outfile, cvar=None):
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
    pylab.xlim([min(x), max(x)])
    pylab.ylim([min(y), max(y)])
    if cvar is not None:
        # there is a 3rd color variable (Normally Redshift)
        cmap = cl.LinearSegmentedColormap.from_list("BlRd", ["blue", "red"])
        # cmap =  pylab.cm.get_cmap('RdBu')
        norm = pylab.Normalize(min(cvar), max(cvar))
        pylab.scatter(x, y, marker='.', c=cvar, norm=norm, cmap=cmap)
        # create the colorbar
        mappable = pylab.cm.ScalarMappable(norm, cmap)
        mappable.set_array(cvar)
        cb = pylab.colorbar(mappable)
        cb.set_label('Redshift')
    else:
        pylab.scatter(x, y, marker='.', s=0.001)
    pylab.savefig(outfile, dpi=(600))
    # pylab.show()
    pylab.close()


def scat3d(x, y, z, xtitle, ytitle, ztitle, outfile):
    fig = pylab.figure()
    ax = p3.Axes3D(fig)
    ax.scatter(x, y, z, marker='.', s=1)
    # ax.bar(x,y,z)
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)
    ax.set_zlabel(ztitle)
    pylab.savefig(outfile, dpi=(200))
    pylab.close()


def hist(data, bins, xlabel, ylabel, outfile):
    pylab.hist(data, bins)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
    pylab.savefig(outfile, dpi=(200))
    pylab.close()


def downsample(x, y, z, size):
    """ e.g.  subsample(phis,thetas, 15000)
    """
    data = np.core.records.fromarrays([x, y, z])
    np.random.shuffle(data)
    # print(repr(data["f0"][:10]))

    return (data["f0"][:size], data["f1"][:size], data["f2"][:size])


def error_margin(a, b, m):
    if (abs(a - b) < m):
        return True
    return False


def print_row(data, i):
    """Print ith 0-based index of data"""
    for col in data:
        print(col[i], end=' ')
    print()


def find_opposite(data):
    """ assumes all columns in data[col1,col2..] have equal length
        :return: subset of data
    """
    # import ipdb
    # ipdb.set_trace()
    n = len(data[0])
    print("Total is: ", n)
    for i in range(n):
        if((i % 100) == 0):
            print(i)
        for j in range(n):
            phi_1 = data[6][i]
            theta_1 = data[7][i]
            z_1 = data[3][i]
            phi_2 = data[6][j]
            theta_2 = data[7][j]
            z_2 = data[3][j]
            if error_margin(phi_1, -phi_2, 0.1) and \
                error_margin(theta_1, 180 + theta_2, 0.1) and \
                    error_margin(z_1, z_2, 0.1):
                print_row(data, i)
                print_row(data, j)
                print()


def main():
    (names, ras, ds, zs, lons, lats, fis, thetas) = data =\
        parse("./data/quasars.all.csv")

    find_opposite(data)
    sys.exit(0)

    scatterplot(lons, lats, "Longitude", "Latitude",
                './images/astroLatLon.png')
    scatterplot(thetas, fis, "Theta", "Phi",
                './images/PhiTheta.png')
    hist(zs, 5000, "Redshift", "Quasars", "./images/Zhist.png")

    # assert names,ras... have same len()
    for i in (names, ras, ds, zs, lons, lats, fis, thetas):
        print("First fields: %s" % repr(i[0]))
        print("len of field: %d" % len(i))

    # downsample:
    # xy = downample(thetas, phi2, 10000)
    # scatterplot(xy[0], xy[1],"Theta","Phi", './images/PhiTheta_sample.png')

    # 3D lat,lon,Z
    scat3d(thetas, fis, zs, "Theta", "Phi", "Z", './images/ThetaPhiZ_3d.png')

    # color with Z me random downsample 15000 giati alliws kalyptoun ta panta
    # kai den ksexwrizeis tipota
    (x, y, z) = downsample(thetas, fis, zs, 15000)
    scatterplot(x, y, "Theta", "Phi",
                './images/PhiThetaKafrilaColor.png', cvar=z)


if __name__ == "__main__":
    main()
