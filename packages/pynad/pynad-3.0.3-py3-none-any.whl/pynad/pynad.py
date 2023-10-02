#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pynad Command Line Interface.

pynad v3
Ipea - 2023
Rafael Guerreiro Osorio

    def _menu_help(self):
        import webbrowser
        webbrowser.open(str(Path(APP_PATH, 'help.html')))
"""
from json import dumps, loads
from pathlib import Path
from platform import system
from shutil import rmtree
from time import sleep
import tkinter as tk
from tkinter import filedialog
from .auxiliares import elapsed, continuar, pausar, cli_main
from .auxiliares import TCOLS, ARROW, HEADER_F, HEADER_B, HEADER_W, COPIA_F
from .auxiliares import COPIA_B, COPIA_H, COPIA_W, UPCLR
from .copia_local import register, verify, sync
from .copia_local import COPIA_LOCAL, IDFILE, LSFILE, MPFILE
from .converter import sync_microdados, MICRO
from .metadados import generate, META
from .paineis import sync_paineis, PAINEIS


def cli_copia_local(folder, data):
    """Info da cópia local."""
    # COPIA LOCAL
    print(COPIA_B + COPIA_F, end='')
    for _linha in range(4):
        print(' ' * TCOLS, end='')
    print('\n\033[4A\033[K', end='')
    print('Pasta da cópia local da PNADC:')
    msg = str(folder)
    if len(str(folder)) > 80:
        msg = str(folder)[:35] + '  (...)  ' + str(folder)[-36:]
    print(COPIA_H + msg)
    msg = aviso = ''
    if data:
        msg = f'Última atualização em {data[1]} (há {elapsed(data[0])})'
        aviso = COPIA_H + 'Cópia local íntegra'
        if data and data[2] is False:
            aviso = COPIA_W + 'CÓPIA LOCAL ADULTERADA!'
    print(COPIA_F + msg)
    print(aviso)


def get_menu(folder):
    """Retorna o menu com os items habilitados."""
    menu = {'1': ('Sincronizar a cópia local com o IBGE', menu_sync),
            '2': ('Organizar e gerar os metadados em formato json',
                  menu_metadados),
            '3': ('Converter os arquivos de microdados',
                  menu_converter),
            '4': ('Montar e identificar os microdados de painéis',
                  menu_paineis),
            'f': ('Definir ou alterar a pasta da cópia local', menu_definir),
            'c': ('Preferências de arquivos de microdados', menu_prefs),
            'h': ('Ajuda', menu_ajuda),
            'q': ('Sair', menu_sair)}
    # selecionar os itens válidos
    if not folder:
        menuitems = ['f', 'h', 'q']
    else:
        with open(Path(folder, LSFILE), encoding='utf-8') as src:
            arquivos = src.read()
        if not arquivos:
            menuitems = ['1', 'f', 'c', 'h', 'q']
        elif not Path(folder, META).is_dir():
            menuitems = ['1', '2', 'f', 'c', 'h', 'q']
        elif not Path(folder, MICRO).is_dir():
            menuitems = ['1', '2', '3', 'f', 'c', 'h', 'q']
        else:
            menuitems = list(menu.keys())
    return {key: value for key, value in menu.items() if key in menuitems}


def get_prefs(folder):
    """Carrega as preferências para microdados."""
    with open(Path(folder, MPFILE), encoding='utf-8') as src:
        return loads(src.read())


def main(folder, data):
    """Inicia pynad."""
    # Apresenta a CLI
    cli_main()
    if not folder and Path(Path.cwd(), IDFILE).is_file():
        folder = Path.cwd()
        data = verify(Path.cwd())
    if not folder:
        folder, data = set_folder(folder)
    # folder pode ter sido ou não definida
    if folder:
        cli_copia_local(folder, data)
    # menu principal
    menu = get_menu(folder)
    print(HEADER_B + HEADER_F)
    print('MENU')
    for key, value in menu.items():
        print(f' {key}) {value[0]}')
    print('\n')
    resp = ''
    while resp not in menu:
        sleep(0.05)
        resp = input(f'{UPCLR}Digite a opção {ARROW} ').lower()
    cli_main()
    return menu[resp][1](folder)


def main_script():
    """Inicia quando roda como script."""
    # ativar terminal escape sequences no Windows
    if system() == 'Windows':
        from ctypes import windll
        windll.kernel32.SetConsoleMode(windll.kernel32.GetStdHandle(-11), 7)
    # dimensiona o terminal
    print(f'\033[8;24;{TCOLS}t', end='')
    folder = data = ''
    loop = True
    while loop:
        loop, folder, data = main(folder, data)


def menu_ajuda(folder):
    """Menu item."""
    print('AJUDA\n')
    print('Use a opção "f" para escolher a pasta da cópia local:')
    print('  - a pasta deve conter uma cópia da pnadc criada por pynad')
    print('    ou, para uma nova cópia, deve existir e estar vazia;')
    print('  - não crie arquivos nela ou em suas subpastas,')
    print('    eles serão removidos nas atualizações.\n')
    print('Use a opção "c" para configurar',
          'as opções dos arquivos csv:')
    print('  - se devem ser gerados;\n  - se devem ser compactados.\n')
    print('As opções do menu surgem ao tornarem-se disponíveis:',
          '\n  - execute-as em ordem - 1, 2, 3, 4 -',
          'para sincronizar.\n')
    print('2023 - Rafael Guerreiro Osorio - Ipea',
          '\nEste programa é gratuito e sem garantias,',
          'use por sua própria conta e risco.\n')
    pausar()
    return True, folder, verify(folder)


def menu_converter(folder):
    """Menu item."""
    sync_microdados(folder, get_prefs(folder))
    return True, folder, verify(folder)


def menu_definir(folder):
    """Menu item."""
    newfolder, newdata = set_folder(folder, True)
    if newfolder:
        return True, newfolder, newdata
    return True, folder, verify(folder)


def menu_metadados(folder):
    """Menu item."""
    generate(folder)
    return True, folder, verify(folder)


def menu_paineis(folder):
    """Menu item."""
    sync_paineis(folder, get_prefs(folder))
    return True, folder, verify(folder)


def menu_prefs(folder):
    """Menu item."""
    set_micro_prefs(folder)
    return True, folder, verify(folder)


def menu_sair(folder):
    """Encerra pynad."""
    print('\033c')
    return False, folder, ''


def menu_sync(folder):
    """Menu item."""
    sync(folder)
    return True, folder, verify(folder)


def set_folder(folder, menu=False):
    """Seleciona a pasta da copia local."""

    def seleciona(folder):
        root = tk.Tk()
        root.withdraw()
        return filedialog.askdirectory(
            title='PYNAD - Selecione a pasta da cópia local',
            initialdir=folder,
            mustexist=True)

    # se não há folder, mostrar o menu reduzido
    if not menu:
        return '', ''
    print('DEFINIR OU ALTERAR A PASTA DA CÓPIA LOCAL')
    newfolder = seleciona(folder)
    if newfolder:
        if Path(newfolder, IDFILE).is_file():
            return newfolder, verify(newfolder)
        cli_main()
        cli_copia_local(newfolder, '')
        print(HEADER_B + HEADER_F)
        # verificar se há arquivos na pasta
        # se não houver, é uma nova instalação
        # se tem a pasta COPIA_LOCAL, pode ser uma copia corrompida
        arquivos = [str(arq) for arq in Path(newfolder).glob('**/*')]
        if arquivos:
            print(HEADER_W, end='')
            print('A pasta selecionada contém arquivos!')
            if any(str(Path(newfolder, COPIA_LOCAL))
                   in arq for arq in arquivos):
                print(HEADER_F, end='')
                print('Os arquivos parecem ser de uma cópia local')
                print('Restaurar a cópia_local na pasta selecionada')
                if continuar():
                    register(newfolder)
                    print('Cópia local restaurada. Sincronize-a com o IBGE\n')
                    pausar()
                    return newfolder, verify(newfolder)
            print(HEADER_W, end='')
            print('Não é possível criar uma cópia local nesta pasta')
            print('Por segurança, a pasta deve estar vazia\n')
            print(HEADER_F, end='')
            pausar()
            return folder, verify(folder)
        print('Criar uma cópia local na pasta selecionada')
        if continuar():
            register(newfolder)
            print('Cópia local criada. Sincronize-a com o IBGE\n')
            pausar()
            return newfolder, verify(newfolder)
    return folder, verify(folder)


def set_micro_prefs(folder):
    """
    Define as opções para arquivos csv.

    O formato obrigatório para os microdados é parquet:
      - arquivos csv são gerados para converter os arquivos originais para
        o formato parquet
      - depois de gerados os arquivos parquet, os arquivos csv não são
        mais necessários
      - também não é necessário gerar os arquivos csv com os
        microdados de painel

    Os arquivos csv podem ser compactados.

    As preferências para arquivos csv são guardadas em arquivo
    de configuração e é preciso gerá-lo antes de converter os microdados
    """
    menu = {'A': ('Microdados em formato parquet e csv compactado (zip)',
                  [True, True]),
            'B': ('Microdados em formato parquet e csv descompactado   ',
                  [True, False]),
            'C': ('Somente microdados em formato parquet               ',
                  [False, False])}
    prefs = get_prefs(folder)
    print('DEFINIR AS PREFERÊNCIAS PARA ARQUIVOS DE MICRODADOS\n')
    for key, value in menu.items():
        if value[1] == prefs:
            print(COPIA_B + COPIA_F, end='')
        else:
            print(HEADER_B + HEADER_F, end='')
        print(f' {key}) {value[0]}')
    print(HEADER_B, HEADER_F, '\n')
    resp = ''
    while resp not in menu:
        sleep(0.05)
        resp = input(f'{UPCLR}Digite a nova opção ou ' +
                     f'ENTER para cancelar {ARROW} ').upper()
        # ENTER ou opção atual
        if not resp or (resp in menu and menu[resp][1] == prefs):
            return
    # se há mudança e pasta de microdados já existe
    # remove pasta de microdados (e paineis) após confirmação
    if Path(folder, MICRO).is_dir():
        print(HEADER_W + '\nATENÇÃO: ' + HEADER_F +
              'Alteração de preferências' +
              '\n\nOs arquivos de microdados já convertidos' +
              '\ne os arquivos de painel serão removidos;' +
              '\ntodos terão que ser gerados novamente\n')
        if continuar():
            try:
                rmtree(Path(folder, MICRO))
            except FileNotFoundError:
                pass
            try:
                rmtree(Path(folder, PAINEIS))
            except FileNotFoundError:
                pass
        else:
            return
    with open(Path(folder, MPFILE), 'w', encoding='utf-8') as tgt:
        tgt.write(dumps(menu[resp][1]))


if __name__ == '__main__':
    main_script()
