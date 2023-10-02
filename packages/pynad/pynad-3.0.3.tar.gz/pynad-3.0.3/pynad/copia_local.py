#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerencia cópias locais dos microdados da Pnadc.

pynad v3
Ipea - 2023
Rafael Guerreiro Osorio
"""
import ssl
from urllib.request import urlopen
from ftplib import FTP, error_perm
from json import dumps, loads
from pathlib import Path, PurePosixPath as pPath
from shutil import disk_usage
from socket import gaierror
from time import strftime, localtime, time
from .auxiliares import continuar, sizestr, elapsed, pausar, cli_main
from .auxiliares import BARRA, CRCLR, UPCLR, HEADER_W, HEADER_F


PNADCA = 'anual'
PNADCT = 'trimestral'
# Servidor FTP IBGE
FTP_FOLDERS = {PNADCA: ('Trabalho_e_Rendimento',
                        'Pesquisa_Nacional_por_Amostra_de_Domicilios_continua',
                        'Anual', 'Microdados'),
               PNADCT: ('Trabalho_e_Rendimento',
                        'Pesquisa_Nacional_por_Amostra_de_Domicilios_continua',
                        'Trimestral', 'Microdados')}
COPIA_LOCAL = 'originais'
IDFILE = str(Path('pynad', 'pynad_data'))
LSFILE = str(Path('pynad', 'pynad_lista'))
LGFILE = str(Path('pynad', 'pynad_sync.log'))
MPFILE = str(Path('pynad', 'pynad_microdados_prefs'))


class AltFTP(FTP):
    """Corrige problema de configuração do servidor de FTP do IBGE."""

    def makepasv(self):
        """
        O servidor do IBGE tem um problema de configuração.

        Retorna um endereço diferente do externo, e em Windows
        isso causa um erro em socket.py, que é chamada por ftplib
        WinError 10060
        """
        _invhost, port = super().makepasv()
        return self.host, port


def download_manager(arquivos, folder):
    """Recebe uma lista de arquivos para download."""
    start = time()
    totalarq = len(arquivos)
    totalbyt = sum(arq['size'] for arq in arquivos)
    print()
    for curarq, arquivo in enumerate(arquivos):
        tgt = Path(folder, COPIA_LOCAL, arquivo['path'], arquivo['name'])
        if not Path(arquivo['path']).parts[1:]:
            src = Path(Path(*FTP_FOLDERS[Path(arquivo['path']).parts[0]]),
                       arquivo['name'])
        else:
            src = Path(Path(*FTP_FOLDERS[Path(arquivo['path']).parts[0]]),
                       '/'.join(Path(arquivo['path']).parts[1:]),
                       arquivo['name'])
        curbyt = sum(arq['size'] for arq in arquivos[:curarq])
        prg = (curarq + 1, totalarq, curbyt, totalbyt, start)
        download_file(src, tgt, prg)
        with open(Path(folder, LSFILE), 'a', encoding='utf-8') as tgt:
            tgt.write(dumps(arquivo) + '\n')
    register(folder)
    print(CRCLR + UPCLR + 'Todos os arquivos foram baixados em',
          elapsed(start), '\n')


def download_file(src, tgt, prg):
    """Baixa um arquivo."""
    def message(src, prg, cum):
        prg_2 = (prg[2] + cum) / prg[3] * 100
        return (f'{CRCLR}{UPCLR}Baixando arquivo {prg[0]} de {prg[1]} - ' +
                f'{prg_2:.0f}% em {elapsed(prg[4])} - ' +
                f'{sizestr((prg[2] + cum)/(time() - prg[4]))}/s' +
                f'\n{src.name}')
    try:
        tgt.parent.mkdir(parents=True)
    except FileExistsError:
        pass

    # baixar com urllib - acrescentar protocolo
    file_url = 'https://ftp.ibge.gov.br/' + str(pPath(src))

    # Servidor do IBGE está com o SSL desatualizado
    # https://stackoverflow.com/questions/71603314/ssl-error-unsafe-legacy-renegotiation-disabled
    # BEGIN Patch
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    # END Patch
    # contexto usado com urlopen
    with urlopen(file_url, context=ctx) as response, open(tgt, 'wb') as tar:
        chunk_size = 1024 * 1024
        bytes_downloaded = 0
        print(message(src, prg, bytes_downloaded), end=' ')
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            tar.write(chunk)
            bytes_downloaded += len(chunk)
            print(message(src, prg, bytes_downloaded), end=' ')


def list_local_files(folder):
    """
    Lista arquivos na copia local.

    Para cada arquivo há um dicionário com 3 entradas:
    - 'parent', 'name' e 'size'
    """
    filelist = [file for file in Path(folder).glob('**/*')
                if file.is_file() and COPIA_LOCAL in file.parts
                and all(part in file.parts for part in Path(folder).parts)]
    arquivos = []
    for file in filelist:
        partes = file.parts
        ini = Path(file).parts.index(COPIA_LOCAL) + 1
        arquivos.append(
            {'path': str(pPath(*partes[ini:-1])),
             'name': partes[-1],
             'size': file.stat().st_size})
    return arquivos


def list_remote_files():
    """
    Lista arquivos de microdados da Pnadc no servidor FTP do IBGE.

    Para cada arquivo há um dicionário com 3 entradas:
        - 'parent', 'name' e 'size'
    """
    def isfolder(path):
        try:
            server.cwd(path)
            server.cwd('..')
            return True
        except error_perm:
            return False

    def mapftp(pnad, ftproot, ftpcur):
        server.cwd(str(pPath(ftproot, ftpcur)))
        itens = server.nlst()
        for item in itens:
            sourcename = pPath(ftproot, ftpcur, item)
            if isfolder(str(sourcename)):
                mapftp(pnad, ftproot, pPath(ftpcur, item))
            else:
                size = server.size(str(sourcename))
                remotefiles.append({'path': str(pPath(pnad, ftpcur)),
                                    'name': item,
                                    'size': size})
                print(f'{UPCLR}Mapeando microdados da Pnadc no servidor' +
                      f' do IBGE - {elapsed(start)}')
                print(f'{CRCLR}{remotefiles[-1]["name"]} ' +
                      f'({sizestr(remotefiles[-1]["size"])})', end='')
    try:
        print('Estabelecendo conexão com o IBGE')
        start = time()
        remotefiles = []
        server = AltFTP('ftp.ibge.gov.br', timeout=60)
        server.connect()
        server.login()
        mapftp(PNADCA, pPath('/', *FTP_FOLDERS[PNADCA]), pPath(''))
        mapftp(PNADCT, pPath('/', *FTP_FOLDERS[PNADCT]), pPath(''))
        server.close()
    except (TimeoutError, gaierror):
        remotefiles = []
    return remotefiles


def register(folder):
    """Registra a cópia local e atualizações criando arquivos."""
    if not Path(folder, 'pynad').is_dir():
        Path(folder, 'pynad').mkdir()
    if not Path(folder, COPIA_LOCAL).is_dir():
        Path(folder, COPIA_LOCAL).mkdir()
    with open(Path(folder, IDFILE), 'w', encoding='utf-8') as tgt:
        tgt.write(str(time()))
    with open(Path(folder, LSFILE), 'w', encoding='utf-8') as tgt:
        for arquivo in list_local_files(folder):
            tgt.write(dumps(arquivo) + '\n')
    # configuração default para microdados
    if not Path(folder, MPFILE).is_file():
        with open(Path(folder, MPFILE), 'w', encoding='utf-8') as tgt:
            tgt.write(dumps((True, True)))


def sync(folder):
    """Sincroniza os arquivos da copia local."""
    print('SINCRONIZAR A CÓPIA LOCAL\n')
    print('Verificar arquivos no servidor do IBGE')
    if not continuar():
        return
    cli_main()
    print('SINCRONIZAR A CÓPIA LOCAL\n')
    arquivos = list_remote_files()
    if not arquivos:
        print(CRCLR + UPCLR + HEADER_W +
              'ERRO DE ACESSO AO SERVIDOR DO IBGE' + HEADER_F)
        print('Causas prováveis:')
        print(' - a conexão com a internet não está ativa')
        print(' - https://ftp.ibge.gov.br está muito lento ou off-line')
        print(' - o firewall não permite conexões nas portas 20000 a 21000\n')
        pausar()
        return
    cli_main()
    print('SINCRONIZAR A CÓPIA LOCAL\n')
    print('Microdados da PNADC no IBGE:', str(len(arquivos)),
          'arquivos:', sizestr(sum(f['size'] for f in arquivos)))
    atuais = list_local_files(folder)
    excluir = [arq for arq in atuais if arq not in arquivos]
    baixar = [arq for arq in arquivos if arq not in atuais]
    if not excluir and not baixar:
        print('A cópia local está sincronizada\n')
        pausar()
        return
    print('A cópia local não está sincronizada!')
    exc_txt = bai_txt = ''
    if excluir:
        exc_txt = (' - remover ' + str(len(excluir)) + ' arquivos: ' +
                   sizestr(sum(f['size'] for f in excluir), 'PT'))
        print(exc_txt)
    if baixar:
        bai_txt = (' - baixar ' + str(len(baixar)) + ' arquivos: ' +
                   sizestr(sum(f['size'] for f in baixar), 'PT'))
        print(bai_txt)
    _total, _used, free = disk_usage(folder)
    print(f'Espaço livre na pasta da cópia local: {sizestr(free)}')
    if not continuar():
        return
    cli_main()
    print('SINCRONIZAR A CÓPIA LOCAL\n')
    for arquivo in excluir:
        Path(folder, COPIA_LOCAL, arquivo['path'], arquivo['name']).unlink()
    register(folder)
    download_manager(baixar, folder)
    write_log(folder, excluir, baixar, exc_txt, bai_txt)
    pausar()


def verify(folder):
    """Verifica a integridade da copia local."""
    if not folder:
        return ''
    integra = False
    with open(Path(folder, IDFILE), encoding='utf-8') as src:
        data = float(src.read())
    datastr = strftime("%Y-%m-%d %H:%M:%S", localtime(data))
    with open(Path(folder, LSFILE), encoding='utf-8') as src:
        lista = src.read()
    arquivos = [loads(item) for item in lista.split('\n')
                if len(item) > 2]
    atuais = list_local_files(folder)
    alterados = [arq for arq in arquivos if arq not in atuais]
    alterados.extend([arq for arq in atuais if arq not in arquivos])
    if not alterados:
        integra = True
    return data, datastr, integra


def write_log(folder, excluir, baixar, exc_txt, bai_txt):
    """Escreve arquivo log com arquivos alterados nas sincronizações."""
    data = verify(folder)
    mode = 'w'
    if Path(folder, LGFILE).is_file():
        mode = 'a'
    with open(Path(folder, LGFILE), mode, encoding='utf-8') as log:
        log.write('Sincronização em ' + data[1] + '\n' + BARRA)
        if excluir:
            log.write('\n' + exc_txt + '\n')
            for arq in excluir:
                log.write(str(Path(arq['path'], arq['name'])) + '\n')
        if baixar:
            log.write('\n' + bai_txt + '\n')
            for arq in baixar:
                log.write(str(Path(arq['path'], arq['name'])) + '\n')
        log.write(BARRA + '\n\n')
