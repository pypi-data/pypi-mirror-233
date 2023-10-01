import pathlib
import uuid

from ckanext.dcor_depot import s3
import pytest
import requests

from dcor_shared import sha256sum


data_path = pathlib.Path(__file__).parent / "data"


def test_create_bucket_again():
    bucket_name = f"test-circle-{uuid.uuid4()}"
    bucket = s3.require_bucket(bucket_name)
    # this is cached
    bucket2 = s3.require_bucket(bucket_name)
    assert bucket2 is bucket, "chached"
    s3.require_bucket.cache_clear()
    bucket3 = s3.require_bucket(bucket_name)
    assert bucket3 is not bucket, "new object"


def test_make_object_public(tmp_path):
    path = data_path / "calibration_beads_47.rtdc"
    bucket_name = f"test-circle-{uuid.uuid4()}"
    rid = str(uuid.uuid4())
    object_name = f"resource/{rid[:3]}/{rid[3:6]}/{rid[6:]}"
    s3_url = s3.upload_file(
        bucket_name=bucket_name,
        object_name=object_name,
        path=path,
        sha256=sha256sum(path),
        private=True)
    # Make sure object is not available publicly
    response = requests.get(s3_url)
    assert not response.ok, "resource is private"
    assert response.status_code == 403, "resource is private"
    # Make the object publicly accessible
    s3.make_object_public(bucket_name=bucket_name,
                          object_name=object_name)
    # Make sure the object is now publicly available
    response2 = requests.get(s3_url)
    assert response2.ok, "the resource is public, download should work"
    assert response2.status_code == 200, "download public resource"
    dl_path = tmp_path / "calbeads.rtdc"
    with dl_path.open("wb") as fd:
        fd.write(response2.content)
    assert sha256sum(dl_path) == sha256sum(path)


def test_presigned_url(tmp_path):
    path = data_path / "calibration_beads_47.rtdc"
    bucket_name = f"test-circle-{uuid.uuid4()}"
    rid = str(uuid.uuid4())
    object_name = f"resource/{rid[:3]}/{rid[3:6]}/{rid[6:]}"
    s3_url = s3.upload_file(
        bucket_name=bucket_name,
        object_name=object_name,
        path=path,
        sha256=sha256sum(path),
        private=True)
    # Make sure object is not available publicly
    response = requests.get(s3_url)
    assert not response.ok, "resource is private"
    # Create a presigned URL
    ps_url = s3.create_presigned_url(bucket_name=bucket_name,
                                     object_name=object_name)
    response2 = requests.get(ps_url)
    assert response2.ok, "the resource is shared, download should work"
    assert response2.status_code == 200, "download public resource"
    dl_path = tmp_path / "calbeads.rtdc"
    with dl_path.open("wb") as fd:
        fd.write(response2.content)
    assert sha256sum(dl_path) == sha256sum(path)


def test_upload_large_file(tmp_path):
    # Create a ~100MB file
    path = tmp_path / "large_file.rtdc"
    with path.open("wb") as fd:
        for ii in range(100):
            fd.write(b"0123456789"*100000)
    # Proceed as in the other tests
    bucket_name = f"test-circle-{uuid.uuid4()}"
    rid = str(uuid.uuid4())
    object_name = f"resource/{rid[:3]}/{rid[3:6]}/{rid[6:]}"
    s3_url = s3.upload_file(
        bucket_name=bucket_name,
        object_name=object_name,
        path=path,
        sha256=sha256sum(path),
        private=False)
    # Make sure object is available publicly
    response = requests.get(s3_url)
    assert response.ok, "the resource is public, download should work"
    assert response.status_code == 200, "download public resource"
    dl_path = tmp_path / "calbeads.rtdc"
    with dl_path.open("wb") as fd:
        fd.write(response.content)
    assert sha256sum(dl_path) == sha256sum(path)


def test_upload_private(tmp_path):
    path = data_path / "calibration_beads_47.rtdc"
    bucket_name = f"test-circle-{uuid.uuid4()}"
    rid = str(uuid.uuid4())
    object_name = f"resource/{rid[:3]}/{rid[3:6]}/{rid[6:]}"
    s3_url = s3.upload_file(
        bucket_name=bucket_name,
        object_name=object_name,
        path=path,
        sha256=sha256sum(path),
        private=True)
    # Make sure object is not available publicly
    response = requests.get(s3_url)
    assert not response.ok, "resource is private"
    assert response.status_code == 403, "resource is private"


def test_upload_public(tmp_path):
    path = data_path / "calibration_beads_47.rtdc"
    bucket_name = f"test-circle-{uuid.uuid4()}"
    rid = str(uuid.uuid4())
    object_name = f"resource/{rid[:3]}/{rid[3:6]}/{rid[6:]}"
    s3_url = s3.upload_file(
        bucket_name=bucket_name,
        object_name=object_name,
        path=path,
        sha256=sha256sum(path),
        private=False)
    # Make sure object is available publicly
    response = requests.get(s3_url)
    assert response.ok, "the resource is public, download should work"
    assert response.status_code == 200, "download public resource"
    dl_path = tmp_path / "calbeads.rtdc"
    with dl_path.open("wb") as fd:
        fd.write(response.content)
    assert sha256sum(dl_path) == sha256sum(path)


def test_upload_wrong_sha256():
    path = data_path / "calibration_beads_47.rtdc"
    bucket_name = f"test-circle-{uuid.uuid4()}"
    rid = str(uuid.uuid4())
    object_name = f"resource/{rid[:3]}/{rid[3:6]}/{rid[6:]}"
    with pytest.raises(ValueError, match="Checksum mismatch"):
        s3.upload_file(
            bucket_name=bucket_name,
            object_name=object_name,
            path=path,
            sha256="INCORRECT-CHECKSUM",
            private=False)
