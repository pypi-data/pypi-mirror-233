import requests
import qbittorrentapi
import pandas
from tabulate import tabulate
import json
from multiprocessing.dummy import Pool as ThreadPool
import click 
global jackett_config
global qbit_config
jackett_config = {"api_key":"","url":"http://localhost:9117"}
qbit_config = {
    "host":"localhost",
    "port":"8080",
    "username":"admin",
    "password":"adminadmin"
}
@click.command()
@click.option("--api", help="jackett api key", required=True)
@click.option("--search", help="search term", required=True)
@click.option("--catagory", help="catagory", required=True)
def main(search,catagory,api):
    jackett_config["api_key"]=api
    t = search
    cat =catagory
    res = []
    def filter(i, catagory=cat):
        if i["catagory"] == catagory:
            return True
        else:
            return False


    def extract_info(i):
        item = {}
        item["Title"] = i["Title"]
        item["catagory"] = i["CategoryDesc"]
        item["source"] = i['Tracker']
        item["link"] = i["Link"]
        item["magnet"] = i["MagnetUri"]
        item["size"] = i["Size"]/1024/1024/1024
        item["size"] = round(item["size"], 2)
        item["size"] = f"{item['size']} GB"
        if item["magnet"] is not None:
            item["qbit"] = True
        else:
            item["qbit"] = False
        if filter(item):
            res.append(item)
    url = f"{jackett_config['url']}/api/v2.0/indexers/all/results?apikey={jackett_config['api_key']}&Query="
    qbt_client = qbittorrentapi.Client(**qbit_config)
    try:
        qbt_client.auth_log_in()
        print("connected to qbit")
    except qbittorrentapi.LoginFailed as e:
        print("login failed")
        exit()
    print("Searching for torrents..........")
    url=url+t
    r = requests.get(url)
    r = r.text
    r = json.loads(r)
    r = r["Results"]
    pool = ThreadPool(1000)
    pool.map(extract_info, (r))
    pool.close()
    pool.join()
    df = pandas.DataFrame(res)
    if df.empty:
        print("no results found")
        exit()
    else:
        print(tabulate(df.drop(["link","magnet"], axis=1), tablefmt="grid"))
        print("select the index no of the torrent to add to qbit")
        print("note:the torrent will be added to qbit only if it has a magnet link")
        print("1.Add Torrent:add index_no\n2.exit:exit")
        while True:
            i = input("enter the option :")
            if i == "exit":
                break
            elif i.startswith("add"):
                i = i.split(" ")
                i = i[1]
                i = int(i)
                if res[i]["qbit"]:
                    qbt_client.torrents_add(urls=res[i]["magnet"])
                    print("torrent added")
                else:
                    print("no magnet link")
            else:
                print("invalid option")

    qbt_client.auth_log_out()

        
if __name__ == "__main__":
    main()