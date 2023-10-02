#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversão de microdados da Pnadc.

pynad v3
Ipea - 2023
Rafael Guerreiro Osorio

Notas:
1) na prática, tanto faz, mesmo com um HD externo lento,
   fazer operações com arquivos de texto na memória ou em disco,
   não tem diferença de tempo grande, então é melhor fazer em disco
   usando pouca memória para não dar problemas
2) separar as colunas dos registros codificados como texto demora de
   qualquer jeito; como as estruturas de dados tem comandos otimizados
   para carregar arquivos csv, converter para csv e depois para outro
   formato, no caso parquet, é mais rápido (com python) do que tentar
   converter direto para parquet
"""

from json import dumps, loads
from time import time, sleep
from pathlib import Path
from shutil import rmtree
from zipfile import ZipFile, ZIP_DEFLATED, BadZipFile
import pyarrow as pa
import pyarrow.parquet as pq
from pyarrow import csv
from .auxiliares import continuar, elapsed, pausar, sizestr, cli_main
from .auxiliares import CRCLR, UPCLR
from .metadados import META, METALIST, _VPOS, csv_name


DLMT = ','
MICRO = 'microdados'
MICROCSV = Path('microdados', 'csv')
MICROPRQ = Path('microdados', 'parquet')


# pyarrow - tipo de dados - bytes
PA_DT = {1: pa.int8,
         2: pa.int16,
         4: pa.int32,
         8: pa.int64,
         15: pa.float64}


def conversion_manager(folder, updates, prefs):
    """Gerencia a conversão de arquivos."""
    def fields(arquivo):
        with open(arquivo, encoding='utf-8') as src:  # json com metadados
            meta = loads(src.read())
        return [(meta[var][_VPOS][0] - 1, meta[var][_VPOS][1], var)
                for var in meta]

    start = time()
    for idx, update in enumerate(updates):
        update.append(str(Path(folder, MICROCSV, csv_name(update[0]))))
        cli_main()
        print('CONVERTER ARQUIVOS DE MICRODADOS\n')
        print(f'Arquivo {idx + 1} de {len(updates)} - {elapsed(start)}')
        print(f'{Path(update[0]).name}')
        print('Descompactando - aguarde...', end='', flush=True)
        with ZipFile(update[0]) as src:
            src.extract(src.namelist()[0], Path(update[3]).parent)
            fixed = Path(Path(update[3]).parent, src.namelist()[0])
        fixed_size = Path(fixed).stat().st_size
        cli_main()
        print('CONVERTER ARQUIVOS DE MICRODADOS\n')
        print(f'Arquivo {idx + 1} de {len(updates)} - {elapsed(start)}')
        print(f'{fixed.name}')
        fixed2csv((idx, len(updates), fixed, fixed_size,
                   fields(update[2]), update[3], start))
        target, target_size = Path(update[3]), Path(update[3]).stat().st_size
        Path(fixed).unlink()
        cli_main()
        print('CONVERTER ARQUIVOS DE MICRODADOS\n')
        print(f'Arquivo {idx + 1} de {len(updates)} - {elapsed(start)}')
        print(f'{target.name}')
        print(f'{CRCLR}Escrevendo arquivo parquet - aguarde...',
              end='')
        parquet, parquet_size = csv2parquet(update[3], update[2])
        if prefs[1] is True:
            cli_main()
            print('CONVERTER ARQUIVOS DE MICRODADOS\n')
            print(f'Arquivo {idx + 1} de {len(updates)} - {elapsed(start)}')
            print(f'{Path(update[3]).name}')
            print(f'{CRCLR}Compactando {sizestr(target_size)}',
                  '- aguarde...', end='', flush=True)
            compacto = Path(Path(update[3]).parent,
                            Path(update[3]).name[:-3] + 'zip')
            with ZipFile(compacto, 'w', ZIP_DEFLATED) as tgt:
                tgt.write(update[3], Path(update[3]).name)
            target, target_size = compacto, compacto.stat().st_size
            Path(update[3]).unlink()
        regcsv = {'name': target.name, 'size': target_size,
                  'files': update[:-1]}
        with open(Path(folder, MICROCSV, METALIST),
                  'a', encoding='utf-8') as tgt:
            tgt.write(dumps(regcsv) + '\n')
        regprq = {'name': parquet.name, 'size': parquet_size,
                  'files': update[:-1]}
        with open(Path(folder, MICROPRQ, METALIST),
                  'a', encoding='utf-8') as tgt:
            tgt.write(dumps(regprq) + '\n')
        if prefs[0] is False:
            Path(update[3]).unlink()
    cli_main()
    print('CONVERTER ARQUIVOS DE MICRODADOS\n')
    print(f'Os arquivos foram convertidos em {elapsed(start)}')


def csv2parquet(micro, metafile):
    """Carrega um arquivo csv."""
    with open(metafile, encoding='utf-8') as src:  # json com metadados
        meta = loads(src.read())
    table = csv.read_csv(micro,
                         convert_options=csv.ConvertOptions(
                             column_types={var: PA_DT[meta[var]['bytes']]()
                                           for var in meta}))
    target = micro.replace(str(MICROCSV), str(MICROPRQ))[:-3] + 'parquet'
    pq.write_table(table, target)
    return Path(target), Path(target).stat().st_size


def fixed2csv(args):
    """Conversão do arquivo de microdados para csv."""
    def message(args):
        idx, tidx, start, fixed, size, totalsize, start_local = args
        return (CRCLR + UPCLR + UPCLR +
                f'Arquivo {idx + 1} de {tidx} - {elapsed(start)}\n' +
                f'{fixed.name}\n' +
                f'Convertendo {sizestr(totalsize)}: ' +
                f'{size * 100 / totalsize:.0f}% ' +
                f'{sizestr(size/(time() - start_local))}/s')
    idx, tidx, fixedfile, totalsize, leitura, csvfile, start = args
    start_local = time()
    with open(fixedfile, encoding='utf-8') as fixed:
        with open(csvfile, 'w', encoding='utf-8') as target:
            chunk = 0
            size = 0
            # em Windows, em msg rola de start_local ser == a time()
            # e ao calular bytes por segundo dá divisão por zero
            # o sleep garante que não ocorra
            sleep(0.01)
            print(message((idx, tidx, start, fixedfile, size,
                           totalsize, start_local)), end=' ')
            chunk_size = 10000  # linhas
            target.write(DLMT.join((var[2] for var in leitura)) + '\n')
            for reg in fixed:
                size += len(reg)
                reg = DLMT.join((reg[var[0]:var[1]].strip(' .')
                                 for var in leitura))
                target.write(reg + '\n')
                chunk += 1
                if chunk == chunk_size:
                    chunk = 0
                    print(message((idx, tidx, start, fixedfile, size,
                                   totalsize, start_local)), end=' ')


def sync_microdados(folder, prefs):
    """Sincroniza arquivos de microdados convertidos."""
    print('CONVERTER ARQUIVOS DE MICRODADOS\n')
    updates, excluir, regcsv, regprq = verify(folder, prefs)
    if not updates and not excluir:
        if prefs[0] is False:
            rmtree(Path(folder, MICROCSV))
        print('Microdados atualizados\n')
        pausar()
        return True
    print('Microdados desatualizados!')
    if excluir:
        print(f' - remover {len(excluir)} arquivos')
    if updates:
        print(f' - converter {len(updates)} arquivos')
    if not continuar():
        if prefs[0] is False:
            rmtree(Path(folder, MICROCSV))
        return False
    for arq in excluir:
        arq.unlink()
    with open(Path(folder, MICROCSV, METALIST), 'w', encoding='utf-8') as tgt:
        if regcsv:
            tgt.write('\n'.join((dumps(reg) for reg in regcsv)) + '\n')
    with open(Path(folder, MICROPRQ, METALIST), 'w', encoding='utf-8') as tgt:
        if regprq:
            tgt.write('\n'.join((dumps(reg) for reg in regprq)) + '\n')
    if updates:
        conversion_manager(folder, updates, prefs)
    if prefs[0] is False:
        rmtree(Path(folder, MICROCSV))
    print('Microdados atualizados\n')
    pausar()
    return True


def verify(folder, prefs):
    """Verifica os arquivos de microdados."""
    # criar as pastas se inexistentes
    if not Path(folder, MICROCSV).is_dir():
        Path(folder, MICROCSV).mkdir(parents=True)
        if not Path(folder, MICROPRQ).is_dir():
            Path(folder, MICROPRQ).mkdir()
    # carrega a lista de microdados e dicionários de metadados
    with open(Path(folder, META, METALIST), encoding='utf-8') as src:
        curmeta = loads(src.read())
    # carrega as listas de arquivos nas pastas de microdados
    curcsv = [{'name': arq.name, 'size': arq.stat().st_size}
              for arq in Path(folder, MICROCSV).glob('*')
              if arq.name != METALIST]
    curprq = [{'name': arq.name, 'size': arq.stat().st_size}
              for arq in Path(folder, MICROPRQ).glob('*')
              if arq.name != METALIST]
    # carrega os registros dos arquivos
    regcsv = []
    regprq = []
    if Path(folder, MICROCSV, METALIST).is_file():
        with open(Path(folder, MICROCSV, METALIST), encoding='utf-8') as src:
            regcsv = [loads(reg[:-1]) for reg in src]
    if Path(folder, MICROPRQ, METALIST).is_file():
        with open(Path(folder, MICROPRQ, METALIST), encoding='utf-8') as src:
            regprq = [loads(reg[:-1]) for reg in src]
    # arquivos que existem nas pastas mas não nos registros
    # devem ser excluídos, pois não se sabe os arquivos que lhe originaram
    # arquivos diferentes dos registros também são excluídos
    excluir = [Path(folder, MICROCSV, arq['name']) for arq in curcsv
               if arq not in [{'name': arq['name'], 'size': arq['size']}
               for arq in regcsv]]
    excluir.extend([Path(folder, MICROPRQ, arq['name']) for arq in curprq
                    if arq not in [{'name': arq['name'], 'size': arq['size']}
                    for arq in regprq]])
    # verificar integridade dos arquivos zip
    if prefs[0] is True and prefs[1] is True:
        for zipf in curcsv:
            try:
                with ZipFile(Path(folder, MICROCSV, zipf['name'])) as src:
                    src.namelist()
            # se bichado, vai para lista de exclusão e acerta o registro
            except BadZipFile:
                excluir.append(Path(folder, MICROCSV, zipf['name']))
                curcsv.remove(zipf)

    # arquivos que não existem nas pastas ou que serão eliminados
    # precisam ser tirados dos registros
    regcsv = [arq for arq in regcsv
              if {'name': arq['name'], 'size': arq['size']} in
              curcsv]
    regprq = [arq for arq in regprq
              if {'name': arq['name'], 'size': arq['size']} in
              curprq]
    # arquivos csv e parquet devem ter correspondência
    csvsemparquet = [arq for arq in regcsv if arq['files'] not in
                     [arq['files'] for arq in regprq]]
    parquetsemcsv = [arq for arq in regprq if arq['files'] not in
                     [arq['files'] for arq in regcsv]]
    excluir.extend([Path(folder, MICROCSV, arq['name'])
                    for arq in csvsemparquet])
    if prefs[0] is True:
        excluir.extend([Path(folder, MICROPRQ, arq['name'])
                        for arq in parquetsemcsv])
        regprq = [arq for arq in regprq if arq not in parquetsemcsv]
    excluir = list(set(excluir))
    regcsv = [arq for arq in regcsv if arq not in csvsemparquet]
    # updates se baseiam nos prqs
    updates = [arq for arq in curmeta if arq not in
               [arq['files'] for arq in regprq]]
    return (updates, excluir, regcsv, regprq)
