
var DefaultoLanguage = {
	'sEmptyTable': 'No Data',
	'sLoadingRecords': 'Loading.  Please wait...',
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
};

var current_temp = []
var wss_client = null;
var RoomTempGraph = null;
var VRATable = null;
var IVRATable = null;
var MAHTable = null;

function DrawRoomTempsGraph() {
	if (RoomTempGraph != null) {
		RoomTempGraph.series[0].update({
			name: $('#RoomSelect option:selected').text(),
			data: current_temp
		}, true);
		return;
	}
	RoomTempGraph = Highcharts.chart('current_temp', {
		chart: {
			type: 'spline'
		},
		title: {
			text: 'Current temperature readings'
		},
		xAxis: {
			title: {
				text: 'time'
			},
			type: "category",
			labels: {
				formatter: function() {
					return new moment(this.value).format("h:mm:ss a");
				},
			}
		},
		yAxis: {
			title: {
				text: 'Temperature'
			}
		},
		legend: {
      align: 'center',
        verticalAlign: 'bottom',
        x: 0,
        y: 0
		},
		series: [{
			name: $('#RoomSelect option:selected').text(),
      data:current_temp
		}],
		responsive: {
			rules: [{
				condition: {
					maxWidth: 500
				},
				chartOptions: {
					legend: {
						layout: 'horizontal',
						align: 'center',
						verticalAlign: 'bottom'
					}
				}
			}]
		}
	});
}

function GrabAvgRoomTemps() {
	$.ajax({
		type: "GET",
		url: "/api/getAvgRoomTemps/" + $('#RoomSelect').val(),
		dataType: "json",
		success: function(data) {
			Highcharts.chart('avg_temp_history', {
				chart: {
					type: 'spline'
				},
				title: {
					text: 'Average temperature readings'
				},
				xAxis: {
					title: {
						text: 'time'
					},
					type: "category",
					labels: {
						formatter: function() {
							var time = new moment(this.value);

							return time.format("D MMM YYYY");
						},
					}
				},
				yAxis: {
					title: {
						text: 'Temperature'
					}
				},
				legend: {
          align: 'center',
        verticalAlign: 'bottom',
        x: 0,
        y: 0
				},
				series: [{
					name: data.RoomName,
					data: data.data
				}],
				responsive: {
					rules: [{
						condition: {
							maxWidth: 500
						},
						chartOptions: {
							legend: {
								layout: 'horizontal',
								align: 'center',
								verticalAlign: 'bottom'
							}
						}
					}]
				}
			});
		}
	});
}

function onDateTimeColumn(CurDateTime, data) {
	var time = new moment(data, "ddd, D MMM YYYY HH:mm:ss zz");
	if (CurDateTime.diff(time, 'hours') < 24)
		return time.fromNow();
	return time.format("ddd, D MMM YYYY HH:mm:ss");
}

function GetValidAccessLogs() {
	if (VRATable != null){
		VRATable.ajax.url('/api/getValidAccessLog/' + $('#RoomSelect').val()).load();
		return;
	}
	var CurDateTime = new moment();
	VRATable = $('#VRATable').DataTable({
		'oLanguage': DefaultoLanguage,
		'iDisplayLength': 5,
		'sPaginationType': 'full_numbers',
		'aoColumns': [{
				'bSearchable': true,
				'mData': 'RoomName'
			},
			{
				'bSearchable': true,
				'mData': 'Username'
			},
			{
				'bSearchable': true,
				'mData': 'Time',
				'mRender': function(data, type, full) {
					return onDateTimeColumn(CurDateTime, data);
				}
			},
			{
				'bSearchable': true,
				'mData': 'Exit_time',
				'mRender': function(data, type, full) {
					return onDateTimeColumn(CurDateTime, data);
				}
			}
		],
		ajax: {
			url: '/api/getValidAccessLog/' + $('#RoomSelect').val(),
			dataSrc: ''
		}
	})
	$("#VRATable_filter label input").addClass("form-control").attr("placeholder", "Search...");
}

