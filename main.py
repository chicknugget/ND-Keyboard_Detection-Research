from data.models import Session, KeystrokeEvent, EmotionLabel, GameResult
from data.constants import TASK_TYPES, FIXED_SENTENCES, EMOJI_OPTIONS

# Test 1: printing task types
print("Task Types:")
print(TASK_TYPES)

#test 2: printing constant sentences
print("\nFixed Sentence for HAPPY task:")
print(FIXED_SENTENCES["HAPPY"])

#test 3: creating a sample session
print("\n --- sample session ---")
session = Session(
    session_id="test-session-123",
    participant_id="P001",
    start_time=1704567890000,
    status="in_progress"
)
print("Session created:", session)

#test 4: creating a sample keystroke event
print("\n --- sample keystroke event ---")
keystroke_event = KeystrokeEvent(
    session_id="test-session-123",
    task_type="HAPPY",
    key_id="A",
    key_char="A",
    press_time_ms=1704567890000,
    release_time_ms=1704567890000,
    hold_duration_ms=100,
    inter_key_interval_ms=50,
    flight_time_ms=200,
    touch_x=100,
    touch_y=100,
    key_center_x=100,
    key_center_y=100,
    pressure=0.5,
    touch_size=1.0,
    is_backspace=False,
    is_error=False,
    position_in_sentence=0
)
print("Keystroke event created:", keystroke_event)

# Test 4: Create a sample EmotionLabel
print("\n--- Creating Sample EmotionLabel ---")
emotion_label = EmotionLabel(
    session_id="test-session-123",
    task_type="HAPPY",
    selected_emoji="😊",
    typed_sentence="I am happy after playing this game.",
    expected_sentence=FIXED_SENTENCES["HAPPY"],
    is_exact_match=True,
    typing_duration_ms=12450,
    total_keystrokes=42,
    backspace_count=2
)

print("EmotionLabel created:")
print(emotion_label)

# Test 5: Create a sample GameResult
print("\n--- Creating Sample GameResult ---")
game_result = GameResult(
    session_id="test-session-123",
    task_type="HAPPY",
    final_score=1050,
    outcome="FORCED_WIN",
    start_time=1704567890000,
    end_time=1704567980000,
    duration_ms=90000,
    attempts=1
)
print("GameResult created:")
print(game_result)

# Test 6: Convert to dictionary
print("\n--- Testing to_dict() Methods ---")
print("Session as dictionary:")
print(session.to_dict())
print("\nKeystroke event as dictionary:")
print(keystroke_event.to_dict())
print("\nEmotionLabel as dictionary:")
print(emotion_label.to_dict())
print("\nGameResult as dictionary:")
print(game_result.to_dict())