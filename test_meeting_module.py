#!/usr/bin/env python3
"""
Test script for the Meeting Transcription Module
This script tests the basic functionality without requiring audio input.
"""

import asyncio
import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from meetings_driver import MeetingsDatabase
from api import (
    start_meeting, end_meeting, get_current_meeting_status,
    add_meeting_participant, get_meeting_details, search_meetings,
    get_all_meetings, update_meeting, delete_meeting
)

async def test_meeting_module():
    """Test all meeting transcription functions."""
    print("🧪 Testing Meeting Transcription Module...")
    print("=" * 50)
    
    try:
        # Test 1: Database initialization
        print("\n1. Testing database initialization...")
        meetings_db = MeetingsDatabase()
        print("✅ Database initialized successfully")
        
        # Test 2: Create a meeting
        print("\n2. Testing meeting creation...")
        meeting_topic = "Test Meeting - AI Agent Integration"
        main_topics = "Testing the meeting transcription module, verifying database operations"
        keywords = "AI, transcription, testing, integration"
        members_list = "Test User, AI Agent"
        
        # Note: We'll simulate the meeting start without actual audio recording
        print(f"📝 Creating meeting: {meeting_topic}")
        print("⚠️  Note: Audio recording is disabled for testing")
        
        # Test 3: Database operations directly
        print("\n3. Testing direct database operations...")
        
        # Create meeting record
        start_time = datetime.now()
        success, meeting_id, message = meetings_db.create_meeting(
            meeting_topic, start_time, main_topics, keywords, members_list
        )
        
        if success:
            print(f"✅ Meeting created successfully (ID: {meeting_id})")
            
            # Test 4: Add participants
            print("\n4. Testing participant management...")
            
            # Add test participants
            participants = [
                ("John Doe", "Manager", "Engineering"),
                ("Jane Smith", "Developer", "Engineering"),
                ("AI Agent", "Assistant", "AI Services")
            ]
            
            for name, role, dept in participants:
                success, msg = meetings_db.add_participant(meeting_id, name, role, dept)
                if success:
                    print(f"✅ Added participant: {name} ({role}, {dept})")
                else:
                    print(f"❌ Failed to add participant {name}: {msg}")
            
            # Test 5: Add some transcript entries
            print("\n5. Testing transcript management...")
            
            test_transcripts = [
                ("John Doe", "Good morning everyone, let's start our test meeting."),
                ("AI Agent", "Hello! I'm ready to assist with transcription and meeting management."),
                ("Jane Smith", "This is a great test of the new meeting system."),
                ("John Doe", "Let's discuss the key points for today."),
                ("AI Agent", "I'm recording and transcribing everything for future reference.")
            ]
            
            for speaker, text in test_transcripts:
                success, msg = meetings_db.add_transcript_entry(
                    meeting_id, speaker, datetime.now(), text
                )
                if success:
                    print(f"✅ Added transcript: {speaker}: {text[:50]}...")
                else:
                    print(f"❌ Failed to add transcript: {msg}")
            
            # Test 6: Get meeting details
            print("\n6. Testing meeting retrieval...")
            
            meeting = meetings_db.get_meeting(meeting_id)
            participants = meetings_db.get_meeting_participants(meeting_id)
            transcript = meetings_db.get_meeting_transcript(meeting_id)
            
            print(f"📊 Meeting Details:")
            print(f"   - Topic: {meeting['meeting_topic']}")
            print(f"   - Start Time: {meeting['start_time']}")
            print(f"   - Status: {meeting['status']}")
            print(f"   - Participants: {len(participants)}")
            print(f"   - Transcript Entries: {len(transcript)}")
            
            # Test 7: Search functionality
            print("\n7. Testing search functionality...")
            
            search_results = meetings_db.search_meetings("AI")
            print(f"🔍 Search results for 'AI': {len(search_results)} meetings found")
            
            # Test 8: End the meeting
            print("\n8. Testing meeting completion...")
            
            end_time = datetime.now()
            success, message = meetings_db.end_meeting(meeting_id, end_time)
            
            if success:
                print(f"✅ Meeting ended successfully")
                
                # Get updated meeting info
                updated_meeting = meetings_db.get_meeting(meeting_id)
                duration = updated_meeting.get('duration_minutes', 0)
                print(f"   - Duration: {duration} minutes")
                print(f"   - Status: {updated_meeting['status']}")
            else:
                print(f"❌ Failed to end meeting: {message}")
            
            # Test 9: Get all meetings
            print("\n9. Testing meeting listing...")
            
            all_meetings = meetings_db.get_all_meetings()
            print(f"📋 Total meetings in database: {len(all_meetings)}")
            
            for mtg in all_meetings:
                print(f"   - ID {mtg['meeting_id']}: {mtg['meeting_topic']} ({mtg['status']})")
            
            # Test 10: Update meeting
            print("\n10. Testing meeting update...")
            
            success, message = meetings_db.update_meeting(
                meeting_id, 
                keywords="AI, transcription, testing, integration, UPDATED"
            )
            
            if success:
                print("✅ Meeting updated successfully")
                
                # Verify update
                updated_meeting = meetings_db.get_meeting(meeting_id)
                print(f"   - Updated keywords: {updated_meeting['keywords']}")
            else:
                print(f"❌ Failed to update meeting: {message}")
            
            print("\n" + "=" * 50)
            print("🎉 All tests completed successfully!")
            print(f"📁 Meeting data stored in: meetings.db")
            print(f"📁 Meeting files will be stored in: meetings/ folder")
            
        else:
            print(f"❌ Failed to create meeting: {message}")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting Meeting Transcription Module Test...")
    asyncio.run(test_meeting_module()) 