import os
import json
from pathlib import Path

class GameManager:
    def __init__(self):
        # Create data directory if it doesn't exist
        self.data_dir = Path.cwd() / "game_data"
        self.data_dir.mkdir(exist_ok=True)
        
        # High score file path
        self.high_score_file = self.data_dir / "high_score.json"
        
        # Load or initialize high score
        self.high_score = self._load_high_score()
        
        # Speed levels configuration
        self.speed_levels = [
            {"score_threshold": 0, "player_speed": 4, "enemy_min_speed": 2, "enemy_max_speed": 4},
            {"score_threshold": 10, "player_speed": 5, "enemy_min_speed": 3, "enemy_max_speed": 5},
            {"score_threshold": 25, "player_speed": 6, "enemy_min_speed": 4, "enemy_max_speed": 6},
            {"score_threshold": 50, "player_speed": 7, "enemy_min_speed": 5, "enemy_max_speed": 7},
            {"score_threshold": 100, "player_speed": 8, "enemy_min_speed": 6, "enemy_max_speed": 8},
            {"score_threshold": 200, "player_speed": 9, "enemy_min_speed": 7, "enemy_max_speed": 9}
        ]
        
        # Current level
        self.current_level = 0
        
        # Game state
        self.game_over = False
        self.current_score = 0
    
    def _load_high_score(self):
        """Load high score from file or create it if doesn't exist"""
        if self.high_score_file.exists():
            try:
                with open(self.high_score_file, 'r') as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
            except (json.JSONDecodeError, IOError):
                return 0
        return 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open(self.high_score_file, 'w') as f:
                json.dump({"high_score": self.high_score}, f)
        except IOError:
            print("Warning: Could not save high score")
    
    def update_score(self, new_score):
        """Update current score and high score if needed"""
        self.current_score = new_score
        
        # Update high score if needed
        if new_score > self.high_score:
            self.high_score = new_score
            self.save_high_score()
        
        # Update current level based on score
        self._update_level()
        
        return self.current_level
    
    def _update_level(self):
        """Update current level based on score"""
        for i, level in enumerate(self.speed_levels):
            if self.current_score >= level["score_threshold"]:
                self.current_level = i
            else:
                break
    
    def get_current_speeds(self):
        """Get the speed settings for current level"""
        return self.speed_levels[self.current_level]
    
    def reset_game(self):
        """Reset game state"""
        self.game_over = False
        self.current_score = 0
        self.current_level = 0
    
    def set_game_over(self):
        """Set game over state"""
        self.game_over = True