import pyshark
import time

def call_with_video():
    capture = pyshark.FileCapture('captures/call_full.pcapng', display_filter="udp and ip.addr==20.202.145.223")

    total_bytes = 0
    start_time = 13
    end_time = start_time + 10 # temps de l'échantillon start time + 10 secondes
    nb_packets = 0
    
    for packet in capture:
        time = float(packet.frame_info.time_relative)
        if time > start_time and time < end_time:
            nb_packets += 1
            total_bytes += int(packet.length)

    
    nb_packets = nb_packets * 6

    print("Volume de données échangées pendant l'appel Skype avec vidéo: ", total_bytes, "bytes")
    total_bytes = total_bytes * 6
    print("Volume de données échangées pendant l'appel Skype avec vidéo: ", total_bytes, "bytes/min")
    print("Nombre de paquets échangés pendant l'appel Skype avec vidéo: ", nb_packets, "paquets/min")
    print("")

def call_without_video():
    capture = pyshark.FileCapture('captures/voice_call_full.pcapng', display_filter="udp and ip.addr==109.136.186.101")

    total_bytes = 0
    start_time = 13
    end_time = start_time + 10 # temps de l'échantillon start time + 10 secondes
    nb_packets = 0

    for packet in capture:
        time = float(packet.frame_info.time_relative)
        if time > start_time and time < end_time:
            nb_packets += 1
            total_bytes += int(packet.length)

    nb_packets = nb_packets * 6
        
    print("Volume de données échangées pendant l'appel Skype sans vidéo : ", total_bytes, "bytes")
    total_bytes = total_bytes * 6
    print("Volume de données échangées pendant l'appel Skype sans vidéo : ", total_bytes, "bytes/min")
    print("Nombre de paquets échangés pendant l'appel Skype sans vidéo : ", nb_packets, "paquets/min")


if __name__ == "__main__":
    call_with_video()
    call_without_video()