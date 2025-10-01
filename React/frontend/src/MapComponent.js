import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icon not showing
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

const MapComponent = () => {
  const base_station = [47.128234, -122.356792]; // Do not change the center
  

  const coordinates = {
    "DUT": {
      "last_mos_value_coords": {
        "latitude": "47.146212",
        "longitude": "-122.357310",
        "distance_to_base_station_km": 1.999446329912468
      },
      "voice_call_drop_coords": {
        "latitude": "47.147595",
        "longitude": "-122.357257",
        "distance_to_base_station_km": 2.153132266606282
      },
      "first_dl_tp_gt_1_coords": {
        "latitude": "47.144150",
        "longitude": "-122.357327",
        "distance_to_base_station_km": 1.7702410668954354
      },
      "first_ul_tp_gt_1_coords": {
        "latitude": "47.144150",
        "longitude": "-122.357327",
        "distance_to_base_station_km": 1.7702410668954354
      }
    },
    "REF": {
      "last_mos_value_coords": {
        "latitude": "47.150115",
        "longitude": "-122.357223",
        "distance_to_base_station_km": 2.433274574224882
      },
      "voice_call_drop_coords": {
        "latitude": "47.150115",
        "longitude": "-122.357223",
        "distance_to_base_station_km": 2.433274574224882
      },
      "first_dl_tp_gt_1_coords": {
        "latitude": "47.148357",
        "longitude": "-122.357232",
        "distance_to_base_station_km": 2.2378229982269593
      },
      "first_ul_tp_gt_1_coords": {
        "latitude": "47.143685",
        "longitude": "-122.357327",
        "distance_to_base_station_km": 1.718549348813673
      }
    }
  };

  const dutIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  const refIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  const baseStationIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  return (
    <MapContainer
      center={base_station} // Use the original center for the map view
      zoom={13}
      zoomControl={false}
      scrollWheelZoom={false}
      doubleClickZoom={false}
      dragging={false}
      touchZoom={false}
      boxZoom={false}
      style={{ height: '600px', width: '600px' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      />
      <Marker position={base_station} icon={baseStationIcon}>
        <Popup>
          <b>基站 (Base Station)</b><br />
          Latitude: {base_station[0]}<br />
          Longitude: {base_station[1]}
        </Popup>
      </Marker>
      {Object.entries(coordinates).map(([deviceType, deviceCoords]) => (
        Object.entries(deviceCoords).map(([coordType, coordData]) => {
          const position = [parseFloat(coordData.latitude), parseFloat(coordData.longitude)];
          const icon = deviceType === "DUT" ? dutIcon : refIcon;
          return (
            <Marker position={position} icon={icon} key={`${deviceType}-${coordType}`}>
              <Popup>
                <b>{deviceType} - {coordType.replace(/_/g, ' ')}</b><br />
                Latitude: {coordData.latitude}<br />
                Longitude: {coordData.longitude}<br />
                Distance to Base Station: {coordData.distance_to_base_station_km} km
              </Popup>
            </Marker>
          );
        })
      ))}
    </MapContainer>
  );
};

export default MapComponent;
