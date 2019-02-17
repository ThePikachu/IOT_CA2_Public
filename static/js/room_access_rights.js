$(document).ready(function() {
  function UpdateFillModal(Id, UserId, RoomId) {
    if (Id <= 0) {
      $('#fillModal .modal-title').html("Add Access Rights");
      $('#Id').parent().hide();
      $('#saveAccessRight').html("Add");
    } else {
      $('#fillModal .modal-title').html("Update Access Rights");
      $('#Id').parent().show();
      $('#saveAccessRight').html("Save chanages");
    }
    $('#Id').val(Id);
    $('#UserSelect').val(UserId);
    $('#RoomSelect').val(RoomId);
  }

  var table = $('#AccessRightsTable').DataTable({
    'oLanguage': {
      'sEmptyTable': 'No Data',
      'sLengthMenu': '<div class="row item_to_show"><div class="col-md-7 col-sm-12">Items to show:</div>' +
        '<div class="col-md-5 col-sm-12"><select class="form-control">' +
        '<option value="5">5</option>' +
        '<option value="10">10</option>' +
        '<option value="20" selected="selected">20</option>' +
        '<option value="25">25</option>' +
        '<option value="50">50</option>' +
        '<option value="100">100</option>' +
        '<option value="250">250</option>' +
        '</select></div></div>',
      "sSearch": ''
    },
    'iDisplayLength': 20,
    'sPaginationType': 'full_numbers',
    'aoColumns': [{
      'bSearchable': false,
      'mData': 'Id'
    }, {
      'bSearchable': true,
      'mData': 'Username'
    }, {
      'bSearchable': true,
      'mData': 'RoomName'
    }, {
      'bSearchable': false,
      'bSortable': false,
      'mData': null,
      'defaultContent': '<a class="btn btn-primary btnUpdate">Update <i class="fa fa-refresh" aria-hidden="true"></i></a>' +
        ' <a class="btn btn-primary btnRemove">Remove <i class="fa fa-trash" aria-hidden="true"></i></i></a>'
    }],
    ajax: {
      url: '/api/getAccessRights',
      dataSrc: ''
    }
  }).on('draw', function() {
    var datas = table.ajax.json();
    $(".btnUpdate").click(function() {
      var data = datas[$(this).parent().parent().index()];
      UpdateFillModal(data.Id, data.UserId, data.RoomId);
      $('#fillModal').modal('show');
    });
    $(".btnRemove").click(function() {
      var data = datas[$(this).parent().parent().index()];
      $('#ACRemoveId').val(data.Id);
      $('#UsernameR').val(data.Username);
      $('#RoomNameR').val(data.RoomName);
      $('#confirmModal').modal('show');
    });
  });
  $("#AccessRightsTable_filter label input").addClass("form-control").attr("placeholder", "Search...");
  $("#btnAdd").click(function(e) {
    UpdateFillModal(0, "", "", "");
    $('#fillModal').modal('show');
  });
  $("#saveAccessRight").click(function(e) {
    var IsAdd = $(this).html().indexOf("Add") >= 0;
    var fd = new FormData(document.getElementById("accessRightForm"));
    $.ajax({
      type: "POST",
      url: IsAdd ? "/api/addAccessRight" : "/api/updateAccessRight",
      data: fd,
      processData: false,
      contentType: false,
      success: function(data) {
        table.ajax.reload();
        $('#fillModal').modal('hide');
      },
      error: function(xhr, error) {
        alert(xhr.responseText)
      }
    });
  });
  $("#removeAccessRight").click(function(e) {
    var fd = new FormData(document.getElementById("ACRemoveForm"));
    $.ajax({
      type: "POST",
      url: "/api/removeAccessRight",
      data: fd,
      processData: false,
      contentType: false,
      success: function(data) {
        table.ajax.reload();
        $('#confirmModal').modal('hide');
      }
    });
  });
});
