# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 14:29:09 2012

@author: polaris
"""
import pylab,sys
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.colors as cl

def parse(fname):
    """ Parse Verocat CSV file and return a list of arrays as [names..], [Ras...], [Ds...],
    [Zs..], [Lons..], [Lats..], [Φs..], [Θs..] """
    (names, ras,ds,zs,lons,lats, fis, thetas) = ([],[],[],[],[],[], [], [])
    linenum = 0
    with open(fname) as f:
        try:
            #skip header
            [ f.readline() for i in range(5)]
            linenum = 5
            while True:
                linenum = linenum + 1
                line = f.readline()
                if (line == ""):#EOF
                        break
                l = line.split("|")
                # sanity checks
                #some redshifts are optional! Ignore empty ones
                if l[4].strip() == "":
                    continue
                ## parse -- strip spaces and convert to floats
                names.append(l[1].strip())
                ra = [float(x) for x in l[2].strip().split(" ")] 
                d = [float(x) for x in l[3].strip().split(" ")]
                ras.append(ra)
                ds.append(d)
                
                ## My calculation of RAs and Ds to degrees φ,θ:
                thetas.append((ra[0] + ra[1]/60.0 + ra[2]/3600.0)*180.0/12.0)
                fis.append(d[0] + d[1]/60.0 + d[2]/3600.0)

                zs.append(float(l[4]))
                lons.append(float(l[5]))
                lats.append(float(l[6]))
        except Exception as e:
            print "Parse Error -- " + e.message
            print "Cuprit line was at " + `linenum` + " -- " + `l`
        return (names, ras,ds,zs,lons,lats,fis,thetas)
        
def scatterplot(x,y,xlabel,ylabel,outfile, cvar=None):
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
    pylab.xlim([min(x),max(x)])
    pylab.ylim([min(y),max(y)])
    if cvar!=None:
        #there is a 3rd color variable (Normally Redshift)        
        cmap = cl.LinearSegmentedColormap.from_list("BlRd",["blue","red"])
        #cmap =  pylab.cm.get_cmap('RdBu')    
        norm = pylab.Normalize(min(cvar),max(cvar))
        pylab.scatter(x,y,marker='.',c=cvar, norm=norm, cmap=cmap)
        # create the colorbar
        mappable = pylab.cm.ScalarMappable(norm, cmap)
        mappable.set_array(cvar)
        cb = pylab.colorbar(mappable)    
        cb.set_label('Redshift')
    else:    
        pylab.scatter(x,y,marker='.',s=0.001)
    pylab.savefig(outfile, dpi=(600))
#    pylab.show()     
    pylab.close()

def scat3d(x,y,z,xtitle,ytitle,ztitle,outfile):
    fig = pylab.figure()
    ax = p3.Axes3D(fig)
    ax.scatter(x,y,z,marker='.',s=1)
    #ax.bar(x,y,z)
    ax.set_xlabel(xtitle)
    ax.set_ylabel(ytitle)
    ax.set_zlabel(ztitle)
    pylab.savefig(outfile, dpi=(200))
    pylab.close()

def hist(data, bins,xlabel,ylabel, outfile):
    pylab.hist(data,bins)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
    pylab.savefig(outfile, dpi=(200))    
    pylab.close()

def downsample(x,y,z,size):
    """ e.g.  subsample(phis,thetas, 15000) 
    """
    data = np.core.records.fromarrays([x,y,z])
    np.random.shuffle(data)
    #print `data["f0"][:10]`
    
    return ( data["f0"][:size], data["f1"][:size], data["f2"][:size] )
    

if __name__ == "__main__":
    (names,ras,ds,zs,lons,lats, fis, thetas) =  parse("./data/quasars.all.csv")
    #assert names,ras... have same len()

    scatterplot(lons,lats,"Longitude","Latitude", './images/astroLatLon.png')
    scatterplot(thetas,fis,"Theta","Phi", './images/PhiTheta_xwrisProsimo.png')
    hist(zs,5000,"Redshift", "Quasars", "./images/Zhist.png")

    for i in (names,ras,ds,zs,lons,lats, fis, thetas):
        print "First fields: %s" %  `i[0]`
        print "len of field: %d" % len(i)

    # kafrocalculation
    phi2 = []
    for i in xrange (len(ds)):
        d = ds[i]
        if d[0] >= 0:
            phi = d[0] + d[1]/60.0 + d[2]/3600.0
        elif d[0] < 0:
            phi = d[0] - d[1]/60.0 - d[2]/3600.0
        else:
            print "ERROR"
            sys.exit(1)
        phi2.append(  phi )
    
    scatterplot(thetas, phi2,"Theta","Phi", './images/PhiThetaKafrila.png')

    #downsample:
    #xy = downample(thetas, phi2, 10000)
    #scatterplot(xy[0], xy[1],"Theta","Phi", './images/PhiThetaKafrila_sample.png')
    
    #3D lat,lon,Z
    scat3d(thetas,phi2,zs,"Theta","Phi","Z",'./images/ThetaPhiZ_3d.png')

    # color with Z me random downsample 15000 giati alliws kalyptoun ta panta kai den ksexwrizeis tipota
    (x,y,z) = downsample(thetas, phi2, zs, 15000)
    scatterplot(x,y,"Theta","Phi", './images/PhiThetaKafrilaColor.png',cvar=z)
