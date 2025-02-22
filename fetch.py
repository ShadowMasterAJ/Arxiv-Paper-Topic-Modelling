import arxiv
import random
import time
from datetime import date, timedelta
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_paper(client, result):
    """Fetch a single paper and return its data."""
    return {
        "title": result.title,
        "abstract": result.summary.replace("\n", " "),
        "category": result.primary_category,
        "published": result.published.strftime("%d-%m-%Y"),
    }

def fetch_papers_for_month_and_category(client, category, first_day, last_day, papers_per_month_per_category):
    try:
        search = arxiv.Search(
            query=f"cat:{category} AND submittedDate:[{first_day.strftime('%Y%m%d%H%M%S')} TO {last_day.strftime('%Y%m%d%H%M%S')}]",
            max_results=papers_per_month_per_category,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        # Fetch results in batches
        papers = []
        for result in client.results(search):
            papers.append({
                "Title": result.title,
                "Abstract": result.summary.replace("\n", " "),
                "Category": result.primary_category,
                "Published": result.published.strftime("%d-%m-%Y")
            })
        
        if len(papers) > papers_per_month_per_category:
            papers = random.sample(papers, papers_per_month_per_category)
        
        return papers
    except Exception as e:
        print(f"Error fetching papers for category {category}: {e}")
        return []

def fetch_arxiv_papers(categories, start_date, end_date, papers_per_month, batch_size=200):
    client = arxiv.Client(page_size=batch_size)
    total_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1
    csv_filename = 'arxiv_papers.csv'
    papers_per_month_per_category = papers_per_month // len(categories)
    
    # Precompute all month ranges
    month_ranges = []
    current_date = start_date
    for _ in range(total_months):
        year = current_date.year
        month_num = current_date.month
        first_day = date(year, month_num, 1)
        if month_num == 12:
            next_month_first_day = date(year + 1, 1, 1)
        else:
            next_month_first_day = date(year, month_num + 1, 1)
        last_day = next_month_first_day - timedelta(days=1)
        month_ranges.append((first_day, last_day))

        if current_date.month == 12:
            current_date = date(current_date.year + 1, 1, 1)
        else:
            current_date = date(current_date.year, current_date.month + 1, 1)

    # Prepare all tasks
    tasks = []
    for _, (first_day, last_day) in enumerate(month_ranges):
        for category in categories:
            tasks.append((client, category, first_day, last_day, papers_per_month_per_category))
            
    # Write header if the file is new
    file_exists = False
    try:
        _ = pd.read_csv(csv_filename, nrows=1)
        file_exists = True
    except FileNotFoundError:
        file_exists = False

    # Process tasks and write to CSV in chunks
    with ThreadPoolExecutor() as executor:
        header = not file_exists
        
        with tqdm(total=len(tasks), desc="Fetching Papers") as pbar:
            for future in as_completed([executor.submit(fetch_papers_for_month_and_category, *task) for task in tasks]):
                papers = future.result()
                if papers:
                    df = pd.DataFrame(papers)
                    df.to_csv(csv_filename, mode='a', header=header, index=False)
                    header = False  # Only write header once
                pbar.update()

    print("Fetching and saving complete.")

# Define parameters
categories = ['cs.AI', 'cs.CL', 'cs.CV', 'cs.LG']
start_date = date(2023, 1, 1)
end_date = date(2024, 12, 1)
papers_per_month = 200
batch_size = 200

# Time the function
start_time = time.time()

# Fetch the papers
fetch_arxiv_papers(categories, start_date, end_date, papers_per_month, batch_size)

end_time = time.time()
print(f"Execution Time: {end_time - start_time} seconds")
