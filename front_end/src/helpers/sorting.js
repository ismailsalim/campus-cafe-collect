function distance (lat1,lon1,lat2,lon2) {
    let R = 6371; // km (change this constant to get miles)
    let dLat = (lat2-lat1) * Math.PI / 180;
    let dLon = (lon2-lon1) * Math.PI / 180;
    let a = Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(lat1 * Math.PI / 180 ) * Math.cos(lat2 * Math.PI / 180 ) *
      Math.sin(dLon/2) * Math.sin(dLon/2);
    let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    let d = R * c;
    // if (d>1) return Math.round(d)+"km";
    // else if (d<=1) return Math.round(d*1000)+"m";
    return d;
}


export function sort_by(venues, metric, data) {
  let sortedVenues = [...venues]

  if (metric == "price_low") {
    sortedVenues.sort(function(a, b) {
      return Number.parseInt(a.pricerank) - Number.parseInt(b.pricerank)
    })

  }

  if (metric == "price_high") {
    sortedVenues.sort(function(a, b) {
      return Number.parseInt(b.pricerank) - Number.parseInt(a.pricerank)
    })
  }

  if (metric == "distance") {
    sortedVenues.sort(function(a, b) {
      return Math.abs(distance(a.latitude, a.longitude, data.latitude, data.longitude)) - Math.abs(distance(b.latitude, b.longitude, data.latitude, data.longitude))
    })
  }

  return sortedVenues;
};


