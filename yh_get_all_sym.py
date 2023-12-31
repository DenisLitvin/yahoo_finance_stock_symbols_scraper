import requests
import logging
import time
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, filename='yh_get_all_sym.log', 
    filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

hdr = {
    "authority": "finance.yahoo.com",
    "method": "GET",
    "scheme": "https",
    "accept": "text/html",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

def get_counts(body, srch):
    count_beg = body.find('Stocks (')
    #print(count_beg)
    rest = body[count_beg+8: count_beg+20]
    #print( rest)
    count_end = rest.find(')')
    #print(count_end)
    count_all = rest[0: count_end]
    logging.info('Counts: ' + srch + ' ' + str(count_all))
    return count_all

def call_url(url,hdr):
    confirmed = False
    while not confirmed:
        try:
            r = requests.get(url, headers=hdr)
            r.raise_for_status()

            confirmed = True
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            logging.warning("Http Error:" + str(errh))
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            logging.warning("Error Connecting" + str(errc.status_code))
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", str(errt.status_code))
            logging.warning("Timeout Error:" + errt)
        except requests.exceptions.RequestException as err:
            print("Something Other Request Error", err)
            logging.warning("Something Other Request Error" + str(err.status_code))

        if not confirmed:
            print("Waiting 1 sec to see if problem resolved then retry")
            time.sleep(1)

    return r.text


def process_block(body, srch, yh_all_sym, hdr):
    for block in range(0, 9999, 100):
        url = "https://finance.yahoo.com/lookup/equity?s=" + srch + "&t=A&b=" + str(block) + "&c=100"
        print('Processing: ', srch, block)
        logging.info('Processing: ' + srch + str(block))
        body = call_url(url,hdr)
        soup = BeautifulSoup(body, 'html.parser')
        links = soup.find_all('a')
        is_empty = True
        for link in links:
            if "/quote/" in link.get('href'):
                symbol = link.get('data-symbol')
                if symbol is not None:
                    is_empty = False
                    yh_all_sym.add(symbol)
        if is_empty:
            break


def main():
    search_set = []
    print(ord('0'), ord('9'), ord('A'), ord('Z'))

    for x in range(65, 91):
        search_set.append(chr(x))

    for x in range(48, 58):
        search_set.append(chr(x))

    yh_all_sym = set()

    term_1 = 0
    term_2 = 0
    term_3 = 0

    for term_1 in search_set:
        for term_2 in search_set:
            search_term = term_1 + term_2

            url = "https://finance.yahoo.com/lookup/equity?s=" + search_term + "&t=A&b=0&c=25"
            print("calling URL: ", url)

            global hdr
            hdr["path"]=url

            body = call_url(url,hdr)
            all_num = get_counts(body, search_term)
            all_num = int(all_num)
            print(search_term, 'Total:', all_num)

            if all_num < 9000:
                process_block(body, search_term, yh_all_sym,hdr)
            else:
                for term_3 in search_set:
                    search_term = term_1 + term_2 + term_3
                    url = "https://finance.yahoo.com/lookup/equity?s=" + search_term + "&t=A&b=0&c=25"
                    hdr["path"] = url

                    body = call_url(url, hdr)
                    all_num= get_counts(body, search_term)
                    all_num = int(all_num)
                    print(search_term, 'Total:', all_num)

                    if all_num < 9000:
                        process_block(body, search_term, yh_all_sym,hdr)
                    else:
                        for term_4 in search_set:
                            search_term = term_1 + term_2 + term_3 + term_4
                            process_block(body, search_term, yh_all_sym, hdr)

            print("Symbols stored so far: ", len(yh_all_sym))
        print("Symbols stored so far: ", len(yh_all_sym))
    print("Total symbols: ", len(yh_all_sym))

    f=open("yh_all_symbols.txt","w",encoding='UTF-8')
    f.write(str(yh_all_sym))
    f.close()

if __name__ == '__main__':
    main()
