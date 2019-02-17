from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

host = "a1mnegx95sc2wp-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "certs/root-CA.crt"
certificatePath = "certs/IotRoom2.cert.pem"
privateKeyPath = "certs/IotRoom2.private.key"

class AwsIot:
    def __init__(self, Name, Queue):
        self.my_rpi = AWSIoTMQTTClient(Name)
        self.my_rpi.configureEndpoint(host, 8883)
        self.my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

        self.my_rpi.configureOfflinePublishQueueing(Queue)  # Infinite offline Publish queueing
        self.my_rpi.configureDrainingFrequency(10)  # Draining: 2 Hz
        self.my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
        self.my_rpi.configureMQTTOperationTimeout(1)  # 5 sec
        self.my_rpi.connect()
