#  Copyright 2020 InfAI (CC SES)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import csv
from datetime import datetime
from typing import List, Callable, Optional

from import_lib.import_lib import ImportLib, get_logger

from lib.station.Ftploader import get_most_recent, get_recent, get_historical
from lib.station.Point import get_message
from lib.station.Station import Station

logger = get_logger(__name__)

QN, MESS_DATUM, PP_10, TT_10, TM5_10, RF_10, TD_10 = "QN", "MESS_DATUM", "PP_10", "TT_10", "TM5_10", "RF_10", "TD_10"
headers = [QN, MESS_DATUM, PP_10, TT_10, TM5_10, RF_10, TD_10]


class StationImport:
    def __init__(self, lib: ImportLib):
        self.__lib = lib

        self.__bboxes = self.__lib.get_config("BBOXES", None)
        if not isinstance(self.__bboxes, List):
            logger.error("Invalid config for BBOXES will not be used")
            self.__bboxes = None

    def import_today(self, stations: List[Station]):
        '''
        Import today's data for a List of stations

        :param stations: List of DWD Stations
        :return: None
        '''
        count = self.__import_with(stations, get_most_recent)
        logger.info("Imported " + str(count) + " most recent data points")

    def import_recent(self, stations: List[Station]):
        '''
        Import current years data for a List of stations
        :param stations: List of DWD stations
        :return: None
        '''
        count = self.__import_with(stations, get_recent)
        logger.info("Imported " + str(count) + " recent data points")

    def import_most_recent(self, stations: List[Station]):
        '''
        Import the last 3 values for a List of stations. New data is published every 30 minutes with a resolution of 10
        minutes, If you keep calling this method every 30 minutes, you'll receive all data.

        :param stations: List of DWD stations
        :return: None
        '''
        count = self.__import_with(stations, get_most_recent, 3)
        logger.info("Imported " + str(count) + " most recent data points")

    def import_historical(self, stations: List[Station]):
        '''
        Import all historic data for a List of stations. Depending on the number of stations,
        this might take a couple minutes.

        :param stations: List of DWD stations
        :return: None
        '''
        get_historical(stations, self.__import_csvs)

    def __import_with(self, stations: List[Station], function: Callable[[Station],
                                                                        Optional[List[csv.DictReader]]],
                      latest_n: int = None) -> int:
        counter = 0
        for station in stations:
            readers = function(station)
            if readers is None:
                continue
            for reader in readers:
                counter += self.__import_csv(station, reader, latest_n)
        return counter

    def __import_csvs(self, station: Station, readers: List[csv.DictReader]):
        for reader in readers:
            self.__import_csv(station, reader)

    def __import_csv(self, station: Station, reader: csv.DictReader, latest_n: int = None) -> int:
        counter = 0
        for field in headers:
            if field not in reader.fieldnames:
                logger.error("csv does not contain header " + field + " and will be ignored")
                return 0
        prepared_points = []
        for row in reader:
            try:
                date_time = datetime.strptime(row[MESS_DATUM], "%Y%m%d%H%M")
            except ValueError:
                logger.error("Could not parse datetime from csv. Format changed? Ignoring message")
                continue
            try:
                point = get_message(station, int(row[QN]), float(row[PP_10]), float(row[TT_10]), float(row[TM5_10]),
                                    float(row[RF_10]), float(row[TD_10]))
            except ValueError:
                logger.error("Could not parse point from csv. Format changed? Ignoring message")
                continue
            if latest_n is None:
                logger.debug(str(date_time) + ": " + str(point))
                self.__lib.put(date_time, point)
                counter += 1
            else:
                prepared_points.append((date_time, point))
        if latest_n is not None:
            prepared_points = prepared_points[len(prepared_points) - latest_n:]  # Cutting top is ok, values in order
            for date_time, point in prepared_points:
                logger.debug(str(date_time) + ": " + str(point))
                self.__lib.put(date_time, point)
                counter += 1
        return counter
