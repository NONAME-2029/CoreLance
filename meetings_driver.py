import sqlite3
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MeetingsDatabase:
    def __init__(self, db_path: str = "meetings.db"):
        """Initialize the meetings database."""
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize the meetings database with required tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create meetings table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS meetings (
                        meeting_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        meeting_topic TEXT NOT NULL,
                        start_time DATETIME NOT NULL,
                        end_time DATETIME,
                        duration_minutes INTEGER,
                        status TEXT DEFAULT 'active',
                        file_path TEXT,
                        file_size INTEGER,
                        main_topics TEXT,
                        keywords TEXT,
                        members_list TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create meeting_transcripts table for detailed transcripts
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS meeting_transcripts (
                        transcript_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        meeting_id INTEGER,
                        speaker_name TEXT,
                        timestamp DATETIME,
                        text_content TEXT,
                        FOREIGN KEY (meeting_id) REFERENCES meetings (meeting_id)
                    )
                ''')
                
                # Create meeting_participants table for detailed participant info
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS meeting_participants (
                        participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        meeting_id INTEGER,
                        name TEXT NOT NULL,
                        role TEXT,
                        department TEXT,
                        join_time DATETIME,
                        leave_time DATETIME,
                        FOREIGN KEY (meeting_id) REFERENCES meetings (meeting_id)
                    )
                ''')
                
                conn.commit()
                logger.info("Meetings database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing meetings database: {e}")
            raise
    
    def create_meeting(self, meeting_topic: str, start_time: datetime, 
                       main_topics: str = "", keywords: str = "", 
                       members_list: str = "") -> Tuple[bool, int, str]:
        """
        Create a new meeting record.
        
        Args:
            meeting_topic: Main topic of the meeting
            start_time: When the meeting started
            main_topics: Main discussion points
            keywords: Key terms discussed
            members_list: List of participants
            
        Returns:
            Tuple of (success, meeting_id, message)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO meetings 
                    (meeting_topic, start_time, main_topics, keywords, members_list, status)
                    VALUES (?, ?, ?, ?, ?, 'active')
                ''', (meeting_topic, start_time, main_topics, keywords, members_list))
                
                meeting_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"Meeting created successfully with ID: {meeting_id}")
                return True, meeting_id, "Meeting created successfully"
                
        except Exception as e:
            logger.error(f"Error creating meeting: {e}")
            return False, 0, f"Error creating meeting: {str(e)}"
    
    def end_meeting(self, meeting_id: int, end_time: datetime, 
                    file_path: str = None, file_size: int = None) -> Tuple[bool, str]:
        """
        End a meeting and update its status.
        
        Args:
            meeting_id: ID of the meeting to end
            end_time: When the meeting ended
            file_path: Path to the generated PDF/TXT file
            file_size: Size of the file in bytes
            
        Returns:
            Tuple of (success, message)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Calculate duration
                start_time = self.get_meeting_start_time(meeting_id)
                if start_time:
                    duration = int((end_time - start_time).total_seconds() / 60)
                else:
                    duration = 0
                
                cursor.execute('''
                    UPDATE meetings 
                    SET end_time = ?, duration_minutes = ?, status = 'completed',
                        file_path = ?, file_size = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE meeting_id = ?
                ''', (end_time, duration, file_path, file_size, meeting_id))
                
                conn.commit()
                
                logger.info(f"Meeting {meeting_id} ended successfully")
                return True, "Meeting ended successfully"
                
        except Exception as e:
            logger.error(f"Error ending meeting: {e}")
            return False, f"Error ending meeting: {str(e)}"
    
    def update_meeting(self, meeting_id: int, **kwargs) -> Tuple[bool, str]:
        """
        Update meeting information.
        
        Args:
            meeting_id: ID of the meeting to update
            **kwargs: Fields to update (meeting_topic, main_topics, keywords, etc.)
            
        Returns:
            Tuple of (success, message)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build dynamic update query
                update_fields = []
                values = []
                
                for field, value in kwargs.items():
                    if field in ['meeting_topic', 'main_topics', 'keywords', 'members_list', 'status']:
                        update_fields.append(f"{field} = ?")
                        values.append(value)
                
                if not update_fields:
                    return False, "No valid fields to update"
                
                update_fields.append("updated_at = CURRENT_TIMESTAMP")
                values.append(meeting_id)
                
                query = f"UPDATE meetings SET {', '.join(update_fields)} WHERE meeting_id = ?"
                cursor.execute(query, values)
                
                conn.commit()
                
                logger.info(f"Meeting {meeting_id} updated successfully")
                return True, "Meeting updated successfully"
                
        except Exception as e:
            logger.error(f"Error updating meeting: {e}")
            return False, f"Error updating meeting: {str(e)}"
    
    def delete_meeting(self, meeting_id: int) -> Tuple[bool, str]:
        """
        Delete a meeting and all related data.
        
        Args:
            meeting_id: ID of the meeting to delete
            
        Returns:
            Tuple of (success, message)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Delete related records first
                cursor.execute("DELETE FROM meeting_transcripts WHERE meeting_id = ?", (meeting_id,))
                cursor.execute("DELETE FROM meeting_participants WHERE meeting_id = ?", (meeting_id,))
                
                # Delete main meeting record
                cursor.execute("DELETE FROM meetings WHERE meeting_id = ?", (meeting_id,))
                
                conn.commit()
                
                logger.info(f"Meeting {meeting_id} deleted successfully")
                return True, "Meeting deleted successfully"
                
        except Exception as e:
            logger.error(f"Error deleting meeting: {e}")
            return False, f"Error deleting meeting: {str(e)}"
    
    def get_meeting(self, meeting_id: int) -> Optional[Dict]:
        """
        Get meeting details by ID.
        
        Args:
            meeting_id: ID of the meeting
            
        Returns:
            Meeting details as dictionary or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM meetings WHERE meeting_id = ?
                ''', (meeting_id,))
                
                row = cursor.fetchone()
                if row:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, row))
                return None
                
        except Exception as e:
            logger.error(f"Error getting meeting: {e}")
            return None
    
    def get_all_meetings(self, status: str = None, limit: int = 100) -> List[Dict]:
        """
        Get all meetings with optional filtering.
        
        Args:
            status: Filter by status (active, completed, cancelled)
            limit: Maximum number of meetings to return
            
        Returns:
            List of meeting dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if status:
                    cursor.execute('''
                        SELECT * FROM meetings 
                        WHERE status = ? 
                        ORDER BY start_time DESC 
                        LIMIT ?
                    ''', (status, limit))
                else:
                    cursor.execute('''
                        SELECT * FROM meetings 
                        ORDER BY start_time DESC 
                        LIMIT ?
                    ''', (limit,))
                
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                return [dict(zip(columns, row)) for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting meetings: {e}")
            return []
    
    def search_meetings(self, query: str, search_fields: List[str] = None) -> List[Dict]:
        """
        Search meetings by text query.
        
        Args:
            query: Search query
            search_fields: Fields to search in (default: meeting_topic, main_topics, keywords)
            
        Returns:
            List of matching meetings
        """
        try:
            if search_fields is None:
                search_fields = ['meeting_topic', 'main_topics', 'keywords']
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build search query
                search_conditions = []
                search_values = []
                
                for field in search_fields:
                    search_conditions.append(f"{field} LIKE ?")
                    search_values.append(f"%{query}%")
                
                search_values.append(query)  # For meeting_id search
                
                query_sql = f'''
                    SELECT * FROM meetings 
                    WHERE ({" OR ".join(search_conditions)}) OR meeting_id = ?
                    ORDER BY start_time DESC
                '''
                
                cursor.execute(query_sql, search_values)
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                return [dict(zip(columns, row)) for row in rows]
                
        except Exception as e:
            logger.error(f"Error searching meetings: {e}")
            return []
    
    def add_transcript_entry(self, meeting_id: int, speaker_name: str, 
                           timestamp: datetime, text_content: str) -> Tuple[bool, str]:
        """
        Add a transcript entry for a meeting.
        
        Args:
            meeting_id: ID of the meeting
            speaker_name: Name of the speaker
            timestamp: When the text was spoken
            text_content: Transcribed text
            
        Returns:
            Tuple of (success, message)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO meeting_transcripts 
                    (meeting_id, speaker_name, timestamp, text_content)
                    VALUES (?, ?, ?, ?)
                ''', (meeting_id, speaker_name, timestamp, text_content))
                
                conn.commit()
                return True, "Transcript entry added successfully"
                
        except Exception as e:
            logger.error(f"Error adding transcript entry: {e}")
            return False, f"Error adding transcript entry: {str(e)}"
    
    def get_meeting_transcript(self, meeting_id: int) -> List[Dict]:
        """
        Get complete transcript for a meeting.
        
        Args:
            meeting_id: ID of the meeting
            
        Returns:
            List of transcript entries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM meeting_transcripts 
                    WHERE meeting_id = ? 
                    ORDER BY timestamp
                ''', (meeting_id,))
                
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                return [dict(zip(columns, row)) for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting transcript: {e}")
            return []
    
    def add_participant(self, meeting_id: int, name: str, role: str = "", 
                       department: str = "", join_time: datetime = None) -> Tuple[bool, str]:
        """
        Add a participant to a meeting.
        
        Args:
            meeting_id: ID of the meeting
            name: Participant name
            role: Participant role
            department: Participant department
            join_time: When they joined
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if join_time is None:
                join_time = datetime.now()
                
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO meeting_participants 
                    (meeting_id, name, role, department, join_time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (meeting_id, name, role, department, join_time))
                
                conn.commit()
                return True, "Participant added successfully"
                
        except Exception as e:
            logger.error(f"Error adding participant: {e}")
            return False, f"Error adding participant: {str(e)}"
    
    def get_meeting_participants(self, meeting_id: int) -> List[Dict]:
        """
        Get all participants for a meeting.
        
        Args:
            meeting_id: ID of the meeting
            
        Returns:
            List of participant dictionaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM meeting_participants 
                    WHERE meeting_id = ? 
                    ORDER BY join_time
                ''', (meeting_id,))
                
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                return [dict(zip(columns, row)) for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting participants: {e}")
            return []
    
    def get_meeting_start_time(self, meeting_id: int) -> Optional[datetime]:
        """Get the start time of a meeting."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT start_time FROM meetings WHERE meeting_id = ?', (meeting_id,))
                row = cursor.fetchone()
                if row and row[0]:
                    return datetime.fromisoformat(row[0])
                return None
        except Exception as e:
            logger.error(f"Error getting meeting start time: {e}")
            return None
    
    def get_active_meeting(self) -> Optional[Dict]:
        """Get the currently active meeting if any."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM meetings 
                    WHERE status = 'active' 
                    ORDER BY start_time DESC 
                    LIMIT 1
                ''')
                row = cursor.fetchone()
                if row:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, row))
                return None
        except Exception as e:
            logger.error(f"Error getting active meeting: {e}")
            return None 