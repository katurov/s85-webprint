import socket
import time
import errno

class S85Printer:
    def __init__(self, address='04:7F:0E:49:91:ED', port=1):
        self.address = address
        self.port = port

    def _connect(self, retries=3):
        for i in range(retries):
            try:
                s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                s.settimeout(10)
                s.connect((self.address, self.port))
                return s
            except OSError as e:
                if e.errno == errno.EBUSY and i < retries - 1:
                    time.sleep(1)
                    continue
                raise e
        return None

    def get_status(self):
        try:
            s = self._connect()
            s.send(b'\x10\x04\x01\x10\x04\x02\x10\x04\x04')
            time.sleep(0.2)
            response = s.recv(10)
            s.close()
            time.sleep(0.5) # Allow BT stack to settle
            
            if not response:
                return False, "No response from printer"
            
            status_msg = []
            # Check bits (ESC/POS standard)
            if len(response) >= 1:
                if response[0] & 0x08: status_msg.append("Offline")
            if len(response) >= 2:
                if response[1] & 0x04: status_msg.append("Cover open")
                if response[1] & 0x40: status_msg.append("Error state")
            if len(response) >= 3:
                if paper_status := (response[2] & 0x60):
                    if paper_status == 0x60: status_msg.append("Out of paper")
            
            if not status_msg:
                return True, "Ready"
            return False, ", ".join(status_msg)
        except Exception as e:
            return False, f"Status check failed: {str(e)}"

    def print_job(self, jobs):
        try:
            raw_data = b'\x1b\x40' # Init
            for job_type, content in jobs:
                if job_type == 'text':
                    raw_data += content.encode('cp866', errors='replace')
                elif job_type == 'qr':
                    raw_data += self._generate_qr(content)
                elif job_type == 'barcode':
                    raw_data += self._generate_barcode(content)
            
            raw_data += b'\n\n\n\n'
            
            s = self._connect()
            s.send(raw_data)
            s.close()
            time.sleep(0.5)
            return True, "Printed"
        except Exception as e:
            return False, str(e)

    def _generate_qr(self, content):
        data = content.encode('utf-8')
        pL = (len(data) + 3) % 256
        pH = (len(data) + 3) // 256
        res = b'\x1d\x28\x6b\x04\x00\x31\x41\x32\x00'
        res += b'\x1d\x28\x6b\x03\x00\x31\x43\x03'
        res += b'\x1d\x28\x6b\x03\x00\x31\x45\x30'
        res += b'\x1d\x28\x6b' + bytes([pL, pH]) + b'\x31\x50\x30' + data
        res += b'\x1d\x28\x6b\x03\x00\x31\x51\x30'
        return res

    def _generate_barcode(self, content):
        data = content.encode('ascii', errors='replace')
        n = len(data)
        return b'\x1d\x6b\x49' + bytes([n]) + data
