import xml.etree.ElementTree as ET
import os
import csv
import pandas as pd
import types
import re

import base64
from base64 import b64decode
import datetime
import io
import tempfile
from urllib.parse import quote as urlquote
import urllib

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

correct_names = {
        'Ato_Abono_Permanencia': 'Abono de Permanência',
        'Ato_Aposentadoria': 'Aposentadoria',
        'Ato_Cessao': 'Cessão',
        'Ato_Exoneracao_Comissionado': 'Exoneração - Comissionado',
        'Ato_Exoneracao_Efetivo': 'Exoneração - Efetivo',
        'Ato_Nomeacao_Comissionado': 'Nomeação - Comissionado',
        'Ato_Nomeacao_Efetivo': 'Nomeação - Efetivo',
        'Ato_Retificacao_Comissionado': 'Retificação - Comissionado',
        'Ato_Retificacao_Efetivo': 'Retificação - Efetivo',
        'Ato_Reversao': 'Reversão',
        'Ato_Substituicao': 'Substituição',
        'Ato_Tornado_Sem_Efeito_Apo': 'Tornar sem efeito - Aposentadoria',
        'Ato_Tornado_Sem_Efeito_Exo_Nom': 'Tornar sem efeito - Exoneração e Nomeação',
        'todos_atos': 'Todos os atos'
}

def extrair_anotacoes(xmls):  
    colunas = ['id_geral', 'id_dodf_rel','id_dodf','tipo_rel', 'id_rel','anotador_rel','tipo_ent','id_ent', 'anotador_ent','texto']
    df = pd.DataFrame(columns = colunas)
    dictData={'id_dodf':'x','tipo_rel':'x', 'id_rel':'x','anotador_rel':'x','tipo_ent':'x','id_ent':'x', 'anotador_ent':'x','texto':'x'}
    
    roots = []
    for xml in xmls:
        tree = ET.parse(xml)
        root = tree.getroot()
        roots.append(root)
    
    for root in roots:
        # coleta id do dodf
        id_dodf = root.find("./document/id")
        id_dodf_text = id_dodf.text
        
        # cria lista de ids de relações
        ids_rel = []
        for rel in root.findall("./document/passage/relation"):
            id_rel = rel.get('id')
            ids_rel.append(id_rel)
            # coleta tipo e anotador da relação
            for info in rel.findall('infon'):
                if info.get('key') == 'type':
                    tipoRel = info.text
                elif info.get('key') == 'annotator':
                    annotatorRel = info.text           

            # cria lista de ids de anotações
            ids_anno = []
            for info in rel.findall('node'):
                id_anno = info.get('refid')
                ids_anno.append(id_anno)

            # loop na lista de ids
            for id_anno in ids_anno:
                # encontra e itera sobre todos os elementos annotation do xml
                for anno in root.findall("./document/passage/annotation"):
                    # para cada anotação definida por um id, coleta o tipo, anotador, offset, length e texto
                    if anno.get('id') == id_anno:
                        # encontra tipo e anotador
                        for info in anno.findall('infon'):
                            if info.get('key') == 'type':
                                tipoAnno = info.text
                            elif info.get('key') == 'annotator':
                                annotatorAnno = info.text
                        # encontra texto
                        for info in anno.findall('text'):
                            texto = info.text
                            
    
                        id_geral = id_dodf_text + id_rel + id_anno
                        id_geral = re.sub('[^0-9]', '', id_geral)
                            
                        dictData["id_geral"] = id_geral    
                        dictData["id_dodf_rel"] = id_dodf_text + id_rel   
                        dictData["id_dodf"] = id_dodf_text   
                        dictData["tipo_rel"] = tipoRel
                        dictData["id_rel"] = id_rel
                        dictData["anotador_rel"] = annotatorRel
                        dictData["tipo_ent"] = tipoAnno
                        dictData["id_ent"] = id_anno
                        dictData["anotador_ent"] = annotatorAnno
                        dictData["texto"] = texto

                        df_length = len(df)
                        df.loc[df_length] = dictData

    df.to_csv("lista_anotacoes.csv",index=False)                            
    return df

def organize_content(list_of_contents, list_of_names, list_of_dates,xmls):
    i = 0
    for contents, filename, date in zip(list_of_contents, list_of_names, list_of_dates):
        content_type, content_string = contents.split(',')

        content = b64decode(content_string, validate=True)
        try:
            if 'xml' in filename:
                temp_xml = tempfile.mkstemp(prefix=str(i), suffix='.xml')
                #
                temp_file = open(temp_xml[0], 'wb+')
                temp_file.write(content)
                #temp_xml.close()

                xmls.append(temp_xml[1])
                i += 1

        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

