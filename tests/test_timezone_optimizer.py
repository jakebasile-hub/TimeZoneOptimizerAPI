import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from timezone_optimizer import TimezoneOptimizer


class TestTimezoneOptimizer:
    def setup_method(self):
        self.optimizer = TimezoneOptimizer()
    
    def test_get_timezone_from_location(self):
        """Test timezone mapping for common locations"""
        assert self.optimizer.get_timezone_from_location("New York, USA") == "America/New_York"
        assert self.optimizer.get_timezone_from_location("Tokyo, Japan") == "Asia/Tokyo"
        assert self.optimizer.get_timezone_from_location("London, UK") == "Europe/London"
        assert self.optimizer.get_timezone_from_location("Unknown Location") == "UTC"
    
    def test_calculate_conflict_cost(self):
        """Test conflict cost calculation"""
        # Working hours should have no conflict
        assert self.optimizer.calculate_conflict_cost(10) == 0.0  # 10 AM
        assert self.optimizer.calculate_conflict_cost(14) == 0.0  # 2 PM
        
        # Sleep hours should have maximum conflict
        assert self.optimizer.calculate_conflict_cost(23) == 1.0  # 11 PM
        assert self.optimizer.calculate_conflict_cost(2) == 1.0   # 2 AM
        
        # Early morning should have some conflict
        cost_7am = self.optimizer.calculate_conflict_cost(7)
        assert 0 < cost_7am < 1
        
        # Evening should have some conflict
        cost_18 = self.optimizer.calculate_conflict_cost(18)
        assert 0 < cost_18 < 1
    
    def test_find_optimal_meeting_time(self):
        """Test optimal meeting time calculation"""
        participants = [
            {"name": "Alice", "location": "New York, USA"},
            {"name": "Bob", "location": "London, UK"}
        ]
        
        result = self.optimizer.find_optimal_meeting_time(
            participants=participants,
            duration_minutes=60,
            num_alternatives=2
        )
        
        # Check response structure
        assert "best_meeting_time_utc" in result
        assert "local_times" in result
        assert "alternatives" in result
        
        # Check local times
        assert len(result["local_times"]) == 2
        assert result["local_times"][0]["name"] == "Alice"
        assert result["local_times"][1]["name"] == "Bob"
        
        # Check alternatives
        assert len(result["alternatives"]) <= 2
        for alt in result["alternatives"]:
            assert "utc_time" in alt
            assert "fairness_score" in alt
            assert 0 <= alt["fairness_score"] <= 1
    
    def test_find_optimal_meeting_time_single_participant(self):
        """Test with single participant"""
        participants = [{"name": "Alice", "location": "New York, USA"}]
        
        result = self.optimizer.find_optimal_meeting_time(
            participants=participants,
            duration_minutes=30,
            num_alternatives=1
        )
        
        assert len(result["local_times"]) == 1
        assert result["local_times"][0]["name"] == "Alice"
    
    def test_find_optimal_meeting_time_many_participants(self):
        """Test with multiple participants across different timezones"""
        participants = [
            {"name": "Alice", "location": "New York, USA"},
            {"name": "Bob", "location": "Tokyo, Japan"},
            {"name": "Cara", "location": "London, UK"},
            {"name": "Dave", "location": "Sydney, Australia"}
        ]
        
        result = self.optimizer.find_optimal_meeting_time(
            participants=participants,
            duration_minutes=90,
            num_alternatives=3
        )
        
        assert len(result["local_times"]) == 4
        assert len(result["alternatives"]) <= 3
        
        # All participants should have local times
        participant_names = [lt["name"] for lt in result["local_times"]]
        assert "Alice" in participant_names
        assert "Bob" in participant_names
        assert "Cara" in participant_names
        assert "Dave" in participant_names
