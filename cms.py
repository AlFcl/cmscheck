# Este script fue creado por alf.cl (github.com/alfcl)
import requests
import argparse
from colorama import Fore, Style, init
import json
from datetime import datetime

# Inicializar colorama
init()

# Máscara del user agent para que no se muestre como python y sea bloqueado
user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/53.0.2785.116 Safari/537.36',
}

def get(websiteToScan):
    try:
        return requests.get(websiteToScan, allow_redirects=False, headers=user_agent)
    except requests.RequestException:
        return None

def verificar_cms(websiteToScan, cms_name, paths, text_check, additional_checks=None):
    for path in paths:
        check = get(websiteToScan + path)
        if check and check.status_code == 200 and text_check in check.text:
            return True, f"[!] Detectado: {cms_name} en {websiteToScan + path}"
    if additional_checks:
        for path, text in additional_checks:
            check = get(websiteToScan + path)
            if check and check.status_code == 200 and text in check.text:
                return True, f"[!] Detectado: {cms_name} en {websiteToScan + path}"
    return False, f" |  No detectado: {cms_name}"

def obtener_certificado(url):
    try:
        cert = ssl.get_server_certificate((url, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        fecha_vencimiento = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
        fecha_creacion = datetime.strptime(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
        return fecha_creacion.strftime('%Y-%m-%d'), fecha_vencimiento.strftime('%Y-%m-%d')
    except Exception as e:
        return None, None

def guardar_resultados(resultados):
    with open('resultados.json', 'w', encoding='utf-8') as file:
        json.dump(resultados, file, ensure_ascii=False, indent=4)

# Iniciar escaneo
def escanear():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sitio", help="Usa esta opción para especificar el dominio o IP a escanear.")
    args = parser.parse_args()
    if args.sitio is None:
        print("Por favor, ingresa el sitio o IP que deseas escanear a continuación.")
        print("Ejemplos - www.sitio.com, https://tienda.org/magento, 192.168.1.50")
        websiteToScan = input('Sitio a escanear: ')
    else:
        websiteToScan = args.sitio

    if websiteToScan.startswith('http://'):
        proto = 'http://'
        websiteToScan = websiteToScan[7:]
    elif websiteToScan.startswith('https://'):
        proto = 'https://'
        websiteToScan = websiteToScan[8:]
    else:
        proto = 'http://'

    if websiteToScan.endswith('/'):
        websiteToScan = websiteToScan.rstrip('/')

    websiteToScan = proto + websiteToScan

    print("\n[+] Verificando si el sitio está en línea...")

    onlineCheck = get(websiteToScan)
    if not onlineCheck:
        print(f"[!] {websiteToScan} parece estar fuera de línea.")
        return

    resultados = []
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fecha_creacion, fecha_vencimiento = obtener_certificado(websiteToScan)

    if onlineCheck.status_code in [200, 301, 302]:
        print(f" |  {websiteToScan} parece estar en línea.")
        print("\nIniciando escaneo...\n")
        print("[+] Verificando si el sitio está redirigiendo...")
        redirectCheck = requests.get(websiteToScan, headers=user_agent)
        if len(redirectCheck.history) > 0 and (redirectCheck.history[0].status_code in [301, 302]):
            print("[!] El sitio ingresado parece estar redirigiendo, ¡por favor verifica el sitio de destino para asegurar resultados precisos!")
            print(f"[!] Parece que el sitio está redirigiendo a {redirectCheck.url}")
        elif 'meta http-equiv="REFRESH"' in redirectCheck.text:
            print("[!] El sitio ingresado parece estar redirigiendo, ¡por favor verifica el sitio de destino para asegurar resultados precisos!")
        else:
            print(" | El sitio no parece estar redirigiendo...")
    else:
        print(f"[!] {websiteToScan} parece estar en línea pero devolvió un error {onlineCheck.status_code}.\n")
        return

    print("\n[+] Intentando obtener los encabezados HTTP...")
    for header in onlineCheck.headers:
        try:
            print(f" | {header} : {onlineCheck.headers[header]}")
        except Exception as ex:
            print(f"[!] Error: {str(ex)}")

    ####################################################
    # Escaneos de CMS y Frameworks
    ####################################################

    escaneos = [
        ("WordPress", 
         ["/wp-login.php", "/wp-admin", "/wp-admin/upgrade.php", "/readme.html", 
          "/wp-json/", "/wp-content/plugins/", "/wp-content/themes/", "/wp-content/uploads/", "/license.txt"], 
         "wp-",
         [("/wp-includes/js/wp-emoji-release.min.js", "wp-emoji"), ("/wp-comments-post.php", "wp-comments-post")]),
        ("Joomla", ["/administrator/", "/readme.txt", "/media/com_joomlaupdate/"], "joomla", None),
        ("Magento", ["/index.php/admin", "/RELEASE_NOTES.txt", "/js/mage/cookies.js", "/skin/frontend/default/default/css/styles.css", "/errors/design.xml"], "mage", None),
        ("Drupal", ["/readme.txt", "/core/COPYRIGHT.txt", "/modules/README.txt"], "drupal", None),
        ("Shopify", ["/admin"], "shopify", None),
        ("Odoo", ["/web/login", "/web"], "odoo", None),
        ("Bsale", ["/bsale"], "bsale", None),
        ("Django", ["/admin"], "csrfmiddlewaretoken", None),
        ("Flask", ["/"], "flask", None),
        ("Ruby on Rails", ["/"], "rails", None),
        ("Laravel", ["/"], "laravel", None),
        ("React", ["/"], "react", [("/", "ReactDOM.render")])
    ]

    cms_detectado = False
    for cms_name, paths, text_check, additional_checks in escaneos:
        detectado, resultado = verificar_cms(websiteToScan, cms_name, paths, text_check, additional_checks)
        print(f"{Fore.GREEN if detectado else Fore.RED}{resultado}{Style.RESET_ALL}")
        if detectado:
            cms_detectado = True
            resultados.append({
                "dominio": websiteToScan,
                "respuesta": resultado,
                "fecha": fecha_actual,
                "detectado": detectado,
                "cms": cms_name,
                "certificado_creacion": fecha_creacion,
                "certificado_vencimiento": fecha_vencimiento
            })
            break

    if not cms_detectado:
        resultados.append({
            "dominio": websiteToScan,
            "respuesta": "No se detectó CMS",
            "fecha": fecha_actual,
            "detectado": False,
            "cms": "No detectado",
            "certificado_creacion": fecha_creacion,
            "certificado_vencimiento": fecha_vencimiento
        })

    guardar_resultados(resultados)
    print("\n¡Escaneo completo! Los resultados se han guardado en 'resultados.json'\n")

escanear()