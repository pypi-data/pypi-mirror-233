import asyncio

import httpx

from .notifier import OSAScriptNotifier


class BitBucket:
    def __init__(self, auth):
        self.auth = auth
        self.ENDPOINT = 'https://api.bitbucket.org/2.0'
        self.repositories = []
        self.state = []

    def get_repos(self):
        print('Getting repos')
        output = asyncio.run(self._get_first_repo())
        self.repositories = list(self.parse_repos(output))
        pages = int(output.get('size') / output.get('pagelen'))
        output = asyncio.run(self._get_all_pages(pages))
        for page in output:
            self.repositories += list(self.parse_repos(page))

    async def _get(self, client, url):
        r = await client.get(url, auth=self.auth.auth)
        return r.json()

    async def _get_first_repo(self):
        url = f'{self.ENDPOINT}/repositories/cioapps'
        async with httpx.AsyncClient() as client:
            r = await self._get(client, url)
            return r

    async def _get_all_pages(self, pages: int):
        async with httpx.AsyncClient() as client:
            tasks = []
            for page in range(1, pages + 1):
                url = f'{self.ENDPOINT}/repositories/cioapps?page={page + 1}'
                tasks.append(asyncio.ensure_future(self._get(client, url)))

            repos = await asyncio.gather(*tasks)
            return repos

    def parse_repos(self, output: dict):
        for repo in output.get('values'):
            yield repo.get('name')

    def _get_pipelines(self, repo: str):
        r = httpx.get(f"{self.ENDPOINT}/repositories/cioapps/{repo}/pipelines?sort=-created_on", auth=self.auth.auth)
        return r.json()

    def check(self, repo: str):
        pipelines = self._get_pipelines(repo)
        self.print_pipeline(pipelines)
        if self.update_state(pipelines):
            OSAScriptNotifier.notify(f"BitBucket {repo} pipeline", "Pipeline state changed")

    def update_state(self, pipelines: dict):
        state = []
        for pipeline in pipelines.get('values'):
            # print(pipeline)
            state.append(self.parse_state(pipeline))

        if self.state != state and self.state != []:
            return True

        self.state = state
        return False

    def print_pipeline(self, pipelines: dict):
        for pipeline in pipelines.get('values'):
            print(
                f"Pipeline: {pipeline.get('state').get('name')} {pipeline.get('created_on')} {pipeline.get('duration_in_seconds')}s")

    def parse_state(self, pipeline: dict):
        return pipeline.get('uuid'), pipeline.get('state').get('name')
        pass
