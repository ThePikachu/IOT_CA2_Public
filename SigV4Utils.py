import hmac
import hashlib

class SigV4Utils:
    @staticmethod
    def getSignatureKey(key, dateStamp, regionName, serviceName):
        kDate = hmac.new(bytes('AWS4'+ key , 'latin-1'),msg = bytes(dateStamp , 'latin-1'),
        digestmod = hashlib.sha256).hexdigest()
        kRegion = hmac.new(bytearray.fromhex(kDate),msg = bytes(regionName , 'latin-1'),
        digestmod = hashlib.sha256).hexdigest()
        kService = hmac.new(bytearray.fromhex(kRegion),msg = bytes(serviceName , 'latin-1'),
        digestmod = hashlib.sha256).hexdigest()
        kSigning = hmac.new(bytearray.fromhex(kService),msg = bytes('aws4_request' , 'latin-1'),
        digestmod = hashlib.sha256).hexdigest()
        return kSigning

    @staticmethod
    def sign(key, msg):
        return hmac.new(bytearray.fromhex(key),msg = bytes(msg , 'latin-1'),
        digestmod = hashlib.sha256).hexdigest()

    @staticmethod
    def sha256(msg):
        return hashlib.sha256(bytes(msg, 'latin-1')).hexdigest()
