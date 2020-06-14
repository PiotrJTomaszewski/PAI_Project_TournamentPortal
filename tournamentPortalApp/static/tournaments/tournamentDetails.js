
function fill_results_table(matches) {
  var html = ""
  for (round=0; round<matches.length; round++) {
    if (matches[round] === undefined) continue;
    var title;
    switch(round) {
      case 0: title = 'Winner'; break;
      case 1: title = 'Final'; break;
      case 2: title = 'Semifinals'; break;
      case 3: title = 'Quarterfinals'; break;
      case 4: title = 'Eighth-finals'; break;
      case 5: title = '16th-finals'; break;
      case 6: title = '32nd-finals'; break;
      case 7: title = '64th-finals'; break;
      default: title = 'Round ' + round; break;
    }
    html += `<table class="table"><thead><tr><th colspan="3">${title}</th></tr></thead><tbody>`
    matches[round].forEach(pair=> {
      html += "<tr>"
      for (i=0; i<2; i++) {
        if (pair.participants[i]) {
          if (pair.winner === i) {
            html += '<td class="winner">'
          } else {
            html += "<td>"
          }
          html += `<img src="${pair.participants[i].gravatar}" class="rounded gravatar"/> ${pair.participants[i].first_name} ${pair.participants[i].last_name}</td>`
        } else {
          html += '<td></td>'
        }
      }
    })
    html += "</tbody></table>"
  }
   

  
  var div = $("#matches-results").html(html)
}

function get_matches() {
  const tournament_uuid = $("#participants-js-data").data('tournamentUuid');
  const url = `${tournament_uuid}/matches/json`;
  $.getJSON(url, (result) => {
    var matches = []
    result.forEach(element => {
      if (matches[element.tournament_round] === undefined) {
        matches[element.tournament_round] = []
      }
      var participants = []
      if (element.participant_zero__user__first_name) {
        participants[0] = {
          'first_name': element.participant_zero__user__first_name,
          'last_name': element.participant_zero__user__last_name,
          'gravatar': element.participant_zero__user__gravatar,
        }
      } else {
        participants[0] = null
      }
      if (element.participant_one__user__first_name) {
        participants[1] = {
          'first_name': element.participant_one__user__first_name,
          'last_name': element.participant_one__user__last_name,
          'gravatar': element.participant_one__user__gravatar
        }
      } else {
        participants[1] = null
      }
      matches[element.tournament_round][element.pair_no] = {
        winner: element.winner,
        participants: participants
      }
      if (matches.length > 0) {
        $("#bracketShowBtn").show();
        fill_results_table(matches);
      }
    });
    console.log(matches)
    const svg = $("#tournament-bracket-id");
    var bracket = new TournamentBracket(matches);
    svg.width(bracket.svgWidth).height(bracket.svgHeight).html(bracket.svgHtml);
  })
}

function setup_map() {
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
}

$(document).ready(() => {
    get_matches();
    setup_map();
  })
