from playwright.sync_api import sync_playwright
import json
import time

def extraer_eventos():
    with sync_playwright() as p:
        # Lanzar el navegador
        browser = p.chromium.launch(headless=True) # headless=False para ver el navegador
        context = browser.new_context()
        page = context.new_page()
        
        # Navegar a la página
        page.goto("https://streamtp3.com/eventos.html")
        
        # Esperar a que la página cargue (ajusta según sea necesario)
        page.wait_for_load_state("networkidle")
        
        # Abrir DevTools programáticamente no es posible directamente,
        # pero podemos ejecutar el código JavaScript para acceder a allEvents
        
        # Verificar si allEvents existe y guardarlo
        result = page.evaluate("""
        () => {
            // Intentar acceder a allEvents
            if (typeof allEvents !== 'undefined') {
                window.savedEvents = allEvents;
                return JSON.stringify(allEvents);
            } else {
                // Si no existe, esperar a que se cargue
                return new Promise((resolve) => {
                    // Crear un observer para detectar cuándo se crea allEvents
                    let checkExist = setInterval(() => {
                        if (typeof allEvents !== 'undefined') {
                            clearInterval(checkExist);
                            window.savedEvents = allEvents;
                            resolve(JSON.stringify(allEvents));
                        }
                    }, 100);
                    
                    // Timeout después de 10 segundos
                    setTimeout(() => {
                        clearInterval(checkExist);
                        resolve(null);
                    }, 10000);
                });
            }
        }
        """)
        
        # Si encontramos los datos, los guardamos
        if result:
            data = []
            for res in json.loads(result):
                if res['status']:
                    res.pop('status')
                    data.append(res)
            eventos = data
            with open('eventos_deportivos.json', 'w', encoding='utf-8') as f:
                json.dump(eventos, f, ensure_ascii=False, indent=2)
            print(f"Se han guardado {len(eventos)} eventos en eventos_deportivos.json")
        else:
            print("No se pudieron encontrar los eventos")
        
        # Cerrar el navegador
        browser.close()

if __name__ == "__main__":
    extraer_eventos()

arr = []