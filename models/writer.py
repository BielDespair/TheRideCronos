import os
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
        self.epc_prefix = '72696465'
        self.epc_start = 6
        self.epc_length = 12
    def register_tag(self, suffix):
        error = self.connect_to_writer()
        if error: return True, error
        
        padding = os.urandom(6).hex()
        new_epc = self.epc_prefix + padding + suffix #2 words prefix + 3 words padding + 1 word suffix
        new_epc = bytes.fromhex(new_epc)
        error = self.write_epc(new_epc)
        if error: return True, error
        
        current_tag_epc = self.get_current_epc()
        if not current_tag_epc:
            return True, "Falha no cadastro. Tente novamente"
        if not current_tag_epc == new_epc:
            return True, "Falha no cadastro. Tente Novamente"
        
        return False, new_epc
        
    def get_current_epc(self):
        cmd = 0x0f
        packet = self.create_packet(cmd)
        
        response = self.send_cmd(packet)
        if not response:
            return
        
        if response[3] == 0x01:
            return response[self.epc_start:self.epc_start+self.epc_length]
        return
    
    def write_epc(self, new_epc):
        cmd = 0x04
        
        data_array = [
            self.epc_length // 2,
            *[0x00,0x00,0x00,0x00],
            *new_epc
        ]
        packet = self.create_packet(cmd, data_array)
        response = self.send_cmd(packet)
        status = response[3]
        if status == 0x00: return
        if status == 0xfb: return f"Tag não encontrada. Tente Novamente"
        
        else: return f"Falha no cadastro! Tente Novamente. ERROR: Writer Status Code: {response[3]}"
    
    def connect_to_writer(self):
        try:
            self.ser.write(b'\0x00')
            time.sleep(0.5)
            self.ser.read_all()
        except:
            self.ser = None
        if not self.ser:
            self.com_port = self.find_com_port()
            if not self.com_port:
                return "Aparelho não encontrado! Verifique a conexão USB e tente novamente"
            if not self.ser:
                try:
                    ser = serial.Serial(self.com_port, self.baudrate, timeout=2)
                    self.ser = ser
                except Exception as e:
                    return e
        return 
        
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
        
        self.ser.write(packet)
        time.sleep(0.5)
        if self.ser.in_waiting > 0:
            response = self.ser.read(self.ser.in_waiting)
            return response
        return None