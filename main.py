import pyshark
import time
import matplotlib.pyplot as plt

def call_with_video():
    capture = pyshark.FileCapture('captures/call_full_supernode.pcapng', display_filter="udp and ip.addr==20.202.145.223")

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

    capture.close()

def call_without_video():
    capture = pyshark.FileCapture('captures/voice_call_full_p2p.pcapng', display_filter="udp and ip.addr==109.136.186.101")

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
    print("")

    capture.close()

def call_with_video_local():
    capture = pyshark.FileCapture('captures/local_video_call.pcapng', display_filter="udp and ip.addr==172.16.177.128")

    total_bytes = 0
    start_time = 7
    end_time = start_time + 10 # temps de l'échantillon start time + 10 secondes
    nb_packets = 0
    
    for packet in capture:
        time = float(packet.frame_info.time_relative)
        if time > start_time and time < end_time:
            nb_packets += 1
            total_bytes += int(packet.length)

    
    nb_packets = nb_packets * 6

    print("Volume de données échangées pendant l'appel Skype avec vidéo local: ", total_bytes, "bytes")
    total_bytes = total_bytes * 6
    print("Volume de données échangées pendant l'appel Skype avec vidéo local: ", total_bytes, "bytes/min")
    print("Nombre de paquets échangés pendant l'appel Skype avec vidéo local: ", nb_packets, "paquets/min")
    print("")

    capture.close()


def call_without_video_local():
    capture = pyshark.FileCapture('captures/local_voice_call.pcapng', display_filter="udp and ip.addr==172.16.177.128")

    total_bytes = 0
    start_time = 6
    end_time = start_time + 10 # temps de l'échantillon start time + 10 secondes
    nb_packets = 0

    for packet in capture:
        time = float(packet.frame_info.time_relative)
        if time > start_time and time < end_time:
            nb_packets += 1
            total_bytes += int(packet.length)

    nb_packets = nb_packets * 6
        
    print("Volume de données échangées pendant l'appel Skype sans vidéo local: ", total_bytes, "bytes")
    total_bytes = total_bytes * 6
    print("Volume de données échangées pendant l'appel Skype sans vidéo local : ", total_bytes, "bytes/min")
    print("Nombre de paquets échangés pendant l'appel Skype sans vidéo local: ", nb_packets, "paquets/min")
    print("")

    capture.close()

def get_destination_ip(capture_file, src_ip):
    capture = pyshark.FileCapture(capture_file, display_filter="ip.src == " + src_ip)
    dest_ips = {}

    total_packets = 0
    for packet in capture:
        total_packets += 1
        if 'IP' in packet:
            dest_ip = packet['IP'].dst

            if dest_ip in dest_ips:
                dest_ips[dest_ip] += 1
            else:
                dest_ips[dest_ip] = 1

    # Calculer le pourcentage pour chaque adresse IP de destination
    dest_ip_percentages = {}
    for dest_ip, frequency in dest_ips.items():
        percentage = (frequency / total_packets) * 100
        dest_ip_percentages[dest_ip] = percentage

    # Trier les adresses IP de destination par ordre décroissant de fréquence
    percentage_sorted = sorted(dest_ip_percentages.items(), key=lambda x: x[1], reverse=True)

    capture.close()

    return percentage_sorted
    
def create_pie_chart(capture_file, src_ip):
    dest_ip_percentages = get_destination_ip(capture_file, src_ip)

    threshold = 10

    labels = []
    sizes = []

    for dest_ip, percentage in dest_ip_percentages:
        if percentage >= threshold:
            labels.append("Proximus")
            sizes.append(percentage)

    labels.append("Other")

    print(sizes)

    other_percentage = 100 - sum(sizes)

    sizes.append(other_percentage)

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})
    ax.axis('equal')

    # Show the chart
    plt.show()

if __name__ == "__main__":
    call_with_video()
    call_without_video()
    call_with_video_local()
    call_without_video_local()

    #create_pie_chart('captures/call_full_supernode.pcapng', "172.16.177.129")
    #create_pie_chart('captures/video_call_2.pcapng', "172.16.177.128")