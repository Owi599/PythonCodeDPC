import pyshark as sharky
from datetime import datetime

def calculate_data_rate(pcap_file, start_time, end_time):
    # Load the pcap file
    cap = sharky.FileCapture(pcap_file)

    total_bytes = 0
    start_time_dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
    end_time_dt = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')

    # Iterate through packets
    for packet in cap:
        # Convert packet time to datetime
        packet_time = datetime.fromtimestamp(float(packet.sniff_timestamp))

        # Debugging prints
        print(f"Packet Time: {packet_time}, Start Time: {start_time_dt}, End Time: {end_time_dt}")

        # Check if the packet is within the specified time range
        if start_time_dt <= packet_time <= end_time_dt:
            total_bytes += int(packet.length)  # Get the packet size in bytes

            # Debugging prints
            print(f"Packet Length: {packet.length}, Total Bytes: {total_bytes}")

    # Calculate the duration in seconds
    duration_seconds = (end_time_dt - start_time_dt).total_seconds()

    # Calculate the data rate (bytes per second)
    if duration_seconds > 0:
        data_rate = total_bytes / duration_seconds
    else:
        data_rate = 0

    cap.close()
    return data_rate,total_bytes

# Example usage
pcap_file = 'UDP.pcapng'  # Replace with your PCAP file path
start_time_1 = '2024-08-26 15:50:08.648'  # Replace with your start time
end_time_1 = '2024-08-26 15:50:12.132'  # Replace with your end time

data_rate_1 = calculate_data_rate(pcap_file, start_time_1, end_time_1)


print(f'Data amount: {data_rate_1[1]} bytes')

