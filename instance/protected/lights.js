var wss_client = null;

function InitializeWSS() {
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
				onSuccess: function() {
             console.log("connected");
					}
			};
			wss_client.connect(connectOptions);
			wss_client.onMessageArrived = function onMessage(message) {
				var status = JSON.parse(message.payloadString);
        console.log(status);
			}
			wss_client.onConnectionLost = function(e) {
				console.log(e)
			};
		}
	});
}

InitializeWSS();
