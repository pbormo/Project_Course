import pyshark  # Libreria per l'analisi di file pcap
import os  # Libreria per interagire con il filesystem
import json  # Libreria per la gestione dei file JSON
from collections import defaultdict  # Dizionario avanzato con valori di default

# Funzione per analizzare i flussi di un file pcap
def analyze_pcap_flows(pcap_file):
    try:
        print(f"Apertura del file pcap: {pcap_file}")
        capture = pyshark.FileCapture(pcap_file)  # Apre il file pcap per l'analisi
        print(f"File pcap aperto con successo: {pcap_file}")
    except Exception as e:
        print(f"Errore nell'aprire il file {pcap_file}: {e}")
        return None, None  # Se fallisce, ritorna None

    # Dizionario per raccogliere i dati sui flussi
    flows = defaultdict(lambda: {'start_time': None, 'end_time': None, 'packet_count': 0, 'total_bytes': 0})
    unique_ips = set()  # Insieme per memorizzare gli IP unici

    # Itera su tutti i pacchetti nel file pcap
    for packet in capture:
        try:
            timestamp = float(packet.sniff_timestamp)  # Estrae il timestamp del pacchetto
            length = int(packet.length)  # Estrae la lunghezza del pacchetto
            protocol = packet.highest_layer  # Determina il protocollo del pacchetto

            if hasattr(packet, 'ip'):
                src_ip = packet.ip.src  # IP sorgente
                dst_ip = packet.ip.dst  # IP destinazione
                unique_ips.update([src_ip, dst_ip])  # Aggiunge gli IP all'insieme
            else:
                continue  # Salta i pacchetti senza IP
            
            # Inizializza le porte sorgente e destinazione
            src_port, dst_port = None, None
            if hasattr(packet, 'tcp'):
                src_port = packet.tcp.srcport
                dst_port = packet.tcp.dstport
            elif hasattr(packet, 'udp'):
                src_port = packet.udp.srcport
                dst_port = packet.udp.dstport
            
            # Chiave identificativa del flusso
            flow_key = (src_ip, dst_ip, src_port, dst_port, protocol)

            # Registra il timestamp iniziale
            if flows[flow_key]['start_time'] is None:
                flows[flow_key]['start_time'] = timestamp
            flows[flow_key]['end_time'] = timestamp  # Aggiorna il timestamp finale
            flows[flow_key]['packet_count'] += 1  # Incrementa il conteggio pacchetti
            flows[flow_key]['total_bytes'] += length  # Incrementa il conteggio bytes

        except AttributeError:
            print(f"Pacchetto ignorato per dati mancanti in {pcap_file}.")
            continue  # Ignora pacchetti con dati mancanti
        except Exception as e:
            print(f"Errore nell'analisi di un pacchetto in {pcap_file}: {e}")
            continue  # Ignora altri pacchetti problematici

    return flows, unique_ips  # Restituisce i dati raccolti

# Funzione per salvare i dati nei due formati richiesti
def save_flows_data(flows, unique_ips, output_base):
    # Salvataggio in TXT
    txt_file = output_base + ".txt"
    with open(txt_file, "w") as file:
        file.write("Indirizzi IP unici:\n")
        file.write("\n".join(unique_ips) + "\n\n")
        file.write("Connessioni attive:\n")
        for (src_ip, dst_ip, src_port, dst_port, protocol), data in flows.items():
            duration = max(data['end_time'] - data['start_time'], 0.001) #questa è una strategia per evitare i casi in cui ci siano pacchetti a 0 o comunque molto prossimi a questo che rischiano di generare malintesi
            avg_throughput = data['total_bytes'] / duration
            file.write(f"{src_ip}:{src_port} -> {dst_ip}:{dst_port} [{protocol}]\n")
            file.write(f"  Start: {data['start_time']}, End: {data['end_time']}\n")
            file.write(f"  Packets: {data['packet_count']}, Bytes: {data['total_bytes']}\n")
            file.write(f"  Throughput: {avg_throughput:.2f} Bps\n\n")
    print(f"Dati sui flussi salvati in '{txt_file}'")

    # Salvataggio in JSON
    json_file = output_base + ".json"
    json_data = {
        "unique_ips": list(unique_ips),
        "connections": []
    }
    for (src_ip, dst_ip, src_port, dst_port, protocol), data in flows.items():
        duration = max(data['end_time'] - data['start_time'], 0.001)
        avg_throughput = data['total_bytes'] / duration #Byte/Secondo e non bit/secondo dovrei moltiplicare per 8
        json_data["connections"].append({
            "source_ip": src_ip, "destination_ip": dst_ip,
            "source_port": src_port, "destination_port": dst_port,
            "protocol": protocol,
            "start_timestamp": data['start_time'], "end_timestamp": data['end_time'],
            "total_packets": data['packet_count'], "total_bytes": data['total_bytes'],
            "average_throughput_bps": avg_throughput
        })
    with open(json_file, "w") as file:
        json.dump(json_data, file, indent=4)
    print(f"Dati sui flussi salvati in '{json_file}'")

# Funzione per elaborare tutti i file pcap in una cartella
def process_pcap_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Crea la cartella di output se non esiste
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".pcap"):
            pcap_path = os.path.join(input_dir, filename)
            output_base = os.path.join(output_dir, filename.replace(".pcap", ""))
            
            flows, unique_ips = analyze_pcap_flows(pcap_path)
            if flows is not None and unique_ips is not None:
                save_flows_data(flows, unique_ips, output_base)

# Esempio di utilizzo
input_directory = r"C:\Users\ACER\Documents\netmod2\tirocinio\pcap_demo"
output_directory = r"C:\Users\ACER\Documents\netmod2\tirocinio\file_extract_demo"
process_pcap_directory(input_directory, output_directory)
