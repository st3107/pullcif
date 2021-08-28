import random
import typing
from pathlib import Path
from pymatgen.ext.matproj import MPRester as MPR
import requests
import math
import fire


def get_api_key():
    #key = input('Please enter the API:\n')
    key = '1TFu8VlEkS4rfewO'
    return key


def search_all_id():
    """Search all material id on Material Project with certain limits.

        Parameters
        ----------
        None.

        Returns
        -------
        final_list(list):
            A list of all material ids with set limitations.
            E.g.
            final_list = ['id_1', 'id_2', 'id_3']
    """

    # Quering with MPRester to obtain corresponding material id, reduced formula and space group.
    with MPR(get_api_key()) as m:

        # Criteria is set as greater than -1 to search materials, which is unphysical in real world, therefore in effect
        # search all available materials.
        llist = m.query(criteria={'band_gap': {'$gt': -1}}, properties=['material_id', 'pretty_formula','spacegroup'],
                        # Chunk size is set as 0 for no chunking.
                        chunk_size=0)

        # Generate an empty dictionary for further sampling.
        space_group_dict = dict()

        # To loop all items in space_group_dict and to label by their space groups.
        for index in llist:

            # To find space group in Hall Symbol.
            space_group = index['spacegroup']['hall']

            # If the item space group is not in space_group_dict, then add it and create an empty value list for further
            # storing.
            if space_group not in space_group_dict:
                space_group_dict[space_group] = []

            # To append the material id (str) to the list(value) of corresponding space group (key).
            space_group_dict[space_group].append(index['material_id'])

        # To sample the space_group_dict by random_sample.
        final_list = random_sample(space_group_dict, 0.01)

    return final_list


def random_sample(dict, ratio):
    """Search all material id on Material Project with certain limits.

        Parameters
        ----------
        dict(dictionary):
            A dictionary with keys of space groups and values of corresponding material ids. The material
            id must be stored in form of list.
            E.g.
            dict = {'P 1':,['id_1', 'id_2', 'id_3']}

        ratio(float):
            For each space group, only certain ratio of total amount are sampled.

        Returns
        -------
        final_list(list):
            A list of all material ids with set limitations.
            E.g.
            final_list = ['id_1', 'id_2', 'id_3']
    """

    # To create an empty list for storing sampled material ids(str).
    final_list = []

    # To loop the sampled dictionary.
    for index in dict:

        # To obtain the size of all materials(value) in a certain space group(key)
        value_size = len(dict[index])

        # To ignore space group whose material size is less than 25 items.
        if value_size >= 25:

            # Round up the sampling size of space group
            sample_size = math.ceil(ratio * value_size)

            # Random sampling
            random_sample = random.sample(dict[index], sample_size)

            # To replace old material list with new one.
            dict[index] = random_sample

        # To append all list together.
        for pointer in dict[index]:
            final_list.append(pointer)

    return final_list



def download_cif(output_dir: str, query: dict = None, config: typing.Dict[str, typing.Any] = None) -> None:
    """Download the CIF files from the Materials Project Database.

    Parameters
    ----------
    output_dir :
        The output directory. The cif files will be saved there.
    query :
        The query for the cif files. It will be parsed and used as the filter to search in database.
    config :
        The configuration for the functionality.

    Returns
    -------
    None.
    """

    # Initialise inputs.
    if config is None:
        config = {}
    if output_dir is None:
        output_dir = 'pullcif/data'

    # If query is empty, then search all material ids.
    if query is None:
        query = search_all_id()

    # To designate output path, if it isn't a directory, then create it.
    _output_dir = Path(output_dir)
    if not _output_dir.is_dir():
        _output_dir.mkdir(parents=True)

    # To loop all query ids.
    for id in query:
        url = 'https://materialsproject.org/materials/' + id + '/cif?type=symmetrized'

        # To get cif files.
        res = requests.get(url)

        # To query material reduced formulae.
        material_property = MPR(get_api_key()).query(criteria=id, properties=['material_id', 'pretty_formula'])
        formula = material_property[0]['pretty_formula']
        material_id = material_property[0]['material_id']

        # To write and save files in designated path.
        fileName = '\\' + material_id + '_' + formula + '.cif'
        cif_file = open(output_dir + fileName, 'w')
        cif_file.write(res.text)
        cif_file.close()

def cli():
    """The cli interface."""
    fire.Fire(download_cif)
    pass