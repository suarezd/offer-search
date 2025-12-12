class JobDomainException(Exception):
    pass


class JobValidationError(JobDomainException):
    pass


class DuplicateJobError(JobDomainException):

    def __init__(self, job_id: str):
        self.job_id = job_id
        super().__init__(f"Job with ID '{job_id}' already exists")


class JobNotFoundError(JobDomainException):

    def __init__(self, job_id: str):
        self.job_id = job_id
        super().__init__(f"Job with ID '{job_id}' not found")


class RepositoryError(JobDomainException):

    def __init__(self, message: str, original_error: Exception = None):
        self.original_error = original_error
        super().__init__(message)


class InvalidSearchCriteriaError(JobDomainException):
    pass
