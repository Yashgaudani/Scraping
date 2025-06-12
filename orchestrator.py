import os
import json
import importlib.util
import sys
from typing import Dict, List, Optional

class ScraperOrchestrator:
    def __init__(self):
        self.scrapers = {
            '7-zip': {
                'path': '7-zip/main.py',
                'module': 'scraper_7zip',
                'function': 'scrape_7zip'
            },
            'anydesk': {
                'path': 'anydesk/main.py',
                'module': 'scraper_anydesk',
                'function': 'scrape_anydesk'
            },
            'docker': {
                'path': 'docker/main.py',
                'module': 'docker_scraper', 
                'function': 'scrape_docker'
            },
            'fontbase': {
                'path': 'fontbase/main.py',
                'module': 'scraper_fontbase',
                'function': 'scrape_fontbase'
            },
            'fortinet': {
                'path': 'fortinet/main.py',
                'module': 'scraper_fortinet',
                'function': 'scrape_fortinet'
            },
            'Foxit_PDF': {
                'path': 'Foxit_PDF/main.py',
                'module': 'scraper_foxit_pdf',
                'function': 'scrape_foxit_pdf'
            },
            'google': {
                'path': 'google/main.py',
                'module': 'scraper_google',
                'function': 'scrape_google'
            },
            'postman': {
                'path': 'postman/main.py',
                'module': 'scraper_postman',
                'function': 'scrape_postman'
            },
            'slack': {
                'path': 'slack/main.py',
                'module': 'scraper_slack',
                'function': 'scrape_slack'
            },
            'teamviwer': {
                'path': 'teamviwer/main.py',
                'module': 'scraper_teamviwer',
                'function': 'scrape_teamviwer'
            },
            'utraviwer': {
                'path': 'utraviews/main.py',
                'module': 'utraviews_scraper', 
                'function': 'utraviews_docker'
            },
            'vlc': {
                'path': 'vlc/main.py',
                'module': 'scraper_vlc',
                'function': 'scrape_vlc'
            },
            'vlc_main': {
                'path': 'vlc_main/main.py',
                'module': 'scraper_vlc_main',
                'function': 'scrape_vlc_main'
            },
            'winscp': {
                'path': 'winscp/main.py',
                'module': 'scraper_winscp',
                'function': 'scrape_winscp'
            },
            'Zoom': {
                'path': 'Zoom/main.py',
                'module': 'scraper_zoom',
                'function': 'scrape_zoom'
            }
        }
        self.results = {}

    def load_scraper(self, scraper_name: str) -> Optional[Dict]:
        """Load a scraper module dynamically."""
        if scraper_name not in self.scrapers:
            print(f"❌ Scraper '{scraper_name}' not found.")
            return None

        scraper_info = self.scrapers[scraper_name]
        scraper_path = os.path.join(os.path.dirname(__file__), scraper_info['path'])

        if not os.path.exists(scraper_path):
            print(f"❌ Scraper file not found: {scraper_path}")
            return None

        try:
            spec = importlib.util.spec_from_file_location(scraper_info['module'], scraper_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[scraper_info['module']] = module
            spec.loader.exec_module(module)
            return {
                'module': module,
                'function': getattr(module, scraper_info['function'])
            }
        except Exception as e:
            print(f"❌ Error loading scraper '{scraper_name}': {str(e)}")
            return None

    def run_scraper(self, scraper_name: str) -> bool:
        """Run a specific scraper."""
        print(f"\n=== Running {scraper_name} scraper ===")
        
        scraper = self.load_scraper(scraper_name)
        if not scraper:
            return False

        try:
            scraper['function']()
            print(f"✅ {scraper_name} scraper completed successfully")
            return True
        except Exception as e:
            print(f"❌ Error running {scraper_name} scraper: {str(e)}")
            return False

    def list_available_scrapers(self) -> List[str]:
        """List all available scrapers."""
        return list(self.scrapers.keys())

    def run_all_scrapers(self) -> Dict[str, bool]:
        """Run all available scrapers."""
        results = {}
        for scraper_name in self.scrapers:
            results[scraper_name] = self.run_scraper(scraper_name)
        return results

    def combine_results(self) -> Dict:
        """Combine results from all scrapers into a single JSON file."""
        combined_data = {
            "products": []
        }

        for scraper_name in self.scrapers:
            info_file = f"{scraper_name}_info.json"
            info_path = os.path.join(os.path.dirname(__file__), info_file)
            
            if os.path.exists(info_path):
                try:
                    with open(info_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        combined_data["products"].append(data)
                except Exception as e:
                    print(f"❌ Error reading {info_file}: {str(e)}")

        # Save combined results
        try:
            output_path = os.path.join(os.path.dirname(__file__), "combined_results.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(combined_data, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Combined results saved to combined_results.json")
        except Exception as e:
            print(f"❌ Error saving combined results: {str(e)}")

        return combined_data

def main():
    orchestrator = ScraperOrchestrator()
    
    while True:
        print("\n=== Product Scraper Orchestrator ===")
        print("1. List available scrapers")
        print("2. Run specific scraper")
        print("3. Run all scrapers")
        print("4. Combine results")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            scrapers = orchestrator.list_available_scrapers()
            print("\nAvailable scrapers:")
            for i, scraper in enumerate(scrapers, 1):
                print(f"{i}. {scraper}")
                
        elif choice == '2':
            scrapers = orchestrator.list_available_scrapers()
            print("\nAvailable scrapers:")
            for i, scraper in enumerate(scrapers, 1):
                print(f"{i}. {scraper}")
            
            try:
                idx = int(input("\nEnter scraper number: ").strip()) - 1
                if 0 <= idx < len(scrapers):
                    orchestrator.run_scraper(scrapers[idx])
                else:
                    print("❌ Invalid scraper number")
            except ValueError:
                print("❌ Please enter a valid number")
                
        elif choice == '3':
            print("\nRunning all scrapers...")
            results = orchestrator.run_all_scrapers()
            print("\nResults:")
            for scraper, success in results.items():
                status = "✅ Success" if success else "❌ Failed"
                print(f"{scraper}: {status}")
                
        elif choice == '4':
            print("\nCombining results from all scrapers...")
            orchestrator.combine_results()
            
        elif choice == '5':
            print("\nGoodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 