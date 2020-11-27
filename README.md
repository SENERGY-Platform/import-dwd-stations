# import-dwd-stations

Allows you to import data from DWD weather stations with a 10-minute resolution. If configured in that way, historic and recent data will be imported first.
Afterwards, the latest data will be imported every 30 minutes.

## Outputs
*Outputs may contain the value -999 to indicate invalid or missing data.*
* pressure (float): barometric pressure at station height
* temperature_2m (float): temperature in 2 m height
* temperature_5cm (float): temperature in 5 cm height
* rel_humidity_2m (float): relative humidity in 2 m height
* dew_point_2m (float): dew point in 2 m height
* meta (Object): 
  + quality_level (int): DWD quality level, see [explanation](https://www.dwd.de/DE/leistungen/klimadatendeutschland/qualitaetsniveau.html)
  + name (string): station name
  + id (string): station id
  + lat (float): station latitude
  + long (float): station longitude
  + height (float): station height
  + pressure_unit (string): Unit of pressure measurement (hpa)
  + temperature_2m_unit (string): Unit of temperature_2m_unit measurement (°C)
  + temperature_5cm_unit (string): Unit of temperature_5cm_unit measurement (°C)
  + rel_humidity_2m_unit (string): Unit of rel_humidity_2m_unit measurement (%)
  + dew_point_2m_unit (string): Unit of dew_point_2m_unit measurement (°C)

## Configs
 * BBOXES (List): You can chain multiple bounding boxes to import multiple areas of interest. Make sure to choose these big enough to include at least one DWD station!
   You may use a tool like [this](http://bboxfinder.com/#51.294988,12.319794,51.370066,12.456779) to simplify the creation of these boxes.
   A map of all DWD stations is available [here](https://www.dwd.de/DE/leistungen/klimadatendeutschland/mnetzkarten/messnetz_tu.pdf?__blob=publicationFile&v=12).
   If not set, data of all stations will be imported. No default value available.
   +  Element (List of 4 floats): a bounding box in epsg 4326 projection, for example [12.178688,51.247304,12.572479,51.439885] covers parts of Leipzig.
 * HISTORIC (bool): If true, all available historic data will be imported. Default: false
 * RECENT (bool): If true, all recent data, will be imported. Default: false
