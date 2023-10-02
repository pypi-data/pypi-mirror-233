#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Montagem de microdados de painel da Pnadc.

pynad v3
Ipea - 2023
Rafael Guerreiro Osorio

Para cada visita de um painel podem haver dois arquivos
  1) o arquivo de trimestre básico está contido no de trimestre anual,
     se disponível, usa-se o anual, que tem o suplemento do trimestre
  2) o arquivo com o suplemento da visita
     - o número de observações em uma visita é identico nos arquivos
       de trimestre/trimestral e nos de visita do trimestre
"""

from json import loads, dumps
from pathlib import Path
from time import time
from zipfile import ZipFile, ZIP_DEFLATED
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from pyarrow import csv
from .metadados import META, METALIST
from .converter import MICROPRQ
from .auxiliares import continuar, elapsed, pausar, cli_main
from .paineis_id import identifica_painel

PAINEIS = 'paineis'
PAINEISCSV = Path(PAINEIS, 'csv')
PAINEISPRQ = Path(PAINEIS, 'parquet')
PAINEISMET = Path(PAINEIS, META)
FILESTUB = 'pnadc.microdados.painel.'
METASTUB = 'pnadc.variaveis.painel.'


def available(folder):
    """
    Confere painéis disponíveis e atualizações.

    Tudo deve estar atualizado:
      - sincronização com IBGE
      - metadados
      - arquivos parquet
    """
    # ler o registro de microdados parquet
    with open(Path(folder, MICROPRQ, METALIST), encoding='utf-8') as src:
        regmicro = [loads(reg[:-1]) for reg in src]
    trimestrais = [reg for reg in regmicro
                   if '.trimestral.' in reg['name']]
    a_visitas = [reg for reg in regmicro
                 if '.anual.visita' in reg['name']]
    a_trimestres = [reg for reg in regmicro
                    if '.anual.trimestre' in reg['name']]
    for lista in (trimestrais, a_visitas, a_trimestres):
        lista.sort(key=lambda lista: lista['name'])
    panels = {}
    # Os microdados trimestrais estão ordenados
    # 4 últimos não fazem um painel completo
    for idx, trimestral in enumerate(trimestrais[:-4]):
        ano = int(trimestral['name'].split('.')[-3])
        tri = int(trimestral['name'].split('.')[-2])
        pid = ano * 10 + tri
        panels[pid] = {}
        for vis in range(5):
            panels[pid][f'{vis + 1}'] = [trimestrais[idx + vis]]
            if tri > 4:
                tri = 1
                ano += 1
            # tem suplemento de trimestre? se sim, usar
            sup = [reg for reg in a_trimestres
                   if all(idt in reg['name'] for idt in (
                           f'{ano}', f'trimestre{tri}'))]
            if sup:
                panels[pid][f'{vis + 1}'] = sup[:1]
            # tem suplemento de visita?
            sup = [reg for reg in a_visitas
                   if all(idt in reg['name'] for idt in (
                           f'{ano}', f'visita{vis + 1}'))]
            if sup:
                panels[pid][f'{vis + 1}'].append(sup[0])
            else:
                panels[pid][f'{vis + 1}'].append(None)
            tri += 1
    return panels


def build_cli_main(pid, cur, total, start):
    """Atualiza a CLI."""
    cli_main()
    print('MONTAR E IDENTIFICAR OS MICRODADOS DE PAINEIS\n')
    print(f'Montando paineis - {cur} de {total} - {elapsed(start)}\n')
    print(f'PAINEL {pid}:')


def build_del_tables(panel):
    """Remove tabelas acrescidas por build_panel ao dicionário."""
    for entry in panel.values():
        for item in range(2):
            try:
                del entry[item]['table']
            except (TypeError, IndexError):
                pass


def build_get_tables(folder, pid, panel, start):
    """Lê as tabelas necessárias e lista as variáveis e suas visitas."""
    def trimestre(visita):
        tri = int(f'{pid}'[-1]) - 1 + visita
        if tri > 4:
            tri = tri - 4
        return tri
    order = (('upa', 'ascending'),
             ('v1008', 'ascending'),
             ('v2003', 'ascending'))
    pesos = ('v1028', 'v1032', 'v1036')
    pesosbs = [f'{peso}{rep:0=3}' for peso in pesos for rep in range(1, 201)]
    variaveis = {}
    for key, value in panel.items():
        filtro = pc.field('v1016') == int(key)
        arquivo = Path(folder, MICROPRQ, value[0]['name'])
        build_cli_main(pid, *start)
        print('Obtendo registros da VISITA', key,
              'do arquivo de trimestre\n' +
              value[0]['name'], end='', flush=True)
        # carregar as tabelas do painel como entrada 'table'
        value[0]['table'] = pq.read_table(
            arquivo).filter(filtro).sort_by(order)
        for var in value[0]['table'].column_names:
            if all(var not in lista for lista in (variaveis, pesosbs)):
                variaveis[var] = [{int(key)}, set()]
            elif var not in pesosbs:
                variaveis[var][0].add(int(key))
        if value[1] is not None:
            build_cli_main(pid, *start)
            print('Obtendo registros da VISITA', key,
                  'do arquivo de visitas\n' +
                  value[1]['name'], end='', flush=True)
            filtro = pc.field('trimestre') == trimestre(int(key))
            arquivo = Path(folder, MICROPRQ, value[1]['name'])
            value[1]['table'] = pq.read_table(
                arquivo).filter(filtro).sort_by(order)
            for var in value[1]['table'].column_names:
                if all(var not in lista for lista in (variaveis, pesosbs)):
                    variaveis[var] = [set(), {int(key)}]
                elif var not in pesosbs:
                    variaveis[var][1].add(int(key))
    return build_sort_vars(variaveis)


def build_panel(folder, pid, panel, start):
    """Monta o painel."""
    keys = ['upa', 'v1008', 'v2003', 'v1016']
    comuns, combos, ordem = build_get_tables(folder, pid, panel, start)
    # a tabela do painel começa com UNION (cancat) das tabelas
    # com as variáveis comuns a todas as visitas
    build_cli_main(pid, *start)
    print(f'Montando a tabela do painel\n{len(comuns)}',
          'variáveis comuns', end='', flush=True)
    tabpan = drop_empty_columns(
        pa.concat_tables([table.select(comuns)
                          for table in
                          [panel[f'{vis}'][0]['table']
                           for vis in range(1, 6)]]))
    # para cada combo de variáveis e visitas, union e left join em tabpan
    for combo in ordem:
        build_cli_main(pid, *start)
        print(f'Montando a tabela do painel\n{len(combos[combo])}',
              'variáveis no padrão', combo, end='', flush=True)
        tables = []
        # tabelas de trimestre
        for visita in combo[0]:
            tables.append(panel[f'{visita}'][0]['table'])
        # tabelas de visita
        for visita in combo[1]:
            if visita not in combo[0]:
                tables.append(panel[f'{visita}'][1]['table'])
                # criar v1016 que não vem em arquivo de visita
                tables[-1] = tables[-1].append_column(
                    'v1016', pa.array(
                        (visita,) * len(tables[-1]), pa.int8()))
        for table in tables:
            tabtmp = drop_empty_columns(
                pa.concat_tables([table.select(keys + combos[combo])
                                  for table in tables]))
        tabpan = tabpan.join(tabtmp, keys)
    build_del_tables(panel)
    return tabpan


def build_manager(folder, panels, prefs):
    """Gerencia a conversão."""
    start = time()
    count = 0
    total = len(panels)
    for key, value in panels.items():
        count += 1
        build_cli_main(key, count, total, start)
        table = build_panel(folder, key, value, (count, total, start))
        build_cli_main(key, count, total, start)
        table = identifica_painel(key, table, (count, total, start))
        build_cli_main(key, count, total, start)
        print('Organizando a tabela e gerando metadados', end='', flush=True)
        table = organise_table(table)
        meta = organise_meta(table, value)
        table = to_wide(key, table, (count, total, start))
        if prefs[0] is True:
            build_cli_main(key, count, total, start)
            csvfile = Path(folder, PAINEISCSV, f'{FILESTUB}{key}.csv')
            print('Escrevendo arquivo csv - aguarde...\n' +
                  f'{csvfile.name}', end='', flush=True)
            csv.write_csv(table, csvfile)
            if prefs[1] is True:
                build_cli_main(key, count, total, start)
                compacto = str(csvfile)[:-3] + 'zip'
                print('Compactando arquivo csv - aguarde...\n' +
                      f'{Path(compacto).name}', end='', flush=True)
                with ZipFile(compacto, 'w', ZIP_DEFLATED) as tgt:
                    tgt.write(str(csvfile), csvfile.name)
                csvfile.unlink()
        parquet = Path(folder, PAINEISPRQ, f'{FILESTUB}{key}.parquet')
        build_cli_main(key, count, total, start)
        print('Escrevendo arquivo parquet - aguarde...\n' +
              f'{parquet.name}', end='', flush=True)
        pq.write_table(table, parquet)
        del table
        with open(Path(folder, PAINEISMET, f'{METASTUB}{key}.json'),
                  'w', encoding='utf-8') as tgt:
            tgt.write(dumps(meta))
        regprq = {'name': parquet.name, 'size': parquet.stat().st_size,
                  'files': value}
        with open(Path(folder, PAINEISPRQ, METALIST),
                  'a', encoding='utf-8') as tgt:
            tgt.write(dumps(regprq) + '\n')


def build_sort_vars(variaveis):
    """Separa as variáveis de acordo com os arquivos em que aparecem."""
    combos = {}
    for key, value in variaveis.items():
        entry = (tuple(value[0]), tuple(value[1]))
        if entry not in combos:
            combos[entry] = [key]
        else:
            combos[entry].append(key)
    ordem = list(combos.keys())
    ordem.sort(key=lambda x: len(x[0]), reverse=True)
    comuns = []
    for combo in ordem:
        if combo[0] == (1, 2, 3, 4, 5):
            comuns.extend(combos[combo])
            del combos[combo]
    ordem = list(combos.keys())
    ordem.sort(key=lambda x: len(x[0]), reverse=True)
    return comuns, combos, ordem


def drop_empty_columns(table):
    """Faz o que diz o nome."""
    schema = table.schema
    columns_to_drop = []
    for field in schema:
        column = table[field.name]
        if column.null_count == len(column):
            columns_to_drop.append(field.name)
    return table.drop(columns_to_drop)


def organise_meta(table, panel):
    """Cria metadados."""
    meta = {}
    for key, value in pid_meta().items():
        meta[key] = value
    for visita in panel.values():
        for source in visita:
            if source is not None:
                with open(source['files'][2], encoding='utf-8') as src:
                    variaveis = loads(src.read())
                for var, varmeta in variaveis.items():
                    if var in table.column_names and var not in meta:
                        meta[var] = {'parte': varmeta['parte'],
                                     'quesito': varmeta['quesito'],
                                     'periodo': varmeta['periodo'],
                                     'nome': varmeta['nome'],
                                     'bytes': varmeta['bytes'],
                                     'valores': varmeta['valores']}
    # etapa final para ordenar os metadados
    sorted_meta = {}
    for var in table.column_names:
        sorted_meta[var] = meta[var]
    return sorted_meta


def organise_table(table):
    """Ordena as variáveis e os casos."""
    # ordena moradores por ordem, visita e domicilio
    order = (('upa', 'ascending'),
             ('v1008', 'ascending'),
             ('v1016', 'ascending'),
             ('v2003', 'ascending'))
    # variáveis de identificação do individuo no painel
    painel = ['upa', 'v1008', 'v1016', 'v2001', 'v2003']
    painel.extend([var for var in table.column_names if var[0:3] == 'pid'])
    # outras variáveis de identificação do registro
    comuns = ['ano', 'trimestre', 'uf', 'capital', 'rm_ride',
              'estrato', 'v1014', 'v1022', 'v1023']
    # pesos e projeções de população
    pesos = ['posest', 'posest_sxi']
    pesos.extend([var for var in table.column_names
                  if var[0:3] == 'v10' and int(var[1:]) > 1023
                  and int(var[1:]) < 2000])
    com_v = [var for var in table.column_names if var[0] == 'v'
             and all(var not in lista for lista in (comuns, painel,
                                                    pesos))]
    com_s = [var for var in table.column_names if var[0] == 's']
    resid = [var for var in table.column_names
             if all(var not in lista for lista in (comuns, painel,
                                                   pesos, com_v, com_s))]
    for lista in (pesos, com_v, com_s, resid):
        lista.sort()
    table = table.select(painel + comuns + pesos + com_v +
                         com_s + resid).sort_by(order)
    return table


def pid_meta():
    """Metadados das variáveis pid."""
    from math import log

    def entrevistas(codigo):
        visitas = []
        i = 1
        while i <= codigo:
            # & bitwise and operator
            if i & codigo:
                visitas.append(f'{int(log(i, 2) + 1)}')
            # << left shift
            i <<= 1
        return '-'.join(visitas)
    combos = {}
    for codigo in range(1, 32):
        combos[codigo] = entrevistas(codigo)
    pidcore = (('parte', 'Painel identificado por pynad'), ('quesito', ''),
               ('nome', ''), ('periodo', '1º tri/2012 - atual'), ('bytes', 1),
               ('valores', ''))
    pidvars = (('pid', 'Código do painel - ano e trimestre da 1a visita',
                'AAAAT'),
               ('pidgrp', 'Número sequencial do grupo doméstico', '1 a 5'),
               ('pidind', 'Número sequencial do indivíduo no grupo doméstico',
                '1 ao total de indivíduos'),
               ('pidcla', 'Categorias de identificação', '1 a 7'),
               ('pidgrpent', 'Visitas do grupo doméstico', ''),
               ('pidindent', 'Visitas do indivíduo', ''),
               ('piddnd', 'Dia de nascimento atribuído', '1 a 99'),
               ('piddnm', 'Mês de nascimento atribuído', '1 a 99'),
               ('piddna', 'Ano de nascimento atribuído', 'AAAA'))
    pidmeta = {var[0]: dict(pidcore) for var in pidvars}
    for var in pidvars:
        pidmeta[var[0]]['nome'] = var[1]
        pidmeta[var[0]]['valores'] = var[2]
        if var[0] in ('pid', 'piddna'):
            pidmeta[var[0]]['bytes'] = 4
        if 'ent' in var[0]:
            pidmeta[var[0]]['valores'] = combos
    return pidmeta


def sync_paineis(folder, prefs):
    """Gera e sincroniza painéis."""
    updates, excluir, regprq = verify(folder, prefs)
    if not updates and not excluir:
        print('Painéis atualizados\n')
        pausar()
        return True
    print('Painéis desatualizados!')
    if excluir:
        print(f' - remover {len(excluir)} arquivos de painéis')
    if updates:
        print(f' - montar {len(updates)} painéis')
    if not continuar():
        return False
    start = time()
    for arq in excluir:
        arq.unlink()
    with open(Path(folder, PAINEISPRQ, METALIST),
              'w', encoding='utf-8') as tgt:
        if regprq:
            tgt.write('\n'.join((dumps(reg) for reg in regprq)) + '\n')
    if updates:
        build_manager(folder, updates, prefs)
    cli_main()
    print('MONTAR E IDENTIFICAR OS MICRODADOS DE PAINEIS\n')
    print(f'Painéis atualizados em {elapsed(start)}\n')
    pausar()
    return True


def to_wide(pid, table, start):
    """Reshape da tabela para criar registros de indivíduo."""
    # variáveis constantes nas visitas
    fixas = ['pid', 'uf', 'capital', 'rm_ride', 'v1014', 'v1022', 'v1023',
             'estrato', 'posest', 'upa', 'v1008', 'pidgrp', 'pidgrpent',
             'pidind', 'pidcla', 'pidindent', 'piddnd', 'piddnm', 'piddna']
    # chaves identificadoras do indivíduo
    indkeys = ['upa', 'v1008', 'pidgrp', 'pidind']
    build_cli_main(pid, *start)
    print('Reformatando a tabela para registros de indíviduo')
    print('Variáveis constantes nas visitas', end='', flush=True)
    # a tabela wide começa com as variáveis que não variam por visita
    wide = table.select(fixas).group_by(indkeys).aggregate(
            [(var, 'one') for var in fixas if var not in indkeys])
    wide = wide.rename_columns([var.replace('_one', '') for var
                                in wide.column_names])
    # acrescenta as variáveis de cada visita
    for visita in range(1, 6):
        build_cli_main(pid, *start)
        print('Reformatando a tabela para registros de indíviduo')
        print(f'Variáveis da visita {visita}', end='', flush=True)
        filtro = pc.field('v1016') == visita
        antes = indkeys + [var for var in table.column_names
                           if var not in fixas]
        depois = indkeys + [f'{var}_{visita}' for var in table.column_names
                            if var not in fixas]
        wide = wide.join(drop_empty_columns(
            table.select(antes).filter(filtro).rename_columns(depois)),
            indkeys)
    final = [f'{var}_{visita}' for var in table.column_names
             if var not in fixas for visita in range(1, 6)]
    del table
    final = fixas + [var for var in final if var in wide.column_names]
    build_cli_main(pid, *start)
    print('Reformatando a tabela para registros de indíviduo')
    print('Organizando variáveis e ordenando a tabela', end='', flush=True)
    wide = wide.select(final).sort_by(
        (('upa', 'ascending'), ('v1008', 'ascending'),
         ('pidgrp', 'ascending'), ('pidind', 'ascending')))
    return wide


def verify(folder, prefs):
    """Verifica os arquivos de microdados."""
    # criar as pastas se inexistentes
    if not Path(folder, PAINEISPRQ).is_dir():
        Path(folder, PAINEISPRQ).mkdir(parents=True)
        Path(folder, PAINEISMET).mkdir()
        if prefs[0] is True and not Path(folder, PAINEISCSV).is_dir():
            Path(folder, PAINEISCSV).mkdir()
    verify_meta_csv(folder, prefs)
    # gera a lista de paineis completos nos microdados da Pnadc
    panels = available(folder)
    # carrega as listas de arquivos nas pastas de microdados
    curprq = [{'name': arq.name, 'size': arq.stat().st_size}
              for arq in Path(folder, PAINEISPRQ).glob('*')
              if arq.name != METALIST]
    # carrega os registros dos arquivos
    regprq = []
    if Path(folder, PAINEISPRQ, METALIST).is_file():
        with open(Path(folder, PAINEISPRQ, METALIST), encoding='utf-8') as src:
            regprq = [loads(reg[:-1]) for reg in src]
    # arquivos que existem nas pastas mas não nos registros
    # devem ser excluídos, pois não se sabe os arquivos que lhe originaram
    # arquivos diferentes dos registros também são excluídos
    excluir = list(set(Path(folder, PAINEISPRQ, arq['name'])
                       for arq in curprq if arq not in
                       [{'name': arq['name'], 'size': arq['size']}
                        for arq in regprq]))
    # arquivos que não existem nas pastas ou que serão eliminados
    # precisam ser tirados dos registros
    regprq = [arq for arq in regprq
              if {'name': arq['name'], 'size': arq['size']} in
              curprq]
    # updates se baseiam nos prqs
    updates = {pid: panel for pid, panel in panels.items() if panel not in
               [arq['files'] for arq in regprq]}
    return updates, excluir, regprq


def verify_meta_csv(folder, prefs):
    """Remove arquivo parquet sem metadados e csv."""
    # TODO: deletar arquivos nas pastas csv e metadados
    # que não tenham um arquivo parquet
    pidprq = {arq.name[-13:-8]: arq
              for arq in Path(folder, PAINEISPRQ).glob('*')
              if arq.name != METALIST}
    pidmeta = [arq.name[-10:-5] for arq in Path(folder, PAINEISMET).glob('*')
               if arq.name != METALIST]
    if prefs[0] is True:
        pidcsv = [arq.name[-9:-4]
                  for arq in Path(folder, PAINEISCSV).glob('*')
                  if arq.name != METALIST]
    else:
        pidcsv = list(pidprq.keys())
    for key, value in pidprq.items():
        if key not in pidmeta or key not in pidcsv:
            value.unlink()
