$(document).ready( function () {

		var Picker = new KellyColorPicker({
		        place : 'picker',
		        size : 150,
		        input : 'color',
		}).addUserEvent("change", function(self){
			var id = $('#IotColourId').val();
			console.log("CHANGE" + id);
			wss_client.send('rooms/' + id + '/ColourChange',JSON.stringify(self.getCurColorRgb()),1,false);
	});
	function UpdateFillModal(Id,roomName,DeviceName,LightDevice){
		if (Id <= 0){
			$('#fillModal .modal-title').html("Add room");
			$('#IotId').parent().hide();
			$('#saveIot').html("Add");
		}else{
			$('#fillModal .modal-title').html("Update Room Info");
			$('#IotId').parent().show();
			$('#saveIot').html("Save chanages");
		}
		$('#IotId').val(Id);
		$('#roomName').val(roomName);
		$('#IotDeviceName').val(DeviceName);
		$('#IoTLightDevice').val(LightDevice);
	}

    var table = $('#roomsTable').DataTable({
		'oLanguage': {
            'sEmptyTable': 'Loading.  Please wait...',
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
        'aoColumns': [
            {
				'bSearchable': false,
                'mData':'Id'
			},
            {
				'bSearchable': true,
                'mData':'RoomName'
			},
            {
				'bSearchable': true,
				'mData':'IotDeviceName'
			},  {
		'bSearchable': true,
		'mData':'IoTLightDevice'
	},
            {
                'bSearchable': false,
                'bSortable': false,
				'mData': null,
				'defaultContent':
				'<a class="btn btn-primary btnUpdate">Update <i class="fa fa-refresh" aria-hidden="true"></i></a>' +
				' <a class="btn btn-primary btnRemove">Remove <i class="fa fa-trash" aria-hidden="true"></i></a>' +
				' <a class="btn btn-primary btnSwitch">Switch On the lights <i class="fa fa-power-off" aria-hidden="true"></i></a>' +
				' <a class="btn btn-primary btnColour">Change Colour</a>'
            }
        ],
		ajax: {
			url: '/api/getRooms',
			dataSrc: ''
		}
	}).on('draw',function(){
		var datas = table.ajax.json();
		$(".btnUpdate").click(function(){
			var data = datas[$(this).parent().parent().index()];
			UpdateFillModal(data.Id,data.RoomName,data.IotDeviceName,data.IoTLightDevice);
			$('#fillModal').modal('show');
		});
		$(".btnRemove").click(function(){
			var data = datas[$(this).parent().parent().index()];
			$('#IotRemoveId').val(data.Id);
			$('#roomNameR').val(data.RoomName);
			$('#IotDeviceNameR').val(data.IotDeviceName);
			$('#IoTLightDeviceR').val(data.IoTLightDevice);
			$('#confirmModal').modal('show');
		});
		$(".btnSwitch").click(function(){
			var data = datas[$(this).parent().parent().index()];
			var IsOn = $(this).text().indexOf("On") >= 0 ? "1" : "0";
			$icon = $(this).children("i");
			wss_client.send('rooms/' + data.Id + '/LightSwitch',IsOn,1,false);
			$(this).text(IsOn == "1" ? "Switch Off the lights " : "Switch On the lights ");
			$(this).append($icon);
		});
		$(".btnColour").click(function(){
				var data = datas[$(this).parent().parent().index()];
					$('#IotColourId').val(data.Id);
			$('#colourModal').modal('show');

		});
	});
	$("#roomsTable_filter label input").addClass("form-control").attr("placeholder", "Search rooms...");
	$("#btnAdd").click(function(e){
		UpdateFillModal(0,"","","");
		$('#fillModal').modal('show');
	});
	$("#saveIot").click(function(e){
		var IsAdd = $(this).html().indexOf("Add") >= 0;
		var fd = new FormData(document.getElementById("iotForm"));
		$.ajax({
			type:"POST",
			url: IsAdd ? "/api/addRoom" : "/api/updateRoom",
			data: fd,
			processData: false,
			contentType: false,
			success: function(data){
				table.ajax.reload();
				$('#fillModal').modal('hide');
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				alert("Error: " + XMLHttpRequest.responseText);
			}
		});
	});
	$("#removeIoT").click(function(e){
		var fd = new FormData(document.getElementById("iotRemoveForm"));
		$.ajax({
			type:"POST",
			url:"/api/removeRoom",
			data: fd,
			processData: false,
			contentType: false,
			success: function(data){
				table.ajax.reload();
				$('#confirmModal').modal('hide');
			}
		});
	});
});
