import os
import shutil
import gzip
import pathlib
import json
import pytest
import tempfile
from bids import BIDSLayout
from bids.layout.models import BIDSImageFile, BIDSJSONFile
from typing import Union
from difflib import get_close_matches


def get_versions():
     #collect version from pyproject.toml
    places_to_look = [pathlib.Path(__file__).parent.absolute(), pathlib.Path(__file__).parent.parent.absolute()]

    __version__ = "unable to locate version number in pyproject.toml"
    
    # we use the default version at the time of this writing, but the most current version
    # can be found in the pyproject.toml file under the [tool.bids] section
    __bids_version__ = "1.8.0"
    
    # search for toml file
    for place in places_to_look:
        for root, folders, files in os.walk(place):
            for file in files:
                if file.endswith("pyproject.toml"):
                    toml_file = os.path.join(root, file)

                    with open(toml_file, "r") as f:
                        for line in f.readlines():
                            if "version" in line and len(line.split("=")) > 1 and "bids_version" not in line:
                                __version__ = line.split("=")[1].strip().replace('"', "")
                            if "bids_version" in line and len(line.split("=")) > 1:
                                __bids_version__ = line.split("=")[1].strip().replace('"', "")
                    break
    return {"ingest_pet_version": __version__, "bids_version": __bids_version__}

def zip_nifti(nifti_file):
    """Zips an un-gzipped nifti file and removes the original file."""
    if str(nifti_file).endswith('.gz'):
        return nifti_file
    else:
        with open(nifti_file, 'rb') as infile:
            with gzip.open(nifti_file + '.gz', 'wb') as outfile:
                shutil.copyfileobj(infile, outfile)
        os.remove(nifti_file)
        return nifti_file + '.gz'

def write_out_dataset_description_json(input_bids_dir, output_bids_dir=None):

    # set output dir to input dir if output dir is not specified
    if output_bids_dir is None:
        output_bids_dir = pathlib.Path(os.path.join(input_bids_dir, "derivatives", "petdeface"))
        output_bids_dir.mkdir(parents=True, exist_ok=True)

    # collect name of dataset from input folder
    try:
        with open(os.path.join(input_bids_dir, 'dataset_description.json')) as f:
            source_dataset_description = json.load(f)
    except FileNotFoundError:
        source_dataset_description = {"Name": "Unknown"}

    with open(os.path.join(output_bids_dir, 'dataset_description.json'), 'w') as f:
        dataset_description = {
            "Name": f"description verygeneric - this is a placeholder: "
                    f"Not much to read here, if this has been published you've messed up`{source_dataset_description['Name']}`",
            "BIDSVersion": __bids_version__,
            "GeneratedBy": [
                {"Name": "TBD",
                 "Version": __version__,
                 "CodeURL": "https://github.com/someuser/someproject"}],
            "HowToAcknowledge": "This ________ uses ______________: `Someone, A., A Title. Journal, 2099. 12(3): p. 1-5.`,"
                                "and the ___________ developed by Some other person: `https://notarealurl.super.fake/extremelyfake`",
            "License": "CCBY"
        }

        json.dump(dataset_description, f, indent=4)

def collect_anat_and_pet(bids_data: Union[pathlib.Path, BIDSLayout], suffixes=["T1w", "T2w"], subjects: list=[]):
    if type(bids_data) is BIDSLayout:
        pass
    elif isinstance(bids_data, (pathlib.PosixPath, pathlib.WindowsPath)) and bids_data.exists():
        bids_data = BIDSLayout(bids_data)
    else:
        raise TypeError(f"{bids_data} must be a BIDSLayout or valid Path object, given type: {type(bids_data)}.")
    
    # return all subjects if no list of subjects is given
    if subjects == []:
        subjects = bids_data.get_subjects()

    mapped_pet_to_anat = {}
    for subject in subjects:
        mapped_pet_to_anat[subject] = {}
    for subject in subjects:
        pet_files = bids_data.get(subject=subject, suffix="pet")
        anat_files = [a.path for a in bids_data.get("anat",suffix=suffixes, subject=subject, extension=["nii", "nii.gz"])]
        # for each pet image file we create an entry our mapping dictionary
        for entry in pet_files:
            if type(entry) is BIDSImageFile:
                try:
                    # search through anatomical files and find the closest match
                    mapped_pet_to_anat[subject][entry.path] = get_close_matches(entry.path, anat_files, n=1)[0]
                except IndexError:
                    mapped_pet_to_anat[subject][entry.path] = ''
    return mapped_pet_to_anat
