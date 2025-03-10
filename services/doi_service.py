"""
DOI Service for interacting with CrossRef and DataCite APIs.

This module provides functionality to check the health of DOI records
for a given organization.
"""

import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# Set up logging
logger = logging.getLogger(__name__)

class DOIService:
    """Service for DOI-related operations."""
    
    # API endpoints
    CROSSREF_API_URL = "https://api.crossref.org/works"
    DATACITE_API_URL = "https://api.datacite.org/dois"
    
    @staticmethod
    def get_health_report(organization_id: str, service: str) -> Dict[str, Any]:
        """
        Get a health report for DOIs belonging to the specified organization.
        
        Args:
            organization_id: The identifier for the organization
            service: The DOI service to check ('crossref' or 'datacite')
            
        Returns:
            A dictionary containing the health report
        """
        if service.lower() == 'crossref':
            return DOIService._get_crossref_report(organization_id)
        elif service.lower() == 'datacite':
            return DOIService._get_datacite_report(organization_id)
        else:
            raise ValueError(f"Unsupported DOI service: {service}")
    
    @staticmethod
    def _get_crossref_report(organization_id: str) -> Dict[str, Any]:
        """
        Get a health report from CrossRef API.
        
        Args:
            organization_id: The prefix or member ID to query
            
        Returns:
            A dictionary containing the health report
        """
        report = {
            'service': 'CrossRef',
            'organization_id': organization_id,
            'timestamp': datetime.utcnow().isoformat(),
            'summary': {},
            'issues': [],
            'dois': [],
            'error': None
        }
        
        try:
            # Check if it's a DOI prefix (starts with 10.)
            if organization_id.startswith('10.'):
                # Query by prefix
                query_url = f"{DOIService.CROSSREF_API_URL}?filter=prefix:{organization_id}&rows=100"
            else:
                # Query by member ID
                query_url = f"{DOIService.CROSSREF_API_URL}?filter=member:{organization_id}&rows=100"
            
            response = requests.get(query_url, headers={'User-Agent': 'EasyJournal/1.0 (support@easyjournal.org)'})
            response.raise_for_status()
            
            data = response.json()
            items = data.get('message', {}).get('items', [])
            total_results = data.get('message', {}).get('total-results', 0)
            
            # Calculate basic statistics
            report['summary'] = {
                'total_dois': total_results,
                'sample_size': len(items),
                'has_issues': False
            }
            
            issues_count = 0
            for item in items:
                doi = item.get('DOI')
                title = item.get('title', ['Untitled'])[0] if item.get('title') else 'Untitled'
                item_issues = []
                
                # Check for common issues
                if not item.get('title'):
                    item_issues.append('Missing title')
                
                if not item.get('author'):
                    item_issues.append('Missing authors')
                
                if not item.get('published-online') and not item.get('published-print'):
                    item_issues.append('Missing publication date')
                
                doi_status = {
                    'doi': doi,
                    'title': title,
                    'issues': item_issues,
                    'status': 'ok' if not item_issues else 'issues'
                }
                
                report['dois'].append(doi_status)
                
                if item_issues:
                    issues_count += 1
                    report['issues'].append({
                        'doi': doi,
                        'title': title,
                        'problems': item_issues
                    })
            
            # Update summary with issues information
            report['summary']['issues_count'] = issues_count
            report['summary']['health_percentage'] = round(100 - (issues_count / len(items) * 100), 2) if items else 0
            report['summary']['has_issues'] = issues_count > 0
            
            return report
            
        except requests.RequestException as e:
            logger.error(f"Error fetching CrossRef data: {str(e)}")
            report['error'] = f"Error connecting to CrossRef API: {str(e)}"
            return report
        except Exception as e:
            logger.error(f"Error processing CrossRef data: {str(e)}")
            report['error'] = f"Error processing CrossRef data: {str(e)}"
            return report
    
    @staticmethod
    def _get_datacite_report(organization_id: str) -> Dict[str, Any]:
        """
        Get a health report from DataCite API.
        
        Args:
            organization_id: The client ID or prefix to query
            
        Returns:
            A dictionary containing the health report
        """
        report = {
            'service': 'DataCite',
            'organization_id': organization_id,
            'timestamp': datetime.utcnow().isoformat(),
            'summary': {},
            'issues': [],
            'dois': [],
            'error': None
        }
        
        try:
            # Check if it's a DOI prefix (starts with 10.)
            if organization_id.startswith('10.'):
                # Query by prefix
                query_url = f"{DOIService.DATACITE_API_URL}?query=prefix:{organization_id}&page[size]=100"
            else:
                # Query by client ID
                query_url = f"{DOIService.DATACITE_API_URL}?query=client.id:{organization_id}&page[size]=100"
            
            response = requests.get(query_url, headers={'User-Agent': 'EasyJournal/1.0 (support@easyjournal.org)'})
            response.raise_for_status()
            
            data = response.json()
            items = data.get('data', [])
            total_results = data.get('meta', {}).get('total', 0)
            
            # Calculate basic statistics
            report['summary'] = {
                'total_dois': total_results,
                'sample_size': len(items),
                'has_issues': False
            }
            
            issues_count = 0
            for item in items:
                attributes = item.get('attributes', {})
                doi = attributes.get('doi')
                title = attributes.get('titles', [{}])[0].get('title', 'Untitled') if attributes.get('titles') else 'Untitled'
                item_issues = []
                
                # Check for common issues
                if not attributes.get('titles'):
                    item_issues.append('Missing title')
                
                if not attributes.get('creators'):
                    item_issues.append('Missing creators')
                
                if not attributes.get('publicationYear'):
                    item_issues.append('Missing publication year')
                
                if attributes.get('state') != 'findable':
                    item_issues.append(f"DOI state is not findable (current: {attributes.get('state')})")
                
                doi_status = {
                    'doi': doi,
                    'title': title,
                    'issues': item_issues,
                    'status': 'ok' if not item_issues else 'issues'
                }
                
                report['dois'].append(doi_status)
                
                if item_issues:
                    issues_count += 1
                    report['issues'].append({
                        'doi': doi,
                        'title': title,
                        'problems': item_issues
                    })
            
            # Update summary with issues information
            report['summary']['issues_count'] = issues_count
            report['summary']['health_percentage'] = round(100 - (issues_count / len(items) * 100), 2) if items else 0
            report['summary']['has_issues'] = issues_count > 0
            
            return report
            
        except requests.RequestException as e:
            logger.error(f"Error fetching DataCite data: {str(e)}")
            report['error'] = f"Error connecting to DataCite API: {str(e)}"
            return report
        except Exception as e:
            logger.error(f"Error processing DataCite data: {str(e)}")
            report['error'] = f"Error processing DataCite data: {str(e)}"
            return report