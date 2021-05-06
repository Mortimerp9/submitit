# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

import pytest
import asyncio
from pathlib import Path

from .test_core import FakeExecutor, _three_time
from . import core, submission, utils


@pytest.mark.asyncio
async def test_result(tmp_path: Path):
    executor = FakeExecutor(folder=tmp_path)
    job = executor.submit(_three_time, 8)
    result_task = asyncio.get_event_loop().create_task(job.async_result())
    with utils.environment_variables(_TEST_CLUSTER_="slurm", SLURM_JOB_ID=str(job.job_id)):
        submission.process_job(folder=job.paths.folder)
    result = await result_task
    assert result == 24

@pytest.mark.asyncio
async def test_results_single(tmp_path: Path):
    executor = FakeExecutor(folder=tmp_path)
    job = executor.submit(_three_time, 8)
    result_task = asyncio.get_event_loop().create_task(job.async_results())
    with utils.environment_variables(_TEST_CLUSTER_="slurm", SLURM_JOB_ID=str(job.job_id)):
        submission.process_job(folder=job.paths.folder)
    result = await result_task
    assert result == [24]