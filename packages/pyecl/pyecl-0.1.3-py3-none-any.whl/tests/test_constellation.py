import datetime
import json
import logging
import os
import pathlib
import random
import string
from zoneinfo import ZoneInfo

import boto3
import pytest

from pyecl import Constellation
from pyecl.exceptions import ConstellationObjectDoesNotExistException
from pyecl.models import Object, VariableUnitValue


def test_login(client):
    """Test that you can successfully login"""
    assert client.is_logged_in()


def test_me(client):
    """Test that the me endpoint works"""
    assert client.me() == {
        "Email": "service+manifold@emeraldcloudlab.com",
        "EmailAddress": "service+manifold@emeraldcloudlab.com",
        "Id": "id:n0k9mG8070Mk",
        "Type": "Object.User.Emerald.Developer",
        "Username": "service+manifold",
    }


# Download features


def test_simple_download(client):
    """Test a simple download on a single object"""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "Name") == "bsmith"


def test_multiple_objects_download(client):
    """Test a simple download on multiple objects"""
    assert client.download([Object("id:Z1lqpMzvkGMV"), Object("id:o1k9jAGmo6Jm")], "Name") == [
        "bsmith",
        "pavan.shah",
    ]


def test_multiple_field_download(client):
    """Test a simple download on multiple fields"""
    assert client.download(Object("id:Z1lqpMzvkGMV"), ["Name", "FirstName"]) == [
        "bsmith",
        "Ben",
    ]


def test_multiple_field_multiple_object_download(client):
    """Test a simple download multiple objects and fields"""
    assert client.download([Object("id:Z1lqpMzvkGMV"), Object("id:o1k9jAGmo6Jm")], ["Name", "FirstName"]) == [
        ["bsmith", "Ben"],
        ["pavan.shah", "Pavan"],
    ]


def test_download_non_existant_object(client):
    """Test a simple download on a non-existant object"""
    with pytest.raises(ConstellationObjectDoesNotExistException):
        client.download(Object("id:abc123"), "Name")


def test_download_non_existant_field(client):
    """Test a simple download on a non-existant field"""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "FakeField") is None


def test_download_empty_field(client):
    """Test a simple download on an empty field"""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "Biography") is None


def test_download_empty_link_field(client):
    """Test a simple download on an empty link field"""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "ProtocolStack") is None


def test_download_multiple_link_field(client):
    """Test a simple download on a non-existant field"""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "FinancingTeams") == [Object("id:1ZA60vLeXa7a")]


def test_download_all(client):
    """Test downloading all fields on an object"""
    all_dict = client.download(Object("id:Z1lqpMzvkGMV"))
    assert all_dict["Name"] == "bsmith"


# Downloading links


def test_chained_download(client):
    """Test that you can chain downloads off of links"""
    assert client.download(client.download(Object("id:Z1lqpMzvkGMV"), "FinancingTeams"), "Name") == ["Engineering"]


def test_single_traversal(client):
    """Test that you can traverse links"""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "FinancingTeams[Name]") == ["Engineering"]


def test_multiple_traversal(client):
    """Test that you can perform multiple link traversals in a single request"""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "FinancingTeams[BillingAddress[Name]]") == ["ECL-1"]


# Downloading various types


def test_download_integer(client):
    """Test that integer field types are correctly formatted"""
    assert client.download(Object("id:BYDOjvG4l3Ol"), "InjectionIndex") == 28


def test_download_string(client):
    """Test that string field types are correctly formatted"""
    assert client.download(Object("id:BYDOjvG4l3Ol"), "DataType") == "Analyte"


def test_download_quantity(client):
    """Test that quantity field types are correctly formatted"""
    assert client.download(Object("id:BYDOjvG4l3Ol"), "SampleVolume") == VariableUnitValue(10, "Microliters")


def test_download_date(client):
    """Test that date fields are correctly formatted"""
    # Note - retrieving the default units automatically is not yet supported
    assert client.download(Object("id:BYDOjvG4l3Ol"), "DateInjected") == datetime.datetime(2022, 1, 7, 17, 12, 19)


def test_file_download_with_automatic_download(client):
    """Test that files are automatically downloaded when requested"""
    cloud_file = client.download(Object("id:Z1lqpMzvkGMV"), "PhotoFile", auto_download_cloud_files=True)
    assert os.path.exists(cloud_file.local_path)


def test_file_download_without_automatic_download(client):
    """Test that files are not automatically downloaded when not requested"""
    cloud_file = client.download(Object("id:Z1lqpMzvkGMV"), "PhotoFile")
    assert cloud_file == Object("id:KBL5Dvw60ve7")
    assert cloud_file.local_path == ""


