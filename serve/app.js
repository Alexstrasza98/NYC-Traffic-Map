const map = tt.map({
    key: 'rTlCip82FgfXSuRLNRYHA5183Wl4mXzZ',
    container: "map",
    center: [-73.9853279, 40.7552281],
    zoom: 13,
    style: `https://api.tomtom.com/style/1/style/22.2.1-9?key=rTlCip82FgfXSuRLNRYHA5183Wl4mXzZ&map=basic_night`
})

map.addControl(new tt.FullscreenControl());
map.addControl(new tt.NavigationControl());

new Foldable('.js-foldable', 'top-right');

async function loadJSON(filename) {
    const response = await fetch(filename);
    return await response.json();
}

async function loadCSV(filename) {
    const response = await fetch(filename);
    const data = await response.text();
    const rows = data.split('\n');

    const header = rows[0].split(',');
    const records = [];

    for (let i = 1; i < rows.length; i++) {
      const row = rows[i].split(',');
      const record = {};

      let hasMissingValues = false;

      for (let j = 0; j < row.length; j++) {
        if (row[j] === '') {
            hasMissingValues = true;
            break;
        }
        record[header[j]] = isNaN(row[j]) ? row[j] : Number(row[j]);
      }
      
      if (!hasMissingValues) {
        records.push(record);
      }
    }

    records.sort((a, b) => a.congestion_level - b.congestion_level);

    return records;
}

function handleTrafficData(trafficData, id) {
    const coordinates = trafficData.coordinates.map(coordinate => [coordinate.longitude, coordinate.latitude]);
    drawLine(id, coordinates, getCongestionColor(trafficData.congestion_level), 3);
}

function getCongestionColor(congestionLevel) {
    switch (congestionLevel) {
      case '1':
        return 'red';
      case '2':
        return 'orange';
      case '3':
        return 'yellow';
      case '4':
        return 'green';
      default:
        return '#999999';
    }
}

function getIncidentType(incidentType) {
    switch (incidentType) {
        case 0:
            return 'Unknown';
        case 1:
            return 'Accident';
        case 2:
            return 'Fog';
        case 3:
            return 'Dangerous Conditions';
        case 4:
            return 'Rain';
        case 5:
            return 'Ice';
        case 6:
            return 'Jam';
        case 7:
            return 'Lane Closed';
        case 8:
            return 'Road Closed';
        case 9:
            return 'Road Working';
        case 10:
            return 'Wind';
        case 11:
            return 'Flooding';
        case 12:
            return 'Cluster';
        case 13:
            return 'Broken Down Vehicle';
    }
}

function incidentColor(incidentType) {
    if (incidentType === 6) {
        return '#ff0000';
    } else if (incidentType === 9) {
        return '#33cc33';
    } else if (incidentType === 8) {
        return '#000000';
    } else {
        return '#999999';
    }
}

function incidentIcon(incidentType) {
    if (incidentType === 6) {
        return 'jam';
    } else if (incidentType === 9) {
        return 'road_work';
    } else if (incidentType === 8) {
        return 'closed';
    } else {
        return 'accident';
    }
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

      document.querySelector('#showredroads').addEventListener('change', function(event) {
        if (color === 'red') {
            if (event.target.checked) {
                map.setLayoutProperty(id, 'visibility', 'visible');
            } else {
                map.setLayoutProperty(id, 'visibility', 'none');
            }
        }
     });

     document.querySelector('#showorangeroads').addEventListener('change', function(event) {
        if (color === 'orange') {
            if (event.target.checked) {
                map.setLayoutProperty(id, 'visibility', 'visible');
            } else {
                map.setLayoutProperty(id, 'visibility', 'none');
            }
        }
     });

     document.querySelector('#showyellowroads').addEventListener('change', function(event) {
        if (color === 'yellow') {
            if (event.target.checked) {
                map.setLayoutProperty(id, 'visibility', 'visible');
            } else {
                map.setLayoutProperty(id, 'visibility', 'none');
            }
        }
     });

     document.querySelector('#showgreenroads').addEventListener('change', function(event) {
        if (color === 'green') {
            if (event.target.checked) {
                map.setLayoutProperty(id, 'visibility', 'visible');
            } else {
                map.setLayoutProperty(id, 'visibility', 'none');
            }
        }
     });
}

function createMarker(type, position, color, popupText) {
    var markerElement = document.createElement('div');
    markerElement.className = 'marker';

    var markerContentElement = document.createElement('div');
    markerContentElement.className = 'marker-content';
    markerContentElement.style.backgroundColor = color;
    markerElement.appendChild(markerContentElement);

    var iconElement = document.createElement('div');
    iconElement.className = 'marker-icon';
    let incident_icon = incidentIcon(type);
    iconElement.style.backgroundImage =
        'url(' + incident_icon + '.png)';
    markerContentElement.appendChild(iconElement);

    var popup = new tt.Popup({offset: 30}).setText(popupText);

    var marker = new tt.Marker({element: markerElement, anchor: 'bottom'})
        .setLngLat(position)
        .setPopup(popup)
        .addTo(map);
    
    document.querySelector('#showjam').addEventListener('change', function(event) {
        if (type === 6) {
            if (event.target.checked) {
                marker = new tt.Marker({element: markerElement, anchor: 'bottom'})
                    .setLngLat(position)
                    .setPopup(popup)
                    .addTo(map);
            } else {
                marker.remove();
            }
        }
    });
}

async function fetchAndUpdateTrafficData() {
    const trafficDataArray = await loadJSON('../data/traffic_data.json');
    trafficDataArray.forEach((trafficData, index) => {
      handleTrafficData(trafficData, `traffic-${index}`);
    });
}

async function fetchAndHandleIncidentData() {
    const incidentDataArray = await loadJSON('../data/incident_tomtom.json');
    incidentDataArray.forEach((incidentData) => {
        const coordinate = incidentData.coordinate;
        createMarker(incidentData.incident_type, coordinate, incidentColor(incidentData.incident_type), `Incident Type: ${getIncidentType(incidentData.incident_type)}`);
    });
}

async function fetchAndDisplayStatisticData() {
    const averageSpeedData = await loadJSON('../data/congestion/average_speed/part-00000-7dbbb57b-685b-4084-ac14-ce052498c8e9-c000.json');
    const averageSpeedElement = document.getElementById('average_speed');
    averageSpeedElement.textContent = `Average Speed: ${averageSpeedData.average_speed}`;

    const averageSpeedPercentData = await loadJSON('../data/congestion/average_speed_percent/part-00000-d7d0f35e-8dc9-4c4b-95c0-4ecf5250ee28-c000.json');
    const averageSpeedPercentElement = document.getElementById('average_speed_percent');
    averageSpeedPercentElement.textContent = `Average Speed Percent: ${averageSpeedPercentData.average_speed_percent}`;

    const congestionLevelData = await loadCSV('../data/congestion/congestion_dist/part-00000-c0e82443-7450-4cf6-806e-b8e0d1c09903-c000.csv');
    const congestionLevelElement = document.getElementById('tbody');
    congestionLevelData.forEach((congestionLevel) => {
        let row = document.createElement("tr");
        let cell1 = document.createElement("td");
        cell1.textContent = congestionLevel.congestion_level;
        row.appendChild(cell1);
        let cell2 = document.createElement("td");
        cell2.textContent = congestionLevel.count;
        row.appendChild(cell2);
        congestionLevelElement.appendChild(row);
    })
}

map.on('load', function() {
    fetchAndUpdateTrafficData();
    fetchAndHandleIncidentData();
    fetchAndDisplayStatisticData();
});
setInterval(fetchAndUpdateTrafficData, 300000);