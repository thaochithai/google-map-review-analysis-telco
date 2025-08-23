import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ReviewsScraper:
    def __init__(self, headless=False):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
    
    def scrape_url(self, url, expected_reviews=None):
        """Scrape reviews from a single URL"""
        # Calculate max_scrolls based on expected reviews (reviews load ~10 per scroll)
        max_scrolls = (expected_reviews // 10 + 1) if expected_reviews else 15
        
        print(f"Processing: {url}")
        if expected_reviews:
            print(f"Expected reviews: {expected_reviews}, Max scrolls: {max_scrolls}")
        
        self.driver.get(url)
        time.sleep(4)
        
        if not self._click_reviews_tab():
            print("Could not access reviews")
            return []
        
        self._scroll_reviews(max_scrolls)
        return self._extract_reviews(url)
    
    def _click_reviews_tab(self):
        """Click Reviews tab"""
        selectors = [
            "[data-value='Reviews']",
            "button[data-value='Reviews']", 
            "//button[contains(@aria-label, 'Reviews')]",
            "//button[contains(text(), 'Reviews')]"
        ]
        
        for selector in selectors:
            try:
                if selector.startswith("//"):
                    element = self.driver.find_element(By.XPATH, selector)
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                
                if element.is_displayed():
                    self.driver.execute_script("arguments[0].click();", element)
                    time.sleep(3)
                    return True
            except NoSuchElementException:
                continue
        return False
    
    def _scroll_reviews(self, max_scrolls):
        """Auto-scroll to load reviews"""
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".jftiEf.fontBodyMedium")))
            container = self.driver.find_element(By.CSS_SELECTOR, ".m6QErb.DxyBCb.kA9KIf.dS8AEf")
        except (TimeoutException, NoSuchElementException):
            print("Could not find reviews container")
            return
        
        last_height = self.driver.execute_script("return arguments[0].scrollHeight", container)
        no_change_count = 0
        
        for scroll in range(max_scrolls):
            current_reviews = len(self.driver.find_elements(By.CSS_SELECTOR, ".jftiEf.fontBodyMedium"))
            
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", container)
            time.sleep(2.5)
            
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", container)
            new_reviews = len(self.driver.find_elements(By.CSS_SELECTOR, ".jftiEf.fontBodyMedium"))
            
            if new_height == last_height and new_reviews == current_reviews:
                no_change_count += 1
                if no_change_count >= 2:
                    print(f"Reached end - {new_reviews} reviews loaded")
                    break
            else:
                no_change_count = 0
            
            last_height = new_height
            print(f"Scroll {scroll + 1}: {new_reviews} reviews")
    
    def _extract_reviews(self, url):
        """Extract review data"""
        reviews = []
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".jftiEf.fontBodyMedium")
        
        for i, element in enumerate(elements):
            try:
                # Expand "More reviews" button
                try:
                    more_btn = element.find_element(By.CSS_SELECTOR, ".w8nwRe.kyuRq")
                    if more_btn.is_displayed():
                        self.driver.execute_script("arguments[0].click();", more_btn)
                        time.sleep(0.3)
                except NoSuchElementException:
                    pass
                
                # Extract data
                review = {
                    'reviewer_name': self._safe_extract(element, ".d4r55"),
                    'rating': self._extract_rating(element),
                    'review_text': self._safe_extract(element, ".wiI7pd"),
                    'date': self._safe_extract(element, ".rsqaWe"),
                    'reviewer_type': self._safe_extract(element, ".RfnDt"), 
                    'source_url': url,
                    'row_number': i + 1
                }
                reviews.append(review)
                
            except Exception as e:
                print(f"Error processing review {i+1}: {e}")
                continue
        
        return reviews
    
    def _safe_extract(self, element, selector, attr="text"):
        """Safely extract data from element"""
        try:
            found = element.find_element(By.CSS_SELECTOR, selector)
            return found.get_attribute("href") if attr == "href" else found.text
        except NoSuchElementException:
            return ""
    
    def _extract_rating(self, element):
        """Extract rating from aria-label"""
        try:
            rating_element = element.find_element(By.CSS_SELECTOR, "[role='img'][aria-label*='star']")
            rating_text = rating_element.get_attribute("aria-label")
            match = re.search(r'(\d+)', rating_text)
            return match.group(1) if match else ""
        except NoSuchElementException:
            return ""
    
    def process_batch(self, urls_data, output_dir, batch_size=10, delay=30):
        """Process URLs in batches with expected review counts"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        all_reviews = []
        total_batches = (len(urls_data) + batch_size - 1) // batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(urls_data))
            batch_data = urls_data[start_idx:end_idx]
            
            print(f"\n=== BATCH {batch_num + 1}/{total_batches} ===")
            batch_reviews = []
            
            for i, (url, expected_reviews) in enumerate(batch_data):
                url_number = start_idx + i + 1
                print(f"URL {url_number}/{len(urls_data)}")
                
                reviews = self.scrape_url(url, expected_reviews)
                for review in reviews:
                    review['batch_number'] = batch_num + 1
                    review['global_url_number'] = url_number
                    review['expected_reviews'] = expected_reviews or 0
                
                batch_reviews.extend(reviews)
                all_reviews.extend(reviews)
                
                if i < len(batch_data) - 1:
                    time.sleep(3)
            
            # Save batch
            if batch_reviews:
                batch_file = os.path.join(output_dir, f"reviews_batch_{batch_num + 1:02d}.csv")
                pd.DataFrame(batch_reviews).to_csv(batch_file, index=False, encoding='utf-8')
                print(f"Saved: {len(batch_reviews)} reviews to batch file")
            
            if batch_num < total_batches - 1:
                print(f"Waiting {delay} seconds...")
                time.sleep(delay)
        
        # Save combined results
        if all_reviews:
            combined_file = os.path.join(output_dir, "reviews_combined.csv")
            pd.DataFrame(all_reviews).to_csv(combined_file, index=False, encoding='utf-8')
            
            print(f"\n=== SUMMARY ===")
            print(f"Total reviews: {len(all_reviews)}")
            print(f"URLs processed: {len(urls_data)}")
            print(f"Combined file saved: {combined_file}")
        
        return all_reviews
    
    def close(self):
        """Close browser"""
        self.driver.quit()

def run_scraper(csv_file, url_column='url', review_count_column='review', output_dir='./output'):
    """Main function to run the scraper"""
    print("Starting Google Reviews scraper...")
    
    # Read URLs and review counts
    df = pd.read_csv(csv_file)
    
    # Create list of tuples (url, expected_reviews)
    urls_data = []
    for _, row in df.iterrows():
        url = row.get(url_column)
        review_count = row.get(review_count_column, 0)
        
        if pd.notna(url): 
            try:
                review_count = int(review_count) if pd.notna(review_count) else 0
            except (ValueError, TypeError):
                review_count = 0
            urls_data.append((url, review_count))
    
    print(f"Found {len(urls_data)} URLs with review counts")
    
    scraper = ReviewsScraper(headless=False)
    try:
        scraper.process_batch(urls_data, output_dir)
    finally:
        scraper.close()
        print("Scraping completed!")

# Usage
if __name__ == "__main__":
    csv_file = r"D:\Data Analysis\Reviews\Shop URL list\scraping_list.csv"
    output_dir = r"D:\Data Analysis\Reviews\Reviews"
    
    run_scraper(csv_file, url_column='url', review_count_column='review', output_dir=output_dir)
