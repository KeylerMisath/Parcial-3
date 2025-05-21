import json, re, requests

regex = r'(\d{1,3}(?:\.\d{1,3}){3}) - - \[(\d{2}/[a-zA-Z]{3}/\d{4}):(\d{2}:\d{2}:\d{2}) .*?] "(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH) ([^ ]+) HTTP/\d\.\d" (\d{3})'

data = ""
for i in range(3): 
    ruta = fr"C:\Users\carol\Downloads\SotM34-anton\SotM34\http\access_log{'' if i == 0 else '.' + str(i)}"
    try:
        with open(ruta, "r", encoding="utf-8", errors="ignore") as file:
            data += file.read()
    except FileNotFoundError:
        continue

# Extraer datos
resultado = re.findall(regex, data)

# Diccionario para guardar ataques por país
ataques_por_pais = {}

# Cache de IPs geolocalizadas
cache_geolocalizacion = {}

# Procesar líneas extraídas
for ip, fecha, hora, metodo, ruta, codigo in resultado:
    if ip not in cache_geolocalizacion:
        try:
            resp = requests.get(f"http://ip-api.com/json/{ip}").json()
            if resp.get("status") == "success":
                pais = resp.get("country", "Desconocido")
            else:
                pais = "Desconocido"
        except:
            pais = "Desconocido"
        cache_geolocalizacion[ip] = pais
    else:
        pais = cache_geolocalizacion[ip]

    ataque = {
        "fecha": fecha,
        "método": metodo,
        "ruta": ruta
    }

    if pais not in ataques_por_pais:
        ataques_por_pais[pais] = []
    ataques_por_pais[pais].append(ataque)

# Reorganizar a estructura deseada
estructura_final = [{"Country": pais, "Attacks": ataques} for pais, ataques in ataques_por_pais.items()]

# Guardar JSON
with open("ataques_por_pais.json", "w", encoding="utf-8") as f:
    json.dump(estructura_final, f, indent=4, ensure_ascii=False)

# Imprimir en consola
print(json.dumps(estructura_final, indent=4, ensure_ascii=False))