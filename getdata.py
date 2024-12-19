import requests

# Mengambil data dari URL
data = requests.get('http://192.168.49.37:1000/api/system/gate/status')

# Mengekstrak nilai dari 'StateGate_1' dan 'isAuto'
gate_status = data.json().get('StateGate_1', {})
is_auto = gate_status.get('isAuto', None)

print(is_auto)
#if is_auto is not None:
#    print(f"Status pintu otomatis: {'Aktif' if is_auto else 'Non-aktif'}")
#else:
#    print("Data tidak ditemukan atau format respons tidak sesuai.")
