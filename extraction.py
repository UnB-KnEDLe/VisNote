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

# recebe o input do usuário e o organiza
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

                xmls.append(temp_xml[1])
                i += 1

        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

def extract_annotations(xmls):
    tipos_atos = ['Ato_Abono_Permanencia','Ato_Aposentadoria','Ato_Cessao','Ato_Exoneracao_Comissionado','Ato_Exoneracao_Efetivo','Ato_Nomeacao_Comissionado','Ato_Nomeacao_Efetivo','Ato_Retificacao_Comissionado','Ato_Retificacao_Efetivo','Ato_Reversao','Ato_Substituicao','Ato_Tornado_Sem_Efeito_Apo','Ato_Tornado_Sem_Efeito_Exo_Nom']
    
    colunas_entidades = ['id_ato', 'id_dodf','num_doc_dodf','data_doc_dodf','tipo_rel', 'id_rel','anotador_rel','texto_rel','tipo_ent','id_ent', 'anotador_ent','texto_ent']
    df_entidades = pd.DataFrame(columns = colunas_entidades)
    dict_entidades= {'id_ato':'x','id_dodf':'x','num_doc_dodf':'x','data_doc_dodf':'x','tipo_rel':'x', 'id_rel':'x','anotador_rel':'x','texto_rel':'x','tipo_ent':'x','id_ent':'x', 'anotador_ent':'x','offset_ent':'x','length_ent':'x','texto_ent':'x',}
    
    colunas_relacoes = ['id_ato','tipo_rel','estado_rel','texto','entidades']
    df_relacoes = pd.DataFrame(columns = colunas_relacoes)
    dict_relacoes = {'id_ato':'x','tipo_rel':'x','estado_rel':'x','texto':'x','entidades':[]}

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
                    tipo_rel = info.text
                elif info.get('key') == 'annotator':
                    annotatorRel = info.text 

            # cria lista de ids de anotações
            ids_anno = []
            for info in rel.findall('node'):
                id_anno = info.get('refid')
                ids_anno.append(id_anno)

            # encontra texto principal da relação
            for id_anno in ids_anno: 
                # encontra e itera sobre todos os elementos annotation do xml
                for anno in root.findall("./document/passage/annotation"):
                    # para cada anotação definida por um id, coleta o tipo, anotador e texto
                    if anno.get('id') == id_anno:
                        # encontra tipo
                        for info in anno.findall('infon'):
                            if info.get('key') == 'type':
                                tipo = info.text
                                if tipo in tipos_atos:
                                    # encontra texto
                                    for info in anno.findall('text'):
                                        texto_rel = info.text 

            id_ato = id_dodf_text +'-'+ id_rel

            dict_relacoes["id_ato"] = id_ato
            dict_relacoes["tipo_rel"] = tipo_rel
            dict_relacoes["estado_rel"] = 'nao_confirmado'
            dict_relacoes["texto"] = texto_rel
            ids_entidades = []

            # loop na lista de ids
            for id_anno in ids_anno:
                # encontra e itera sobre todos os elementos annotation do xml
                for anno in root.findall("./document/passage/annotation"):
                    # para cada anotação definida por um id, coleta o tipo, anotador, offset, length e texto
                    if anno.get('id') == id_anno:
                        # encontra tipo e anotador
                        for info in anno.findall('infon'):
                            if info.get('key') == 'type':
                                tipo_ent = info.text
                            elif info.get('key') == 'annotator':
                                annotatorAnno = info.text
                        
                        # encontra texto
                        for info in anno.findall('text'):
                            texto_ent = info.text  
                        
                        
                        underscore_num_data = re.sub('^[^_]+(?=_)', '', id_dodf_text)
                        ponto_data = re.sub('^([^.])+(?=\.)', '', underscore_num_data)
                        index_inicio_data = underscore_num_data.find(ponto_data)
                        num_doc_dodf = underscore_num_data[1:index_inicio_data]
                        data_doc_dodf = ponto_data[1:]

                        id_geral = id_dodf_text + id_rel + id_anno
                        id_geral = re.sub('[^0-9]', '', id_geral)
                        dict_entidades["id_geral"] = id_geral  

                        ids_entidades.append(id_geral)                   
                        
                        dict_entidades["id_ato"] = id_ato    
                        dict_entidades["id_dodf"] = id_dodf_text  
                        dict_entidades["num_doc_dodf"] = num_doc_dodf
                        dict_entidades["data_doc_dodf"] = data_doc_dodf 
                        dict_entidades["tipo_rel"] = tipo_rel
                        dict_entidades["id_rel"] = id_rel
                        dict_entidades["anotador_rel"] = annotatorRel
                        dict_entidades["texto_rel"] = texto_rel
                        dict_entidades["tipo_ent"] = tipo_ent
                        dict_entidades["id_ent"] = id_anno
                        dict_entidades["anotador_ent"] = annotatorAnno
                        dict_entidades["texto_ent"] = texto_ent
                        dict_entidades["estado_ent"] = "nao_confirmado"

                        df_length = len(df_entidades)
                        df_entidades.loc[df_length] = dict_entidades

            dict_relacoes["entidades"] = ids_entidades
            df_relacoes_length = len(df_relacoes)
            df_relacoes.loc[df_relacoes_length] = dict_relacoes

    df_entidades.to_csv("./csv/lista_entidades.csv",index=False)   
    df_relacoes.to_csv("./csv/lista_relacoes.csv",index=False)  

    return df_entidades, df_relacoes        

