$(document).ready(() => {
    const mapDiv = document.getElementById("event-map-id");
    const eventName = mapDiv.dataset.name;
    const eventLocationLat = mapDiv.dataset.lat;
    const eventLocationLng = mapDiv.dataset.lng;
    var eventLocationMap = L.map("event-map-id").setView([eventLocationLat, eventLocationLng], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>',
    }).addTo(eventLocationMap);
    L.control.scale().addTo(eventLocationMap);
    L.marker({ lat: eventLocationLat, lon: eventLocationLng }).bindPopup(eventName).addTo(eventLocationMap);
  })

  const svg = $("#tournament-bracket-id");
  $(bracketShowBtn).click(() => {
    var content = $("#bracketContentId");
    var drawRegionArea = {
      width: content.width(),
      height: content.height() - 0.2 * content.height(),
    };
    var bracket = new TournamentBracket(null, null, drawRegionArea);
    svg.html(bracket.svgHtml);
  });