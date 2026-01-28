import requests, json, time
import supabase



def scraper():
    
    try:
        
        url = 'https://streamtp10.com/eventos.json'
        arr = []
        res = requests.get(url=url)
        res.encoding = 'utf-8'
        for data in json.loads(res.text):
            del data['language']
            del data['status']
            arr.append(data)
        return arr

    except ConnectionError as e:
        print('conexion a url fallida', e)


def database():
    if len(scraper()) < 5:
        print('error >> la longitud de la data es 0')
        return
    data = supabase.create_client(
        supabase_url="https://wbvkmekdjbapttseyrpx.supabase.co", 
                           supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndidmttZWtkamJhcHR0c2V5cnB4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjYxNjU4MywiZXhwIjoyMDU4MTkyNTgzfQ.vAWWknSAq4pHIuIlisyJzH8cOGQw44ceGsDxBDprp3w")

    try:

        r = data.from_('data_futbol').insert(json=scraper()).execute()
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
        
        print('data eliminada =>>' , len(res.data))
       

    except supabase.AuthUnknownError as e:
        print(e)



if __name__ == '__main__':
    delete()
    time.sleep(5)
    scraper()
    database()
