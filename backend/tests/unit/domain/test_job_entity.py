import pytest
from datetime import datetime

from app.domain.entities.job import Job


@pytest.mark.unit
class TestJobEntityCreation:

    def test_create_job_with_all_fields(self, valid_job_data):
        job = Job(**valid_job_data)

        assert job.id == "job-123"
        assert job.title == "Senior Python Developer"
        assert job.company == "TechCorp"
        assert job.location == "Paris, France"
        assert job.url == "https://linkedin.com/jobs/view/123"
        assert job.source == "linkedin"
        assert job.posted_date == "2 days ago"
        assert job.description == "We are looking for a senior Python developer..."
        assert job.scraped_at == datetime(2025, 12, 12, 10, 30, 0)
        assert job.created_at == datetime(2025, 12, 12, 10, 30, 0)
        assert job.updated_at is None

    def test_create_job_with_minimal_fields(self, minimal_job_data):
        job = Job(**minimal_job_data)

        assert job.id == "job-minimal"
        assert job.title == "Developer"
        assert job.company == "Company"
        assert job.location == "Location"
        assert job.url == "https://example.com/job"
        assert job.source == "linkedin"
        assert job.posted_date is None
        assert job.description is None
        assert job.scraped_at is None
        assert job.created_at is None
        assert job.updated_at is None


@pytest.mark.unit
class TestJobEntityValidation:

    @pytest.mark.parametrize("field_name,error_field", [
        ("id", "ID"),
        ("title", "title"),
        ("company", "company"),
        ("location", "location"),
        ("url", "URL"),
        ("source", "source")
    ])
    def test_required_fields_cannot_be_empty_string(self, valid_job_data, field_name, error_field):
        valid_job_data[field_name] = ""

        with pytest.raises(ValueError, match=f"Job {error_field} cannot be empty"):
            Job(**valid_job_data)

    @pytest.mark.parametrize("field_name,error_field", [
        ("id", "ID"),
        ("title", "title"),
        ("company", "company"),
        ("location", "location"),
        ("url", "URL"),
        ("source", "source")
    ])
    def test_required_fields_cannot_be_whitespace(self, valid_job_data, field_name, error_field):
        valid_job_data[field_name] = "   "

        with pytest.raises(ValueError, match=f"Job {error_field} cannot be empty"):
            Job(**valid_job_data)

    def test_id_cannot_exceed_50_characters(self, valid_job_data):
        valid_job_data["id"] = "a" * 51

        with pytest.raises(ValueError, match="Job ID cannot exceed 50 characters"):
            Job(**valid_job_data)

    def test_id_with_exactly_50_characters_is_valid(self, valid_job_data):
        valid_job_data["id"] = "a" * 50

        job = Job(**valid_job_data)
        assert len(job.id) == 50

    def test_title_cannot_exceed_255_characters(self, valid_job_data):
        valid_job_data["title"] = "a" * 256

        with pytest.raises(ValueError, match="Job title cannot exceed 255 characters"):
            Job(**valid_job_data)

    def test_company_cannot_exceed_255_characters(self, valid_job_data):
        valid_job_data["company"] = "a" * 256

        with pytest.raises(ValueError, match="Job company cannot exceed 255 characters"):
            Job(**valid_job_data)

    def test_location_cannot_exceed_255_characters(self, valid_job_data):
        valid_job_data["location"] = "a" * 256

        with pytest.raises(ValueError, match="Job location cannot exceed 255 characters"):
            Job(**valid_job_data)

    def test_url_cannot_exceed_500_characters(self, valid_job_data):
        valid_job_data["url"] = "https://example.com/" + "a" * 500

        with pytest.raises(ValueError, match="Job URL cannot exceed 500 characters"):
            Job(**valid_job_data)

    def test_source_cannot_exceed_50_characters(self, valid_job_data):
        valid_job_data["source"] = "a" * 51

        with pytest.raises(ValueError, match="Job source cannot exceed 50 characters"):
            Job(**valid_job_data)


@pytest.mark.unit
class TestJobEntityMethods:

    def test_is_from_linkedin_returns_true_for_linkedin_source(self, valid_job):
        assert valid_job.is_from_linkedin() is True

    def test_is_from_linkedin_returns_true_for_uppercase_linkedin(self, valid_job_data):
        valid_job_data["source"] = "LINKEDIN"
        job = Job(**valid_job_data)

        assert job.is_from_linkedin() is True

    def test_is_from_linkedin_returns_false_for_other_sources(self, job_from_different_source):
        assert job_from_different_source.is_from_linkedin() is False

    def test_matches_search_returns_true_when_term_in_title(self, valid_job):
        assert valid_job.matches_search("Python") is True
        assert valid_job.matches_search("python") is True
        assert valid_job.matches_search("PYTHON") is True

    def test_matches_search_returns_true_when_term_in_company(self, valid_job):
        assert valid_job.matches_search("TechCorp") is True
        assert valid_job.matches_search("techcorp") is True

    def test_matches_search_returns_true_when_term_in_description(self, valid_job):
        assert valid_job.matches_search("looking for") is True

    def test_matches_search_returns_false_when_term_not_found(self, valid_job):
        assert valid_job.matches_search("Java") is False

    def test_matches_search_returns_true_when_search_term_is_empty(self, valid_job):
        assert valid_job.matches_search("") is True

    def test_matches_search_handles_job_without_description(self, minimal_job):
        assert minimal_job.matches_search("Developer") is True
        assert minimal_job.matches_search("nonexistent") is False

    def test_matches_location_returns_true_when_location_matches(self, valid_job):
        assert valid_job.matches_location("Paris") is True
        assert valid_job.matches_location("paris") is True
        assert valid_job.matches_location("France") is True

    def test_matches_location_returns_false_when_location_does_not_match(self, valid_job):
        assert valid_job.matches_location("London") is False

    def test_matches_location_returns_true_when_location_is_empty(self, valid_job):
        assert valid_job.matches_location("") is True

    def test_matches_company_returns_true_when_company_matches(self, valid_job):
        assert valid_job.matches_company("TechCorp") is True
        assert valid_job.matches_company("techcorp") is True
        assert valid_job.matches_company("Tech") is True

    def test_matches_company_returns_false_when_company_does_not_match(self, valid_job):
        assert valid_job.matches_company("Google") is False

    def test_matches_company_returns_true_when_company_is_empty(self, valid_job):
        assert valid_job.matches_company("") is True
