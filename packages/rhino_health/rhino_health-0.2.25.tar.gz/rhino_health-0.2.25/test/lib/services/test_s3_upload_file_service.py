import pytest

from rhino_health.lib.services.s3_upload_file_service import (
    MAX_CHUNK_SIZE,
    MAX_PART_SIZE,
    MIN_PART_SIZE,
    S3UploadFileService,
)


@pytest.mark.local
class TestS3uploadUtils:
    def test_chunk_part_size_calculator(self):
        file_size = MAX_CHUNK_SIZE * 2.5
        (
            part_size,
            parts_amount,
            chunk_amount,
        ) = S3UploadFileService._calculate_part_size_and_chunk_amount(file_size)
        assert part_size == MAX_PART_SIZE
        assert parts_amount == 100
        assert chunk_amount == 3

        file_size = MAX_CHUNK_SIZE + 1
        (
            part_size,
            parts_amount,
            chunk_amount,
        ) = S3UploadFileService._calculate_part_size_and_chunk_amount(file_size)
        assert part_size == MAX_PART_SIZE
        assert parts_amount == 100
        assert chunk_amount == 2

        file_size = MAX_CHUNK_SIZE
        (
            part_size,
            parts_amount,
            chunk_amount,
        ) = S3UploadFileService._calculate_part_size_and_chunk_amount(file_size)
        assert parts_amount == 100
        assert part_size == 107374183  # We round up to the nearest MB
        assert chunk_amount == 1

        file_size = MIN_PART_SIZE * 10
        (
            part_size,
            parts_amount,
            chunk_amount,
        ) = S3UploadFileService._calculate_part_size_and_chunk_amount(file_size)
        assert part_size == MIN_PART_SIZE
        assert parts_amount == 10
        assert chunk_amount == 1

        file_size = MAX_PART_SIZE
        (
            part_size,
            parts_amount,
            chunk_amount,
        ) = S3UploadFileService._calculate_part_size_and_chunk_amount(file_size)
        assert part_size == MIN_PART_SIZE
        assert parts_amount == 20
        assert chunk_amount == 1
