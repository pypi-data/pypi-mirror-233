from prodia.resources.engine import Engine
import time
import asyncio


class Upscaler(Engine):
    def __init__(self, api_key, base_url=None):
        self.base = base_url or "https://api.prodia.com/v1"
        self.api_key = api_key

    def upscale(self, params):
        return super()._post(url=f"{self.base}/upscale", body=params, api_key=self.api_key)

    def get_job(self, job_id):
        return super()._get(url=f"{self.base}/job/{job_id}", api_key=self.api_key)

    def wait_for(self, job):
        job_result = job

        while job_result['status'] not in ['succeeded', 'failed']:
            time.sleep(0.25)
            job_result = self.get_job(job['job'])

        if job_result['status'] == 'failed':
            raise Exception("Job failed")

        return job_result


class AsyncUpscaler(Engine):
    def __init__(self, api_key, base_url=None):
        self.base = base_url or "https://api.prodia.com/v1"
        self.api_key = api_key

    async def upscale(self, params):
        return await super()._apost(url=f"{self.base}/upscale", body=params, api_key=self.api_key)

    async def get_job(self, job_id):
        return await super()._aget(url=f"{self.base}/job/{job_id}", api_key=self.api_key)

    async def wait_for(self, job):
        job_result = job

        while job_result['status'] not in ['succeeded', 'failed']:
            await asyncio.sleep(0.25)
            job_result = await self.get_job(job['job'])

        if job_result['status'] == 'failed':
            raise Exception("Job failed")

        return job_result