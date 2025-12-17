"""WebAPI client for fetching data from devices"""
import requests
from typing import Optional, Dict, Any, List, Tuple
from app.models import Device
from app.services.device_service import DeviceService
from sqlalchemy.orm import Session
import json


class WebAPIClient:
    """Generic WebAPI client for fetching data from devices"""
    
    def __init__(self, device: Device):
        self.device = device
        self.api_endpoint = device.api_endpoint
        self.api_key = None  # Will be set from device
        self.configuration = device.configuration or {}
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Add API key if available
        if self.api_key:
            # Support different auth methods
            auth_method = self.configuration.get("auth_method", "header")
            auth_header = self.configuration.get("auth_header", "Authorization")
            
            if auth_method == "header":
                headers[auth_header] = f"Bearer {self.api_key}" if "Bearer" not in auth_header else self.api_key
            elif auth_method == "query":
                # API key will be added to query params
                pass
        
        return headers
    
    def fetch_data(self, endpoint: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        Fetch data from device API
        
        Args:
            endpoint: API endpoint path (relative to base endpoint)
            params: Query parameters
        
        Returns:
            Tuple of (data_list, error_message)
        """
        try:
            # Construct full URL
            if endpoint:
                url = f"{self.api_endpoint.rstrip('/')}/{endpoint.lstrip('/')}"
            else:
                url = self.api_endpoint
            
            # Add API key to query params if needed
            if self.configuration.get("auth_method") == "query":
                if params is None:
                    params = {}
                api_key_param = self.configuration.get("api_key_param", "api_key")
                params[api_key_param] = self.api_key
            
            # Make request
            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=self.configuration.get("timeout", 30)
            )
            
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            
            # Handle different response formats
            if isinstance(data, list):
                return data, None
            elif isinstance(data, dict):
                # Check for common data wrapper keys
                data_key = self.configuration.get("data_key", "results")
                if data_key in data:
                    return data[data_key], None
                elif "data" in data:
                    return data["data"], None
                else:
                    # Return as single-item list
                    return [data], None
            else:
                return None, f"Unexpected response format: {type(data)}"
                
        except requests.exceptions.RequestException as e:
            return None, f"API request failed: {str(e)}"
        except json.JSONDecodeError as e:
            return None, f"Invalid JSON response: {str(e)}"
        except Exception as e:
            return None, f"Error fetching data: {str(e)}"


class IntersightAPIClient(WebAPIClient):
    """Intersight-specific API client"""
    
    def fetch_alarms(self, filters: Optional[Dict[str, Any]] = None) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """Fetch alarms from Intersight"""
        endpoint = self.configuration.get("alarms_endpoint", "api/v1/cond/Alarms")
        return self.fetch_data(endpoint, filters)
    
    def fetch_devices(self, filters: Optional[Dict[str, Any]] = None) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """Fetch devices from Intersight"""
        endpoint = self.configuration.get("devices_endpoint", "api/v1/asset/DeviceRegistrations")
        return self.fetch_data(endpoint, filters)


def get_api_client(db: Session, device_id: str) -> Optional[WebAPIClient]:
    """Get API client for a device"""
    device = DeviceService.get_device(db, device_id)
    if not device or not device.is_active:
        return None
    
    # Get decrypted API key
    api_key = DeviceService.get_device_api_key(device)
    
    # Create appropriate client based on device type
    if device.device_type.lower() == "intersight":
        client = IntersightAPIClient(device)
    else:
        client = WebAPIClient(device)
    
    client.api_key = api_key
    return client

