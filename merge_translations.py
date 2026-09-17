import json

def merge_translations(old_translated_path, new_english_extracted_path, output_path, log_missing=True):
    # 1. Carica la traduzione esistente (es. italiano)
    with open(old_translated_path, 'r', encoding='utf-8') as f:
        old_translation = json.load(f)

    # 2. Carica le nuove stringhe estratte in inglese (aggiornate)
    with open(new_english_extracted_path, 'r', encoding='utf-8') as f:
        new_english = json.load(f)

    merged_output = {}
    added_keys = []
    retained_keys_count = 0

    # Iteriamo sulla struttura del NUOVO file inglese per preservare l'ordine
    for key, english_text in new_english.items():
        # Se la chiave esisteva già nella vecchia traduzione, manteniamo il testo tradotto
        if key in old_translation:
            merged_output[key] = old_translation[key]
            retained_keys_count += 1
        else:
            # Se la chiave è nuova, usiamo il testo inglese come fallback
            merged_output[key] = english_text
            added_keys.append(key)

    # Salva il risultato unito
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_output, f, ensure_ascii=False, indent=4)

    # Stampa resoconto
    print("--- RISULTATO UNIONE TRADUZIONI ---")
    print(f" Stringhe mantenute dalla vecchia traduzione: {retained_keys_count}")
    print(f" Nuove chiavi aggiunte (in inglese): {len(added_keys)}")
    print(f" File salvato in: {output_path}")

    # Salva un log delle nuove chiavi da tradurre per comodità
    if log_missing and added_keys:
        log_file = "keys_to_translate.json"
        missing_dict = {k: new_english[k] for k in added_keys}
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(missing_dict, f, ensure_ascii=False, indent=4)
        print(f" Le {len(added_keys)} nuove chiavi da tradurre sono state salvate anche in '{log_file}'")


if __name__ == "__main__":
    merge_translations(
        old_translated_path="translated_strings_it.json",     # La tua traduzione esistente
        new_english_extracted_path="extracted_strings.json",  # Il nuovo file estratto dall'inglese
        output_path="translated_strings_updated.json",        # Il file finale unito
        log_missing=True                                      # Genera un file separato con solo le nuove righe
    )