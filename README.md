# Project_Course
<<<<<<< HEAD
Simulazione dati con mininet ed estrazione features
=======

Questo progetto nasce come parte di un corso universitario e ha l'obiettivo di simulare una rete SDN usando Comnetsemu, generare traffico, salvare file .pcap, estrarre metriche di rete (throughput, delay, jitter) tramite un codice python e salvare i risultati all'interno di un file txt facilmente leggibile e un file json.

## Requisiti

- Comnetsemu installato su VirtualBox
- Python 3
- Docker
- tshark / Wireshark
- Conda
- Librerie Python: pyshark, os, json, defauldict 

## Struttura del progetto

network.py: Script per configurare la rete in Mininet e generare traffico.

estrazione_features_tirocinio.py: Script per estrarre le caratteristiche dai file pcap e salvarle su txt e json.

pcap_demo/: Cartella dove posizionare i file pcap da analizzare.

file_extract_demo/: Cartella dove verranno salvati i risultati dell'analisi.

- `README.md` → questo file

## Come usare il progetto
1. Accedere a virtualbox ed attivare la macchina di comnetsemu
2. Connettersi a github da macchina virtuale e scaricare il file network.py
3. Lanciare il comando: `sudo python3 network.py` 
4. Genera traffico e salva i file .pcap nella cartella `pcap_dumps/`
5. Trasferire i risultati nella cartella `pcap_dumps/` sul PC nella cartella pcap_demo/
6. Quindi utilizzare il file estrazione_features_tirocinio.py, una volta che questo codice finirà verranno salvati i file txt e json contenenti le metriche d'interesse all'interno della cartella `file_extract_demo`

## Esempi di risultati dei file pcap_demo già inseriti nella cartella


## Note

Il progetto è eseguito all’interno di una macchina virtuale con Comnetsemu e si basa sulla raccolta dati real-time generati tramite simulazione. Possibili estensioni del progetto includono l’uso di altri modelli predittivi e l’aggiunta di ulteriori metriche.

## Autori

Progetto sviluppato nell’ambito del corso universitario di networking 2 presso l'Università degli Studi di Trento.
>>>>>>> 28e1c7d3f8e940a8565a35a40442376331b749f6
