import requests
import jsons
import pandas as pd

def main():
    print("Estabelecendo conexão com o link...")
    response = requests.get("http://dadosabertos.ibama.gov.br/dados/SICAFI/AC/Quantidade/multasDistribuidasBensTutelados.json")
    if response.status_code == 200:
        print("Conectado...")
        list_of_processes = response.json()
        amount = len(list_of_processes['data'])
        print("Foram encontrados %d processos..." %amount)
        #criando listas vazias
        list_municipio = []
        list_nomeRazaoSocial = []
        list_valorAuto = []
        list_dataAuto = []
        list_situcaoDebito = []
        #criando uma lista de categorias que vão ser utilizadas
        categories = ["Fauna", "Flora", "Pesca", "Outras"]
        #category é criado no momento da execução for
        for category in categories:
            print("Acessando multas sobre %s ..." % category)
            # process é criado no momento da execução for
            # tradução: para processo em lista de processo, se process é tipoInfração dentro de categoria
            for process in list_of_processes['data']:
                print(process)
                if process["tipoInfracao"] == category:
                    list_municipio.append(process["municipio"])
                    list_nomeRazaoSocial.append(process["nomeRazaoSocial"])
                    list_valorAuto.append(process["valorAuto"])
                    list_dataAuto.append(process["dataAuto"])
                    list_situcaoDebito.append(process["situcaoDebito"])
            #transpose tabela
            row = {'municipio': list_municipio, 'nomeRazaoSocial': list_nomeRazaoSocial,
               'valorAuto': list_valorAuto, 'dataAuto': list_dataAuto, 'situcaoDebito': list_situcaoDebito}
            df = pd.DataFrame(row,columns=['municipio', 'nomeRazaoSocial', 'valorAuto', 'dataAuto', 'situcaoDebito'])
            df.to_csv('%s.csv' % category)
            print("Multas relacionadas a %s foram salvas na tabela!" % category)
            #é preciso limpar as listas antes de começar o segundo csv
            list_municipio.clear()
            list_nomeRazaoSocial.clear()
            list_valorAuto.clear()
            list_dataAuto.clear()
            list_situcaoDebito.clear()

    else:
        print("Site com algum problema")

if __name__ == "__main__":
    main()