function GetInvalidAccessLogs() {
	if (IVRATable != null){
		IVRATable.ajax.url('/api/getInvalidAccessLog/' + $('#RoomSelect').val()).load();
		return;
	}
	var CurDateTime = new moment();
	IVRATable = $('#IVRATable').DataTable({
		'oLanguage': DefaultoLanguage,
		'iDisplayLength': 5,
		'sPaginationType': 'full_numbers',
		'aoColumns': [{
				'bSearchable': true,
				'mData': 'RoomName'
			},
			{
				'bSearchable': true,
				'mData': 'Username'
			},
			{
				'bSearchable': true,
				'mData': 'Time',
				'mRender': function(data, type, full) {
					return onDateTimeColumn(CurDateTime, data);
				}
			}
		],
		ajax: {
			url: '/api/getInvalidAccessLog/' + $('#RoomSelect').val(),
			dataSrc: ''
		}
	})
	$("#IVRATable_filter label input").addClass("form-control").attr("placeholder", "Search...");
}

function GetMotionDetectedHistory() {
	if (MAHTable != null){
		MAHTable.ajax.url('/api/getMotionEvents/' + $('#RoomSelect').val()).load();
		return;
	}
	MAHTable = $('#MAHTable').DataTable({
		'oLanguage': DefaultoLanguage,
		'iDisplayLength': 5,
		'sPaginationType': 'full_numbers',
		'aoColumns': [{
				'bSearchable': true,
				'mData': 'Id'
			},
			{
				'bSearchable': true,
				'mData': 'Time'
			},
			{
				'bSearchable': false,
				'bSortable': false,
				'mData': 'FilePath',
				'mRender': function(data, type, full) {
					return '<a class="btn btn-primary btnView" href="https://s3-us-west-2.amazonaws.com/iotsmartroom/' + data + '">View <i class="fa fa-file-video-o" aria-hidden="true"></i></a>';
				}

			}
		],
		"order": [
			[2, "desc"]
		],
		ajax: {
			url: '/api/getMotionEvents/' + $('#RoomSelect').val(),
			dataSrc: ''
		}
	}).on('draw', function() {
		$(".btnView").click(function(e) {
			var link = $(this).attr("href");
			$('#VideoPreview').attr('src', link)
			$('#VideoModal').modal('show');
			e.preventDefault()
		});
	});
	$("#MAHTable_filter label input").addClass("form-control").attr("placeholder", "Search...");
}

function InitializeWSS() {
  DrawRoomTempsGraph()
	$.ajax({
		type: "GET",
		url: "/api/getAwsIotWSS",
		success: function(data) {
			var clientId = Math.random().toString(36).substring(7);
			wss_client = new Paho.MQTT.Client(data, clientId);
			var connectOptions = {
				useSSL: true,
				timeout: 3,
				mqttVersion: 4,
				onSuccess: function subscribe() {
             wss_client.subscribe("rooms/" + $('#RoomSelect').val() + "/enviroData");
             console.log("subscribed");
            }
			};
			wss_client.connect(connectOptions);
			wss_client.onMessageArrived = function onMessage(message) {
				var status = JSON.parse(message.payloadString);
        console.log(status);
        current_temp.push([status.time,status.temp])
        DrawRoomTempsGraph()
			}
			wss_client.onConnectionLost = function(e) {
				console.log(e)
			};
		}
	});
}

$(document).ready(function() {
	GetValidAccessLogs();
	GetInvalidAccessLogs();
	GetMotionDetectedHistory();
	GrabAvgRoomTemps();
	InitializeWSS();

	$roomSelect = $('#RoomSelect');
	$roomSelect.data("prev",$roomSelect.val());
	$roomSelect.change(function(){
		GetValidAccessLogs();
		GetInvalidAccessLogs();
		GetMotionDetectedHistory();
		GrabAvgRoomTemps();
		current_temp = []
		if (wss_client != null){
			wss_client.subscribe("rooms/" + $(this).val() + "/enviroData");
			wss_client.unsubscribe("rooms/" + $roomSelect.data("prev") + "/enviroData");
		}
		$(this).data("prev",$(this).val());
	});
});
