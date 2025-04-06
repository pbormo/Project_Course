# Project_Course

Questo progetto nasce come parte di un corso universitario e ha l'obiettivo di simulare una rete SDN usando Comnetsemu, generare traffico, salvare file .pcap, estrarre metriche di rete (throughput, delay, jitter).

## Requisiti

- Comnetsemu installato su VirtualBox
- Python 3
- Docker
- tshark / Wireshark
- Conda
- Librerie Python: pyshark, os, json, defauldict 

## Struttura del progetto

network.py: Script per configurare la rete in Mininet e generare traffico.

estrazione_features_tirocinio.py: Script per analizzare i file pcap e estrarre le caratteristiche.

pcap_demo/: Cartella dove posizionare i file pcap da analizzare.

csv_demo/: Cartella dove verranno salvati i risultati dell'analisi.

- `README.md` → questo file

## Come usare il progetto

1. Avvia la rete: `sudo python3 topology/topology.py`  
2. Genera traffico e salva i file .pcap nella cartella `pcap_dumps/`  
3. Estrai metriche con: `python3 scripts/parse_pcap.py --input pcap_dumps/file.pcap --output dati.csv`  
4. Addestra il modello: `python3 ml/lstm_train.py --data dati.csv`  
5. Fai una previsione: `python3 ml/lstm_predict.py --model modello.h5 --input nuovo_file.csv`  
6. Visualizza i risultati: `python3 scripts/plot_results.py --input predictions.csv`

## Note

Assicurati che la cartella `/home/comnetsemu/pcap_dumps` sia montata anche nei container Docker usati dagli host h5, h6, h7. Il progetto è eseguito all’interno di una macchina virtuale con Comnetsemu e si basa sulla raccolta dati real-time generati tramite simulazione. Possibili estensioni del progetto includono l’uso di altri modelli predittivi (es. Prophet) e l’aggiunta di ulteriori metriche.

## Autori

Progetto sviluppato nell’ambito del corso universitario su reti e machine learning.
