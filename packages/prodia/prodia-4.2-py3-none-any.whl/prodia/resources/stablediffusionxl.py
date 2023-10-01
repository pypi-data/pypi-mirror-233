from prodia.resources.engine import Engine
import time
import asyncio


class StableDiffusionXL(Engine):
    def __init__(self, api_key, base_url=None):
        self.base = base_url or "https://api.prodia.com/v1"
        self.api_key = api_key

    def generate(self, params):
        return super()._post(url=f"{self.base}/sdxl/generate", body=params, api_key=self.api_key)

    def get_job(self, job_id):
        return super()._get(url=f"{self.base}/job/{job_id}", api_key=self.api_key)

    def models(self):
        return super()._get(url=f"{self.base}/sdxl/models", api_key=self.api_key)

    def loras(self):
        return super()._get(url=f"{self.base}/sdxl/loras", api_key=self.api_key)

    def wait_for(self, job):
        job_result = job

        while job_result['status'] not in ['succeeded', 'failed']:
            time.sleep(0.25)
            job_result = self.get_job(job['job'])

        if job_result['status'] == 'failed':
            raise Exception("Job failed")

        return job_result


class AsyncStableDiffusionXL(Engine):
    def __init__(self, api_key, base_url=None):
        self.base = base_url or "https://api.prodia.com/v1"
        self.api_key = api_key

    async def generate(self, params):
        return await super()._apost(url=f"{self.base}/sdxl/generate", body=params, api_key=self.api_key)

    async def get_job(self, job_id):
        return await super()._aget(url=f"{self.base}/job/{job_id}", api_key=self.api_key)

    async def models(self):
        return await super()._aget(url=f"{self.base}/sdxl/models", api_key=self.api_key)

    async def loras(self):
        return await super()._aget(url=f"{self.base}/sdxl/loras", api_key=self.api_key)

    async def wait_for(self, job):
        job_result = job

        while job_result['status'] not in ['succeeded', 'failed']:
            await asyncio.sleep(0.25)
            job_result = await self.get_job(job['job'])

        if job_result['status'] == 'failed':
            raise Exception("Job failed")

        return job_result