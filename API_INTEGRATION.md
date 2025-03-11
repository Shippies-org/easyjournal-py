# EasyJournal - API Integration Guide

This document provides information about integrating EasyJournal with external services and APIs.

## External Service Integrations

EasyJournal can integrate with several external services to enhance functionality. This guide explains how to configure and use these integrations.

## DOI Integration

### CrossRef Integration

EasyJournal can integrate with CrossRef to register Digital Object Identifiers (DOIs) for published articles.

#### Configuration

1. **Prerequisites**:
   - A CrossRef membership and account credentials
   - Access to the CrossRef API

2. **Environment Configuration**:
   Add these variables to your `.env` file:
   ```
   CROSSREF_USERNAME=your_username
   CROSSREF_PASSWORD=your_password
   CROSSREF_PREFIX=your_doi_prefix
   ```

3. **Admin Setup**:
   - Navigate to Admin → DOI Settings
   - Configure your CrossRef deposit settings
   - Set the DOI pattern template (e.g., `{prefix}/easyjournal.{year}.{issue}.{article}`)

#### Usage

Once configured, the DOI service will:
- Automatically generate DOIs for newly published articles
- Submit metadata to CrossRef when articles are published
- Display DOIs on article pages with proper citation information
- Handle DOI resolution through CrossRef

### DataCite Integration

EasyJournal also supports DataCite for DOI registration and management.

#### Configuration

1. **Prerequisites**:
   - A DataCite account and API credentials
   - Access to the DataCite API

2. **Environment Configuration**:
   Add these variables to your `.env` file:
   ```
   DATACITE_REPOSITORY_ID=your_repository_id
   DATACITE_PASSWORD=your_password
   DATACITE_PREFIX=your_doi_prefix
   DATACITE_URL=https://api.datacite.org  # or test environment URL
   ```

3. **Admin Setup**:
   - Navigate to Admin → DOI Settings
   - Select DataCite as the DOI provider
   - Configure repository information and metadata

## ORCID Integration

EasyJournal supports ORCID integration to verify author identities and streamline the submission process.

### Configuration

1. **Prerequisites**:
   - Register as an ORCID member or public API client
   - Obtain ORCID API credentials

2. **Environment Configuration**:
   Add these variables to your `.env` file:
   ```
   ORCID_CLIENT_ID=your_client_id
   ORCID_CLIENT_SECRET=your_client_secret
   ORCID_REDIRECT_URI=https://your-journal.com/orcid/callback
   ```

3. **Admin Setup**:
   - Navigate to Admin → Integration Settings
   - Enable ORCID integration
   - Configure display options for ORCID iDs

### Usage

The ORCID integration allows:
- Authors to connect their ORCID iD during registration or profile update
- Display of verified ORCID iDs on author profiles and published articles
- Simplified submission process with ORCID profile information

## Email Integration

EasyJournal can use external email services to send notifications.

### SMTP Configuration

1. **Environment Configuration**:
   Add these variables to your `.env` file:
   ```
   MAIL_SERVER=smtp.your-provider.com
   MAIL_PORT=587
   MAIL_USERNAME=your_username
   MAIL_PASSWORD=your_password
   MAIL_USE_TLS=True
   MAIL_DEFAULT_SENDER=journal@your-domain.com
   ```

2. **Admin Setup**:
   - Navigate to Admin → Email Settings
   - Configure email templates
   - Set notification preferences

### Transactional Email Services

EasyJournal also supports SendGrid and Mailgun for transactional emails.

#### SendGrid Configuration

1. **Environment Configuration**:
   ```
   MAIL_SERVICE=sendgrid
   SENDGRID_API_KEY=your_api_key
   ```

#### Mailgun Configuration

1. **Environment Configuration**:
   ```
   MAIL_SERVICE=mailgun
   MAILGUN_API_KEY=your_api_key
   MAILGUN_DOMAIN=mg.your-domain.com
   ```

## Plagiarism Detection Integration

EasyJournal can integrate with plagiarism detection services.

### iThenticate Integration

1. **Prerequisites**:
   - An iThenticate account and API credentials

2. **Environment Configuration**:
   ```
   ITHENTICATE_USERNAME=your_username
   ITHENTICATE_PASSWORD=your_password
   ```

3. **Admin Setup**:
   - Navigate to Admin → Integration Settings
   - Enable plagiarism detection
   - Configure submission options and thresholds

### Usage

Once configured, the plagiarism detection service will:
- Allow editors to submit manuscripts for plagiarism checking
- Display similarity reports within the editor interface
- Flag submissions with high similarity scores

## Citation Management Integration

EasyJournal provides integration with citation management services.

### Configuration

1. **Admin Setup**:
   - Navigate to Admin → Integration Settings
   - Enable citation exports
   - Configure export formats (BibTeX, RIS, EndNote, etc.)

2. **Usage**:
   Published articles will include export options for various citation formats.

## Archiving Service Integration

### CLOCKSS/LOCKSS Integration

1. **Prerequisites**:
   - Partnership with CLOCKSS/LOCKSS

