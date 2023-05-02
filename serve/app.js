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

function weatherIcon(weatherType) {
    switch (weatherType) {
        case "Clouds":
            return '02';
        case "Clear":
            return '01';
        case "Snow":
            return '13';
        case "Rain":
            return '10';
        case "Thunderstorm":
            return '11';
        case "Mist":
            return '50';
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

    document.querySelector('#showroadclosed').addEventListener('change', function(event) {
        if (type === 8) {
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

    document.querySelector('#showroadworking').addEventListener('change', function(event) {
        if (type === 9) {
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

    document.querySelector('#showother').addEventListener('change', function(event) {
        if (type !== 6 && type !== 8 && type != 9) {
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
    //const trafficDataArray = await loadJSONWithGlob('../data/congestion/congestion');
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

async function fetchAndDisplayWeatherData() {
    const weatherData = await loadJSON('../data/weather/weather_result/part-00000-bb54208c-627c-4d2e-a859-7416dbb955a7-c000.json');

    const averageTempElement = document.querySelector('#averagetemp');
    averageTempElement.innerHTML = `Temperature:<br>${parseFloat(weatherData.average_temp.toFixed(2))}`;

    const averageHumidityElement = document.querySelector('#averagehumidity');
    averageHumidityElement.innerHTML = `Humidity:<br>${parseFloat(weatherData.average_humidity.toFixed(2))}`;

    const averageRain = document.querySelector('#averagerain');
    averageRain.innerHTML = `Rain:<br>${parseFloat(weatherData.average_rain.toFixed(2))}`;

    const averageVisibility = document.querySelector('#averagevisibility');
    averageVisibility.innerHTML = `Visibility:<br>${parseFloat(weatherData.average_visibility.toFixed(2))}`;

    const averageWindSpeed = document.querySelector('#averagewindspeed');
    averageWindSpeed.innerHTML = `Wind Speed:<br>${parseFloat(weatherData.average_wind_speed.toFixed(2))}`;

    const imageElement = document.querySelector('#dynamicImage');
    imageElement.src = `https://openweathermap.org/img/wn/${weatherIcon(weatherData.weather)}d@2x.png`;
}

async function fetchAndDisplayIncidentCount() {
    const incidentStatisticData = await loadCSV('../data/incident/incident_dist/part-00000-a8bbd320-854c-4abf-8c7d-615dfa4ca911-c000.csv');
    incidentStatisticData.sort((a, b) => a.incident_type - b.incident_type);

    let sum = incidentStatisticData.reduce((accumulator, currentRecord) => {
        return accumulator + currentRecord.count;
    }, 0);
    const incidentCountElement = document.querySelector('#totalincident');
    incidentCountElement.textContent = `Total Incidents: ${sum}`;

    const incidentTypes = incidentStatisticData.map(record => record.incident_type);
    const counts = incidentStatisticData.map(record => record.count);

    const ctx = document.getElementById('incidenthistogram').getContext('2d');
    const histogram = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: incidentTypes,
            datasets: [{
                label: 'Incident Count',
                data: counts,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

async function fetchAndDisplayCongestionStatistics() {
    const congestionStatisticData = await loadCSV('../data/congestion/congestion_dist/part-00000-f6472eb1-375b-456f-81dd-49c4c1400aa9-c000.csv');
    congestionStatisticData.sort((a, b) => a.congestion_level - b.congestion_level);
    const congestionLevels = congestionStatisticData.map(record => record.congestion_level);
    const counts = congestionStatisticData.map(record => record.count);

    const ctx = document.getElementById('congestionhistogram').getContext('2d');
    const histogram = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: congestionLevels,
            datasets: [{
                label: 'Congestion Level',
                data: counts,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

async function fetchAndDisplayAverageSpeed() {
    const averageSpeedData = await loadJSON('../data/congestion/average_speed_percent/part-00000-6a0918fb-a720-4fcd-832a-7070e04ae086-c000.json');
    const averageSpeed = averageSpeedData.average_speed_percent;

    const percentage = averageSpeed * 100;
    const remainingPercentage = 100 - percentage;

    const averageSpeedElement = document.querySelector('#averagespeeddata');
    averageSpeedElement.innerHTML = `Average Speed:${parseFloat(percentage.toFixed(2))}%`;

    const ctx = document.getElementById('percentage-chart').getContext('2d');
    const doughnutChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Percentage', 'Remaining'],
        datasets: [{
        data: [percentage, remainingPercentage],
        backgroundColor: ['rgba(75, 192, 192, 0.2)', '#E0E0E0'],
        borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        cutout: '80%'
    }
    });
}

map.on('load', function() {
    fetchAndUpdateTrafficData();
    fetchAndHandleIncidentData();
    fetchAndDisplayWeatherData();
    fetchAndDisplayIncidentCount();
    fetchAndDisplayCongestionStatistics();
    fetchAndDisplayAverageSpeed();
});
setInterval(fetchAndUpdateTrafficData, 300000);