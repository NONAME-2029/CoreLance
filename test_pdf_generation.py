#!/usr/bin/env python3
"""
Test script for PDF generation functionality
"""

import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from meetings_driver import MeetingsDatabase

def test_pdf_generation():
    """Test PDF generation with sample data."""
    print("🧪 Testing PDF Generation...")
    print("=" * 50)
    
    try:
        # Initialize database
        meetings_db = MeetingsDatabase()
        
        # Create a test meeting
        print("\n1. Creating test meeting...")
        start_time = datetime.now()
        meeting_topic = "Test PDF Generation"
        main_topics = "Testing PDF creation, verifying functionality"
        keywords = "PDF, test, generation"
        members_list = "Test User"
        
        success, meeting_id, message = meetings_db.create_meeting(
            meeting_topic, start_time, main_topics, keywords, members_list
        )
        
        if success:
            print(f"✅ Meeting created (ID: {meeting_id})")
            
            # Add test participants
            print("\n2. Adding test participants...")
            participants = [
                ("John Doe", "Manager", "Engineering"),
                ("Jane Smith", "Developer", "Engineering")
            ]
            
            for name, role, dept in participants:
                success, msg = meetings_db.add_participant(meeting_id, name, role, dept)
                if success:
                    print(f"✅ Added participant: {name}")
                else:
                    print(f"❌ Failed to add {name}: {msg}")
            
            # Add test transcript entries
            print("\n3. Adding test transcript...")
            test_transcripts = [
                ("John Doe", "Let's start our test meeting."),
                ("Jane Smith", "I'm ready to test the PDF generation."),
                ("John Doe", "This should create a nice summary."),
                ("Jane Smith", "Let's see how it looks.")
            ]
            
            for speaker, text in test_transcripts:
                success, msg = meetings_db.add_transcript_entry(
                    meeting_id, speaker, datetime.now(), text
                )
                if success:
                    print(f"✅ Added transcript: {speaker}: {text[:30]}...")
                else:
                    print(f"❌ Failed to add transcript: {msg}")
            
            # End the meeting
            print("\n4. Ending meeting...")
            end_time = datetime.now()
            success, message = meetings_db.end_meeting(meeting_id, end_time)
            
            if success:
                print("✅ Meeting ended successfully")
                
                # Get meeting details
                meeting = meetings_db.get_meeting(meeting_id)
                participants = meetings_db.get_meeting_participants(meeting_id)
                transcript = meetings_db.get_meeting_transcript(meeting_id)
                
                print(f"\n📊 Meeting Summary:")
                print(f"   - Topic: {meeting['meeting_topic']}")
                print(f"   - Start: {meeting['start_time']}")
                print(f"   - End: {meeting['end_time']}")
                print(f"   - Duration: {meeting['duration_minutes']} minutes")
                print(f"   - Participants: {len(participants)}")
                print(f"   - Transcript entries: {len(transcript)}")
                
                # Test PDF generation directly
                print("\n5. Testing PDF generation...")
                from api import generate_meeting_summary
                
                pdf_path = generate_meeting_summary(meeting_id)
                
                if pdf_path and os.path.exists(pdf_path):
                    file_size = os.path.getsize(pdf_path)
                    print(f"✅ PDF generated successfully!")
                    print(f"   - Path: {pdf_path}")
                    print(f"   - Size: {file_size} bytes")
                    
                    # Check if file is in completed folder
                    completed_dir = "meetings/completed"
                    if os.path.exists(completed_dir):
                        files = os.listdir(completed_dir)
                        print(f"   - Files in completed folder: {files}")
                    else:
                        print(f"   - Completed folder not found: {completed_dir}")
                        
                else:
                    print(f"❌ PDF generation failed")
                    print(f"   - Path returned: {pdf_path}")
                    print(f"   - File exists: {os.path.exists(pdf_path) if pdf_path else 'N/A'}")
                    
            else:
                print(f"❌ Failed to end meeting: {message}")
                
        else:
            print(f"❌ Failed to create meeting: {message}")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting PDF Generation Test...")
    test_pdf_generation() 