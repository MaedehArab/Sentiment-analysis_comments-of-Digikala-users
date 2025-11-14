import requests
import pandas as pd
import time
from tqdm import tqdm
from random import uniform


# Function to fetch JSON data from a URL with retries
def get_json(url, retries=3, delay=2):
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return r.json()
            else:
                print(f"Status {r.status_code} for {url}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        time.sleep(delay)
    return None


# Function to fetch Samsung mobile products across multiple pages
def get_samsung_products(pages=45):
    products = []
    for page in range(1, pages + 1):
        url = f"https://api.digikala.com/v1/categories/mobile-phone/brands/samsung/search/?page={page}&_rch=db340a7f7c4f"
        data = get_json(url)
        if not data or "data" not in data or "products" not in data["data"]:
            print(f"No data on page {page}")
            continue

        # Extract products from the response
        for p in data["data"]["products"]:
            variant = p.get("default_variant", {})
            if isinstance(variant, list) and len(variant) > 0:
                variant = variant[0]
            elif not isinstance(variant, dict):
                variant = {}

            price_info = variant.get("price", {})
            rating_info = p.get("rating", {})
            brand_info = p.get("brand", {})
            category_info = p.get("category", {})
            review_info = p.get("review", {}).get("recommendation", {})
            colors = p.get("colors", [])
            first_color = colors[0]["title"] if colors else None

            # Append product details as a dictionary
            products.append({
                "id": p.get("id"),
                "title_fa": p.get("title_fa"),
                "title_en": p.get("title_en"),
                "brand": brand_info.get("title_fa"),
                "category": category_info.get("title_fa"),
                "status": p.get("status"),
                "selling_price": price_info.get("selling_price"),
                "rrp_price": price_info.get("rrp_price"),
                "rating": rating_info.get("rate"),
                "rating_count": rating_info.get("count"),
                "recommendation_percentage": review_info.get("recommended_percentage"),
                "color": first_color,
                "url": p.get("url", {}).get("uri"),
            })

    # Random delay after fetching all pages
    time.sleep(uniform(0.5, 1.2))

    # Convert list to DataFrame and save to CSV
    df_products = pd.DataFrame(products)
    df_products.to_csv("samsung_products.csv", index=False, encoding="utf-8-sig")
    print(f"Saved {len(df_products)} products → samsung_products.csv")
    return df_products


# Function to fetch comments for a single product
def get_comments_for_product(product_id, max_pages=45):
    comments = []
    for page in range(1, max_pages + 1):
        url = f"https://api.digikala.com/v1/product/{product_id}/comments/?page={page}"
        data = get_json(url)
        if not data or "data" not in data or "comments" not in data["data"]:
            break

        cmts = data["data"]["comments"]
        if not cmts:
            break

        for c in cmts:
            comments.append({
                "product_id": product_id,
                "comment_id": c.get("id"),
                "title": c.get("title"),
                "body": c.get("body"),
                "rate": c.get("rate"),
                "date": c.get("created_at"),
                "user_name": c.get("user_name")
            })

        total_pages = data.get("metadata", {}).get("paging", {}).get("total_pages", 1)
        if page >= total_pages:
            break

        # Random delay between pages    
        time.sleep(uniform(0.5, 1.2))
    return comments


# Function to fetch comments for all products
def get_all_comments(products_df):
    all_comments = []

    # Loop through product IDs with progress bar
    for pid in tqdm(products_df["id"], desc="Fetching comments", ncols=100):
        cmts = get_comments_for_product(pid, max_pages=45)
        all_comments.extend(cmts)
        time.sleep(uniform(1.0, 2.0))

    # Convert to DataFrame and save to CSV
    df_comments = pd.DataFrame(all_comments)
    df_comments.to_csv("samsung_comments.csv", index=False, encoding="utf-8-sig")
    print(f"Saved {len(df_comments)} comments → samsung_comments.csv")
    return df_comments


# Main execution block
if __name__ == "__main__":
    print("Fetching Samsung mobile products and comments from Digikala...")
    df_products = get_samsung_products(pages=45)  
    df_comments = get_all_comments(df_products)
    print("Done! Data saved successfully.")
