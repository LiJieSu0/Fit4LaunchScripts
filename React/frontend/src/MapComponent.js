import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default icon issue with Leaflet and Webpack
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

// Custom icons for different colors
const greenIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [20, 33],
  iconAnchor: [10, 33],
  popupAnchor: [1, -28],
  shadowSize: [33, 33]
});

const redCircleIcon = L.divIcon({
  className: 'red-circle-icon',
  html: '<div style="background-color: red; width: 12px; height: 12px; border-radius: 50%;"></div>',
  iconSize: [12, 12],
  iconAnchor: [6, 6],
  popupAnchor: [0, -6]
});

const blueCircleIcon = L.divIcon({
  className: 'blue-circle-icon',
  html: '<div style="background-color: blue; width: 12px; height: 12px; border-radius: 50%;"></div>',
  iconSize: [12, 12],
  iconAnchor: [6, 6],
  popupAnchor: [0, -6]
});

const MapComponent = ({ dutCoords, refCoords, baseStationCoords }) => {
  let validCoords = [baseStationCoords];
  if (dutCoords && dutCoords[0] !== null) {
    validCoords.push(dutCoords);
  }
  if (refCoords && refCoords[0] !== null) {
    validCoords.push(refCoords);
  }

  const centerLat = validCoords.reduce((sum, coords) => sum + coords[0], 0) / validCoords.length;
  const centerLon = validCoords.reduce((sum, coords) => sum + coords[1], 0) / validCoords.length;
  const center = [centerLat, centerLon];

  return (
    <div className="map-container" style={{ height: '500px', width: '500px', margin: '20px 0' }}>
      <MapContainer center={center} zoom={13} scrollWheelZoom={false} zoomControl={false} attributionControl={false} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution=""
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {dutCoords && dutCoords[0] !== null && (
          <Marker position={dutCoords} icon={redCircleIcon}>
            <Popup>Average DUT Location</Popup>
          </Marker>
        )}
        {refCoords && refCoords[0] !== null && (
          <Marker position={refCoords} icon={blueCircleIcon}>
            <Popup>Average REF Location</Popup>
          </Marker>
        )}
        <Marker position={baseStationCoords} icon={greenIcon}>
          <Popup>Base Station Location</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
};

export default MapComponent;
