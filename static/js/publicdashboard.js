$(document).ready(function() {
  $("#cardIDbtn").click(function(e) {
    var formdata = new FormData();
    formdata.append("cardID", $("#cardID").val());
    $.ajax({
      type: "POST",
      url: "/api/setCardID",
      data: formdata,
      processData: false,
      contentType: false,
      success: function(data) {
        $("#cardIdWrapper").hide();
        new Noty({
          type: 'success',
          layout: 'topCenter',
          closeWith: ['click'],
          timeout: 1500,
          text: "Successfully added your Card ID!",
          animation: {
            open: 'animated bounceInRight',
            close: 'animated bounceOutRight'
          },
        }).show();
      },
      error: function(xhr, error) {
        new Noty({
          type: 'error',
          layout: 'topCenter',
          modal: true,
          closeWith: ['click'],
          timeout: 1500,
          text: xhr.responseText,
          animation: {
            open: 'animated bounceInRight',
            close: 'animated bounceOutRight'
          },
        }).show();
      }
    });
    e.preventDefault();
  });
  loadAccessRequestTable();
  loadAccessRightsTable();
  initRooms();
});

function initRooms() {
  setInterval(function() {
    d = new Date();
    $(".room").each(function(index) {
      var imageSrc = `https://s3-us-west-2.amazonaws.com/iotsmartroom/snapshot/${index+1}.png?` + d.getTime();
      $(this).find(".liveImage").attr("src", imageSrc);
      retrieveRoomValues(index+1, $(this));
    });
  }, 2000)
}

function retrieveRoomValues(roomID, room) {
  $.ajax({
    type: "GET",
    url: "/api/LatestEnviroInfo/" + roomID,
		dataType: "json",
    success: function(data) {
      console.log(data);
      if (data != null) {
        room.find('.caption').find(".time").text("Last Updated: " + data.time);
        room.find('.caption').find(".light").text("Light: " + data.light);
        room.find('.caption').find(".humidity").text("Humidity: " + data.humidity + "%");
        room.find('.caption').find(".temp").text("Temperature: " + data.temp + "°C");
      }
    },
    error: function(xhr, error) {
      console.log(xhr.responseText);
    }
  });
}

function loadAccessRightsTable() {
  var table = $('#accessRightsTable').DataTable({
    "ajax": {
      "url": "/api/getUserAccessRights",
      "dataType": "json",
      "dataSrc": "",
      "contentType": "application/json",
    },
    "columns": [{
        "data": "RoomName"
      }
    ],
    "order": [
      [ 0, "desc"]
    ]
  });

  setInterval(function() {
    table.ajax.reload();
  }, 3000);
}

function loadAccessRequestTable() {
  var table = $('#requestTable').DataTable({
    "ajax": {
      "url": "/api/getUserAccessRequests",
      "dataType": "json",
      "dataSrc": "",
      "contentType": "application/json",
    },
    "columns": [{
        "data": "RoomName"
      },
      {
        "data": "DateRequested"
      },
      {
        "data": "IsApproved",
        "render": function(data, type, row) {
          return (data == 0) ? '<span class="red">Rejected</span>' :
            (data == 1) ? '<span class="green">Approved</span>' : '<span class="orange">Pending</span>';
        }
      }
    ],
    "order": [
      [ 2, 'asc' ],
      [ 0, "desc"]
    ]
  });

  $("#requestFormBtn").click(function(e) {
    var formdata = new FormData();
    var roomName = $("#room option:selected").text();
    formdata.append("roomID", $("#room").val());
    $.ajax({
      type: "POST",
      url: "/api/requestNewAccess",
      data: formdata,
      processData: false,
      contentType: false,
      success: function(data) {
        new Noty({
          type: 'success',
          layout: 'topCenter',
          closeWith: ['click'],
          timeout: 1500,
          text: `Successfully requested access for ${roomName}!`,
          animation: {
            open: 'animated bounceInRight',
            close: 'animated bounceOutRight'
          },
        }).show();
        $('#myModal').modal('hide');
      },
      error: function(xhr, error) {
        new Noty({
          type: 'error',
          layout: 'topCenter',
          modal: true,
          closeWith: ['click'],
          timeout: 1500,
          text: xhr.responseText,
          animation: {
            open: 'animated bounceInRight',
            close: 'animated bounceOutRight'
          },
        }).show();
      }
    });
    e.preventDefault();
    table.ajax.reload();
  });

  setInterval(function() {
    table.ajax.reload();
  }, 3000);
}
