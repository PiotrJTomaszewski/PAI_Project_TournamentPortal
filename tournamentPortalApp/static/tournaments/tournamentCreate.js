var eventLocationMap;
var selectedLocation = undefined;
$(document).ready(() => {
  eventLocationMap = L.map("event-map-id");
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>',
  }).addTo(eventLocationMap);
  L.control.scale().addTo(eventLocationMap);

  $("#id_event_start_date").datetimepicker({
    format: 'Y-m-d H:i',
    minDateTime: (Date.now())
  });
  $("#id_entry_deadline").datetimepicker({
    format: 'Y-m-d H:i',
    minDateTime: (Date.now()),
    onShow: function(ct){
      this.setOptions({
        maxDateTime: $("#id_event_start_date").val() ? $("#id_event_start_date").val(): false
      })
    }
  });
  $("#id_event_end_date").datetimepicker({
    format: 'Y-m-d H:i',
    minDate: (Date.now()),
    onShow: function(ct){
      this.setOptions({
        minDateTime: $("#id_event_start_date").val() ? $("#id_event_start_date").val(): false
      })
    }
  });
  $(`<div><span id="id_description_counter">${$("#id_description").val().length}</span>/${$("#id_description").attr('maxlength')} characters</div>`).insertAfter("#id_description")
  $(`<div><span id="id_prizes_counter">${$("#id_prizes").val().length}</span>/${$("#id_prizes").attr('maxlength')} characters</div>`).insertAfter("#id_prizes")
  eventLocationMap.on('click', (event)=>{
    L.popup().setLatLng(event.latlng).setContent('Event location').openOn(eventLocationMap);
    selectedLocation = event.latlng;
  })
});

$("#id_description").on('input', () => {
  $("#id_description_counter").text($("#id_description").val().length);
})
$("#id_prizes").on('input', () => {
  $("#id_prizes_counter").text($("#id_prizes").val().length);
})

showMapModal = () => {
  const lat = $("#id_location_lat").val();
  const lng = $("#id_location_long").val();
  setTimeout(()=>{
    eventLocationMap.invalidateSize();
    if (!isNaN(lat) && !isNaN(lng) && lat !== '' && lng !== '') {
      eventLocationMap.setView([lat, lng], 13);
    } else {
      eventLocationMap.setView([52.4035, -1063.050], 13);
    }
  }, 500);
  $("#id-map-modal").modal('show');
}

$("#id_location_lat").dblclick((showMapModal));
$("#id_location_long").dblclick(showMapModal);

$("#event-map-confirm-btn-id").click(() =>{
  if (selectedLocation !== undefined) {
    $("#id_location_lat").val(selectedLocation.lat.toFixed(5))
    $("#id_location_long").val(selectedLocation.lng.toFixed(5));
    $("#id-map-modal").modal('hide');
  }
})