def test_blob_ref_download(client):
    """Test that blob refs are downloaded automatically correctly"""
    absorbance_data = client.download(Object("id:BYDOjvG4l3Ol"), "Absorbance")
    assert len(absorbance_data) == 7201
    assert len(absorbance_data[3]) == 2
    assert absorbance_data[3][0].unit == "'Minutes'"
    assert absorbance_data[3][1].unit == "'Milli' 'AbsorbanceUnit'"


def test_quantity_array_download(client):
    """Test that quantity arrays are downloaded correctly"""
    scatter_info = client.download(Object("id:BYDOjvG4l3Ol"), "Scattering")
    assert isinstance(scatter_info, list)
    assert len(scatter_info) == 361


def test_variable_unit_download(client):
    """Test that variable units are downloaded correctly"""
    composition = client.download(Object("id:O81aEB16GlJ1"), "Composition")
    assert isinstance(composition, list)
    assert len(composition) == 2
    assert isinstance(composition[0], list)
    assert len(composition[0]) == 2
    assert isinstance(composition[0][0], VariableUnitValue)
    assert composition[0][1] == Object("id:E8zoYvN6m61A")


def test_association_download(client):
    """Test that associations are downloaded correctly"""
    composition = client.download(Object("id:XnlV5jKZwmp3"), "ResolvedOptions")
    assert isinstance(composition, dict)
    assert len(composition) == 295
    assert isinstance(composition["AbsorbanceSamplingRate"], VariableUnitValue)
    assert composition["AbsorbanceSamplingRate"].value == 20
    assert composition["Instrument"] == Object("id:wqW9BP4ARZVw")


def test_single_upload_cloud_file(client, sample_file):
    """Create a dummy file and upload it as a cloud file"""

    file_name, contents = sample_file
    assert contents

    logging.info(f"uploading file {file_name} to cloud...")
    logging.info(contents)

    response = client.upload_cloud_file(file_name, None)
    resolved_object = response["resolved_object"]

    download_response = client.download(
        Object(resolved_object["id"]), ["id", "FileSize", "FileName", "FileType", "type"]
    )
    assert download_response[0] == resolved_object["id"]
    assert download_response[1] == VariableUnitValue(len(contents), "Bytes")
    assert download_response[2] == pathlib.Path(file_name).stem
    assert download_response[3] == '"txt"'
    assert download_response[4] == "Object.EmeraldCloudFile"
    assert "Notebook" not in download_response


def test_single_upload_cloud_file_with_notebook(client: Constellation, sample_file: tuple[str, str]):
    """Create a dummy file and upload it as a cloud file"""

    file_name, contents = sample_file
    assert contents

    logging.info(f"uploading file {file_name} to cloud...")
    logging.info(contents)

    response = client.upload_cloud_file(file_name, None)
    resolved_object = response["resolved_object"]

    download_response = client.download(
        Object(resolved_object["id"]), ["id", "FileSize", "FileName", "FileType", "type"]
    )
    assert download_response[0] == resolved_object["id"]
    assert download_response[1] == VariableUnitValue(len(contents), "Bytes")
    assert download_response[2] == pathlib.Path(file_name).stem
    assert download_response[3] == '"txt"'
    assert download_response[4] == "Object.EmeraldCloudFile"
    assert "Notebook" not in download_response


@pytest.fixture(scope="session")
def client():
    """Helper function to retrieve an actively logged in client

    This uses AWS secrets manager to retrieve credentials.  If you do not have access to
    ECL'S AWS secrets manager, you must override this function in order to run the tests.
    """
    secrets_client = boto3.session.Session().client(service_name="secretsmanager")
    credentials_secret = secrets_client.get_secret_value(SecretId="manifold-service-user-constellation-credentials")
    credentials_dict = json.loads(credentials_secret["SecretString"])
    username = credentials_dict["username"]
    password = credentials_dict["password"]

    # Now, get an auth token by logging into constellation for each environment
    client = Constellation(host="https://constellation-stage.emeraldcloudlab.com")
    client.login(username, password)
    return client


@pytest.fixture(scope="session")
def sample_file():
    test_file_path = f"cloud-file-test_{''.join(random.choices(string.ascii_lowercase, k=12))}.txt"

    entropy = "".join(random.choices(string.printable, k=30))
    contents = "\n".join(
        [
            "cloud file test!",
            f"generated on: {datetime.datetime.utcnow().replace(tzinfo=ZoneInfo('UTC')).isoformat()}",
            f"here's some entropy: {entropy}",
        ]
    )
    with open(test_file_path, "w") as f:
        f.write(contents)

    yield test_file_path, contents

    try:
        os.remove(test_file_path)
    except FileNotFoundError:
        pass
