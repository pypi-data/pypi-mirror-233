#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020, 2023 - Rafael Guerreiro Osorio - Ipea.

pynad - métodos de identificação

"""
import pyarrow as pa
import pyarrow.compute as pc
from .auxiliares import elapsed, CRCLR, UPCLR


IDVARS = ['ano', 'trimestre', 'upa', 'v1008', 'v1016',
          'v2001', 'v2003', 'v2005', 'v2007', 'v2008',
          'v20081', 'v20082', 'v2009']
KEYS = ['upa', 'v1008', 'v2003', 'v1016']


def cli_parcial(count, total, pid, cli_args):
    """Atualiza CLI."""
    print(CRCLR, UPCLR * 4)
    print(f'Montando paineis - {cli_args[0]} de {cli_args[1]} -',
          f'{elapsed(cli_args[2])}\n')
    print(f'PAINEL {pid}:')
    print(f'Identificando o painel - {count * 100 / total:.1f}%',
          f'(UPA {count} de {total})', end='', flush=True)


def identifica_painel(pid, table, cli_args):
    """Identifica um painel recebido como pyarrow table."""
    tabpid = table.select(IDVARS)
    classificadores = (__id_cls1__, __id_cls2__, __id_cls3__)
    upas = tuple(value[0].as_py() for value in
                 pc.value_counts(tabpid['upa']))
    uparows = []
    for idx, upa in enumerate(upas):
        cli_parcial(idx + 1, len(upas), pid, cli_args)
        doms = tuple(value[0].as_py() for value in
                     pc.value_counts(tabpid.filter(
                         pc.field('upa') == upa)['v1008']))
        for dom in doms:
            pessoas = tabpid.filter((pc.field('upa') == upa) &
                                    (pc.field('v1008') == dom)).to_pylist()
            pessoas = load_persons(pid, pessoas)
            # alguma pessoa tem data de nascimento ignorada
            if any(pessoa.dtd == 99 for pessoa in pessoas):
                __id_birthdate_unknown__(pessoas)

            # identificar e separar os grupos domésticos do domicílio
            grpsdom = __id_split_grpds__(pessoas)

            # identificar os indivíduos de cada grupo doméstico
            for grpdom in grpsdom:
                for classificador in classificadores:
                    classificadas = classificador(grpsdom[grpdom],
                                                  grpdom)
                    if classificadas:
                        break
                for pessoa in classificadas:
                    uparows.append(pessoa.classificada())
    dtypes = [pa.field('upa', pa.int32()),
              pa.field('pid', pa.int32()),
              pa.field('piddna', pa.int32())]
    dtypes.extend([pa.field(var, pa.int8()) for var in
                   ('v1008', 'v1016', 'v2003', 'pidcla',
                    'pidgrp', 'pidgrpent', 'pidind', 'pidindent',
                    'piddnd', 'piddnm')])
    dtypes = pa.schema(dtypes)
    return table.join(pa.Table.from_pylist(uparows, schema=dtypes), KEYS)


def __id_aggr_persons__(pessoas, estrita):
    """
    Agrega pessoas em indivíduos.

    **pessoas** são os registros das diferentes pessoas de todas
    as entrevistas realizadas em um domicílio

    **estrita** = True considera sexo, data de nascimento
    número de ordem e situação no domicílio

    **estrita** = False considera sexo e data de nascimento

    Retorna um dicionário de indivíduos com duas listas, a das entrevistas
    do indivíduo, e a das pessoas que lhe correspondem em cada entrevista
    """
    individuos = {}
    for pessoa in pessoas:
        identidade = pessoa.ident(estrita)
        if identidade not in individuos:
            individuos[identidade] = [[], []]
        individuos[identidade][0].append(pessoa.ent)
        individuos[identidade][1].append(pessoa)

    # se apenas sexo e data de nascimento, precisa controlar gemeos,
    # que aparecem como um indivíduo com entrevistas duplicadas
    # é preciso separá-los
    if not estrita:
        for individuo in list(individuos.keys()):
            reflist = list(set(individuos[individuo][0]))
            reflist.sort()
            if individuos[individuo][0] != reflist:
                for entrevista in reflist:
                    gemeos = [idx for idx, item in
                              enumerate(individuos[individuo][0])
                              if item == entrevista]
                    for gemeo, ordem in enumerate(gemeos):
                        identidade = individuo + 'gemeo' + str(gemeo + 1)
                        if identidade not in individuos:
                            individuos[identidade] = [[], []]
                        individuos[identidade][0].append(
                            individuos[individuo][1][ordem].ent)
                        individuos[identidade][1].append(
                            individuos[individuo][1][ordem])
                del individuos[individuo]

    # lista para conjunto de entrevistas do indivíduo
    for individuo in individuos:
        individuos[individuo][0] = list(set(individuos[individuo][0]))
    return individuos


def __id_birthdate_unknown__(pessoas):
    """
    Trata datas de nascimento ignoradas.

    Verifica se uma pessoa com data de nascimento ignorada em uma
    entrevista teve data declarada em outra, imputando a data em caso
    afirmativo
    """
    # separa as pessoas segundo a situação da data de nascimento
    dataign = [pessoa for pessoa in pessoas if pessoa.dtd == 99]
    datacon = [pessoa for pessoa in pessoas if pessoa.dtd != 99]
    for ign in dataign:

        # para cada pessoa com data ignorada, a lista de doadores
        # inicial considera todas as com data conhecida em outras
        # entrevistas, do mesmo sexo e, e com diferença de até
        # 3 anos do ano de nascimento estimado para a data ignorada
        doadores = [pessoa for pessoa in datacon
                    if pessoa.ent != ign.ent
                    and pessoa.sex == ign.sex
                    and abs(pessoa.dta - ign.dta) <= 3]

        # preferência para doadores com a mesma situação no domicílio
        # se existirem, desprezar os demais
        if [pessoa for pessoa in doadores if pessoa.std == ign.std]:
            doadores = [pessoa for pessoa in doadores
                        if pessoa.std == ign.std]

        # se não há doadores com a mesma situação no domicílio,
        # verificar se há doadores do conjunto permitido de troca
        # de código de situação, eliminando os que não estejam
        elif doadores:
            filtro = []
            if ign.std in (1, 2, 3):
                filtro = (1, 2, 3)
            elif ign.std in (4, 5, 6):
                filtro = (4, 5, 6)
            elif ign.std in (8, 9):
                filtro = (8, 9)
            else:
                filtro = (ign.std, )
            doadores = [doador for doador in doadores
                        if doador.std in filtro]

        # havendo doadores, a lista é ordenada pela proximidade
        # do ano de nascimento, sendo escolhido o mais próximo
        # o primeiro da lista
        if doadores:
            difs = [abs(doador.dta - ign.dta) for doador in doadores]
            mindif = [idx for idx, dif in enumerate(difs)
                      if dif == min(difs)][0]
            doador = doadores[mindif]
            ign.igd = doador.dtd
            ign.igm = doador.dtm
            ign.iga = doador.dta

    # imputa as datas de nascimento para as pessoas com data ignorada que
    # encontraram doadoras
    for pessoa in pessoas:
        if pessoa.igd:
            pessoa.dtd = pessoa.igd
            pessoa.dtm = pessoa.igm
            pessoa.dta = pessoa.iga
    return pessoas


def __id_cls1__(pessoas, grpdom):
    """Classificador 1, grupo doméstico sem mudanças."""
    # verifica se o tamanho do grupo doméstico é o mesmo
    # em todas as entrevistas e gera sua lista de entrevistas
    tamanho = pessoas[0].tam
    entdom = []
    for pessoa in pessoas:
        if pessoa.tam != tamanho:
            return []
        if pessoa.ent not in entdom:
            entdom.append(pessoa.ent)
    entdom.sort()

    # agrega as pessoas em indivíduos
    # estrita=True: sexo, data, ordem e sitdom
    individuos = __id_aggr_persons__(pessoas, True)

    # verifica se indivíduos aparecem em todas as entrevistas do grupo
    for individuo in individuos:
        if individuos[individuo][0] != entdom:
            return []

    # identifica as pessoas
    for idx, individuo in enumerate(individuos):
        for pessoa in pessoas:
            identidade = pessoa.ident(True)
            if identidade == individuo:
                pessoa.cla = 1
                pessoa.grp = grpdom
                pessoa.ind = idx + 1
                pessoa.indent = sum(2 ** (item - 1) for item in
                                    individuos[individuo][0])
                pessoa.grpent = sum(2 ** (item - 1) for item in
                                    entdom)
    return pessoas


def __id_cls2__(pessoas, grpdom):
    """Classificador 2 grupos domésticos com tamanho constante e mudanças."""
    # verifica se o tamanho do grupo doméstico é o mesmo
    # em todas as entrevistas e gera sua lista de entrevistas
    tamanho = pessoas[0].tam
    entdom = []
    for pessoa in pessoas:
        if pessoa.tam != tamanho:
            return []
        if pessoa.ent not in entdom:
            entdom.append(pessoa.ent)
    entdom.sort()

    # agrega as pessoas em indivíduos
    # estrita=False: sexo e data
    individuos = __id_aggr_persons__(pessoas, False)

    # verifica se indivíduos aparecem em todas as entrevistas do grupo
    for individuo in individuos:
        if individuos[individuo][0] != entdom:
            return []

    # identifica as pessoas controlando gemeos do mesmo sexo
    indents = {}
    for individuo in individuos:
        indents[individuo] = []
    for idx, individuo in enumerate(individuos):
        for pessoa in pessoas:
            if (pessoa in individuos[individuo][1]
                    and pessoa.ent not in indents[individuo]):
                pessoa.cla = 2
                pessoa.grp = grpdom
                pessoa.ind = idx + 1
                pessoa.indent = sum(2 ** (item - 1) for item in
                                    individuos[individuo][0])
                pessoa.grpent = sum(2 ** (item - 1) for item in
                                    entdom)
                indents[individuo].append(pessoa.ent)
    return pessoas


def __id_cls3__(pessoas, grpdom):
    """Classificador 3 grupos domésticos com mudanças variadas."""
    # recursiva para gerar todas as permutações de individuos
    # que não aparecem na mesma entrevista
    def __permuta__(indids, entrevistas, outras, possiveis):
        for outra in outras:
            entconjunta = entrevistas + individuos[outra][0]
            entconjunta.sort()

            possiveis.append([entconjunta, indids[:] + [outra]])
            if entconjunta != entdom:
                mais = [out for out in outras
                        if not any(ent in entconjunta
                                   for ent in individuos[out][0])]
                if mais:
                    possiveis = __permuta__(indids[:] + [outra],
                                            entconjunta[:], mais,
                                            possiveis)
        return possiveis

    # agrega indívíduos
    def __aggr_ind__(juntar, cla):
        individuos[juntar[1][0]][0] = juntar[0][:]
        for outra in juntar[1][1:]:
            individuos[juntar[1][0]][1].extend(
                individuos[outra][1])
            del individuos[outra]
        for pessoa in individuos[juntar[1][0]][1]:
            pessoa.cla = cla
        return juntar[1]

    # entrevistas do grupo doméstico
    entdom = []
    for pessoa in pessoas:
        if pessoa.ent not in entdom:
            entdom.append(pessoa.ent)
    entdom.sort()

    # agrega as pessoas em indivíduos
    # estrita=False: sexo e data
    individuos = __id_aggr_persons__(pessoas, False)

    # separa e classifica os indivíduos que aparecem em todas as entrevistas
    todas = [individuo for individuo in individuos
             if individuos[individuo][0] == entdom]
    for individuo in todas:
        for pessoa in individuos[individuo][1]:
            pessoa.cla = 3

    # separa e classifica provisoriamente os que aparecem em algumas
    algumas = [individuo for individuo in individuos
               if individuo not in todas]
    for individuo in algumas:
        for pessoa in individuos[individuo][1]:
            pessoa.cla = 4

    # permutações de indivíduos sem aparições conjuntas
    possibilidades = []
    for individuo in algumas:
        entrevistas = list(individuos[individuo][0])
        outras = [outra for outra in list(algumas)
                  if outra != individuo
                  and not any(entrevista in entrevistas
                              for entrevista in individuos[outra][0])]
        if outras:
            possibilidades.extend(__permuta__([individuo],
                                              entrevistas,
                                              outras, []))

    # reduzir permutações a combinações
    organizadas = []
    for possibilidade in possibilidades:
        if not organizadas:
            organizadas.append(possibilidade)
        elif possibilidade not in organizadas:
            adicionar = True
            for organizada in organizadas:
                if (organizada[0] == possibilidade[0]
                        and len(organizada[1]) == len(possibilidade[1])
                        and all(individuo in organizada[1]
                                for individuo in possibilidade[1])):
                    adicionar = False
                    break
            if adicionar:
                organizadas.append(possibilidade)

    # comparar todos os pares de atributos e registrar diferenças
    # a ordem de atribs é relevante
    atribs = ('sex', 'dtd', 'dtm', 'dta', 'std')
    for idx, organizada in enumerate(organizadas):
        organizadas[idx].append([])
        organizadas[idx].append([])
        organizadas[idx].append([])
        possiveis = organizada[1][:]
        while possiveis:
            possivel = possiveis.pop(0)
            pessoa1 = individuos[possivel][1][0]
            outras = [outra for outra in possiveis
                      if outra != possivel]
            for outra in outras:
                pessoa2 = individuos[outra][1][0]
                difs = [atrib for atrib in atribs
                        if pessoa1.__dict__[atrib] !=
                        pessoa2.__dict__[atrib]]
                organizadas[idx][2].append(difs)
                organizadas[idx][3].append([pessoa1.std, pessoa2.std])
                organizadas[idx][4].append([pessoa1.dta, pessoa2.dta])

    # ordenar as combinações para processar primeiro as
    # que resultariam em fusão de mais fragmentos e maior número
    # de entrevistas
    organizadas.sort(key=lambda item: len(item[0]) * 100 + len(item[1]) * 10
                     + 5 - max([len(difs) for difs in item[2]]),
                     reverse=True)

    # conjunto de erros permitidos
    erros = [['sex'],
             ['dtd'],
             ['dtm'],
             ['dta'],
             ['sex', 'dtd'],
             ['sex', 'dtm'],
             ['sex', 'dta'],
             ['dtd', 'dtm'],
             ['dtm', 'dta'],
             ['dtd', 'dta']]

    # com mudança de condição no domicílio
    erstd = [erro[:] + ['std'] for erro in erros]

    # agregar fragmentos de indivíduos
    juntados = []
    residuos = []
    for organizada in organizadas:
        if not any(individuo in organizada[1] for individuo in juntados):

            # fragmentos com mesma condição no domicílio
            # diferença de até 3 anos entre anos de nascimento
            if (all(erro in erros for erro in organizada[2])
                    and all(abs(dta[0] - dta[1]) <= 3
                            for dta in organizada[4])):
                juntados.extend(__aggr_ind__(organizada, 6))

            # fragmentos com diferente condição no domicílio
            # diferença de até 3 anos entre anos de nascimento
            elif (all(erro in erstd for erro in organizada[2])
                  and all(abs(dta[0] - dta[1]) <= 3
                          for dta in organizada[4])):
                juntados.extend(__aggr_ind__(organizada, 7))
            else:
                residuos.append(organizada)
                for individuo in organizada[1]:
                    for pessoa in individuos[individuo][1]:
                        pessoa.cla = 5

    # identifica as pessoas controlando gemeos do mesmo sexo
    indents = {}
    for individuo in individuos:
        indents[individuo] = []
    for idx, individuo in enumerate(individuos):
        for pessoa in pessoas:
            if (pessoa in individuos[individuo][1]
                    and pessoa.ent not in indents[individuo]):
                pessoa.grp = grpdom
                pessoa.ind = idx + 1
                pessoa.indent = sum(2 ** (item - 1) for item in
                                    individuos[individuo][0])
                pessoa.grpent = sum(2 ** (item - 1) for item in
                                    entdom)
                indents[individuo].append(pessoa.ent)
    return pessoas


def __id_split_grpds__(pessoas):
    """Identifica e separa os grupos domésticos de um domicílio."""
    # dicionário de grupos domésticos
    grpsdom = {}

    # separa as pessoas por entrevista
    ents = {}
    for pessoa in pessoas:
        if pessoa.ent not in ents:
            ents[pessoa.ent] = []
        ents[pessoa.ent].append(pessoa)

    # uma entrevista, um grupo; nada a separar...
    if len(ents) == 1:
        grpsdom[1] = pessoas
        for pessoa in grpsdom[1]:
            pessoa.grp = 1
        return grpsdom

    # se mais de uma entrevista
    # agrega as pessoas em indivíduos
    # estrita=False: sexo e, data
    individuos = __id_aggr_persons__(pessoas, False)

    # procurar a entrevista com mais pessoas com data de nascimento conhecida
    inicio = [(ent, len([pessoa for pessoa in ents[ent]
                         if pessoa.dtd < 99]))
              for ent in ents]
    inicio.sort(key=lambda e: e[1], reverse=True)
    ent = inicio[0][0]
    curdom = 0

    # processar entrevistas e ir retirando as atribuídas a um grupo
    # doméstico da lista de entrevistas
    while ents:

        # atribui ao primeiro grupo as pessoas da entrevista inicial
        # e a retira da lista
        curdom += 1
        grpsdom[curdom] = ents[ent]
        del ents[ent]

        # achar outras entrevistas com pessoas de indivíduos que estavam
        # na entrevista inicial e removê-las
        for individuo in individuos.values():
            if any(pessoa in grpsdom[curdom] for pessoa in individuo[1]):
                for ent in individuo[0]:
                    if ent in ents:
                        grpsdom[curdom].extend(ents[ent])
                        del ents[ent]
                    for ini in inicio:
                        if ini[0] == ent:
                            inicio.remove(ini)
                    if not ents:
                        break
            if not ents:
                break

        # verifica se há entrevistas não atribuídas, havendo
        # seleciona a com maior número de pessoas e reinicia o loop
        # criando outro grupo doméstico
        if inicio:
            ent = inicio[0][0]

    # reordenar pessoas
    reord = []
    for grpdom in grpsdom:
        grpsdom[grpdom].sort(key=lambda pessoa: pessoa.ent * 100 + pessoa.ord)
        reord.append([min([pessoa.ent for pessoa in grpsdom[grpdom]]), grpdom])
    reord.sort(key=lambda e: e[0])

    # ordenar grupos domésticos segundo a visita
    # o grupo 1 é o da primeira entrevista
    grpsdomord = {}
    for idx, val in enumerate(reord):
        grpsdomord[idx + 1] = grpsdom[val[1]]
    return grpsdomord


class Person():
    """
    representa um registro de pessoa.

    As instâncias desta classe representam registros de pessoas e
    seus atributos correspondem às variáveis empregadas na identificação,
    especificadas em __load_panel_metadata__(), função que retorna
    **attribs** e **categs** usados para criar uma instância;
    **values** é o registro como lista de valores e os
    códigos dos atributos da pessoa
    """

    def __init__(self, attribs, categs):
        for key, value in attribs.items():
            self.__dict__[key] = value
        self.sexcat = categs['sexcat'][str(self.sex)]
        self.stdcat = categs['stdcat'][str(self.std)] + 18 * ' '
        self.pid = 0
        self.cla = 0
        self.grp = 0
        self.ind = 0
        self.igi = 0
        self.igd = 0
        self.igm = 0
        self.iga = 0
        self.grpent = 0
        self.indent = 0

    def __repr__(self):
        """
        Retorna uma string que representa a pessoa.

        Contém os atributos usados na identificação,
        bem como os resultantes
        """
        repres = (f'e{self.ent} {self.sexcat[:3]} '
                  + f'{self.dta}-{self.dtm:02.0f}-{self.dtd:02.0f} '
                  + f'{self.ord:02.0f} {self.stdcat[:18]} '
                  + f'cla {self.cla} grpd {self.grp} ind {self.ind:02.0f}')
        if self.igd:
            repres += f' ({self.age} anos - {self.ano - self.age}-99-99)'
        return repres

    def classificada(self):
        """
        Retorna o registro da pessoa.

        como dicionário python para a tabela de identificação
        """
        names = ('upa', 'v1008', 'v1016', 'v2003', 'pid', 'pidcla',
                 'pidgrp', 'pidgrpent', 'pidind', 'pidindent',
                 'piddnd', 'piddnm', 'piddna')
        keys = ('upa', 'dom', 'ent', 'ord', 'pid', 'cla',
                'grp', 'grpent', 'ind', 'indent', 'igd', 'igm', 'iga')
        return {names[idx]: self.__dict__[keys[idx]]
                for idx in range(len(names))}

    def ident(self, estrita):
        """Retorna os atributos para a agregação em indivíduos."""
        idnt = f'{self.sexcat[:3]} '
        idnt += f'{self.dta}-{self.dtm:02.0f}-{self.dtd:02.0f}'
        if estrita:
            idnt += f' {self.ord:02.0f} {self.stdcat[:18]}'
        return idnt


def load_persons(pid, pessoas):
    """Carrega uma pessoa."""
    v2005 = {'1': 'pessoa responsável pelo domicílio',
             '2': 'cônjuge ou companheiro(a) de sexo diferente',
             '3': 'cônjuge ou companheiro(a) do mesmo sexo',
             '4': 'filho(a) do responsável e do cônjuge',
             '5': 'filho(a) somente do responsável',
             '6': 'enteado(a)',
             '7': 'genro ou nora',
             '8': 'pai, mãe, padrasto ou madrasta',
             '9': 'sogro(a)',
             '10': 'neto(a)',
             '11': 'bisneto(a)',
             '12': 'irmão ou irmã',
             '13': 'avô ou avó',
             '14': 'outro parente',
             '15': 'agregado(a) - não parente que não compartilha despesas',
             '16': 'convivente - não parente que compartilha despesas',
             '17': 'pensionista',
             '18': 'empregado(a) doméstico(a)',
             '19': 'parente do(a) empregado(a) doméstico(a)'}
    persons = []
    for pessoa in pessoas:
        attribs = {'ano': pessoa['ano'],
                   'tri': pessoa['trimestre'],
                   'upa': pessoa['upa'],
                   'dom': pessoa['v1008'],
                   'ent': pessoa['v1016'],
                   'tam': pessoa['v2001'],
                   'ord': pessoa['v2003'],
                   'std': pessoa['v2005'],
                   'sex': pessoa['v2007'],
                   'dtd': pessoa['v2008'],
                   'dtm': pessoa['v20081'],
                   'dta': pessoa['v20082'],
                   'age': pessoa['v2009']}
        categs = {'stdcat': v2005,
                  'sexcat': {'1': 'homem', '2': 'mulher'}}
        persons.append(Person(attribs, categs))
        persons[-1].pid = pid
        if persons[-1].dtd == 99:
            persons[-1].dta = int(persons[-1].pid / 10) - persons[-1].age
    return persons
