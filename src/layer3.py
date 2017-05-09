
class layer3_device:

	def __init__(self, name, ifaces, routes):		# Class constructor
		self.name = name			# Identification for the device
		self.ifaces = ifaces		# List of iface objects
		self.routes = routes		# List of dictionaries containing routes. Hosts have only one entry
		self.ARP_table = []			# Empty list for ARP table.		REVIEW: Is it useless?

	def send_ARP(self):
		pass

class iface:

	def __init__(self, name, IP_addr, MAC_addr):				# Class constructor
		self.name = name
		self.IP_addr = IP_addr
		self.MAC_addr = MAC_addr

class IP_utils:

	@staticmethod
	def IP_to_number(str_IP_addr):
		byte_elements = str_IP_addr.split(".")
		IP_num = 0

		for k in range(0, 4):
			IP_num = IP_num + int(byte_elements[3-k])*(2**(k*8))

		return IP_num

	@staticmethod
	def number_to_IP(num_IP_addr):
		IP_str = ""
		temp = num_IP_addr
		
		return IP_str
