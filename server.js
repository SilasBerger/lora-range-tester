const express = require('express');
const path = require('path');
const fs = require('fs');

const port = process.env.PORT ? parseInt(process.env.PORT) : 3000;

const app = express();
app.use(express.json());

const logFilename = `datalog_${Date.now()}.csv`;
fs.writeFile(logFilename, 'timeSinceLastPing;latitude;longitude;altitude;accuracy;altitudeAccuracy;heading;speed\n', {}, () => {});

let timestampLastPing = Date.now();

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '/index.html'));
});

app.post('/lora-ping', (req, res) => {
  console.log('✅ LoRa ping received');
  timestampLastPing = Date.now();
  res.status(204);
  res.send();
});

app.post('/coordinates', async (req, res) => {
  const coordinates = req.body;
  const timeSinceLastPing = Date.now() - timestampLastPing;
  const dataPoint = `${timeSinceLastPing};${coordinates.latitude};${coordinates.longitude};${coordinates.altitude};${coordinates.accuracy};${coordinates.altitudeAccuracy};${coordinates.heading};${coordinates.speed}`;
  console.log(dataPoint);
  fs.writeFile(logFilename, `${dataPoint}\n`, { flag: 'a+' }, err => {});
  res.status(200);
  res.send({timeSinceLastPing})
});

app.listen(port, () => {
  console.log(`🚀 Range tester listening on port ${port}!`);
});