2. **Admin Setup**:
   - Navigate to Admin → Preservation Settings
   - Configure CLOCKSS/LOCKSS harvesting endpoints
   - Set up content exposure policies

### Portico Integration

1. **Prerequisites**:
   - Portico membership and credentials

2. **Environment Configuration**:
   ```
   PORTICO_USERNAME=your_username
   PORTICO_PASSWORD=your_password
   PORTICO_FTP_HOST=ftp.portico.org
   ```

3. **Admin Setup**:
   - Configure Portico deposit settings
   - Set up automated deposit schedule

## Metrics and Analytics Integration

### Google Analytics Integration

1. **Environment Configuration**:
   ```
   GA_TRACKING_ID=UA-XXXXXXXXX-X
   ```

2. **Admin Setup**:
   - Navigate to Admin → Analytics Settings
   - Enable Google Analytics
   - Configure tracking options

### Plum Analytics Integration

1. **Environment Configuration**:
   ```
   PLUM_ANALYTICS_KEY=your_api_key
   ```

2. **Admin Setup**:
   - Navigate to Admin → Metrics Settings
   - Enable Plum Analytics integration

## Custom API Integrations

EasyJournal provides extension points for custom API integrations through the plugin system.

### Creating a Custom Integration Plugin

1. Create a plugin directory in `plugins/`:
   ```
   plugins/my_integration/
   ├── __init__.py
   ├── plugin.py
   └── api_client.py
   ```

2. Implement the API client:
   ```python
   # api_client.py
   import requests
   
   class MyServiceClient:
       def __init__(self, api_key):
           self.api_key = api_key
           self.base_url = 'https://api.myservice.com/v1'
           
       def get_data(self, resource_id):
           headers = {'Authorization': f'Bearer {self.api_key}'}
           response = requests.get(f'{self.base_url}/resources/{resource_id}', headers=headers)
           response.raise_for_status()
           return response.json()
           
       def send_data(self, data):
           headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
           response = requests.post(f'{self.base_url}/resources', json=data, headers=headers)
           response.raise_for_status()
           return response.json()
   ```

3. Register the plugin with hooks:
   ```python
   # plugin.py
   from plugin_system import PluginSystem
   from .api_client import MyServiceClient
   import os
   
   def register_plugin():
       # Register hooks
       PluginSystem.register_hook('after_submission_create', on_submission_created)
       
       # Create client instance
       api_key = os.environ.get('MY_SERVICE_API_KEY')
       if api_key:
           # Store in Flask g object for access in hooks
           from flask import g
           g.my_service_client = MyServiceClient(api_key)
       
       # No blueprint needed for this example
       return None
       
   def on_submission_created(args):
       from flask import g, current_app
       submission = args.get('submission')
       
       if hasattr(g, 'my_service_client'):
           try:
               # Send submission data to external service
               data = {
                   'title': submission.title,
                   'authors': submission.authors,
                   'abstract': submission.abstract
               }
               result = g.my_service_client.send_data(data)
               current_app.logger.info(f"Data sent to external service: {result}")
           except Exception as e:
               current_app.logger.error(f"Error sending data to external service: {str(e)}")
   ```

## Security Considerations

When integrating with external services, follow these security best practices:

1. **API Key Security**:
   - Store API keys and credentials as environment variables
   - Never commit API keys to version control
   - Use encryption for sensitive credentials
   
2. **Request Validation**:
   - Validate responses from external APIs
   - Implement proper error handling
   - Include timeout handling for API requests
   
3. **Rate Limiting**:
   - Respect API rate limits
   - Implement backoff strategies for failed requests
   - Use job queues for bulk operations

4. **Data Privacy**:
   - Only share necessary data with external services
   - Ensure GDPR compliance when transferring user data
   - Document all data sharing in your privacy policy

## Troubleshooting

### Common Integration Issues

1. **API Connectivity Problems**:
   - Check network connectivity
   - Verify API endpoint URLs
   - Ensure correct credentials
   
2. **Authentication Failures**:
   - Verify API keys are valid and not expired
   - Check for correct implementation of authentication headers
   - Confirm proper encoding of credentials
   
3. **Data Format Issues**:
   - Review API documentation for required formats
   - Validate data before sending
   - Check for character encoding issues

### Debugging Tools

1. **Logging**:
   EasyJournal logs API interactions at the DEBUG level. Increase logging to debug integration issues:
   ```python
   # In a plugin
   current_app.logger.debug(f"API request: {url}, data: {data}")
   ```

2. **Testing Endpoints**:
   Use tools like curl or Postman to test API endpoints:
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" https://api.example.com/resource
   ```

## API Reference Documentation

For detailed references on the supported APIs, consult these resources:

- [CrossRef API Documentation](https://www.crossref.org/documentation/metadata-deposit-protocol/)
- [DataCite API Documentation](https://support.datacite.org/docs/api)
- [ORCID API Documentation](https://info.orcid.org/documentation/api-tutorials/)
- [iThenticate API Documentation](https://api.ithenticate.com/documentation/)

## Support

For help with API integrations:
- Contact our support team
- Post in the community forum
- Review the GitHub repository for integration examples