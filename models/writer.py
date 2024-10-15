import time
import serial
import serial.tools
import serial.tools.list_ports
from crcmod import mkCrcFun
class Writer():

    def __init__(self):
        self.address = 0x00
        self.com_port = None
        self.ser = None
        self.baudrate = 57600
        
    def get_current_epc(self):
        packet = self.create_packet(0x0f)
        return self.send_cmd(packet)
    
    
    def find_com_port(self):
        vid_pid = "10C4:EA60"
        serial_number = "0001"
        ports = serial.tools.list_ports.comports()
        com_port = None
        for port in ports:
            if port.vid == vid_pid or port.serial_number == serial_number:
                com_port = port.device
        self.com_port = com_port
        return com_port
    def connect_to_serial(self):

        timeout = 2
        try:
            ser = serial.Serial(self.com_port, self.baudrate, timeout=timeout)
            self.ser = ser
        except serial.SerialException as e:
            self.ser = None
        
    def _crc16(self, packet):
        PRESET_VALUE = 0xFFFF
        POLYNOMIAL = 0x11021
        crc16_func = mkCrcFun(POLYNOMIAL, initCrc=PRESET_VALUE, xorOut=0x0000, rev=True)
        crc = crc16_func(packet)
        lsb_crc = crc & 0xFF
        msb_crc = (crc >> 8) & 0xFF
        return [lsb_crc, msb_crc]
    def create_packet(self, cmd, data_array=None):
        data_array = data_array if data_array else []
        length = len(data_array) + 4
        address = self.address
        
        cmd_block = [
            length,
            address,
            cmd,
        ] + data_array
        packet = bytearray(cmd_block)
        packet.extend(self._crc16(packet))
        return packet
    
    def send_cmd(self, packet):
        time_now = time.time()
        self.ser.write(packet)
        time.sleep(0.5)
        
        c = 0
        while c < 10:
            c += 1
        if self.ser.in_waiting > 0:
            response = self.ser.read(self.ser.in_waiting)
            return response
        return None
    
'''        
import time
writer = Writer()
writer.find_com_port()
writer.connect_to_serial()
print(writer.get_current_epc())
'''
    