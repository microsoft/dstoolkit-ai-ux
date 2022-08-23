import datetime
import re
import os
from unittest import TestCase

import requests
import yaml

__here__ = os.path.dirname(__file__)
CONFIGS_DIR = os.path.join(__here__, '..', 'app', 'demo_configs')
IMG_DIR = os.path.join(__here__, '..', 'app', 'static', 'assets', 'img')

EXPECTED_YML_KEYS = (
    'name', 'tagline', 'industry', 'use_case_type', 'license',
    'main_technology', 'released', 'updated', 'authors', 'description',
    'feature_bullets', 'images', 'links'
)
VALID_INDSUTRIES = (
    'Agriculture', 'Automotive', 'Banking', 'Energy', 'Insurance', 'Media',
    'Retail', 'Telecomms', 'Public Sector', 'Defense', 'Manufacturing',
    'Healthcare', 'Life Sciences', 'Insurance', 'Mining', 'Travel',
    'Cross-Industry'
)
VALID_USE_CASE_TYPES = (
    'Optimization', 'Regression', 'Classification', 'Clustering',
    'Search', 'Vision', 'NLP', 'Other'
)
EXPECTED_AUTHOR_KEYS = ('name', 'github_alias')
EXPECTED_IMAGE_KEYS = ('thumbnail_filename', 'screenshot_filename')


def get_yml_files():
    configs_dir_files = os.listdir(CONFIGS_DIR)
    yml_files = [
        yml_file for yml_file in configs_dir_files
        if yml_file.endswith('.yml')
    ]
    return yml_files


def get_order_files():
    order_filepath = os.path.join(CONFIGS_DIR, '.order')
    with open(order_filepath, 'r') as f:
        demo_order = [f.strip('\n') for f in f.readlines()]
    return demo_order


def get_yml_file_data(yml_files):
    yml_file_data = {}
    for yml_file in yml_files:
        with open(os.path.join(CONFIGS_DIR, yml_file), 'r') as f:
            yml_file_data[yml_file] = yaml.safe_load(f)
    return yml_file_data


def get_image_files():
    demo_screenshot_files = os.listdir(
        os.path.join(IMG_DIR, 'demo_screenshots')
    )
    demo_thumbnail_files = os.listdir(
        os.path.join(IMG_DIR, 'demo_thumbnails')
    )
    return demo_screenshot_files, demo_thumbnail_files


class TestDemoConfigs(TestCase):
    def setUp(self):
        self.order_files = get_order_files()
        self.yml_files = get_yml_files()
        self.yml_file_data = get_yml_file_data(self.yml_files)

    def test_use_cases_in_order_file(self):
        for yml_file in self.yml_files:
            if re.sub('\.yml$', '', yml_file) not in self.order_files:
                msg = '{} missing from .order file'.format(
                    re.sub('\.yml$', '', yml_file)
                )
                raise ValueError(msg)

    def test_expected_keys_in_yml_files(self):
        for yml_file, yml_data in self.yml_file_data.items():
            for key in EXPECTED_YML_KEYS:
                if key not in yml_data:
                    msg = f'{key} not found in {yml_file} demo config'
                    raise KeyError(msg)
    
    def test_industry_is_valid(self):
        for yml_file, yml_data in self.yml_file_data.items():
            industry = yml_data['industry']
            if industry not in VALID_INDSUTRIES:
                msg = f'"{industry}" Industry given for {yml_file} not valid. '
                msg += 'Valid industries: {}'.format(
                    ', '.join(VALID_INDSUTRIES)
                )
                raise ValueError(msg)

    def test_use_case_is_valid(self):
        for yml_file, yml_data in self.yml_file_data.items():
            use_case_type = yml_data['use_case_type']
            if use_case_type not in VALID_USE_CASE_TYPES:
                msg = f'Use Case Type "{use_case_type}" given for {yml_file}'
                msg += ' not valid. '
                msg += 'Valid Use Case Types: {}'.format(
                    ', '.join(VALID_USE_CASE_TYPES)
                )
                raise ValueError(msg)

    def test_date_format(self):
        for yml_file, yml_data in self.yml_file_data.items():
            released = yml_data['released']
            updated = yml_data['updated']
            try:
                datetime.datetime.strptime(released, '%Y-%m-%d')
            except ValueError:
                msg = f'Released date "{released}" for {yml_file}'
                msg += " doesn't match format '%Y-%m-%d'"
                raise ValueError(msg)
            try:
                datetime.datetime.strptime(updated, '%Y-%m-%d')
            except ValueError:
                msg = f'Released date "{updated}" for {yml_file}'
                msg += " doesn't match format '%Y-%m-%d'"
                raise ValueError(msg)

    def test_valid_authors(self):
        for yml_file, yml_data in self.yml_file_data.items():
            for author in yml_data['authors']:
                for key in EXPECTED_AUTHOR_KEYS:
                    if key not in author:
                        msg = f'Author missing {key} data in {yml_file}'
                        raise ValueError(msg)
                github_alias = author['github_alias']
                response = requests.get(f'https://github.com/{github_alias}')
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError:
                    msg = f"Github Alias '{github_alias}' from {yml_file}"
                    msg += " not found."
                    raise ValueError(msg)
    
    def test_feature_bullets(self):
        for yml_file, yml_data in self.yml_file_data.items():
            if not len(yml_data['feature_bullets']):
                raise ValueError(f'No feature bullets found for {yml_file}')

    def test_images_present(self):
        demo_screenshot_files, demo_thumbnail_files = get_image_files()
        for yml_file, yml_data in self.yml_file_data.items():
            for key in EXPECTED_IMAGE_KEYS:
                if key not in yml_data['images']:
                    msg = f'Key {key} not found in "images" data for {yml_file}'
                    raise KeyError(msg)
            screenshot = yml_data['images']['screenshot_filename']
            thumbnail = yml_data['images']['thumbnail_filename']
            if screenshot not in demo_screenshot_files:
                msg = f'{screenshot} screenshot for {yml_file} not found'
                msg += ' in demo_screenshots directory.'
                raise ValueError(msg)
            if thumbnail not in demo_thumbnail_files:
                msg = f'{thumbnail} thumbnail for {yml_file} not found'
                msg += ' in demo_thumbnails directory.'
                raise ValueError(msg)

    def test_links_valid(self):
        for yml_file, yml_data in self.yml_file_data.items():
            for link_type, link in yml_data['links'].items():
                # Dummy link
                if link == '#':
                    continue
                # Currently our repo is private so these links return 404
                ds_toolkit_url = 'https://github.com/microsoft/dstoolkit-ai-ux'
                if link.startswith(ds_toolkit_url):
                    continue
                response = requests.get(link)
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError:
                    msg = f"{link_type} link {link} for {yml_file}"
                    msg += " could not be found."
                    raise ValueError(msg)
