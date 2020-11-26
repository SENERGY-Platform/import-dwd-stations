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

from typing import Dict

from lib.station.Station import Station


def get_message(station: Station, quality_level: int, pressure: float, temperature_2m: float, temperature_5cm: float,
                rel_humidity_2m: float, dew_point_2m: float) -> Dict:
    return {
        "pressure": pressure,
        "temperature_2m": temperature_2m,
        "temperature_5cm": temperature_5cm,
        "rel_humidity_2m": rel_humidity_2m,
        "dew_point_2m": dew_point_2m,
        "meta": {
            "quality_level": quality_level,  # See https://www.dwd.de/DE/leistungen/klimadatendeutschland/qualitaetsniveau.html
            "name": station.name,
            "id": station.station_id,
            "lat": station.lat,
            "long": station.long,
            "pressure_unit": "hpa",
            "temperature_2m_unit": "°C",
            "temperature_5cm_unit": "°C",
            "rel_humidity_2m_unit": "%",
            "dew_point_2m_unit": "°C",
        }
    }
