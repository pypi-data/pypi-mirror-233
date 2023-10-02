#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 09:03:34 2022

@author: jbrajkovic
"""

import numpy as np
import matplotlib.pyplot as plt
import commontools as ct
from mpl_toolkits.basemap import Basemap
import netCDF4 as nc
import xarray as xr
import matplotlib as mpl
import pandas as pd



def openfile(fileloc,col):
    f=open(fileloc,mode='r')
    V=[]
    for line in f:
            lines=line.strip()
            columns=lines.split()
            V=np.append(V,float(columns[col]))
    return(V)

def openfileh(fileloc,col):
    f=open(fileloc,mode='r')
    V=[]
    r=0
    for line in f:
        if r>0:
            lines=line.strip()
            columns=lines.split()
            V=np.append(V,float(columns[col]))
        r=r+1
    return(V)    

def isbis(year):
    if((year%4==0 and year%100!=0)or(year%4==0 and year%400==0 and year%100==0)):
        t=1
    else:
        t=0
    return(t)

def seasonalmeans(fileloc,col,start_year,end_year,mod,season):
    years=openfile(fileloc,0)
    var=openfile(fileloc,col)
    T=[]
    # T=np.zeros(end_year-start_year+1)


    for y in range(start_year,end_year+1):   
        beg_summer=np.array([173,173,170]);end_summer=np.array([264,264,259])
        beg_falls=end_summer+1;end_falls=np.array([355,355,359])
        beg_winter=end_falls+1;end_winter=np.array([80,80,69])
        beg_spring=end_winter+1;end_spring=beg_summer-1
        end_year=np.array([365,365,360]) 
        
        if(isbis(y)==1 and mod==0):
            beg_summer=beg_summer+1;end_summer=end_summer+1
            beg_falls=beg_falls+1;end_falls=end_falls+1
            beg_winter=beg_winter+1;end_winter=end_winter+1
            beg_spring=beg_spring+1;end_spring=beg_summer-1
            end_year=end_year+1  
        # ind=y-start_year                      
        if season=="Summer":                        
            MASK=years==y
            T=np.append(T,np.mean(var[MASK][beg_summer[mod]-1:end_summer[mod]-1]))
            # T[ind]=np.mean(var[MASK][beg_summer[mod]-1:end_summer[mod]-1])
        elif season=="Falls":
            MASK=years==y
            T=np.append(T,np.mean(var[MASK][beg_falls[mod]-1:end_falls[mod]-1])) 
            # T[ind]=np.mean(var[MASK][beg_falls[mod]-1:end_falls[mod]-1])
        elif season=="Winter":
            MASK1=years==y;MASK2=years==y+1
            V1=var[MASK1][beg_winter[mod]-1:end_year[mod]-1];V2=var[MASK2][0:end_winter[mod]-1]
            V=np.append(V1,V2)
            T=np.append(T,np.mean(V))
            # T[ind]=np.mean(V)
        elif season=="Spring":
            MASK=years==y
            T=np.append(T,np.mean(var[MASK][beg_spring[mod]-1:end_spring[mod]-1]))
            # T[ind]=np.mean(var[MASK][beg_spring[mod]-1:end_spring[mod]-1])
        elif season=="year":
            MASK=years==y
            T=np.append(T,np.mean(var[MASK][0:end_year[mod]-1])) 
            # T[ind]=np.mean(var[MASK][0:end_year[mod]-1])
    return(T)

def slidingmeans(TS,interval):
    int2=int((interval-1)/2)
    s=np.size(TS)
    newTS=np.zeros(s)
    for i in range(0,s):
        if i<int2:
            newTS[i]=np.mean(TS[0:i+int2])
        elif i>(s-int2-1):
            newTS[i]=np.mean(TS[i-int2:s-1])
        else:
            newTS[i]=np.mean(TS[i-int2:i+int2])
    return(newTS)

            
def RGPD(vec,shape,scale,pu,teta,th):
    r=th+(scale/shape)*((vec*pu*teta)**shape-1) 
    return (r)
   
def CIGPD(vec,shape,scale,pu,teta,th,varsc,varsh,cov):
    T1=(((vec*pu*teta)**shape-1)/shape)**2*varsc
    T2=((scale*(-(vec*teta*pu)**shape+shape*(vec*teta*pu)**shape*np.log(vec*teta*pu)+1)/shape**2))**2*varsh
    T3=2*(((vec*pu*teta)**shape-1)/shape)*\
        ((scale*(-(vec*teta*pu)**shape+shape*(vec*teta*pu)**shape*np.log(vec*teta*pu)+1)/shape**2))*cov
    CI=np.sqrt(T1+T2+T3)*1.645
    return(CI)
            
def map_belgium(ax,lons,lats):
    
    m = Basemap(width=55000,height=50000,
                rsphere=(649328.00,665262.0),\
                area_thresh=1000.,projection='lcc',\
                lat_1=49.83,lat_2=51.17,lat_0=np.mean(lats),lon_0=np.mean(lons),resolution='h')
    m.drawcountries()
    m.drawcoastlines()
    return(m)

def map_belgium_zoom(ax,lons,lats):
    
    m = Basemap(width=35000,height=28000,
                rsphere=(649328.00,665262.0),\
                area_thresh=1000.,projection='lcc',\
                lat_1=49.83,lat_2=51.17,lat_0=np.mean(lats),lon_0=np.mean(lons)-0.35,resolution='h')
    m.drawcountries()
    m.drawcoastlines()
    return(m)


def JJ2date(day,year):
    end_month=[31,28,31,30,31,30,31,31,30,31,30,31]
    end_monthcum=np.zeros(12);end_monthcum[0]=end_month[0]
    monthlab=np.arange(1,13,1)
    jj=0;m=0
    if (ct.isbis(year)==1):end_month[1]=29
    else:end_month=[31,28,31,30,31,30,31,31,30,31,30,31]

    for i in range(1,12):
        end_monthcum[i]=end_monthcum[i-1]+end_month[i]
        
    for i in range(0,12):
        if i > 0:
            if (day<=end_monthcum[i] and day>end_monthcum[i-1]):
                m=monthlab[i]
                jj=day-end_monthcum[i-1]
        else:
            if (day<=end_monthcum[i] and day>0):
                m=monthlab[i]
                jj=day
        
    date=np.array([jj,m,year]);date.astype(int)
    return(date)

def date2JJ(day,month,year):
    day=int(day);month=int(month);year=int(year)
    end_month=[31,28,31,30,31,30,31,31,30,31,30,31]
    if (ct.isbis(year)==1):end_month[1]=29
    
    JJ=0
    for i in range(0,month-1):
        JJ=JJ+end_month[i]
    JJ=JJ+day
    return(JJ)
    
        

def Diverging_bounds(M,step):
    M1=np.array(M)
    mask=pd.isna(M)
    M1[mask]=0.
    if (np.min(M1)*-1>np.max(M1)) or (np.max(M1)<=0.) :
        vmax=np.min(M1)*-1+(step-(np.min(M1)*-1)%step)      
    else :
        vmax=np.max(M1)+(step-(np.max(M1))%step)  
    bounds = np.arange(-1*vmax,vmax+step,step)
    return(bounds)

def makebounds(M,step):
    M1=np.array(M)
    mask=pd.isna(M)
    M1[mask]=0.   
    vmax=np.max(M1)
    vmin=int(np.min(M1[M1>0.]))
    print(vmin,vmax,step)
    bounds = np.arange(float(vmin),vmax+step,step)
    return(bounds)
    