#####
pynad
#####
An application to download, sync, organize and prepare the microdata and metadata of the Brazilian National Household Survey, **Pesquisa Nacional por Amostra de Domicílios Contínua** - **Pnadc** - fielded by the Instituto Brasileiro de Geografia e Estatística, `IBGE <http://www.ibge.gov.br>`_.

The **PNADC** is a rotating panel survey. The residential dwellings sampled for a panel are visited five times, quarterly. Every quarter a new panel starts, thus there are five active panels in visits 1 to 5. However, IBGE only disseminates Pnadc microdata as cross-section datasets, aggregating records from distinct panels. The *trimestral* and the *anual-trimestre* datasets are aggregates of the distinct visits of the five panels surveyed in a quarter; the *anual-visita* datasets are annual aggregates of first or fifth visit interviews, comprised by four panels visited for the first or fifth time in a year.

----------------
What pynad does?
----------------
**IBGE periodically releases new PNADC datasets and documents. Eventually, previously released datasets and documents are patched. Currently, there are more than a hundred files to download and monitor for updates.**

Pynad ascertains one always have the latest versions of data and documents, and helps to keep track of the versions used in an application. It clones the *Microdados* folder of the Pnadc distributions at IBGE's `FTP server <ftp://ftp.ibge.gov.br/>`_ copying all its files to a local folder, syncing it at user demand.

**PNADC datasets are disseminated as text files with fixed width records. The position of each variable in the record must be declared to load them. The full metadata (names and columns of variables, categories etc.) are in binary xls Excel files.**

Pynad converts the original microdata to standard **csv** text files and/or **parquet** binary files; conveniently organizes copies of the original *dicionários de variáveis*; and generates machine and human readable **json** text files containing all metadata. The new files are stored in the archive containing the local copy of the PNADC, in distinct folders.

When the local copy is synced, pynad updates the metadata and **csv** and/or **parquet** files on a need basis.

**PNADC datasets are organized for use as a quarterly or annual cross-section survey, mixing records from 4 or 5 distinct panels. One panel has variables scattered in different datasets. Though dwellings are identified, households and individuals are not. Population weights are not available for the panels**

Pynad creates another archive for panel files. It separates the panels retrieving their records from the cross-sectional datasets, then pynad identifies the households and individuals in each dwelling and generates and generates a **parquet**  and/or a **csv**  microdata file for each panel.
Original variables have up to five instances in the identified individual records. E.g. for literacy, v3001, the identified individual record has v3001_1, v3001_2 v3001_3, v3001_4, v3001_5.

Pynad updates the panel files on a need basis.

-------
Install
-------
`Windows <https://docs.python.org/3/using/windows.html#install-layout-option>`_ users should add Python to the PATH environment variable.

Use `pip <https://docs.python.org/3/installing/index.html#installing-index>`_ to install pynad.

Type *pynad* in a terminal to run it.

************
Requirements
************
Two additional packages will be installed: `pyarrow <https://pypi.org/project/pyarrow/>`_, `xlrd <https://pypi.org/project/xlrd/>`_.

At least 200GB free storage if generating uncompressed **csv** files.