const map = tt.map({
    key: 'rTlCip82FgfXSuRLNRYHA5183Wl4mXzZ',
    container: "map",
    center: [-73.9712, 40.7831],
    zoom: 15,
})

function getTrafficData(point, callback) {
  const url = `https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key=rTlCip82FgfXSuRLNRYHA5183Wl4mXzZ&point=${point}`;
  fetch(url)
    .then(response => response.json())
    .then(data => callback(data))
    .catch(error => console.error('Error fetching traffic data:', error));
}

function handleTrafficData(trafficData) {
  const rawcoordinates = trafficData.flowSegmentData.coordinates.coordinate;
  const coordinates = rawcoordinates.map(coordinate => [coordinate.longitude, coordinate.latitude]);
  drawLine('traffic', coordinates, getSpeedColor(trafficData.flowSegmentData.currentSpeed), 5);
}

function getSpeedColor(speedUnits) {
  if (speedUnits < 10) return 'red';
  if (speedUnits < 20) return 'orange';
  if (speedUnits < 30) return 'yellow';
  return 'green';
}

function drawLine(id, coordinates, color, width) {
      if (map.getLayer(id)) {
          map.removeLayer(id);
          map.removeSource(id);
      }

      const lineData = {
          type: 'Feature',
          properties: {
              color: color
          },
          geometry: {
              type: 'LineString',
              coordinates: coordinates
          }
      };

      map.addSource(id, {
          type: 'geojson',
          data: lineData
      });


      var layerProperties = {
          id: id,
          type: 'line',
          source: id,
          paint: {
              'line-width': width,
              'line-color': ['get', 'color']
          }
      };

      map.addLayer(layerProperties);
  }

const point = '40.7831,-73.9712';

function fetchAndUpdateTrafficData() {
  getTrafficData(point, handleTrafficData);
}
map.on('load', function() {
    fetchAndUpdateTrafficData();
    new tt.Marker().setLngLat([-73.9712, 40.7831]).addTo(map)
});
setInterval(fetchAndUpdateTrafficData, 300000);