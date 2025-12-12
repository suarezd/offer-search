from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobsSubmitRequest, JobsSubmitResponse, JobResponse, JobFilter
from typing import List

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

@router.post("/submit", response_model=JobsSubmitResponse)
def submit_jobs(request: JobsSubmitRequest, db: Session = Depends(get_db)):
    inserted = 0
    duplicates = 0

    for job_data in request.jobs:
        existing = db.query(Job).filter(Job.id == job_data.id).first()

        if existing:
            duplicates += 1
            continue

        new_job = Job(
            id=job_data.id,
            title=job_data.title,
            company=job_data.company,
            location=job_data.location,
            url=job_data.url,
            posted_date=job_data.posted_date,
            description=job_data.description,
            source=job_data.source,
            scraped_at=job_data.scraped_at
        )
        db.add(new_job)
        inserted += 1

    db.commit()

    return JobsSubmitResponse(
        success=True,
        inserted=inserted,
        duplicates=duplicates,
        total=len(request.jobs)
    )

@router.post("/search", response_model=List[JobResponse])
def search_jobs(filters: JobFilter, db: Session = Depends(get_db)):
    query = db.query(Job)

    if filters.search:
        search_term = f"%{filters.search}%"
        query = query.filter(
            or_(
                Job.title.ilike(search_term),
                Job.company.ilike(search_term),
                Job.description.ilike(search_term)
            )
        )

    if filters.location:
        query = query.filter(Job.location.ilike(f"%{filters.location}%"))

    if filters.company:
        query = query.filter(Job.company.ilike(f"%{filters.company}%"))

    if filters.source:
        query = query.filter(Job.source == filters.source)

    query = query.order_by(Job.created_at.desc())
    query = query.offset(filters.offset).limit(filters.limit)

    return query.all()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total_jobs = db.query(func.count(Job.id)).scalar()
    total_companies = db.query(func.count(func.distinct(Job.company))).scalar()
    total_locations = db.query(func.count(func.distinct(Job.location))).scalar()

    jobs_by_source = {}
    sources = db.query(Job.source, func.count(Job.id)).group_by(Job.source).all()
    for source, count in sources:
        jobs_by_source[source] = count

    return {
        "total_jobs": total_jobs,
        "total_companies": total_companies,
        "total_locations": total_locations,
        "jobs_by_source": jobs_by_source
    }
