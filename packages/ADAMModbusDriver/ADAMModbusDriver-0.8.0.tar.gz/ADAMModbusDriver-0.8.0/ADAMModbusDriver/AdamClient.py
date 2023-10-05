from pyModbusTCP.client import ModbusClient

class AdamClient:
        
    thermocouple_ranges = {
        "J": {"min": 0.0, "max": 760.0},
        "K": {"min": 0.0, "max": 1370.0},
        "T": {"min": -100.0, "max": 400.0},
        "E": {"min": 0.0, "max": 1000.0},
        "R": {"min": 500.0, "max": 1750.0},
        "S": {"min": 500.0, "max": 1750.0},
        "B": {"min": 500.0, "max": 1800.0},
    }

    def __init__(self, host, thermocouple_type, port=502, unit_id=1):
        if thermocouple_type not in self.thermocouple_ranges:
            raise ValueError(f"Unsupported thermocouple type: {thermocouple_type}")
        
        self.client = ModbusClient(host=host, port=port, unit_id=unit_id)
        self.thermocouple_type = thermocouple_type
        self.chans_in = 8
        self.channel_names = [f"Thermo Channel {i+1}" for i in range(self.chans_in)]

    def convert(self, reg_values):
        thermocouple_range = self.thermocouple_ranges[self.thermocouple_type]
        range_min = thermocouple_range["min"]
        range_max = thermocouple_range["max"]
        converted_values = [(raw_temperature / 65535.0) * (range_max - range_min) + range_min for raw_temperature in reg_values]
        return [round(value, 2) for value in converted_values]

    def read_temps(self, address=0, count=8):
        if self.client.open():
            regs = self.client.read_holding_registers(address, count)
            self.client.close()
            if regs:
                return self.convert(regs)
            else:
                raise Exception("Read failed")
        else:
            raise Exception("Failed to Connect")
        
    def get_channel_names(self):
        return self.channel_names
    
    def set_channel_name(self, position, name):
        """
        Set the name of a specific channel based on its position.

        Args:
            position (int): Position of the channel (0-based index).
            name (str): New name for the channel.
        """
        if position < 0 or position >= self.chans_in:
            raise ValueError(f"Invalid position value. Must be between 0 and {self.chans_in-1}.")
        self.channel_names[position] = name

