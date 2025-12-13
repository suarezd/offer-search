from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.domain.entities.job import Job


class IJobRepository(ABC):
    @abstractmethod
    async def save(self, job: Job) -> Job:
        pass

    @abstractmethod
    async def save_many(self, jobs: List[Job]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def find_by_id(self, job_id: str) -> Optional[Job]:
        pass

    @abstractmethod
    async def exists_by_id(self, job_id: str) -> bool:
        pass

    @abstractmethod
    async def search(
        self,
        search_term: Optional[str] = None,
        location: Optional[str] = None,
        company: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Job]:
        pass

    @abstractmethod
    async def count_total(self) -> int:
        pass

    @abstractmethod
    async def count_distinct_companies(self) -> int:
        pass

    @abstractmethod
    async def count_distinct_locations(self) -> int:
        pass

    @abstractmethod
    async def count_by_source(self) -> Dict[str, int]:
        pass

    @abstractmethod
    async def delete_by_id(self, job_id: str) -> bool:
        pass

    @abstractmethod
    async def update(self, job: Job) -> Job:
        pass
