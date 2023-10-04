from pymodbus.client.serial import ModbusSerialClient
from pymodbus.client.tcp import ModbusTcpClient
import struct 
import time
class SimpleLoggerV1:

    def __init__(self,method,ip=None,serialPort=None):
        if(method=='rtu'):
            self.client = ModbusSerialClient(method='rtu', port=serialPort, timeout=1,baudrate=460800)
        else:
            self.client = ModbusTcpClient(host=ip,port = 80)
        try:
            self.readA6()
        except:
            pass

    def uint16_to_float32(self,MSB,LSB):
        float32_msb = MSB.to_bytes(2, byteorder='big', signed=False)
        float32_lsb = LSB.to_bytes(2, byteorder='big', signed=False)
        float32_full = float32_msb + float32_lsb
        float32 = struct.unpack(">f",float32_full)
        return float32[0]

    def uint32_to_uint16(self,val):
        ba = bytearray(struct.pack(">L", val)) 
        msb = struct.unpack(">H",ba[0:2])
        lsb = struct.unpack(">H",ba[2:4])
        return msb[0],lsb[0]

    def uint16_to_uint32(self,MSB,LSB):
        uint32_msb = MSB.to_bytes(2, byteorder='big', signed=False)
        uint32_lsb = LSB.to_bytes(2, byteorder='big', signed=False)
        uint32_full = uint32_msb + uint32_lsb
        uint32 = struct.unpack(">L",uint32_full)
        return uint32[0]

    def uint16_to_hex_string(self,uintArray):
        hexStr=b''
        for uint in uintArray:
            hexStr+=uint.to_bytes(2, byteorder='big', signed=False)
        return hexStr.hex()

    def getUid(self):
        rslt = self.client.read_holding_registers(40004,6,unit=4).registers
        return self.uint16_to_hex_string(rslt)
        
    def getType(self):
        rslt = self.client.read_holding_registers(40010,1,unit=4).registers
        return rslt[0] 

    def getEpoch(self):
        response = self.client.read_holding_registers(40026,2,unit=4)
        return self.uint16_to_uint32(response.registers[0],response.registers[1])

    def setEpoch(self,epoch):
        self.client.write_registers(40030,self.uint32_to_uint16(epoch),unit=4)
        self.client.write_registers(40028,1,unit=4)

    def readA0(self):
        response = self.client.read_input_registers(30000,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA1(self):
        response = self.client.read_input_registers(30002,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA2(self):
        response = self.client.read_input_registers(30004,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA3(self):
        response = self.client.read_input_registers(30006,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA4(self):
        response = self.client.read_input_registers(30008,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA5(self):
        response = self.client.read_input_registers(30010,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA6(self):
        response = self.client.read_input_registers(30012,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA7(self):
        response = self.client.read_input_registers(30014,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA12(self):
        response = self.client.read_input_registers(30016,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA13(self):
        response = self.client.read_input_registers(30018,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def read14(self):
        response = self.client.read_input_registers(30020,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA15(self):
        response = self.client.read_input_registers(30022,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA12A13(self):
        response = self.client.read_input_registers(30024,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA14A15(self):
        response = self.client.read_input_registers(30026,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA16(self):
        response = self.client.read_input_registers(30028,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA17(self):
        response = self.client.read_input_registers(30030,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA18(self):
        response = self.client.read_input_registers(30032,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA19(self):
        response = self.client.read_input_registers(30034,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA16A17(self):
        response = self.client.read_input_registers(30036,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readA18A19(self):
        response = self.client.read_input_registers(30038,2,unit=4)
        return self.uint16_to_float32(response.registers[0],response.registers[1])

    def readAllA(self):
        response = self.client.read_input_registers(30000,40,unit=4)
        result = []
        for i in range(0,len(response.registers),2):
            result.append(self.uint16_to_float32(response.registers[i],response.registers[i+1]))
        return result

    def readA8(self):
        return self.client.read_coils(0x00,4,unit=4).bits[0]

    def readA9(self):
        return self.client.read_coils(0x00,4,unit=4).bits[1]

    def readA10(self):
        return self.client.read_coils(0x00,4,unit=4).bits[2]

    def readA11(self):
        return self.client.read_coils(0x00,4,unit=4).bits[3]

    def writeA8(self,value):
        return self.client.write_coil(0x00, value,unit=4)

    def writeA9(self,value):
        return self.client.write_coil(0x01, value,unit=4)

    def writeA10(self,value):
        return self.client.write_coil(0x02, value,unit=4)

    def writeA11(self,value):
        return self.client.write_coil(0x03, value,unit=4)
