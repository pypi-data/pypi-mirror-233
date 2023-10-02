#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Organiza os metadados da Pnadc.

pynad v3
Ipea - 2023
Rafael Guerreiro Osorio

ROTINAS QUE DEPENDEM DE COMO O IBGE DIVULGA METADADOS
"""
import json
import re
import time
import zipfile
from shutil import rmtree
from pathlib import Path
import xlrd
from .copia_local import COPIA_LOCAL, PNADCA, PNADCT, list_local_files
from .auxiliares import elapsed, pausar, CRCLR


DICTRI = 'dicionario_PNADC_microdados_trimestral.xls'


# pastas especificas no IBGE
TRIDOCS = 'Documentacao'
CA_DOCS = 'Documentacao'
CA_DATA = 'Dados'
CA_VIS = 'Visita'
CA_TRI = 'Trimestre'

# nome para pastas das cópias locais e paineis
META = 'metadados'
METALIST = 'pnadc.microdados.dicionarios.json'

# chaves dos dicionários de variáveis json
_VPART = 'parte'  # parte do registro: identificação e controle etc.
_VDESC = 'nome'  # nome da variável
_VPER = 'periodo'  # periodo
_VPOS = 'colunas'  # posição no arquivo COPIA_LOCALginal
_VSIZE = 'bytes'  # bytes necessários para o tipo de dado
_VCAT = 'valores'  # categCOPIA_LOCALas ou valores
_VQUES = 'quesito'  # número da questão para variáveis do questionário
_MISS = 'vazio'  # chave para "não aplicável" em _VCAT


def import_xls(xls):
    """Importa um dicionário de variáveis e retorna em texto TSV."""
    dicionario = xlrd.open_workbook(xls).sheet_by_index(0)
    rows = dicionario.nrows
    cols = dicionario.ncols
    tsv = ''
    for row in range(rows):
        for col in range(cols):
            try:
                datum = str(int(
                    dicionario.cell_value(row, col))).replace('\n', ' ')
            except ValueError:
                datum = str(
                    dicionario.cell_value(row, col)).replace('\n', ' ')
            tsv += datum + '\t'
        tsv = tsv[:-1] + '\n'
    return tsv


def generate(folder):
    """Gera ou atualiza os metadados."""
    print('METADADOS\n')
    start = time.time()
    # é mais prático remover e gerar
    # os metadados do que atualizá-los
    try:
        rmtree(Path(folder, META))
    except FileNotFoundError:
        pass
    finally:
        Path(folder, META).mkdir()
    arquivos = [str(Path(folder, COPIA_LOCAL, arq['path'], arq['name']))
                for arq in list_local_files(folder)]
    anuais = metadata_pnadc_anual(folder, arquivos, start)
    trimestrais = metadata_pnadc_trimestral(folder, arquivos, start)
    microdados = []
    for anual in anuais:
        processados = []
        target = Path(folder, META, Path(anual[1]).name)
        if anual[1] not in processados:
            processados.append(anual[1])
            with open(anual[1], 'rb') as src:
                with open(target, 'wb') as tgt:
                    tgt.write(src.read())
        if anual[2][0] not in processados:
            processados.append(anual[2][0])
            with open(anual[2][0], 'w', encoding='utf-8') as tgt:
                tgt.write(json.dumps(anual[2][1]))
        microdados.append((anual[0], anual[1], anual[2][0]))
    if trimestrais:
        with open(trimestrais[0][2][0], 'w', encoding='utf-8') as tgt:
            tgt.write(json.dumps(trimestrais[0][2][1]))
        for tri in trimestrais:
            microdados.append((tri[0], tri[1], tri[2][0]))
        target = Path(folder, META, METALIST)
        with open(target, 'w', encoding='utf-8') as tgt:
            tgt.write(json.dumps(microdados))
    print(f'{CRCLR}Metadados gerados em {elapsed(start)}\n')
    pausar()


def metadata_pnadc_anual(folder, arquivos, start):
    """
    Extrai e organiza metadados da pnadc anual.

    Esta rotina depende de como o IBGE organiza os
    arquivos para divulgação

    Em dezembro de 2019 a estrutura de disseminação da pnadc
    anual mudou radicalmente

    Há pastas para:
     - 5 visitas (dicionario por visita e por ano)
     - 4 trimestres (dicionário por trimestre vale para todos os anos)
    """
    microdados = metadata_pnadc_anual_arquivos(folder, arquivos)
    for microdado in microdados:
        print(f'{CRCLR}Gerando metadados {elapsed(start)}', end='')
        # lê o dicionário correspondente
        dicionario = metadata_pnadc_vars(import_xls(microdado[1]))
        nome = Path(microdado[0]).name
        if 'trimestre' in nome:
            dicid = nome[:-4].split('_')[2]
        else:
            dicid = '.'.join((nome[:-4].split('_')[2],
                              nome[:-4].split('_')[1]))
        target = f'pnadc.variaveis.anual.{dicid}.json'
        microdado[2] = [str(Path(folder, META, target)), dicionario]
    return microdados


def metadata_pnadc_anual_arquivos(folder, arquivos):
    """Identifica arquivos de microdados anuais."""
    microdados = []
    for vis in range(1, 6):
        datafolder = Path(folder, COPIA_LOCAL, PNADCA, CA_VIS,
                          f'{CA_VIS}_{vis}', CA_DATA)
        docsfolder = Path(folder, COPIA_LOCAL, PNADCA, CA_VIS,
                          f'{CA_VIS}_{vis}', CA_DOCS)
        docfiles = [item for item in arquivos
                    if str(docsfolder) in item
                    and 'dicionario' in item
                    and item.endswith('xls')]
        datafiles = [item for item in arquivos
                     if str(datafolder) in item
                     and item.endswith('zip')]

        # relaciona arquivos de microdados com dicionarios de variaveis
        for doc in docfiles:
            anodoc = Path(doc).name.split('_')[3]
            microdados.extend([[item, doc, '', PNADCA]
                               for item in datafiles
                               if (Path(item).name.split('_')[1]
                                   == anodoc and f'{CA_VIS.lower()}{vis}'
                                   in item) or
                               (Path(item).name.split('_')[1]
                                in ('2013', '2014') and
                                f'{CA_VIS.lower()}{vis}'
                                in item and anodoc == '2012')])
    for tri in range(1, 5):
        datafolder = Path(folder, COPIA_LOCAL, PNADCA, CA_TRI,
                          f'{CA_TRI}_{tri}', CA_DATA)
        docsfolder = Path(folder, COPIA_LOCAL, PNADCA, CA_TRI,
                          f'{CA_TRI}_{tri}', CA_DOCS)
        docfiles = [item for item in arquivos
                    if str(docsfolder) in item
                    and 'dicionario' in item
                    and item.endswith('xls')]
        datafiles = [item for item in arquivos
                     if str(datafolder) in item
                     and item.endswith('zip')]
        if docfiles:
            doc = docfiles[0]
            microdados.extend([[item, doc, '', PNADCA]
                               for item in datafiles])
    return microdados


def metadata_pnadc_trimestral(folder, arquivos, start):
    """
    Extrai e organiza metadados da pnadc trimestral.

    Esta rotina depende de como o IBGE organiza os
    arquivos para divulgação
    """
    # apenas um dicionário para a pnadc trimestral
    archive = [file for file in arquivos if
               all(stub in file for stub
                   in (COPIA_LOCAL, PNADCT, TRIDOCS,
                       'Dicionario_e_input'))][0:1]
    if not archive:
        return []
    with zipfile.ZipFile(archive[0]) as zpf:
        zpf.extract(DICTRI, str(Path(folder, META)))
    dicionario = metadata_pnadc_vars(import_xls(
        str(Path(folder, META, DICTRI))))
    target = str(Path(folder, META, 'pnadc.variaveis.trimestral.json'))

    # lista com os arquivos de microdados trimestrais
    microdados = [[arq, str(Path(folder, META, DICTRI)),
                   [target, dicionario], PNADCT]
                  for arq in arquivos
                  if COPIA_LOCAL in arq and PNADCT in arq and
                  any(parte.isnumeric() for parte in Path(arq).parts)]
    print(f'{CRCLR}Gerando metadados {elapsed(start)}', end='')
    return microdados


def metadata_pnadc_vars(contents):
    """Depende da estrutura dos dicionários de variáveis."""
    def __clean_label(label):
        label = label.replace('"', '').strip()
        label = label.replace('\n', ' ')
        label = re.sub(' +', ' ', label)
        try:
            label = int(float(label))
        except ValueError:
            pass
        return label

    def __set_bytes(size):
        # dtype bytes para armazenar 9 * colunas da var
        # C signed numeric types
        # 99 - 1 byte
        # 9999 - 2 bytes
        # 999999999 - 4 bytes - float ou int
        # >999999999 - 8 bytes - double ou long
        # pnadc pesos são floats - code 15
        bts = 'ERROR'
        if size <= 2:
            bts = 1
        elif size <= 4:
            bts = 2
        elif size <= 9:
            bts = 4
        elif size <= 14:
            bts = 8
        elif size == 15:
            bts = 15
        return bts

    # meta é o dicionário de variáveis
    meta = {}
    curvar = None

    # seção do questionário
    parte = ''

    # pula linhas de cabeçalho e processa
    rows = contents.split('\n')[3:-1]
    for row in rows:

        # line breaks, double spaces e outras coisas
        # limpar campos para processar linhas
        fields = [__clean_label(field) for field in row.split('\t')]

        # linha com informação de "parte" do questionário
        if fields[0] and not fields[1]:
            parte = fields[0].lower()

        # linha principal de variável
        elif all(isinstance(field, int)
                 for field in (fields[0], fields[1])):

            # código (uf, v1008 etc) é a chave em meta
            curvar = fields[2].lower()
            meta[curvar] = {}

            # parte atual
            meta[curvar][_VPART] = parte

            # tuple com:
            # coluna inicial - index em 1
            # coluna final
            # número de colunas
            meta[curvar][_VPOS] = (fields[0],
                                   fields[0] + fields[1] - 1,
                                   fields[1])

            meta[curvar][_VSIZE] = __set_bytes(meta[curvar][_VPOS][2])

            # número do quesito (se tiver)
            meta[curvar][_VQUES] = fields[3]

            # descrição da variável
            meta[curvar][_VDESC] = fields[4].lower()
            if not meta[curvar][_VDESC]:
                meta[curvar][_VDESC] = curvar

            # período
            meta[curvar][_VPER] = fields[7].lower()

            # tem campo 5 - categórica ou info adicional
            meta[curvar][_VCAT] = {}
            especial = (' a ', 'código', 'valor', '130', '01-')
            if (isinstance(fields[5], int)
                    or any(item in fields[5].lower() for item in especial)):
                meta[curvar][_VCAT][fields[5]] = str(fields[6]).lower()
            elif fields[5] or fields[6]:
                meta[curvar][_VCAT] = ', '.join([item.lower()
                                                 for item in fields[5:7]
                                                 if item])

        # linha de categCOPIA_LOCALa
        elif not fields[0] and not fields[1]:
            if not fields[5]:
                fields[5] = _MISS
            try:
                meta[curvar][_VCAT][fields[5]] = fields[6].strip().lower()
            except TypeError:
                # INSPECIONAR AQUI SE ESTIVEREM FALTANDO CATEGCOPIA_LOCALAS
                # print(curvar, fields)
                pass
    return meta


def csv_name(file, keep_ext=False):
    """Retorna o nome do arquivo a partir do original e tipo de pnad."""
    name = str(Path(file).name)
    # originalmente era só csv, mas podem ser zip ou parquet
    ext = name[-name[::-1].find('.'):]
    if str(Path(COPIA_LOCAL, PNADCA)) in file:
        stub = '.'.join((name[:-4].split('_')[2],
                         name[:-4].split('_')[1]))
        pnad = PNADCA
    else:
        stub = name[:-4].split('_')
        stub = f'{stub[1][2:]}.{stub[1][1]}'
        pnad = PNADCT
    if keep_ext:
        return f'pnadc.microdados.{pnad}.{stub}.{ext}'
    return f'pnadc.microdados.{pnad}.{stub}.csv'
