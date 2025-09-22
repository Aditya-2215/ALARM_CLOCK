import time
import os
import sys
from datetime import datetime, timedelta
import pygame
import threading
from pathlib import Path

class AlarmClock:
    def __init__(self):
        self.is_running = False
        self.alarm_thread = None
        self.snooze_time = 5  # minutes
        self.default_sounds = ["alarm.mp3", "alarm.wav", "beep.mp3", "wake_up.wav"]
        
    def find_alarm_sound(self, sound_file=None):
        """Find a valid alarm sound file"""
        if sound_file and os.path.exists(sound_file):
            return sound_file
            
        # Check for default sound files
        for sound in self.default_sounds:
            if os.path.exists(sound):
                return sound
                
        # If no sound file found, we'll use a system beep
        return None
    
    def play_alarm_sound(self, sound_file):
        """Play the alarm sound with error handling"""
        try:
            if sound_file and os.path.exists(sound_file):
                pygame.mixer.init()
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                print(f"🔊 Playing alarm sound: {sound_file}")
            else:
                print("🔊 No sound file found, using system beep")
                self.system_beep()
        except pygame.error as e:
            print(f"❌ Error playing sound: {e}")
            self.system_beep()
    
    def system_beep(self):
        """Fallback system beep for when no sound file is available"""
        for i in range(10):
            print("\a", end="")  # System beep
            time.sleep(0.5)
    
    def stop_alarm(self):
        """Stop the alarm sound"""
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
    
    def parse_time_input(self, time_input):
        """Parse various time input formats"""
        try:
            # Handle HH:MM:SS format
            if len(time_input.split(':')) == 3:
                return datetime.strptime(time_input, "%H:%M:%S").time()
            # Handle HH:MM format
            elif len(time_input.split(':')) == 2:
                return datetime.strptime(time_input, "%H:%M").time()
            else:
                raise ValueError("Invalid time format")
        except ValueError:
            return None
    
    def get_next_alarm_datetime(self, alarm_time):
        """Get the next occurrence of the alarm time (today or tomorrow)"""
        now = datetime.now()
        alarm_datetime = datetime.combine(now.date(), alarm_time)
        
        # If the alarm time has already passed today, set it for tomorrow
        if alarm_datetime <= now:
            alarm_datetime += timedelta(days=1)
            
        return alarm_datetime
    
    def countdown_display(self, target_time):
        """Display countdown to alarm"""
        while self.is_running:
            current_time = datetime.now()
            time_diff = target_time - current_time
            
            if time_diff.total_seconds() <= 0:
                break
                
            hours, remainder = divmod(int(time_diff.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            
            countdown = f"⏰ Time until alarm: {hours:02d}:{minutes:02d}:{seconds:02d}"
            current = f"🕐 Current time: {current_time.strftime('%H:%M:%S')}"
            
            print(f"\r{current} | {countdown}", end="", flush=True)
            time.sleep(1)
    
    def alarm_controls(self):
        """Handle user input while alarm is ringing"""
        print("\n" + "="*50)
        print("🚨 ALARM IS RINGING! 🚨")
        print("="*50)
        print("Options:")
        print("  [S] - Snooze (5 minutes)")
        print("  [O] - Turn off alarm")
        print("  [Q] - Quit program")
        print("="*50)
        
        while pygame.mixer.music.get_busy() or True:
            try:
                choice = input("\nEnter your choice (S/O/Q): ").upper().strip()
                
                if choice == 'S':
                    self.stop_alarm()
                    snooze_time = datetime.now() + timedelta(minutes=self.snooze_time)
                    print(f"⏰ Snoozed! Alarm will ring again at {snooze_time.strftime('%H:%M:%S')}")
                    return 'snooze', snooze_time
                    
                elif choice == 'O':
                    self.stop_alarm()
                    print("✅ Alarm turned off!")
                    return 'off', None
                    
                elif choice == 'Q':
                    self.stop_alarm()
                    print("👋 Goodbye!")
                    return 'quit', None
                    
                else:
                    print("❌ Invalid choice. Please enter S, O, or Q.")
                    
            except KeyboardInterrupt:
                self.stop_alarm()
                return 'quit', None
    
    def set_alarm(self, alarm_time_str, sound_file=None):
        """Main alarm function"""
        # Parse the alarm time
        alarm_time = self.parse_time_input(alarm_time_str)
        if not alarm_time:
            print("❌ Invalid time format! Please use HH:MM or HH:MM:SS")
            return
        
        # Get the next occurrence of this time
        target_datetime = self.get_next_alarm_datetime(alarm_time)
        
        # Find sound file
        sound_path = self.find_alarm_sound(sound_file)
        
        print(f"⏰ ALARM SET FOR {target_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        if sound_path:
            print(f"🔊 Sound file: {sound_path}")
        else:
            print("🔊 Will use system beep (no sound file found)")
        print("Press Ctrl+C to cancel\n")
        
        self.is_running = True
        
        try:
            # Start countdown in a separate thread
            countdown_thread = threading.Thread(target=self.countdown_display, args=(target_datetime,))
            countdown_thread.daemon = True
            countdown_thread.start()
            
            # Wait until alarm time
            while datetime.now() < target_datetime and self.is_running:
                time.sleep(0.1)
            
            if self.is_running:
                self.trigger_alarm(sound_path)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Alarm cancelled by user!")
            self.is_running = False
    
    def trigger_alarm(self, sound_path):
        """Trigger the alarm and handle user response"""
        self.is_running = False  # Stop countdown
        print("\n" + "🚨" * 20)
        print("  🚨 WAKE UP! ALARM TRIGGERED! 🚨")
        print("🚨" * 20)
        
        # Play alarm sound
        self.play_alarm_sound(sound_path)
        
        # Handle user controls
        action, snooze_time = self.alarm_controls()
        
        if action == 'snooze':
            print("💤 Starting snooze countdown...")
            self.is_running = True
            self.countdown_display(snooze_time)
            if self.is_running:
                self.trigger_alarm(sound_path)  # Recursive call for snooze
        elif action == 'quit':
            sys.exit(0)

def main():
    """Main function with enhanced user interface"""
    alarm_clock = AlarmClock()
    
    print("=" * 50)
    print("🕐 ENHANCED ALARM CLOCK")
    print("=" * 50)
    print("Features:")
    print("  ✅ Multiple time formats (HH:MM or HH:MM:SS)")
    print("  ✅ Automatic next-day scheduling")
    print("  ✅ Snooze functionality")
    print("  ✅ Countdown display")
    print("  ✅ Multiple sound format support")
    print("  ✅ Fallback system beep")
    print("=" * 50)
    
    try:
        # Get alarm time
        alarm_time = input("⏰ Enter alarm time (HH:MM or HH:MM:SS): ").strip()
        
        # Optional: Get custom sound file
        sound_file = input("🔊 Enter sound file path (optional, press Enter to skip): ").strip()
        if not sound_file:
            sound_file = None
        
        print()
        alarm_clock.set_alarm(alarm_time, sound_file)
        
    except KeyboardInterrupt:
        print("\n\n👋 Program terminated by user!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()