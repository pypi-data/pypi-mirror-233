from pyModbusTCP.client import ModbusClient
from pymodbus.exceptions import ModbusException


class StrideClient:
    def __init__(self, host, port=502, unit_id=1):
        self.client = ModbusClient(host=host, port=port, unit_id=unit_id)
        self.chans_in = 8
        self.channel_names = [f"Thermo Channel {i+1}" for i in range(self.chans_in)]


    def read_samples(self, count=8):
        if self.client.open():
            regs = self.client.read_input_registers(40, count)
            
            self.client.close()
            if regs:
                formatted_regs = [round(reg / 10.0, 1) for reg in regs]
                return formatted_regs
            else:
                raise Exception("Read failed")
        else:
            raise Exception("Failed to Connect")
        
    def write_units(self, unit):
            # Define a dictionary to map unit strings to values
            unit_map = {'C': 0, 'F': 1, 'K': 2}
            if unit in unit_map:
                value = unit_map[unit]
                if self.client.open():
                    for address in range(1217, 1225):  # from 1218 to 1225
                        result = self.client.write_single_register(address, value)
                        if not result:
                            self.client.close()
                            raise Exception(f"Failed to write value {value} to address {address}")
                    self.client.close()
                else:
                    raise Exception("Failed to Connect")
            else:
                raise Exception(f"Invalid unit '{unit}'. Acceptable values are 'C', 'F', or 'K'.")
            
        
    def set_input_type(self, value_number, input_type):
        # Define a dictionary to map input types to values
        input_map = {'Disabled': 0x00, 'Voltage': 0x01, 'K': 0x05, 'J': 0x04, 'R': 0x06, 'S': 0x07, 'T': 0x08, 'B': 0x09, 'E': 0x0A, 'N': 0x0B}

        if input_type not in input_map:
            raise Exception(f"Invalid input type '{input_type}'. Acceptable values are 'K' or 'J'.")

        # Determine the appropriate register address and position based on the value number
        if value_number in range(0, 8):
            # Determine base address (30, 31, 32, 33)
            address = 30 + (value_number) // 2
            # Determine position (top or bottom)
            position = "bottom" if value_number % 2 == 1 else "top"
        else:
            raise Exception(f"Invalid value number {value_number}. It should be between 1 and 8 inclusive.")

        if position == "top":
            # Shift the value 8 bits to the left to set the top half
            value_to_write = input_map[input_type] << 8
        else:  # position == "bottom"
            # Use the value directly to set the bottom half
            value_to_write = input_map[input_type]

        if self.client.open():
            # Read the current value of the register
            current_value = self.client.read_holding_registers(address, 1)
            if not current_value:
                self.client.close()
                raise Exception(f"Failed to read current value at address {address}.")

            # Update the half specified by the user while keeping the other half unchanged
            if position == "top":
                value_to_write |= current_value[0] & 0x00FF
            else:  # position == "bottom"
                value_to_write |= current_value[0] & 0xFF00

            # Write the updated value back to the register
            result = self.client.write_single_register(address, value_to_write)
            self.client.close()
            if not result:
                raise Exception(f"Failed to set input type {input_type} for value number {value_number}.")
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

    def start(self):
        pass

    def stop(self):
        pass

    def close(self):
        pass
