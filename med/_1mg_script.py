import requests
import re

def get_medicine_info(medicine_name, city):
    base_url = "https://www.1mg.com/pwa-api/api/v4/search/all"
    params = {
        "q": medicine_name,
        "city": city,
        "filter": "",
        "page_number": 0,
        "scroll_id": "",
        "per_page": 10,
        "types": "sku,allopathy",
        "sort": "relevance",
        "fetch_eta": True,
        "is_city_serviceable": True
    }
    
    headers = {
        # 'Cookie': 'AWSALBTG=lCoPVF7Rd9sLy5ARb+jxRYjgETJEu1rT3Nz1ZrIzgm4YIlHIK7A6cvEp+L4NxbOYLesDtZllKP8eonwPgY/mwwjmWEV1FM4SDZmCrz2GHHMSktzRnAmiSntj2K4+paMNUEX/7s/QqkYe6ZGOAtDIrzap9kD1SLxQZ0s0PGkSA0Q7; AWSALBTGCORS=lCoPVF7Rd9sLy5ARb+jxRYjgETJEu1rT3Nz1ZrIzgm4YIlHIK7A6cvEp+L4NxbOYLesDtZllKP8eonwPgY/mwwjmWEV1FM4SDZmCrz2GHHMSktzRnAmiSntj2K4+paMNUEX/7s/QqkYe6ZGOAtDIrzap9kD1SLxQZ0s0PGkSA0Q7; _csrf=mqDrP_Og6Fep3ARiYLrJ-CR5'
        'Cookie': '...',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',

        'X-1mgLabs-Platform': 'mWeb',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?1',
        'X-Precise-Pincode': '',
        'X-Access-Key': '1mg_client_access_key',
        'Accept': 'application/vnd.healthkartplus.v4+json',
        'X-Polygon-Ids': '[\'670b9d009071201ff4632afa\', \'6692480cb2e5553ee8fd53b0\', \'6692480ce50b6b246aeb116d\', \'6692477ee50b6b246aeb112c\', \'669246a3910c9679c6f71fca\', \'669246a3e50b6b246aeb07c0\', \'66924436910c9679c6f715ed\', \'66924436b2e5553ee8fd41c0\', \'66853fe9b2e5553ee8fcf447\', \'668124aab2e5553ee8fcb228\', \'665727179e51468b1d574f58\', \'6656d6da85f79c5077e1f9b8\', \'664b65e985f79c5077e1d455\', \'663f073a4a26aaf78e9ea71f\', \'663db75117210da5fd8e0ba8\', \'662e6b3d4a26aaf78e991af5\', \'65f988371118eb86fadcd625\', \'65f19550b2a1fcb8f3ead9c3\', \'65f193b91118eb86fadbbad5\', \'65f192e44956847e4ffc13bd\', \'65f1923c4956847e4ffc13b1\', \'65f1917a4956847e4ffc07f1\', \'65969e535c0e2a405f108c61\', \'65785756342921cc23b87a04\', \'65545f5b342921cc23b79182\', \'654cbae1bffdf6f8f070bc98\', \'64afd7d3cd2e3d2da548aaf5\', \'64b3ed2dcd2e3d2da54ae447\', \'644a87bb1318ae8fbdcb6947\']',
        'locale': 'en',
        'X-Geodata-Latitude': '28.4433747',
        'x-platform': 'mobileweb-0.0.1',
        'x-csrf-token': 'CdPPMZCP-ejP6XAXuuJ42kBkYgkjp--jo6s8',
        'Referer': '',
        'HKP-Platform': 'Healthkartplus-0.0.1-mobileweb',
        'X-Geodata-Longitude': '77.100729',
        'X-City': f'{city}',
        'VISITOR-ID': '99a218b9-9ba7-4d4a-8dfd-c2baafe90bfb_FKcNSQwHNF_3447_1729076696801',
        'X-Visitor-Id': '99a218b9-9ba7-4d4a-8dfd-c2baafe90bfb_FKcNSQwHNF_3447_1729076696801',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36',
        # 'Cookie': 'AWSALBTG=lCoPVF7Rd9sLy5ARb+jxRYjgETJEu1rT3Nz1ZrIzgm4YIlHIK7A6cvEp+L4NxbOYLesDtZllKP8eonwPgY/mwwjmWEV1FM4SDZmCrz2GHHMSktzRnAmiSntj2K4+paMNUEX/7s/QqkYe6ZGOAtDIrzap9kD1SLxQZ0s0PGkSA0Q7; AWSALBTGCORS=lCoPVF7Rd9sLy5ARb+jxRYjgETJEu1rT3Nz1ZrIzgm4YIlHIK7A6cvEp+L4NxbOYLesDtZllKP8eonwPgY/mwwjmWEV1FM4SDZmCrz2GHHMSktzRnAmiSntj2K4+paMNUEX/7s/QqkYe6ZGOAtDIrzap9kD1SLxQZ0s0PGkSA0Q7; _csrf=mqDrP_Og6Fep3ARiYLrJ-CR5'
            
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Store search results in array
        search_results = []
        for result in data["data"]["search_results"]:
            if result["type"] == "drug" and result["available"]:
                search_results.append({
                    "id": result["id"],
                    "name": result["name"],
                    "label": result["label"],
                    "discounted_price": result["prices"]["discounted_price"],
                    "url": f"https://www.1mg.com{result['url']}"
                })

        # Match exact word
        matched_results = [result for result in search_results if re.search(r'\b' + re.escape(medicine_name) + r'\b', result["name"], re.IGNORECASE)]

        return matched_results[:5]

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return []
    except Exception as err:
        print(f'Other error occurred: {err}')
        return []
      
      
if __name__ == "__main__":
    medicine_name = "Dolo"
    city = "Delhi"
    results = get_medicine_info(medicine_name, city)
    print(results)