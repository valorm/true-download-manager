from typing import Dict, Optional
from yt_dlp import YoutubeDL
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dataclasses import dataclass

@dataclass
class MediaInfo:
    url: str
    title: str
    description: Optional[str]
    duration: Optional[int]
    thumbnail: Optional[str]
    formats: list
    extractor: str

class MediaExtractor:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        # Initialize Chrome options for Selenium
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
    
    def extract_info(self, url: str) -> MediaInfo:
        """Extract media information using yt-dlp"""
        with YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return MediaInfo(
                    url=url,
                    title=info.get('title', ''),
                    description=info.get('description'),
                    duration=info.get('duration'),
                    thumbnail=info.get('thumbnail'),
                    formats=info.get('formats', []),
                    extractor=info.get('extractor', 'generic')
                )
            except Exception as e:
                raise Exception(f"Failed to extract media info: {str(e)}")
    
    def get_best_format(self, media_info: MediaInfo, preferred_format: Optional[str] = None) -> Dict:
        """Get the best format based on quality and user preference"""
        formats = media_info.formats
        
        if not formats:
            raise Exception("No available formats found")
        
        if preferred_format:
            # Filter formats by preferred format
            matching_formats = [f for f in formats if f.get('ext') == preferred_format]
            if matching_formats:
                # Return the highest quality format matching the preference
                return max(matching_formats, key=lambda x: x.get('filesize', 0))
        
        # If no preferred format or no matching formats, return the best quality
        return max(formats, key=lambda x: x.get('filesize', 0))
    
    def extract_with_selenium(self, url: str) -> Dict:
        """Extract media information using Selenium for sites that require JavaScript"""
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=self.chrome_options)
        
        try:
            driver.get(url)
            # Add custom extraction logic here for specific sites
            # This is a placeholder for site-specific extraction
            media_data = {
                'url': url,
                'title': driver.title,
                'description': None,
                'duration': None,
                'thumbnail': None,
                'formats': [{'url': url, 'ext': 'html'}],
                'extractor': 'selenium'
            }
            return media_data
        finally:
            driver.quit()

# Create a global instance of the media extractor
media_extractor = MediaExtractor()