def return_tables(xmls):
    df = extrair_anotacoes(xmls)
    list_of_tables = []
        
    if df.shape[0] > 0 :
        dff = df
        csv_string = dff.to_csv(index=False, encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8," + \
            urllib.parse.quote(csv_string)

        download_button = html.A(
            children=['Download CSV'],
            id='download-link',
            download="annotations_teste.csv",
            href=csv_string,
            target="_blank")
            
        list_of_tables.append(\
            html.Div([
                html.H2("Anotações", className='text-act'),
                html.H4("Atos anotados: " + str(df.shape[0]), className='text-ocu'),

                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': '150px',
                            'height':'auto'
                    }, 
                    style_table={
                            'maxHeight': '700px',
                            'overflowY': 'auto',
                            'overflowX': 'auto',
                            'marginBottom': '40px'
                        }
                ),
                download_button,
            ], className='card-csv')\
        )
    else:
        list_of_tables.append(\
            html.Div([
                html.H2(correct_names[act_name], className='text-act'),
                html.H4("Atos anotados: " + str(df.shape[0]), className='text-ocu'),
            ], className='card-csv')\
        )

    return html.Div(list_of_tables)




'''
def extrair_entidades(xmls):
    df = pd.read_csv("_tsne_umap.csv")  
    roots = []
    info_atos = create_dictAtos()
    dictGerais = {'documento':'x','id':'x', 'anotador':'x', 'tipo':'x'}
    
    for xml in xmls:
        tree = ET.parse(xml)
        root = tree.getroot()
        roots.append(root)

    for root in roots:
        for documento in root.findall('document'):
            #dentro do documento
            for idx in documento.findall('id'):
                dictGerais['documento'] = idx.text
            for paragrafo in documento.findall('passage'):
                #dentro de cada parágrafo
                for relation in paragrafo.findall('relation'):
                    #dentro de cada relacao

                    dictGerais['id'] = relation.get('id')

                    num1= dictGerais['id']
                    num2= dictGerais['documento']
                    codigo = num1+num2
                    codigo = re.sub('[^0-9]', '', codigo)
                    X = [codigo]
                    indice = df[(df['cod'].isin(X))].index

                    tipo = df['tipo'][indice]
                    tipo = tipo.tolist()[0]
                    dictGerais['tipo'] = tipo 

                    for infon in relation.findall('infon'):
                        if infon.get('key') == 'annotator':
                            dictGerais['anotador'] = infon.text  

                    acharEntidades(tipo, info_atos[tipo]["atributos"], dictGerais, info_atos[tipo]["dataframe"],relation,paragrafo)
                    acharConteudo(tipo, dictGerais, info_atos["todos_atos"]["dataframe"],relation,paragrafo)

    all_dfs = {}

    for i in info_atos:
        all_dfs[i] = info_atos[i]["dataframe"]
    all_dfs["todos_atos"] = info_atos["todos_atos"]["dataframe"]
    
    
    return all_dfs

def return_entidades(xmls):
    acts_dfs = extrair_entidades(xmls)
    list_of_tables = []

    for act_name in acts_dfs:
        df = acts_dfs[act_name]
        
        if df.shape[0] > 0 :
            dff = df
            csv_string = dff.to_csv(index=False, encoding='utf-8')
            csv_string = "data:text/csv;charset=utf-8," + \
                urllib.parse.quote(csv_string)

            download_button = html.A(
                children=['Download CSV'],
                id='download-link',
                download="annotations_teste.csv",
                href=csv_string,
                target="_blank")
            
            list_of_tables.append(\
                html.Div([
                    html.H2(correct_names[act_name], className='text-act'),
                    html.H4("Atos anotados: " + str(df.shape[0]), className='text-ocu'),

                    dash_table.DataTable(
                        data=df.to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in df.columns],
                        style_cell={
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': '150px',
                            'height':'auto'
                        }, 
                        style_table={
                            'maxHeight': '700px',
                            'overflowY': 'auto',
                            'overflowX': 'auto',
                            'marginBottom': '40px'
                        }
                    ),
                    download_button,
                ], className='card-csv')\
            )
        else:
            list_of_tables.append(\
                html.Div([
                    html.H2(correct_names[act_name], className='text-act'),
                    html.H4("Atos anotados: " + str(df.shape[0]), className='text-ocu'),
                ], className='card-csv')\
            )

    return html.Div(list_of_tables)
'''