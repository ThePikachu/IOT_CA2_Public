$(document).ready(function() {
  loadPendingAccessRequestTable();
  loadResolvedRequestTable();
});

function loadPendingAccessRequestTable() {
  var table = $('#pendingTable').DataTable({
    "ajax": {
      "url": "/api/getPendingRequests",
      "dataType": "json",
      "dataSrc": "",
      "contentType": "application/json",
    },
    "columns": [{
        "data": "Username"
      },
      {
        "data": "RoomName"
      },
      {
        "data": "DateRequested"
      },
      {
        "data": "IsApproved",
        "render": function(data, type, row) {
          return '<a class="btn btn-success btnApprove">Approve <i class="fa fa-refresh" aria-hidden="true"></i></a>' +
            ' <a class="btn btn-primary btnReject">Reject <i class="fa fa-trash" aria-hidden="true"></i></i></a>'
        }
      },
      {
        "data": "Id"
      }
    ],
    "order": [
      [2, "desc"]
    ],
    "columnDefs": [{
      "targets": [4],
      "visible": false,
      "searchable": false
    }]
  });

  $('#pendingTable').on('click', '.btnApprove', function() {
    var RowIndex = $(this).closest('tr');
    var requestID = table.row(RowIndex).data().Id;
    var formdata = new FormData();
    formdata.append("approval", 1);
    $.ajax({
      type: "POST",
      url: "/api/approveAccessRequest/" + requestID,
      data: formdata,
      processData: false,
      contentType: false,
      success: function(data) {
        new Noty({
          type: 'success',
          layout: 'topCenter',
          modal: true,
          closeWith: ['click'],
          timeout: 1500,
          text: "Successfully Approved Access Rights Request",
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
    table.ajax.reload();
  });

  $('#pendingTable').on('click', '.btnReject', function() {
    var RowIndex = $(this).closest('tr');
    var requestID = table.row(RowIndex).data().Id;
    var formdata = new FormData();
    formdata.append("approval", 0);
    $.ajax({
      type: "POST",
      url: "/api/approveAccessRequest/" + requestID,
      data: formdata,
      processData: false,
      contentType: false,
      success: function(data) {
        new Noty({
          type: 'success',
          layout: 'topCenter',
          modal: true,
          closeWith: ['click'],
          timeout: 1500,
          text: "Successfully Rejected Access Rights Request",
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
    table.ajax.reload();
  });

  setInterval(function() {
    table.ajax.reload();
  }, 3000);
}

function loadResolvedRequestTable() {
  var table = $('#resolvedTable').DataTable({
    "ajax": {
      "url": "/api/getCompletedRequests",
      "dataType": "json",
      "dataSrc": "",
      "contentType": "application/json",
    },
    "columns": [{
        "data": "Username"
      },
      {
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
      [2, "desc"]
    ]
  });

  setInterval(function() {
    table.ajax.reload();
  }, 3000);
}
