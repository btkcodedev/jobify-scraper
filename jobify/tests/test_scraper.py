import unittest
from unittest.mock import MagicMock, patch


class TestScrapeAllJobs(unittest.TestCase):
    @patch("jobify.sources.importlib.import_module")
    @patch("jobify.sources.insert_jobs_to_db")
    @patch("jobify.sources.update_qualified_jobs")
    def test_scrape_all_jobs(self, mock_update_qualified_jobs, mock_insert_jobs_to_db, mock_import_module):

        mock_browser = MagicMock()
        mock_browser.load_all_jobs = MagicMock()
        mock_browser.scrape_all_jobs = MagicMock(
            return_value={
                "job1": {
                    "Role": "Engineer",
                    "Location": "Remote",
                    "Category": "Tech",
                    "Permanency": "Full-time",
                    "URL": "http://example.com/job1",
                }
            }
        )
        mock_browser.close_browser = MagicMock()

        mock_import_module.return_value = MagicMock(SporifyBrowser=mock_browser)

        company = "sporify"
        url = "http://example.com/jobs"

        # Test the scrape_all_jobs function
        from jobify.sources import scrape_all_jobs

        job_info = scrape_all_jobs(company, url)

        # Assertions
        self.assertEqual(
            job_info,
            {
                "job1": {
                    "Role": "Engineer",
                    "Location": "Remote",
                    "Category": "Tech",
                    "Permanency": "Full-time",
                    "URL": "http://example.com/job1",
                }
            },
        )
        mock_browser.load_all_jobs.assert_called_once()
        mock_browser.scrape_all_jobs.assert_called_once()
        mock_browser.close_browser.assert_called_once()

    @patch("jobify.sources.scrape_all_jobs")
    @patch("jobify.sources.insert_jobs_to_db")
    @patch("jobify.sources.update_qualified_jobs")
    def test_scrape_webpage(self, mock_update_qualified_jobs, mock_insert_jobs_to_db, mock_scrape_all_jobs):
        # Mock the job dictionary returned by scrape_all_jobs
        mock_scrape_all_jobs.return_value = {
            "job1": {
                "Role": "Engineer",
                "Location": "Remote",
                "Category": "Tech",
                "Permanency": "Full-time",
                "URL": "http://example.com/job1",
            }
        }

        # Define the parameters for the test
        company = "spotify"
        url = "http://example.com/jobs"
        conn = MagicMock()  # Mock the database connection
        keywords = ["engineer", "remote"]

        # Test the scrape_webpage function
        from jobify.sources import scrape_webpage

        scrape_webpage(company, url, conn, keywords)

        # Assertions
        mock_scrape_all_jobs.assert_called_once_with(company, url)
        mock_insert_jobs_to_db.assert_called_once_with(
            job_dict={
                "job1": {
                    "Role": "Engineer",
                    "Location": "Remote",
                    "Category": "Tech",
                    "Permanency": "Full-time",
                    "URL": "http://example.com/job1",
                }
            },
            conn=conn,
        )
        mock_update_qualified_jobs.assert_called_once_with(conn=conn, keywords=keywords, company=company)
