from jobify.config import COMPANIES, KEYWORDS_MAP, URLS_MAP
from jobify.database import connect_to_database
from jobify.firebase import write_companies
from jobify.scraper import scrape_webpage
from jobify.utils import setup_chromedriver


def main():
    setup_chromedriver()
    conn = connect_to_database()

    if conn is not None:
        try:
            for company in COMPANIES:
                keywords = KEYWORDS_MAP[company]
                url = URLS_MAP[company]

                print(f"Scraping {company} job site ...")
                scrape_webpage(company, url, conn, keywords)
                print("Scrape job completed... 100%")

        except Exception as e:
            print(e)

        finally:
            write_companies()
            conn.close()
            print("Database connection closed")
    else:
        print("Failed to connect to the database. Exiting...")


if __name__ == "__main__":
    main()