# trata o input do usuário e retorna um dataframe
def extract_entidades(xmls):  
    colunas = ['id_geral', 'id_ato','id_dodf','tipo_rel', 'id_rel','anotador_rel','tipo_ent','id_ent', 'anotador_ent','texto','estado_ent']
    df = pd.DataFrame(columns = colunas)
    dictData={'id_dodf':'x','tipo_rel':'x', 'id_rel':'x','anotador_rel':'x','tipo_ent':'x','id_ent':'x', 'anotador_ent':'x','texto':'x','estado_ent':'x'}
    
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
                        dictData["id_ato"] = id_dodf_text + id_rel   
                        dictData["id_dodf"] = id_dodf_text   
                        dictData["tipo_rel"] = tipoRel
                        dictData["id_rel"] = id_rel
                        dictData["anotador_rel"] = annotatorRel
                        dictData["tipo_ent"] = tipoAnno
                        dictData["id_ent"] = id_anno
                        dictData["anotador_ent"] = annotatorAnno
                        dictData["texto"] = texto
                        dictData["estado_ent"] = "nao_confirmado"

                        df_length = len(df)
                        df.loc[df_length] = dictData

    df.to_csv("./csv/lista_entidades.csv",index=False)                            
    return df

def find_entidades(df,j):
    entidades = []
    i = 0
    while i < len(df.texto):
        if df.id_ato[i] == df.id_ato[j]:
            entidades.append(df.id_geral[i])
        i += 1
    return entidades

