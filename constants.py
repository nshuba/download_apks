#!/usr/bin/python

#  This file is part of NoMoATS <http://athinagroup.eng.uci.edu/projects/nomoads/>.
#  Copyright (C) 2019 Anastasia Shuba.
#
#  NoMoATS is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  NoMoATS is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with NoMoATS.  If not, see <http://www.gnu.org/licenses/>.

class Constants(object):
    # Keys for app data/columns in our csv file
    key_pkg_name = 'docid'
    key_app_name = 'title'
    key_developer = 'creator'
    key_category = 'category'
    key_rating = 'starRating'
    key_num_rat = 'ratingsCount'
    key_num_down = 'numDownloads'