#!/usr/bin/python3
#    MovieGo
#    Copyright (C) 2017  Charlie J Smotherman
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
import unittest
import movietime as MT

MovTestPathPrefix = "/home/pi/taz/Videos/Movies"
TVTestPathPrefix = "/home/pi/taz/Videos/TVShows"
PicPath = "/nfs/home/charlie/Pictures"

MovieTestPath = "/".join((MovTestPathPrefix, 
    "Action/Some Made Up Movie (2018).mp4"))
DiscoveryTestPath = "/".join((TVTestPathPrefix, 
    "Discovery/S1/Star Trek Discovery S01E01 The Volcan Hello.mkv"))
EnterpriseTestPath = "/".join((TVTestPathPrefix, 
    "Enterprise/S1/Star Trek ENT S01E01 Broken Bow.mkv"))
OrvilleTestPath = "/".join((TVTestPathPrefix, 
    "Orville/S1/The Orville S01E01 Old Wounds.mkv"))
STTVTestPath = "/".join((TVTestPathPrefix, 
    "STTV/S1/Star Trek STTV S01E01 The Cage.mp4"))
TheLastShipTestPath = "/".join((TVTestPathPrefix, 
    "TheLastShip/S1/The Last Ship S01E01 Phase Six.mp4"))
VoyagerTestPath = "/".join((TVTestPathPrefix, 
    "Voyager/S1/Star Trek Voyager S01E01 Caretaker.mkv"))
TNGTestPath =  "/".join((TVTestPathPrefix, 
    "TNG/S1/Star Trek TNG S01E01 Encounter at Farpoint.mkv"))

MF = MT.MyFile(MovieTestPath)

class TestMyFile(unittest.TestCase):
    def test_media(self):
        self.assertEqual(MF.media, "/".join((MovTestPathPrefix,
            "Action/Some Made Up Movie (2018).mp4")))
    
    def test_parts(self):
        self.assertEqual(len(MF.parts), 8)
    
    def test_parent(self):
        self.assertEqual(str(MF.parent), "/home/pi/taz/Videos/Movies/Action")
    
    def test_name(self):
        self.assertEqual(str(MF.name), "Some Made Up Movie")
    
    def test_name_and_year(self):
        self.assertEqual(str(MF.name_and_year), "Some Made Up Movie (2018)")
    
    def test_year(self):
        self.assertEqual(str(MF.year), "2018")
 
    def test_search_path(self):
        self.assertEqual(str(MF.search_path), "/home/pi/taz/Videos/Movies/Action/Some Made Up Movie (2018)")
    
    def test_jpg_search_path(self):
        self.assertEqual(str(MF.jpg_search_path), "/home/pi/taz/Videos/Movies/Action/Some Made Up Movie (2018).jpg")
    
    def test_png_search_path(self):
        self.assertEqual(str(MF.png_search_path), "/home/pi/taz/Videos/Movies/Action/Some Made Up Movie (2018).png")

    def test_picfolder(self):
        self.assertEqual(str(MF.picfolder), "/".join((MT.PICPATH, MF.name_and_year)))

    def test_picfolder_jpg_search_path(self):
        self.assertEqual(str(MF.picfolder_jpg_search_path), ".".join((MF.picfolder, "jpg")))
    
    def test_picfolder_png_search_path(self):
        self.assertEqual(str(MF.picfolder_png_search_path), ".".join((MF.picfolder, "png")))

    def test_save_location(self):
        path = "/".join(("/home/pi/MovieTime2/static/images/thumbnails", MF.name_and_year))
        self.assertEqual(str(MF.save_location), path)
    
    def test_id(self):
        self.assertEqual(len(MF.id), 32)

    def test_voyager(self):
        MyF = MT.MyFile(VoyagerTestPath)
        self.assertEqual(MyF.name, "Caretaker")
        self.assertEqual(MyF.season, "01")
        self.assertEqual(MyF.episode, "01")
        
    def test_STTV(self):
        MyF = MT.MyFile(STTVTestPath)
        self.assertEqual(MyF.name, "The Cage")
        self.assertEqual(MyF.season, "01")
        self.assertEqual(MyF.episode, "01")

    def test_Enterprise(self):
        MyF = MT.MyFile(EnterpriseTestPath)
        self.assertEqual(MyF.name, "Broken Bow")
        self.assertEqual(MyF.season, "01")
        self.assertEqual(MyF.episode, "01")
        
    def test_TNG(self):
        MyF = MT.MyFile(TNGTestPath)
        self.assertEqual(MyF.name, "Encounter at Farpoint")
        self.assertEqual(MyF.season, "01")
        self.assertEqual(MyF.episode, "01")
        
    def test_Discovery(self):
        MyF = MT.MyFile(DiscoveryTestPath)
        self.assertEqual(MyF.name, "The Volcan Hello")
        self.assertEqual(MyF.season, "01")
        self.assertEqual(MyF.episode, "01")
        
    def test_Orville(self):
        MyF = MT.MyFile(OrvilleTestPath)
        self.assertEqual(MyF.name, "Old Wounds")
        self.assertEqual(MyF.season, "01")
        self.assertEqual(MyF.episode, "01")
        
    def test_TheLastShip(self):
        MyF = MT.MyFile(TheLastShipTestPath)
        self.assertEqual(MyF.name, "Phase Six")
        self.assertEqual(MyF.season, "01")
        self.assertEqual(MyF.episode, "01")
