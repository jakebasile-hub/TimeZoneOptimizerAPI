import pytz
from datetime import datetime, timedelta
from typing import List, Tuple, Dict
import math


class TimezoneOptimizer:
    def __init__(self):
        self.working_hours = (9, 17)  # 9 AM to 5 PM
        self.sleep_hours = (22, 7)  # 10 PM to 7 AM (next day)
    
    def get_timezone_from_location(self, location: str) -> str:
        """Convert location string to IANA timezone"""
        # Comprehensive mapping for common locations
        location_mapping = {
            # North America
            "new york": "America/New_York",
            "los angeles": "America/Los_Angeles",
            "chicago": "America/Chicago",
            "denver": "America/Denver",
            "toronto": "America/Toronto",
            "vancouver": "America/Vancouver",
            "miami": "America/New_York",
            "seattle": "America/Los_Angeles",
            "boston": "America/New_York",
            "san francisco": "America/Los_Angeles",
            "usa": "America/New_York",
            "united states": "America/New_York",
            "canada": "America/Toronto",
            
            # Europe
            "london": "Europe/London",
            "paris": "Europe/Paris",
            "berlin": "Europe/Berlin",
            "rome": "Europe/Rome",
            "madrid": "Europe/Madrid",
            "amsterdam": "Europe/Amsterdam",
            "zurich": "Europe/Zurich",
            "vienna": "Europe/Vienna",
            "moscow": "Europe/Moscow",
            "uk": "Europe/London",
            "united kingdom": "Europe/London",
            "france": "Europe/Paris",
            "germany": "Europe/Berlin",
            "italy": "Europe/Rome",
            "spain": "Europe/Madrid",
            "netherlands": "Europe/Amsterdam",
            "switzerland": "Europe/Zurich",
            "austria": "Europe/Vienna",
            "russia": "Europe/Moscow",
            
            # Asia
            "tokyo": "Asia/Tokyo",
            "beijing": "Asia/Shanghai",
            "shanghai": "Asia/Shanghai",
            "hong kong": "Asia/Hong_Kong",
            "singapore": "Asia/Singapore",
            "mumbai": "Asia/Kolkata",
            "delhi": "Asia/Kolkata",
            "bangalore": "Asia/Kolkata",
            "seoul": "Asia/Seoul",
            "taipei": "Asia/Taipei",
            "bangkok": "Asia/Bangkok",
            "jakarta": "Asia/Jakarta",
            "manila": "Asia/Manila",
            "japan": "Asia/Tokyo",
            "china": "Asia/Shanghai",
            "india": "Asia/Kolkata",
            "south korea": "Asia/Seoul",
            "korea": "Asia/Seoul",
            "taiwan": "Asia/Taipei",
            "thailand": "Asia/Bangkok",
            "indonesia": "Asia/Jakarta",
            "philippines": "Asia/Manila",
            
            # Australia/Oceania
            "sydney": "Australia/Sydney",
            "melbourne": "Australia/Melbourne",
            "perth": "Australia/Perth",
            "brisbane": "Australia/Brisbane",
            "auckland": "Pacific/Auckland",
            "australia": "Australia/Sydney",
            "new zealand": "Pacific/Auckland",
            
            # South America
            "sao paulo": "America/Sao_Paulo",
            "rio de janeiro": "America/Sao_Paulo",
            "buenos aires": "America/Argentina/Buenos_Aires",
            "lima": "America/Lima",
            "bogota": "America/Bogota",
            "mexico city": "America/Mexico_City",
            "brazil": "America/Sao_Paulo",
            "argentina": "America/Argentina/Buenos_Aires",
            "peru": "America/Lima",
            "colombia": "America/Bogota",
            "mexico": "America/Mexico_City",
            
            # Africa
            "cairo": "Africa/Cairo",
            "johannesburg": "Africa/Johannesburg",
            "lagos": "Africa/Lagos",
            "nairobi": "Africa/Nairobi",
            "egypt": "Africa/Cairo",
            "south africa": "Africa/Johannesburg",
            "nigeria": "Africa/Lagos",
            "kenya": "Africa/Nairobi"
        }
        
        location_lower = location.lower()
        for key, tz in location_mapping.items():
            if key in location_lower:
                return tz
        
        # Fallback to UTC if not found
        return "UTC"
    
    def calculate_conflict_cost(self, local_hour: int, local_minute: int = 0) -> float:
        """Calculate conflict cost for a given local time"""
        local_time = local_hour + local_minute / 60.0
        
        # Check if in sleep hours (10 PM to 7 AM)
        if local_time >= 22 or local_time <= 7:
            return 1.0  # Maximum conflict
        
        # Check if in working hours (9 AM to 5 PM)
        if 9 <= local_time <= 17:
            return 0.0  # No conflict
        
        # Calculate distance from working hours
        if local_time < 9:
            distance = 9 - local_time
        else:  # local_time > 17
            distance = local_time - 17
        
        # Normalize distance (max 8 hours away from working hours)
        return min(distance / 8.0, 1.0)
    
    def find_optimal_meeting_time(self, participants: List[Dict], duration_minutes: int = 60, 
                                 num_alternatives: int = 3) -> Dict:
        """Find optimal meeting time for participants"""
        
        # Get timezones for all participants
        participant_timezones = []
        for participant in participants:
            tz_name = self.get_timezone_from_location(participant["location"])
            tz = pytz.timezone(tz_name)
            participant_timezones.append({
                "name": participant["name"],
                "timezone": tz,
                "tz_name": tz_name
            })
        
        best_utc_time = None
        best_score = float('inf')
        all_scores = []
        
        # Test each hour in a 24-hour period
        base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for hour in range(24):
            utc_time = base_date.replace(hour=hour)
            total_cost = 0
            
            for participant in participant_timezones:
                # Convert UTC to local time
                local_time = utc_time.replace(tzinfo=pytz.UTC).astimezone(participant["timezone"])
                conflict_cost = self.calculate_conflict_cost(local_time.hour, local_time.minute)
                total_cost += conflict_cost
            
            # Calculate fairness score (lower cost = higher fairness)
            fairness_score = max(0, 1 - (total_cost / len(participants)))
            
            all_scores.append({
                "utc_time": utc_time,
                "total_cost": total_cost,
                "fairness_score": fairness_score
            })
            
            if total_cost < best_score:
                best_score = total_cost
                best_utc_time = utc_time
        
        # Sort by fairness score (descending)
        all_scores.sort(key=lambda x: x["fairness_score"], reverse=True)
        
        # Get best time and alternatives
        best_result = all_scores[0]
        alternatives = all_scores[1:num_alternatives+1]
        
        # Format local times for best result
        local_times = []
        for participant in participant_timezones:
            local_time = best_result["utc_time"].replace(tzinfo=pytz.UTC).astimezone(participant["timezone"])
            local_times.append({
                "name": participant["name"],
                "local_time": local_time.isoformat()
            })
        
        return {
            "best_meeting_time_utc": best_result["utc_time"].isoformat() + "Z",
            "local_times": local_times,
            "alternatives": [
                {
                    "utc_time": alt["utc_time"].isoformat() + "Z",
                    "fairness_score": round(alt["fairness_score"], 2)
                }
                for alt in alternatives
            ]
        }