def extract_relacoes(df):
    tipos_atos = ['Ato_Abono_Permanencia','Ato_Aposentadoria','Ato_Cessao','Ato_Exoneracao_Comissionado','Ato_Exoneracao_Efetivo','Ato_Nomeacao_Comissionado','Ato_Nomeacao_Efetivo','Ato_Retificacao_Comissionado','Ato_Retificacao_Efetivo','Ato_Reversao','Ato_Substituicao','Ato_Tornado_Sem_Efeito_Apo','Ato_Tornado_Sem_Efeito_Exo_Nom']
    colunas = ['id_geral', 'id_ato','tipo_rel','estado_rel','texto','anotacoes']
    df_result = pd.DataFrame(columns = colunas)
    
    dictAux = {'id_geral':'x', 'id_ato':'x','tipo_rel':'x','estado_rel':'x','texto':'x','anotacoes':[]}

    i = 0
    while i < len(df.texto):
        if (len(df.texto[i]) > 0) and (df.tipo_ent[i] in tipos_atos):
            dictAux["id_geral"] = df.id_geral[i]    
            dictAux["id_ato"] = df.id_ato[i]
            dictAux["tipo_rel"] = df.tipo_rel[i]
            dictAux["estado_rel"] = 'nao_confirmado'
            dictAux["texto"] = df.texto[i]
            dictAux["anotacoes"] = find_entidades(df,i)
            df_length = len(df_result)
            df_result.loc[df_length] = dictAux
        i += 1
    df_result.to_csv("./csv/lista_relacoes.csv",index=False)  
    return df_result

# Organiza o output em uma tabela para mostrar ao o usuário as anotações que foram extraídas
def return_tables(xmls):
    df_entidades = extract_entidades(xmls)
    df_relacoes = extract_relacoes(df_entidades)

    #df_entidades, df_relacoes = extract_annotations(xmls)

    list_of_tables = []
        
    if df_entidades.shape[0] > 0 :
        #dff = df_entidades

        csv_string_entidades = df_entidades.to_csv(index=False, encoding='utf-8')
        csv_string_entidades = "data:text/csv;charset=utf-8," + \
            urllib.parse.quote(csv_string_entidades)

        csv_string_relacoes = df_relacoes.to_csv(index=False, encoding='utf-8')
        csv_string_relacoes = "data:text/csv;charset=utf-8," + \
            urllib.parse.quote(csv_string_relacoes)

        '''csv_string = dff.to_csv(index=False, encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8," + \
            urllib.parse.quote(csv_string)
       
        download_button = html.A(
            children=['Download CSV'],
            id='download-link',
            download="visnote_annotations.csv",
            href=csv_string,
            target="_blank")
        '''   
        list_of_tables.append(\
            html.Div([
                html.H2("Anotações de Entidades", className='text-act'),
                html.H4("Quantidade: " + str(df_entidades.shape[0]), className='text-ocu'),

                dash_table.DataTable(
                    data=df_entidades.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df_entidades.columns],
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
                html.A(
                    className = 'choose-button',
                    children=['Download CSV'],
                    id='download-link-entidades',
                    download="visnote_annotations_entidades.csv",
                    href=csv_string_entidades,
                    target="_blank"),
            ], className='card-csv')\
        )
        list_of_tables.append(\
            html.Div([
                html.H2("Anotações de Relações", className='text-act'),
                html.H4("Quantidade: " + str(df_relacoes.shape[0]), className='text-ocu'),

                dash_table.DataTable(
                    data=df_relacoes.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df_relacoes.columns],
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
                html.A(
                    className = 'choose-button',
                    children=['Download CSV'],
                    id='download-link-entidades',
                    download="visnote_annotations_entidades.csv",
                    href=csv_string_entidades,
                    target="_blank"),
            ], className='card-csv')\
        )
    else:
        list_of_tables.append(\
            html.Div([
                html.H2('Não foram encontradas anotações nos arquivos xml. Por favor, tente novamente.', className='text-act'),
            ], className='card-csv')\
        )

    return html.Div(list_of_tables)

# Função principal    
def extraction_callbacks(app):
    @app.callback(
        [
            Output('output-data-upload', 'children'),
            Output("loading-output-2", "children")
        ],
        [
            Input('upload-data', 'contents')
        ],
        [
            State('upload-data', 'filename'),
            State('upload-data', 'last_modified')
        ])
    def update_output(list_of_contents, list_of_names, list_of_dates):
        children = []
        if list_of_contents is not None:
            xmls = []
            organize_content(list_of_contents, list_of_names, list_of_dates,xmls)
            children = [return_tables(xmls)]
        return [children,0]