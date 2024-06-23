# LoRa Range Tester
- Run `yarn install` and `yarn run start`, or push this repository to a Dokku instance
- Set up a LoRa sender to ping a LoRa receiver every 5000ms
- Set up the LoRa receiver to `POST` to `https://<url>/lora-ping` (no body), where `<url>` is the base URL of the server deployment
- Open a browser to `https://<url>/` on a smartphone and allow position access
- Walk around the LoRa sender and the smartphone (keep the browser page open)
- When done, retrieve the `datalog*.csv` file which is created at the root of this repository
- Run `python export_kml.py /path/to/datalog.csv /path/to/output.kml <base_station_lat> <base_station_lon>` to export a report in a KML format compatible with the [Swisstopo map](https://map.geo.admin.ch/). 

For a sender/receiver example, see https://github.com/SilasBerger/cipherlock/tree/experiment/range-test.
