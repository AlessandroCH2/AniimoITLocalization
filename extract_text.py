import json
import struct

def extract_strings(json_map_path, bin_path, output_path):
    with open(json_map_path, 'r', encoding='utf-8') as f:
        text_map = json.load(f)
    
    extracted = {}
    
    with open(bin_path, 'rb') as bin_file:
        # Legge i primi 4 byte dell'header
        version_bytes = bin_file.read(4)
        # Converti i 4 byte in un intero a 32-bit (little-endian: '<I')
        version_num = struct.unpack('<I', version_bytes)[0]
        print(f"Versione rilevata nel file BIN: {version_num}")

        for key, value in text_map.items():
            if key.startswith('_'):
                continue
            
            offset, length = value[0], value[1]
            
            # Posiziona il cursore tenendo conto che il testo parte dall'offset specificato
            bin_file.seek(offset)
            raw_bytes = bin_file.read(length)
            
            text = raw_bytes.decode('utf-8', errors='replace')
            extracted[key] = text

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(extracted, f, ensure_ascii=False, indent=4)
        
    print(f"Estrazione completata! Create {len(extracted)} stringhe.")

if __name__ == "__main__":
    extract_strings("NewTextMap_en.json", "Compress_en.bin", "extracted_strings.json")