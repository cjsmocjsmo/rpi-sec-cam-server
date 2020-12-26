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
from unittest.mock import patch
import movietime
MovieTestPath = "/home/pi/taz/Movies/Some Made Up Movie (2018).mp4"

TVShowTestPath = "/home/pi/taz/TVShows/Some Made Up Movie (2018).mp4"


PicPath = "/nfs/home/charlie/Pictures"

class TestFindMovieArt(unittest.TestCase):
    @patch('os.path.exists')
    def test_find_movie_art_true(self, mock_exists):
        MovieTestPathJPG = "/home/pi/taz/Movies/Some Made Up Movie (2018).jpg"
        MF = movietime.MyFile(MovieTestPath)
        mock_exists.return_value = True
        result = movietime.Thumbnails(MF.media).find_movie_art()
        self.assertEqual(MovieTestPathJPG, result)

    @patch('os.path.exists')
    def test_find_movie_art_false(self, mock_exists):
        MovieTestPathPNG = "/home/pi/taz/Movies/Some Made Up Movie (2018).png"
        MF = movietime.MyFile(MovieTestPath)
        NOART = "/home/pi/MovieTime/static/images/animals.jpg"
        mock_exists.return_value = False
        result = movietime.Thumbnails(MF.media).find_movie_art()
        self.assertEqual(NOART, result)

class TestFindTvshowArt(unittest.TestCase):
    @patch('os.path.exists')
    def test_find_tvshow_art_true(self, mock_exists):
        TVShowTestPathJPG = "/home/pi/taz/TVShows/Some Made Up Movie (2018).jpg"
        MF = movietime.MyFile(TVShowTestPath)
        mock_exists.return_value = True
        result = movietime.Thumbnails(MF.media).find_tvshow_art()
        self.assertEqual(TVShowTestPathJPG, result)

    @patch('os.path.exists')
    def test_find_tvshow_art_false(self, mock_exists):
        TVShowTestPathJPG = "/home/pi/taz/TVShows/Some Made Up Movie (2018).jpg"
        MF = movietime.MyFile(TVShowTestPath)
        mock_exists.return_value = False
        result = movietime.Thumbnails(MF.media).find_tvshow_art()
        self.assertNotEqual(TVShowTestPathJPG, result)
        pass          