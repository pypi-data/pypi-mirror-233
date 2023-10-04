
########################################
from rpa_coop import Dados, Sms, Whatsapp, gerador_pwd
sms = Sms()
dados = Dados()
whatsapp = Whatsapp()     
import time, requests, json

# rpa_hist_envio_whatsapp
# rpa_hist_envio_sms
# rpa_hist_sem_optin_whatsapp

# 1 - ler a planilha base de envia whatsapp
# 2 - remover (traço, ponto, parenteses) e validar se o numero é celular, se for e nao possui o 9 entao o rpa add o nove
# 3 - caso nao seja celular, ou nao tenha o ddd remove da lista
# 4 - validar se o numero possui optin 
# 5 - caso nao tenha optin add o celular na tabela rpa_hist_sem_optin_whatsapp, e envia sms
# 6 - caso possui optin, envia a mensagem whatsapp e add na tabela rpa_hist_envio_whatsapp
# 7 - atualizar status de entregas whatsapp na tabela rpa_hist_envio_whatsapp
# 8 - consultar a tabela rpa_hist_envio_whatsapp where combinando estas colunas... area_solicitante, msg_enviada, data_registro, processo_fluid, cod_rpa
# 9 - enviar relatorio mensagens entregues para o solicitante

url_api_whats = str(gerador_pwd('url_api_whats', 'ip_host'))
token_api_whats = str(gerador_pwd('url_api_whats', 'senha'))


def gravar_hist_envio_msg(conexao_db_fluid, id_de_envio:str, num_celular:str, msg_enviada:str, canal_envio:str, area_solicitante:str, campanha_produto:str = 'NULL', processo_fluid:str = 'NULL', cod_rpa:str = 'NULL'):
    try:            
        query = f'''INSERT INTO rpa_central_mensagens(id_de_envio, num_celular, msg_enviada, canal_envio, area_solicitante, campanha_produto) 
                    VALUES("{id_de_envio}", "{num_celular}", "{msg_enviada}", "{canal_envio}", "{area_solicitante}", "{campanha_produto}")'''
        if processo_fluid != 'NULL' or cod_rpa != 'NULL': 
            query = f'''INSERT INTO rpa_central_mensagens(id_de_envio, num_celular, msg_enviada, canal_envio, area_solicitante, campanha_produto, processo_fluid, cod_rpa) 
                    VALUES("{id_de_envio}", "{num_celular}", "{msg_enviada}", "{canal_envio}", "{area_solicitante}", "{campanha_produto}", "{processo_fluid}", "{cod_rpa}")'''
            
        dados.insert_banco_dados(conexao_db_fluid, query)
    except:
        raise Exception(f'Erro ao inserir numero {num_celular} na tabela rpa_central_mensagens')
        
        

def atualizar_status_entregas_whatsapp(conexao_db_fluid, data_registro='opcional ano-mes-dia'):
        try:
            if data_registro == 'opcional ano-mes-dia':
                consulta = f'''SELECT * FROM rpa_central_mensagens WHERE status_msg="consultar_id_de_envio" AND canal_envio="whatsapp" '''
            else:
                consulta = f'''SELECT * FROM rpa_central_mensagens WHERE status_msg="consultar_id_de_envio" AND canal_envio="whatsapp" AND data_registro like "{data_registro}%"'''
                
            df = dados.consultar_banco_dados(conexao_db_fluid, consulta)
            
            print('buscando status de entrega das mensagens whatsapp...')
            for line in df.itertuples():
                try:
                    id_msg = str(line.id_de_envio)
                    url = f'{url_api_whats}/notification/{id_msg}'
                    headers = {"Content-Type": "application/json; API Key", "x-api-key": token_api_whats}
                    # Get status da mensagem pela API através do ID da mensagem
                    resposta = requests.get(url, headers = headers)
                    # print(resposta.text)
                    # Extraindo o motivo da não entrega, caso a mensagem possua status de erro ou não.
                    if json.loads(resposta.text).get('error'):
                        status = json.loads(resposta.text).get('errors')[0]
                        status_entrega = status.get('message')
                    else:
                        status_entrega =  'Mensagem enviada'
                    query_update = f'''UPDATE rpa_central_mensagens SET status_msg="{status_entrega}" WHERE id_de_envio="{id_msg}"'''
                    dados.update_banco_dados(conexao_db_fluid, query_update)
                except Exception as e:
                    print(f'Erro ao consultar status de entrega a mensagem id {id_msg}. Erro: {str(e)}.')
        except Exception as e:
            raise Exception(f'Erro ao consultar status de entrega de uma ou mais mensagens whats. Erro: {str(e)}.')


conex = dados.criar_conexao('fluid')

celulares = ['1983504100', '4498623103']

# for celular in celulares:
#     celular = whatsapp.validar_ajustar_celular(celular)
#     mensagem = 'teste1 02-10-2023'
#     area_solicitante = 'seguros'
#     campanha_produto = 'renovacao seguros'
#     id_msg = '37a6353244-f5ca-40f9-acc1-d9aa45220001'

#     if not celular: continue 
#     gravar_hist_envio_msg(conex, id_msg, celular, mensagem, 'whatsapp', area_solicitante, campanha_produto, cod_rpa='56700')
    
 
    # enviou_esta_msg_hoje = whatsapp.validar_se_msg_whats_ja_enviou_hoje(conex, celular, mensagem)
    # if enviou_esta_msg_hoje: continue

    # status_code = whatsapp.verificar_opt_in(celular)
    
    # if status_code != 200:
    #     whatsapp.add_hist_sem_optin_whatsapp(conex, celular)
    #     print('nao possui optin, enviando sms...')
    #     status_code, response, id_sms = sms.enviar_SMS(celular, mensagem, return_list=True)
    #     sms.add_hist_envio_sms(conex, id_sms, celular, mensagem , area_solicitante, campanha_produto, cod_rpa='56800')
    # else:
    #     status_code, response, id_msg = whatsapp.enviar_texto_whatsapp(celular, area_solicitante, mensagem, return_list=True)
    #     if status_code == 200:
    #         whatsapp.add_hist_envio_whatsapp(conex, id_msg, celular, mensagem , area_solicitante, campanha_produto, cod_rpa='56800')
    #         print('enviado com sucesso')
        



# atualizar_status_entregas_whatsapp(conex)   



# atualizar status de entregas zap
# time.sleep(5)
# whatsapp.atualizar_status_entregas_whatsapp(conex)
# celular = '19983504100'
# mensagem = 'teste de hoje 6'
# area_solicitante = 'marketing'
# campanha_produto = 'poupança premiada'
# status_code, response, id_sms = sms.enviar_SMS(celular, mensagem, return_list=True)
# sms.add_hist_envio_sms(conex, id_sms, celular, mensagem , area_solicitante, campanha_produto, cod_rpa='56800')
# print()
    






