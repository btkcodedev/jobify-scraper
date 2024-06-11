import importlib
import os
import sys

from .database import insert_jobs_to_db, update_qualified_jobs


def import_sources():
    source_dir = os.path.join(os.path.dirname(__file__), "sources")
    source_files = [f[:-3] for f in os.listdir(source_dir) if f.endswith(".py") and f != "__init__.py"]
    for module_name in source_files:
        importlib.import_module(f"jobify.sources.{module_name}")


def scrape_all_jobs(company: str, url) -> dict:
    import_sources()
    browser_class = None
    browser_class_name = company.capitalize()
    for module_name in sys.modules:
        if module_name.startswith("jobify.sources."):
            module = sys.modules[module_name]
            if hasattr(module, browser_class_name):
                browser_class = getattr(module, browser_class_name)
                break

    if not browser_class:
        raise ImportError(f"No browser class found for company: {company}")
    browser = browser_class(url)
    browser.load_all_jobs()
    job_info = browser.scrape_all_jobs()
    browser.close_browser()
    return job_info


def scrape_webpage(company, url, conn, keywords):
    job_dict = scrape_all_jobs(company, url)
    insert_jobs_to_db(job_dict=job_dict, conn=conn, company=company)
    update_qualified_jobs(conn=conn, keywords=keywords, company=company)
    return
