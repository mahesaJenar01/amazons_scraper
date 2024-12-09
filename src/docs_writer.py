from typing import Dict
from googleapiclient.discovery import build

def write_results_to_docs(creds, config, results: Dict[str, dict]):
    """Write scraping results to corresponding Google Docs."""
    service = build('docs', 'v1', credentials=creds)
    
    for url, result in results.items():
        doc_id = config.get_doc_id_for_url(url)
        if not doc_id:
            print(f"No document ID found for URL: {url}")
            continue
            
        try:
            content = format_results(url, result)
            # Get the current document
            doc = service.documents().get(documentId=doc_id).execute()
            
            # Check if document has content to delete
            doc_content = doc.get('body').get('content')
            end_index = doc_content[-1].get('endIndex') - 1 if doc_content else 1
            
            requests = []
            if end_index > 1:
                requests.append({
                    'deleteContentRange': {
                        'range': {
                            'startIndex': 1,
                            'endIndex': end_index
                        }
                    }
                })
                
            requests.append({
                'insertText': {
                    'location': {
                        'index': 1
                    },
                    'text': content
                }
            })
            
            service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print(f"Results written to document {doc_id}")
            
        except Exception as e:
            print(f"Error writing to document {doc_id}: {str(e)}")

def format_results(url: str, result: dict) -> str:
    """Format scraping results as text for Google Docs."""
    content = [f"Results for {url}:\n"]
    content.append("="*50 + "\n")
    
    # Add timing statistics
    timing = result.get('timing', {})
    content.append("\nTiming Statistics:\n")
    content.append(f"Total Time: {timing.get('total_time', 0):.2f} seconds\n")
    content.append(f"Total Items: {timing.get('total_items', 0)}\n")
    
    avg_times = timing.get('average_times', {})
    content.append("\nAverage Times per Item:\n")
    content.append(f"Brand Extraction: {avg_times.get('brand', 0):.3f} seconds\n")
    content.append(f"Product Extraction: {avg_times.get('product', 0):.3f} seconds\n")
    content.append(f"Rating Extraction: {avg_times.get('rating', 0):.3f} seconds\n")
    content.append(f"Review Extraction: {avg_times.get('review', 0):.3f} seconds\n")
    content.append(f"Sales Info Extraction: {avg_times.get('sales_info', 0):.3f} seconds\n")
    content.append(f"Price Extraction: {avg_times.get('price', 0):.3f} seconds\n")
    
    # Add scraped items
    content.append("\nScraped Items:\n")
    for i, (brand, product, rating, review, sales_info, price, sustainability) in enumerate(result['data'], 1):
        content.append(f"\nItem {i}:\n")
        content.append(f"Brand: {brand}\n")
        content.append(f"Product: {product}\n")
        content.append(f"Rating: {rating}\n")
        content.append(f"Review: {review}\n")
        content.append(f"Sales Info: {sales_info}\n")
        content.append(f"Price: {price}\n")
        content.append(f"Sustainability: {sustainability if '-' == sustainability else "\n"+ sustainability}\n")
    
    content.append("\n" + "="*50 + "\n")
    return "".join(content)