from playwright.sync_api import sync_playwright
import json
import time
import supabase

def extraer_eventos():
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=True) # headless=False para ver el navegador
        context = browser.new_context()
        page = context.new_page()
        
        
        page.goto("https://streamtp3.com/eventos.html")
        
        
        page.wait_for_load_state("networkidle")
        
        # Abrir DevTools programáticamente no es posible directamente,
        # pero podemos ejecutar el código JavaScript para acceder a allEvents
        
        # Verificar si allEvents existe y guardarlo
        try:
            
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
        except BaseException as e:
            print(e, 'no se pudo extraer la data')
        
        
        if result:
            data = []
            for res in json.loads(result):
                if res['status']:
                    res.pop('status')
                    data.append(res)
            
            return data
        else:
            print("No se pudieron encontrar los eventos")
        
        
        browser.close()

def database():
    if len(extraer_eventos()) < 5:
        print('error al extraer la data en el scraping')
        return
    data = supabase.create_client(
        supabase_url="https://wbvkmekdjbapttseyrpx.supabase.co", 
                           supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndidmttZWtkamJhcHR0c2V5cnB4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjYxNjU4MywiZXhwIjoyMDU4MTkyNTgzfQ.vAWWknSAq4pHIuIlisyJzH8cOGQw44ceGsDxBDprp3w")

    try:

        r = data.from_('data_futbol').insert(json=extraer_eventos()).execute()
        print(r)
    except supabase.NotConnectedError as e:
        print(e, 'no se conecto')
    

def delete():
    data = supabase.create_client(
        supabase_url="https://wbvkmekdjbapttseyrpx.supabase.co", 
                           supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndidmttZWtkamJhcHR0c2V5cnB4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjYxNjU4MywiZXhwIjoyMDU4MTkyNTgzfQ.vAWWknSAq4pHIuIlisyJzH8cOGQw44ceGsDxBDprp3w")

    try:
        arr = data.from_('data_futbol').select('id').execute()
        rows = [x['id'] for x in arr.data]
        
        res = data.from_('data_futbol').delete().in_('id', rows).execute()
        if len(res.data) == 0:
            print('data eliminada', res.data)
        else:
            print('no se elimino al data')

    except supabase.AuthUnknownError as e:
        print(e)
    
if __name__ == "__main__":
    delete()
    time.sleep(30)
    database()
    
