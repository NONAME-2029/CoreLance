#!/usr/bin/env python3
"""
Test script for AI-powered meeting summary generation using Gemini API
"""

import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from meetings_driver import MeetingsDatabase

def test_ai_summary_generation():
    """Test AI-powered meeting summary generation."""
    print("🧪 Testing AI-Powered Meeting Summary Generation...")
    print("=" * 60)
    
    try:
        # Check if Gemini API key is available
        gemini_api_key = os.getenv("GOOGLE_API_KEY")
        if not gemini_api_key:
            print("❌ GOOGLE_API_KEY not found in environment variables")
            print("Please set your Gemini API key in the summary.env file")
            return
        
        print("✅ Gemini API key found")
        
        # Initialize database
        meetings_db = MeetingsDatabase()
        
        # Create a test meeting with realistic transcript
        print("\n1. Creating test meeting with realistic transcript...")
        start_time = datetime.now()
        meeting_topic = "Q4 Product Strategy Planning"
        main_topics = "Product roadmap, market analysis, resource allocation"
        keywords = "strategy, planning, Q4, product, market"
        members_list = "Product Manager, Engineering Lead, Marketing Director"
        
        success, meeting_id, message = meetings_db.create_meeting(
            meeting_topic, start_time, main_topics, keywords, members_list
        )
        
        if success:
            print(f"✅ Meeting created (ID: {meeting_id})")
            
            # Add test participants
            print("\n2. Adding test participants...")
            participants = [
                ("Sarah Chen", "Product Manager", "Product"),
                ("Mike Rodriguez", "Engineering Lead", "Engineering"),
                ("Lisa Thompson", "Marketing Director", "Marketing"),
                ("David Kim", "Data Analyst", "Analytics")
            ]
            
            for name, role, dept in participants:
                success, msg = meetings_db.add_participant(meeting_id, name, role, dept)
                if success:
                    print(f"✅ Added participant: {name} ({role})")
                else:
                    print(f"❌ Failed to add {name}: {msg}")
            
            # Add realistic test transcript
            print("\n3. Adding realistic test transcript...")
            test_transcripts = [
                ("Sarah Chen", "Good morning everyone. Let's start our Q4 product strategy planning session. We need to finalize our roadmap for the next quarter."),
                ("Mike Rodriguez", "Thanks Sarah. From engineering perspective, we have three major features in development. The AI recommendation engine is 70% complete, mobile app redesign is 85% done, and the new analytics dashboard is about 60%."),
                ("Lisa Thompson", "Great progress Mike. From marketing side, we're seeing strong demand for the AI features. Customer surveys show 78% interest in personalized recommendations."),
                ("David Kim", "I can confirm that. Our data shows users spend 40% more time on pages with AI recommendations. Conversion rates are up 25%."),
                ("Sarah Chen", "Excellent insights David. So we should prioritize the AI engine completion. What's the timeline for that?"),
                ("Mike Rodriguez", "We can complete the AI engine by end of October if we allocate two more developers. That would give us November for testing and December for launch."),
                ("Lisa Thompson", "Perfect timing for holiday season. We can run a major marketing campaign around the AI launch. Budget-wise, we need about $50K for the campaign."),
                ("Sarah Chen", "Agreed. Let's also discuss the mobile app redesign. How critical is that for Q4?"),
                ("Mike Rodriguez", "The mobile redesign is important but not critical. We could push it to Q1 if needed. The current app is functional, just not as user-friendly."),
                ("David Kim", "I agree. Mobile usage is only 30% of our traffic, so the AI engine will have bigger impact on our overall metrics."),
                ("Sarah Chen", "Perfect. So our Q4 priorities are: 1) Complete AI recommendation engine, 2) Launch marketing campaign, 3) Begin mobile redesign planning for Q1. Any objections?"),
                ("Mike Rodriguez", "None from engineering. We're good with the timeline."),
                ("Lisa Thompson", "Marketing is ready to execute. We'll start preparing the campaign materials next week."),
                ("David Kim", "Analytics team will set up tracking for the AI features and prepare success metrics."),
                ("Sarah Chen", "Excellent. Meeting adjourned. Next review in two weeks.")
            ]
            
            for speaker, text in test_transcripts:
                success, msg = meetings_db.add_transcript_entry(
                    meeting_id, speaker, datetime.now(), text
                )
                if success:
                    print(f"✅ Added transcript: {speaker}: {text[:50]}...")
                else:
                    print(f"❌ Failed to add transcript: {msg}")
            
            # End the meeting
            print("\n4. Ending meeting...")
            end_time = datetime.now()
            success, message = meetings_db.end_meeting(meeting_id, end_time)
            
            if success:
                print("✅ Meeting ended successfully")
                
                # Test AI summary generation
                print("\n5. Testing AI-powered summary generation...")
                from api import generate_ai_meeting_summary
                
                ai_summary = generate_ai_meeting_summary(meeting_id)
                
                if ai_summary:
                    print("✅ AI summary generated successfully!")
                    print("\n" + "="*50)
                    print("AI-GENERATED MEETING SUMMARY:")
                    print("="*50)
                    print(ai_summary)
                    print("="*50)
                    
                    # Test PDF generation with AI summary
                    print("\n6. Testing PDF generation with AI summary...")
                    from api import generate_meeting_summary
                    
                    pdf_path = generate_meeting_summary(meeting_id)
                    
                    if pdf_path and os.path.exists(pdf_path):
                        file_size = os.path.getsize(pdf_path)
                        print(f"✅ PDF generated successfully with AI summary!")
                        print(f"   - Path: {pdf_path}")
                        print(f"   - Size: {file_size} bytes")
                    else:
                        print(f"❌ PDF generation failed")
                        
                else:
                    print("❌ AI summary generation failed")
                    
            else:
                print(f"❌ Failed to end meeting: {message}")
                
        else:
            print(f"❌ Failed to create meeting: {message}")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting AI Summary Generation Test...")
    test_ai_summary_generation() 