import json
import struct

def rebuild_files(original_map_path, translated_json_path, new_bin_path, new_map_path, version_number=1789637180):
    with open(original_map_path, 'r', encoding='utf-8') as f:
        original_map = json.load(f)
        
    with open(translated_json_path, 'r', encoding='utf-8') as f:
        translated_texts = json.load(f)

    new_text_map = {}
    
    # Copia o imposta i metadati speciali
    for key, value in original_map.items():
        if key.startswith('_'):
            new_text_map[key] = value
            
    # Forziamo il valore di versione nel JSON
    new_text_map["_version"] = version_number

    # L'offset del testo inizia a 4 byte dopo l'header della versione
    current_offset = 4
    
    with open(new_bin_path, 'wb') as bin_out:
        # 1. Scrittura dei 4 byte della versione nell'header (Unsigned Int 32-bit, little-endian)
        version_bytes = struct.pack('<I', version_number)
        bin_out.write(version_bytes)
        
        # 2. Scrittura di tutte le stringhe
        for key, text in translated_texts.items():
            text_bytes = text.encode('utf-8')
            length = len(text_bytes)
            
            bin_out.write(text_bytes)
            
            # Salviamo l'offset effettivo nel nuovo JSON
            new_text_map[key] = [current_offset, length]
            
            current_offset += length

    # Aggiorna eventuale contatore
    if "_count" in new_text_map:
        new_text_map["_count"] = len(translated_texts)

    with open(new_map_path, 'w', encoding='utf-8') as f:
        json.dump(new_text_map, f, ensure_ascii=False, indent=4)
        
    print(f"Ricostruzione completata!")
    print(f"- Versione usata: {version_number}")
    print(f"- File creati: {new_bin_path} e {new_map_path}")

if __name__ == "__main__":
    rebuild_files(
        original_map_path="NewTextMap_en.json",
        translated_json_path="translated_strings_it.json",
        new_bin_path="Compress_en_new.bin",
        new_map_path="NewTextMap_en_new.json",
        version_number=1789637180
    )