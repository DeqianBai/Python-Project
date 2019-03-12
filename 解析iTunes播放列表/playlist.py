#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/3/12

"""
playlist.py
Description: Playing with iTunes Playlists.
Author: Mahesh Venkitachalam
Website: electronut.in
"""

import re, argparse
import sys
from matplotlib import pyplot
import plistlib
import numpy as np


# 1.3.3 查找多个播放列表中的共同音轨
def findCommonTracks(fileNames):
    # a list of sets of track names
    trackNameSets=[]
    for fileName in fileNames:
        # creat  a new sets
        trackNames=set()
        # read in playlist
        plist=plistlib.readPlist(fileName)
        # get the tracks
        tracks=plist['Tracks']
        # iterate through the tracks
        for trackId,track in tracks.items():
            try:
                # add the track name to a set
                trackNames.add(track['Name'])
            except:
                # ignore
                pass

        # add to list
        trackNameSets.append(trackNames)

    # get set of common tracks
    commonTracks =set.intersection(*trackNameSets)
    # write to file
    if len(commonTracks)>0:
        f=open("common.txt",'wb')
        for val in commonTracks:
            s="%s\n"%val
            f.write(s.encode("UTF-8"))

        f.close()
        print("%d common tracks found."
              "Track names written to common.txt"%len(commonTracks))
    else:
        print("No common tracks!")


def plotStats(fileName):
    """
    Plot some statistics by readin track information from playlist.
    """
    # read in playlist
    plist=plistlib.readPlist(fileName)
    # get the tracks from the playlist
    tracks=plist['Tracks']
    # creat lists of song ratings and track durations
    ratings=[]
    durations=[]
    # iterate through the tracks
    for trackId,track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            # ignore
            pass

    # ensure that valid data was collected
    if ratings==[]or durations==[]:
        print("No valid Album Rating/Total Time data in %s."% fileName)
        return

    # cross plot
    x=np.array(durations,np.int32)
    # convent to minutes
    x=x/60000.0
    y=np.array(ratings,np.int32)
    pyplot.subplot(2,1,1)
    pyplot.plot(x,y,'o')
    pyplot.axis([0,1.05*np.max(x),-1,110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    # plot histogram
    pyplot.subplot(2,1,2)
    pyplot.hist(x,bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    # show plot
    pyplot.show()



# 1.3.1 查找重复
# 使用findDuplicates()方法查找重复的曲目
def findDuplicates(fileName):
    print('Finding duplicate tracks in %s...'% fileName)
    # read in a list
    plist=plistlib.readPlist(fileName)
    # get the tracks from the Tracks dictionary
    tracks=plist['Tracks']
    # create a track name dictionary
    trackNames={}
    # iterate through the tracks
    for trackId, track in tracks.items():
        try:
            name=track['Name']
            duration=track['Total Time']
            # look for existing entrise
            if name in trackNames:
                # if a name and duration match,increment the coumt
                #  round the track length to the nearest second
                if duration//1000==trackNames[name][0]//1000:
                    count=trackNames[name][1]
                    trackNames[name]=(duration,count+1)
            else:
                # add dictionary entry as tuple(duration,count)
                trackNames[name]=(duration,1)

        except:
            # ignore
            pass

    # 1.3.2 提取重复
    # store duplicates as (name,count) tuples
    dups=[]
    for k,v in trackNames.items():
        if v[1]>1:
            dups.append((v[1],k))

    # save dups to file
    if len(dups)>0:
        print("Found %d duplicates. Track names saved to dup.txt"%len(dups))

    else:
        print("No duplicate tracks found!")

    f=open("dups.txt","w")
    for val in dups:
        f.write("[%d %s\n" % (val[0],val[1]))
    f.close()


def main():
    # create parser
    descStr="""
    This program analyzes playlist files (.xml) exported from iTunes."""

    parser=argparse.ArgumentParser(description=descStr)
    # add a mutually exclusive group of arguments
    group=parser.add_mutually_exclusive_group()

    # add expected arguments
    group.add_argument('--common',nargs='*',dest='plFiles',required=False)
    group.add_argument('--stats',dest='plFile',required=False)
    group.add_argument('--dup',dest='plFileD',required=False)


    # parse args
    args=parser.parse_args()

    if args.plFiles:
        # find common tracks
        findCommonTracks(args.plFiles)
    elif args.plFile:
        # plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        # find duplicate tracks
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for.")


# main method
if __name__=='__main__':
    main()

