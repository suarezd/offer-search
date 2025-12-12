class JobDomainException(Exception):
    """Base exception for all job domain errors"""
    pass


class JobValidationError(JobDomainException):
    """Raised when job validation fails"""
    pass


class DuplicateJobError(JobDomainException):
    """Raised when attempting to create a job that already exists"""

    def __init__(self, job_id: str):
        self.job_id = job_id
        super().__init__(f"Job with ID '{job_id}' already exists")


class JobNotFoundError(JobDomainException):
    """Raised when a job cannot be found"""

    def __init__(self, job_id: str):
        self.job_id = job_id
        super().__init__(f"Job with ID '{job_id}' not found")


class RepositoryError(JobDomainException):
    """Raised when there's an error in the repository layer"""

    def __init__(self, message: str, original_error: Exception = None):
        self.original_error = original_error
        super().__init__(message)


class InvalidSearchCriteriaError(JobDomainException):
    """Raised when search criteria are invalid"""
    pass
