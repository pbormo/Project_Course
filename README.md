# Project_Course
Simulazione dati con mininet ed estrazione features
=======

Questo progetto nasce come parte di un corso universitario e ha l'obiettivo di simulare una rete SDN usando Comnetsemu, generare traffico, salvare file .pcap, estrarre metriche di rete (throughput, delay, jitter) tramite un codice python e salvare i risultati all'interno di un file txt facilmente leggibile e un file json.

## Requisiti

- Comnetsemu installato su VirtualBox
- Python 3
- tshark / Wireshark
- Conda
- Librerie Python: pyshark, os, json, defauldict 

## Struttura del progetto
```plaintext
Project_course/
│
├── file_extract_demo/     # Cartella dove verranno salvati i risultati dell'analisi. (json and text)
│
├── pcap_demo/             # Cartella dove posizionare i file pcap da analizzare.
├──────── aaa.pcap e tcp-ecn-sample.pcap     # File di test per il funzionamento dell'estrazione delle features senza la generazione dei file .pcap tramite Comnetsemu
│
├── README.md                                       # Documentazione del progetto (Questo file)
├── network.py                                      # Script per configurare la rete in Mininet e generare traffico.
├── estrazione_features_tirocinio.py                # Estrarre le caratteristiche dai file pcap e salvarle su txt e json
```
## Come usare il progetto
1. Accedere a virtualbox ed attivare la macchina di comnetsemu
2. Connettersi a github da macchina virtuale e scaricare il file network.py
3. Lanciare il comando: `sudo python3 network.py` 
4. Genera traffico e salva i file .pcap nella cartella `pcap_dumps/`
5. Trasferire i risultati nella cartella `pcap_dumps/` sul PC nella cartella pcap_demo/
6. Quindi utilizzare il file estrazione_features_tirocinio.py, una volta che questo codice finirà verranno salvati i file txt e json contenenti le metriche d'interesse all'interno della cartella `file_extract_demo`

## Esempi di risultati dei file pcap_demo già inseriti nella cartella

Partendo dal file h1_traffic.pcap si riescono ad estrarre le seguenti metriche scritte nel file h1_traffic.txt e h1_traffic.json:
```plaintext
json:
{
    "unique_ips": [
        "10.0.0.1",
        "10.0.0.3",
        "10.0.0.5",
        "10.0.0.6",
        "10.0.0.4",
        "10.0.0.2",
        "10.0.0.7"
        ],
    "connections": [
        {
            "source_ip": "10.0.0.1",
            "destination_ip": "10.0.0.2",
            "source_port": null,
            "destination_port": null,
            "protocol": "ICMP",
            "start_timestamp": 1741092804.801575,
            "end_timestamp": 1741092811.984088,
            "total_packets": 4,
            "total_bytes": 392,
            "average_throughput_bps": 54.57699833991925
        } ...

txt: 
Indirizzi IP unici:
10.0.0.1
10.0.0.3
10.0.0.5
10.0.0.6
10.0.0.4
10.0.0.2
10.0.0.7

Connessioni attive:
10.0.0.1:None -> 10.0.0.2:None [ICMP]
  Start: 1741092804.801575, End: 1741092811.984088
  Packets: 4, Bytes: 392
  Throughput: 54.58 Bps ....
```
## Note

Il progetto è eseguito all’interno di una macchina virtuale con Comnetsemu e si basa sulla raccolta dati real-time generati tramite simulazione. Per l'estrazione delle feature è stato lanciato il codice all'interno di un'ambiente conda. Possibili estensioni del progetto includono l’uso di altri modelli predittivi e l’aggiunta di ulteriori metriche.

## Autori
Progetto sviluppato nell’ambito del corso universitario di networking 2 presso l'Università degli Studi di Trento da
Paolo Bormolini (studente universitario) numero matricola 257775, e-mail: paolo.bormolini@studenti.unitn.it.

