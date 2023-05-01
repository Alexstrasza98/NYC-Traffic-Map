const map = tt.map({
    key: 'rTlCip82FgfXSuRLNRYHA5183Wl4mXzZ',
    container: "map",
    center: [-73.9712, 40.7831],
    zoom: 15,
})

map.addControl(new tt.FullscreenControl());
map.addControl(new tt.NavigationControl());

async function loadJSON(filename) {
    const response = await fetch(filename);
    return await response.json();
}

function handleTrafficData(trafficData, id) {
    const coordinates = trafficData.coordinates.map(coordinate => [coordinate.longitude, coordinate.latitude]);
    drawLine(id, coordinates, getCongestionColor(trafficData.congestion_level), 5);
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
        return 'blue';
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
            return 'Road Works';
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

    new tt.Marker({element: markerElement, anchor: 'bottom'})
        .setLngLat(position)
        .setPopup(popup)
        .addTo(map);
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

map.on('load', function() {
    fetchAndUpdateTrafficData();
    fetchAndHandleIncidentData();
});
setInterval(fetchAndUpdateTrafficData, 300000);